from cicada.preprocessing.convert_to_nwb import ConvertToNWB
from cicada.preprocessing.utils import load_tiff_movie_in_memory, update_frames_to_add
from cicada.utils.display.cells_map_utils import CellsCoord
from pynwb.ophys import ImageSegmentation, Fluorescence
import numpy as np
from PIL import ImageSequence
import PIL
import PIL.Image as pil_image
import os


class ConvertSuite2pRoisToNWB(ConvertToNWB):
    """Class to convert ROIs data from Suite2P to NWB
       if raw_traces from Suite2p are available they are loaded.
       Otherwise if the movie is available, build the raw_traces.
       create_roi_response_series
    """

    def __init__(self, nwb_file):
        super().__init__(nwb_file)

    def convert(self, **kwargs):
        """
        Convert the data and add to the nwb_file

        Args:
            **kwargs: arbitrary arguments
        """

        super().convert(**kwargs)
        if ("suite2p_dir" not in kwargs) and ("stat" not in kwargs):
            # not mandatory
            print(f"No suite2p_dir or stat in class {self.__class__.__name__}")
            return
            # raise Exception(f"'suite2p_dir' argument should be pass to convert "
            #                 f"function in class {self.__class__.__name__}")

        suite2p_dir = kwargs.get("suite2p_dir", None)
        stat_file = kwargs.get("stat", None)

        if (suite2p_dir is None) and (stat_file is None):
            # not mandatory
            print(f"No suite2p_dir or stat in class {self.__class__.__name__}")
            return

        data_id = kwargs.get("data_id", None)
        # identify the data (for ex: "all_cells", "INs" etc...)
        if data_id is None:
            # not mandatory
            print(f"No data_id in class {self.__class__.__name__}")
            return

        # cells to be removed according to their cell type
        # using the cell type code to identify them
        cell_type_codes_to_remove = kwargs.get("cell_type_codes_to_remove", [])

        if isinstance(cell_type_codes_to_remove, int):
            cell_type_codes_to_remove = [cell_type_codes_to_remove]
        elif not isinstance(cell_type_codes_to_remove, list):
            # then empty list
            cell_type_codes_to_remove = []


        # list of int and str representing the code and name of cell type of each cell
        # the length is the number of cells
        # could be None if cell type is not known
        # filtered means we removed the cells with code in cell_type_codes_to_remove
        cell_type_codes = kwargs.get("cell_type_codes", None)
        cell_type_codes_filtered = None if cell_type_codes is None else []
        cell_type_names = kwargs.get("cell_type_names", None)
        cell_type_names_filtered = None if cell_type_names is None else []

        if "ci_frames" not in self.nwb_file.acquisition:
            print(f"No ci_frames available in the acquisition of the nwb_file in class {self.__class__.__name__}")
            # return
            self.ci_frames = None
        else:
            self.ci_frames = self.nwb_file.acquisition["ci_frames"]

        # looking for the motion_corrected_ci_movie, return None if it doesn't exists
        # TODO: take in consideration the movie is not available
        #  then don't construct image mask and don't build raw-traces, use F.npy is available
        image_series = self.nwb_file.acquisition.get("motion_corrected_ci_movie")
        if image_series is None:
            raise Exception(f"No calcium imaging movie named 'motion_corrected_ci_movie' found in nwb_file")

        if 'ophys' in self.nwb_file.processing:
            mod = self.nwb_file.processing['ophys']
        else:
            mod = self.nwb_file.create_processing_module('ophys', 'contains optical physiology processed data')
        img_seg = ImageSegmentation(name=f"{data_id}")
        mod.add_data_interface(img_seg)
        imaging_plane = self.nwb_file.get_imaging_plane("my_imgpln")
        ci_sampling_rate = imaging_plane.imaging_rate
        # description, imaging_plane, name=None
        ps = img_seg.create_plane_segmentation(description='output from segmenting',
                                               imaging_plane=imaging_plane, name='my_plane_seg',
                                               reference_images=image_series)

        # spks.npy array of deconvolved traces (ROIs by timepoints)
        spks_suite2p = None
        if suite2p_dir is not None and stat_file is None:
            if not os.path.isfile(os.path.join(suite2p_dir, "stat.npy")):
                return
            stat = np.load(os.path.join(suite2p_dir, "stat.npy"), allow_pickle=True)
            if os.path.isfile(os.path.join(suite2p_dir, "iscell.npy")):
                is_cell = np.load(os.path.join(suite2p_dir, "iscell.npy"), allow_pickle=True)
            else:
                is_cell = None
            if os.path.isfile(os.path.join(suite2p_dir, "spks.npy")):
                spks_suite2p = np.load(os.path.join(suite2p_dir, "spks.npy"), allow_pickle=True)
        else:
            print(f"USING STAT FILE")
            stat = np.load(stat_file, allow_pickle=True)
            is_cell = None
        # TODO: load f.npy for raw_traces if available

        if image_series.format == "tiff":
            dim_y, dim_x = image_series.data.shape[1:]
            n_frames = image_series.data.shape[0]
            print(f"Dimensions double check: n_lines, n_cols: {image_series.data.shape[1:]}")
        elif image_series.format == "external":
            im = PIL.Image.open(image_series.external_file[0])
            n_frames = len(list(ImageSequence.Iterator(im)))
            dim_y, dim_x = np.array(im).shape
            print(f"Dimensions double check: n_lines, n_cols: {np.array(im).shape}")
        else:
            raise Exception(f"Format of calcium movie imaging {image_series.format} not yet implemented")

        n_cells = 0
        # print(f'### ConvertSuite2pRoisToNWB stat {stat}')
        # Add rois
        # represent the real index of the cell, will be different than cell if is_cell is not None
        # keep the index of the cell not taking in consideration the one remove due to their cell tyoe
        # this allows to keep the correspondance with the cell type listing
        cell_index_without_the_removed_one = 0
        # number of cells removed due to their cell type
        n_cells_removed = 0
        pixel_masks = []
        if cell_type_codes is not None:
            print(f"len(cell_type_codes) {len(cell_type_codes)}, len(stat) {len(stat)}")
        for cell in np.arange(len(stat)):
            if is_cell is not None:
                if is_cell[cell][0] == 0:
                    continue
            if cell_type_codes is not None:
                if cell_type_codes[cell_index_without_the_removed_one] in cell_type_codes_to_remove:
                    n_cells_removed += 1
                    cell_index_without_the_removed_one += 1
                    # skipping this cell as its cell type is not good
                    continue
                else:
                    cell_type_codes_filtered.append(cell_type_codes[cell_index_without_the_removed_one])
                    cell_type_names_filtered.append(cell_type_names[cell_index_without_the_removed_one])
            cell_index_without_the_removed_one += 1
            n_cells += 1
            # first (y, x) inverted recently (12th of may 2020)
            pix_mask = [(y, x, 1) for x, y in zip(stat[cell]["xpix"], stat[cell]["ypix"])]
            image_mask = np.zeros((dim_y, dim_x)) # recently inverted (12th of may 2020)
            for pix in pix_mask:
                image_mask[int(pix[0]), int(pix[1])] = pix[2] # pix[0] pix[1] recently inverted (12th of may 2020)
            # we can id to identify the cell (int) otherwise it will be incremented at each step
            pixel_masks.append(pix_mask)
            ps.add_roi(pixel_mask=pix_mask, image_mask=image_mask)

        print(f"Removing {n_cells_removed} out of {n_cells + n_cells_removed} cells from suite2p rois "
              f"with cell type codes among {cell_type_codes_to_remove}")

        fl = Fluorescence(name=f"fluorescence_{data_id}")
        mod.add_data_interface(fl)

        rt_region = ps.create_roi_table_region('all cells', region=list(np.arange(n_cells)))
        if image_series.format == "external":
            print(f"external: {image_series.external_file[0]}")
            if image_series.external_file[0].endswith(".tiff") or \
                    image_series.external_file[0].endswith(".tif"):
                frames_to_add = dict()
                # print(f"ci_sampling_rate {ci_sampling_rate}")
                update_frames_to_add(frames_to_add=frames_to_add, nwb_file=self.nwb_file,
                                     ci_sampling_rate=ci_sampling_rate)
                ci_movie = load_tiff_movie_in_memory(image_series.external_file[0], frames_to_add=frames_to_add)
            else:
                raise Exception(f"Calcium imaging format not supported yet {image_series.external_file[0]}")
        else:
            ci_movie = image_series.data

        if self.ci_frames is None:
            timestamps = np.arange(n_frames)
        else:
            timestamps = self.ci_frames.timestamps

        if ci_movie is not None:
            raw_traces = np.zeros((n_cells, ci_movie.shape[0]))
            for cell in np.arange(n_cells):
                img_mask = ps['image_mask'][cell]
                img_mask = img_mask.astype(bool)
                raw_traces[cell, :] = np.mean(ci_movie[:, img_mask], axis=1)

            """
            control (Iterable) – Numerical labels that apply to each element in data
            control_description (Iterable) – Description of each control value
            """
            rrs = fl.create_roi_response_series(name='raw_traces', data=np.transpose(raw_traces), unit='lumens',
                                                rois=rt_region, timestamps=timestamps,
                                                description="raw traces", control=cell_type_codes_filtered,
                                                control_description=cell_type_names_filtered)
            print(f"- Creating Roi Response Series with raw traces of shape: {(np.transpose(raw_traces)).shape}")

            # adding raw tracew without overlap
            cells_coord = CellsCoord(pixel_masks=pixel_masks, from_matlab=False, invert_xy_coord=False)
            raw_traces_without_overlap = cells_coord.build_raw_traces_from_movie(movie=ci_movie, without_overlap=True)
            rrs = fl.create_roi_response_series(name='raw_traces_wo', data=np.transpose(raw_traces_without_overlap),
                                                unit='lumens',
                                                rois=rt_region, timestamps=timestamps,
                                                description="raw traces without overlap",
                                                control=cell_type_codes_filtered,
                                                control_description=cell_type_names_filtered)
            print(f"- Creating Roi Response Series with: raw traces without overlap of "
                  f"shape: {(np.transpose(raw_traces_without_overlap)).shape}")

        if spks_suite2p is not None:
            # removing cells that are not True
            spks_filtered = np.zeros((n_cells, spks_suite2p.shape[1]))
            real_cell_index = 0
            # represent the real index of the cell, will be different than cell if is_cell is not None
            # keep the index of the cell not taking in consideration the one remove due to their cell tyoe
            # this allows to keep the correspondance with the cell type listing
            cell_index_without_the_removed_one = 0
            for cell in np.arange(len(spks_suite2p)):
                if is_cell is not None:
                    if is_cell[cell][0] == 0:
                        continue
                if (cell_type_codes is not None) and \
                        (cell_type_codes[cell_index_without_the_removed_one] in cell_type_codes_to_remove):
                    # skipping this cell as its cell type is not good
                    cell_index_without_the_removed_one += 1
                    continue
                cell_index_without_the_removed_one += 1
                spks_filtered[real_cell_index] = spks_suite2p[cell]
                real_cell_index += 1

            """
            control (Iterable) – Numerical labels that apply to each element in data
            control_description (Iterable) – Description of each control value
            """
            rrs = fl.create_roi_response_series(name='spks_suite2p', data=np.transpose(spks_filtered), unit='lumens',
                                                rois=rt_region, timestamps=timestamps,
                                                description="deconvolved traces from suite2p",
                                                control=cell_type_codes_filtered,
                                                control_description=cell_type_names_filtered)

            print(f"- Creating Roi Response Series with: suite2p deconvolved traces  of "
                  f"shape: {(np.transpose(spks_filtered)).shape}")

