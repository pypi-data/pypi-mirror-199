from cicada.preprocessing.convert_to_nwb import ConvertToNWB
from cicada.preprocessing.utils import load_tiff_movie_in_memory, update_frames_to_add
from cicada.utils.display.cells_map_utils import CellsCoord, get_coords_extracted_from_fiji
from pynwb.ophys import ImageSegmentation, Fluorescence
import numpy as np
from PIL import ImageSequence
import PIL
import PIL.Image as pil_image
import os
from scipy import ndimage


class ConvertFijiRoisToNWB(ConvertToNWB):
    """Class to convert ROIs data from Fiji to NWB
       if the CI movie is available, build the raw_traces.
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

        fiji_coords_file = kwargs.get("fiji_coords_file", None)
        if fiji_coords_file is None:
            # not mandatory
            print(f"No fiji_coords_file in class {self.__class__.__name__}")
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
        coords = get_coords_extracted_from_fiji(fiji_coords_file)

        if cell_type_codes is not None:
            print(f"len(cell_type_codes) {len(cell_type_codes)}, len(coords) {len(coords)}")

        for cell, coord in enumerate(coords):
            if coord.shape[0] == 0:
                print(f'Error: {cell} coord.shape {coord.shape}')
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

            image_mask = np.zeros((dim_y, dim_x))
            image_mask[coord[1, :] - 1, coord[0, :] - 1] = 1
            # we  use morphology.binary_fill_holes to build pixel_mask from coord
            image_mask = ndimage.binary_fill_holes(image_mask).astype(int)
            pix_mask = np.argwhere(image_mask)
            pix_mask = [(pix[0], pix[1], 1) for pix in pix_mask]
            # we can add id to identify the cell (int) otherwise it will be incremented at each step
            ps.add_roi(pixel_mask=pix_mask, image_mask=image_mask)

        print(f"Removing {n_cells_removed} out of {n_cells + n_cells_removed} cells from fiji rois "
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

