from cicada.analysis.cicada_analysis import CicadaAnalysis
from cicada.utils.display.cells_map_utils import CellsCoord, get_coords_from_caiman_format_file, \
    get_coords_extracted_from_fiji
import sys
from cicada.utils.cell_type_utils import read_cell_type_categories_yaml_file
from time import sleep, time
import os
import numpy as np
from sortedcontainers import SortedDict


# import matplotlib.cm as cm
# from cicada.utils.display.colors import BREWER_COLORS
# import matplotlib.colors as plt_colors
# from cicada.utils.cell_assemblies.malvache.utils import load_cell_assemblies_data
# from cicada.utils.display.videos import load_tiff_movie


class CicadaCellsMapsFusionAnalysis(CicadaAnalysis):
    ADD_FUSION = "Add"
    REPLACE_FUSION = "Replace"
    ADD_AND_REPLACE_FUSION = "Add & Replace"
    ALL_OPTIONS_FUSION = "All options"

    def __init__(self, config_handler=None):
        """
        """
        long_description = "<p align='center'><b>Fusion of cells' maps</b></p><br>"
        long_description = long_description + 'Allows to fusion other cell segmentation to this one. <br><br>'
        long_description = long_description + "The file won't be modify but new segmentation file " \
                                              "will be created <br><br>"
        long_description = long_description + 'It is possible to associate a cell type to cells that ' \
                                              'are segmented through another method<br><br>'
        CicadaAnalysis.__init__(self, name="Cells' maps fusion", family_id="Pre-processing",
                                short_description="Fusion cells' maps",
                                long_description=long_description,
                                config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

        self.n_max_maps = 3

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaCellsMapsFusionAnalysis(config_handler=self.config_handler)
        self.transfer_attributes_to_tabula_rasa_copy(analysis_copy=analysis_copy)
        return analysis_copy

    def check_data(self):
        """
        Check the data given one initiating the class and return True if the data given allows the analysis
        implemented, False otherwise.
        :return: a boolean
        """
        super().check_data()

        for session_index, session_data in enumerate(self._data_to_analyse):
            if session_data.DATA_FORMAT != "CI_DATA":
                self.invalid_data_help = f"Non CI_DATA format compatibility not yet implemented: " \
                                         f"{session_data.DATA_FORMAT}"
                return False

        if len(self._data_to_analyse) != 1:
            self.invalid_data_help = "This analysis works only if 1 session is selected"
            return False

        for data in self._data_to_analyse:

            segmentations = data.get_segmentations()

            # we need at least one segmentation
            if (segmentations is None) or len(segmentations) == 0:
                self.invalid_data_help = "No segmentation data available"
                return False

        return True

    def set_arguments_for_gui(self):
        """

        Returns:

        """
        CicadaAnalysis.set_arguments_for_gui(self)

        self.add_choices_arg_for_gui(arg_name="match_mode",
                                     choices=["Closest with min area", "Closest", "Biggest"],
                                     short_description="Cells match mode",
                                     default_value="Closest with min area",
                                     multiple_choices=False,
                                     long_description="'Closest with min area': Match the cell with the closest "
                                                      "cell whose area is superior "
                                                      "to the minimum cell area. If take the biggest cell option"
                                                      "if choosen. 'Closest': take the closest cell. "
                                                      "'Biggest': Match the cell with the biggest cell in "
                                                      "the range given, "
                                                      "otherwise the closest cell found will be use as match.",
                                     family_widget="match_mode")

        self.add_int_values_arg_for_gui(arg_name="min_cell_area", min_value=5, max_value=1500,
                                        short_description="Minimum cell area",
                                        default_value=100, long_description=None, family_widget="match_mode")

        max_dist_bw_centroids_arg = {"arg_name": "max_dist_bw_centroids", "value_type": "int",
                                     "min_value": 1, "max_value": 30,
                                     "long_description": "Max distance between 2 centroids in pixels",
                                     "default_value": 7, "short_description": "Max distance between 2 centroids",
                                     "family_widget": "match_mode"}

        self.add_argument_for_gui(**max_dist_bw_centroids_arg)

        self.add_open_file_dialog_arg_for_gui(key_names=[f"Map {n + 1}" for n in range(self.n_max_maps)],
                                              arg_name="segmentation_data_file",
                                              extensions=["zip", "roi", "npz", "mat"],
                                              mandatory=True,
                                              short_description="Files containing the segmentation to extract",
                                              long_description="If .mat or .npz file, it should be in the CaImAn format. "
                                                               "Zip and roi corresponds to the output of ImageJ (fiji)",
                                              family_widget="maps")

        self.add_choices_arg_for_gui(arg_name="fusion_mode",
                                     choices=[self.ADD_FUSION, self.REPLACE_FUSION, self.ADD_AND_REPLACE_FUSION,
                                              self.ALL_OPTIONS_FUSION],
                                     short_description="Fusion mode",
                                     default_value=self.ALL_OPTIONS_FUSION,
                                     multiple_choices=False,
                                     long_description="Choose what fusion will be done with the maps given."
                                                      "If Add: only cells with no matches are added. "
                                                      "If replace: only cells that have a match will replace."
                                                      "If Add & replace: then both action are done."
                                                      "Finaly if all options: it will create an output map "
                                                      "for each option",
                                     family_widget="maps")
        # 100
        self.add_bool_option_for_gui(arg_name="cell_type_to_add", true_by_default=False,
                                     short_description="Produce cell type predictions",
                                     long_description="If True, then a cell predictions file will be produce, indicating"
                                                      "the cell type of the cells according to the info given below",
                                     family_widget="maps")

        for n in range(self.n_max_maps):
            self.add_open_file_dialog_arg_for_gui(arg_name="cell_type_config_file",
                                                  extensions=["yaml", "yml"],
                                                  mandatory=False,
                                                  short_description="Config file for cell type encoding",
                                                  long_description="Allows to know the code (int) of the cell type"
                                                                   "given. Cell type given should be on the yaml",
                                                  family_widget="maps")
            self.add_field_text_option_for_gui(arg_name=f"extracted_cell_type Map {n + 1}",
                                               default_value="interneuron",
                                               short_description=f"Map {n + 1} cell type of the extracted cells",
                                               long_description="The cell type should be in the yaml file, "
                                                                "otherwise no cell type will be given. Keep "
                                                                "empty to assign no cell type",
                                               family_widget="maps")

            self.add_field_text_option_for_gui(arg_name=f"other_cell_type Map {n + 1}",
                                               default_value="",
                                               short_description=f"Map {n + 1} cell type of the cells not in this map",
                                               long_description="The cell type should be in the yaml file, "
                                                                "otherwise no cell type will be given. Keep"
                                                                " empty to assign no cell type",
                                               family_widget="maps")

        self.add_segmentation_arg_for_gui()

        matlab_indexation_arg = {"arg_name": "matlab_indexation", "value_type": "bool",
                                 "default_value": True, "short_description": "Matlab indexation ?"}

        self.add_argument_for_gui(**matlab_indexation_arg)

        invert_xy_coord_arg = {"arg_name": "invert_xy_coord", "value_type": "bool",
                               "default_value": False, "short_description": "Invert xy coords of loaded contours",
                               "long_description": "Could be useful if the coordinates are inverted,"
                                                   " do it for the loaded contours"}

        self.add_argument_for_gui(**invert_xy_coord_arg)

        verbose_arg = {"arg_name": "verbose", "value_type": "bool",
                       "default_value": True, "short_description": "Verbose",
                       "long_description": "If selected, some information might be printed during the analysis."}

        self.add_argument_for_gui(**verbose_arg)

    def update_original_data(self):
        """
        To be called if the data to analyse should be updated after the analysis has been run.
        :return: boolean: return True if the data has been modified
        """
        pass

    def run_analysis(self, **kwargs):
        """
        test
        :param kwargs:
          segmentation

        :return:
        """
        CicadaAnalysis.run_analysis(self, **kwargs)

        n_sessions = len(self._data_to_analyse)

        segmentation_dict = kwargs['segmentation']

        matlab_indexation = kwargs["matlab_indexation"]

        max_dist_bw_centroids = kwargs["max_dist_bw_centroids"]

        invert_xy_coord = kwargs.get("invert_xy_coord", True)

        match_mode = kwargs.get("match_mode")

        min_cell_area = kwargs.get("min_cell_area", True)

        take_the_biggest_match = False
        if match_mode == "Biggest":
            take_the_biggest_match = True
            min_cell_area = 0
        elif match_mode == "Closest":
            min_cell_area = 0

        # indicate if a cell type predictions should be produce
        cell_type_to_add = kwargs.get("cell_type_to_add", False)

        cell_type_config_file = kwargs.get("cell_type_config_file")
        cell_type_from_code_dict = dict()
        cell_type_to_code_dict = dict()
        if cell_type_config_file is not None and cell_type_to_add:
            cell_type_from_code_dict, cell_type_to_code_dict, multi_class_arg = \
                read_cell_type_categories_yaml_file(yaml_file=cell_type_config_file)
        # use to initiate the array of predictions
        cell_type_code_max = 0
        if len(cell_type_from_code_dict.keys()) > 0:
            cell_type_code_max = np.max(list(cell_type_from_code_dict.keys()))

        verbose = kwargs.get("verbose", True)

        fusion_modes = [kwargs.get("fusion_mode")]
        if fusion_modes[0] == self.ALL_OPTIONS_FUSION:
            fusion_modes = [self.ADD_FUSION, self.REPLACE_FUSION, self.ADD_AND_REPLACE_FUSION]

        dpi = kwargs.get("dpi", 200)

        session_data = self._data_to_analyse[0]
        session_identifier = session_data.identifier
        if verbose:
            print(f"-------------- {session_identifier} -------------- ")
        if isinstance(segmentation_dict, dict):
            segmentation_info = segmentation_dict[session_identifier]
        else:
            segmentation_info = segmentation_dict

        if verbose:
            print(f"Get pixels masks")
        pixel_mask = session_data.get_pixel_mask(segmentation_info=segmentation_info)

        if pixel_mask is None:
            print(f"pixel_mask not available in for {session_data.identifier} "
                  f"in {segmentation_info}")
            self.update_progressbar(self.analysis_start_time, 100)
            return

        for fusion_mode_index, fusion_mode in enumerate(fusion_modes):
            if verbose:
                print(f"## Fusion mode: {fusion_mode}")

            # pixel_mask of type pynwb.core.VectorIndex
            # each element of the list will be a sequences of tuples of 3 floats representing x, y and a float between
            # 0 and 1 (not used in this case)
            pixel_mask_list = [pixel_mask[cell] for cell in range(len(pixel_mask))]
            if verbose:
                print(f" ")
                print(f"Get CI movie dimensions")
            # for now we use a dict, as cells might be added so the number of cells will change
            cell_type_predictions_dict = SortedDict()
            # Try to get CI movie dimensions from the 'TwoPhotonSeries'
            is_ci_movie = session_data.contains_ci_movie(consider_only_2_photons=True)
            if is_ci_movie:
                n_lines, n_cols = session_data.get_ci_movie_dimension(only_2_photons=True)
                if (n_lines is not None) and (n_cols is not None):
                    print(f"Dimension of calcium imaging movie (n_lines x n_cols) is {n_lines}x{n_cols} pixels")
            else:
                n_lines = None
                n_cols = None
            # If it does not return n_lines and n_cols try to get them from 'image mask' in PlanSegmentation
            if (n_lines is None) and (n_cols is None):
                n_lines, n_cols = session_data.get_ci_dimension_from_img_mask(segmentation_info=segmentation_info)
                if (n_lines is not None) and (n_cols is not None):
                    print(f"Dimension of calcium imaging movie (n_lines x n_cols) is {n_lines}x{n_cols} pixels")
                else:
                    print(f"Image size was not found from the 'TwoPhotonSeries' or from 'image_mask'")

            cells_coord = CellsCoord(pixel_masks=pixel_mask_list, nb_lines=n_lines, nb_col=n_cols,
                                     from_matlab=False, invert_xy_coord=invert_xy_coord)
            if verbose:
                print(f"N cells before fusion: {cells_coord.n_cells}")

            cells_coord_list = []
            coords_ids = []
            extracted_cell_types = []
            other_cell_types = []
            for map_file_index in range(self.n_max_maps):
                segmentation_data_file = kwargs['segmentation_data_file'].get(f"Map {map_file_index + 1}")
                if segmentation_data_file is None:
                    continue

                if segmentation_data_file.endswith("mat") or segmentation_data_file.endswith("npz"):
                    coords_loaded = get_coords_from_caiman_format_file(file_name=segmentation_data_file)
                elif segmentation_data_file.endswith("zip") or segmentation_data_file.endswith("roi"):
                    coords_loaded = get_coords_extracted_from_fiji(file_name=segmentation_data_file)
                else:
                    raise Exception(f"The segmentation data file should be either a .mat, .npz, .roi or .zip file. "
                                    f"The file given is {segmentation_data_file}")
                cells_coord_list.append(coords_loaded)
                coords_ids.append(os.path.basename(segmentation_data_file)[:-4])
                if cell_type_to_add:
                    extracted_cell_types.append(kwargs.get(f"extracted_cell_type Map {map_file_index + 1}"))
                    other_cell_types.append(kwargs.get(f"other_cell_type Map {map_file_index + 1}"))

            for coords_index, coords_loaded in enumerate(cells_coord_list):
                coords_id = coords_ids[coords_index]

                cells_coord_loaded = CellsCoord(coords=coords_loaded, from_matlab=matlab_indexation,
                                                invert_xy_coord=invert_xy_coord)

                contours_mapping = cells_coord.match_cells_indices(cells_coord_loaded,
                                                                   max_dist_bw_centroids=max_dist_bw_centroids,
                                                                   path_results=self.get_results_path(),
                                                                   plot_result=(fusion_mode_index == 0),
                                                                   plot_title_opt=session_identifier + "_" + coords_id,
                                                                   take_the_biggest=take_the_biggest_match,
                                                                   min_cell_area=min_cell_area)

                cells_to_replace = []
                cells_to_replace_by = []
                cells_to_add = []
                # cells that have been replaced or added from the loaded map
                extracted_cells_indices = []

                for index, cell_mapped in enumerate(contours_mapping):
                    if cell_mapped < 0:
                        cells_to_add.append(index)
                        # meaning the cell from the data loaded has no match
                        continue
                    cells_to_replace.append(cell_mapped)
                    cells_to_replace_by.append(index)

                if len(cells_to_replace) > 0 and fusion_mode in [self.REPLACE_FUSION, self.ADD_AND_REPLACE_FUSION]:
                    if verbose:
                        print(f"{len(cells_to_replace)} cells replaced with {coords_id}")
                    cells_coord.replace_cells(cells_to_replace=cells_to_replace,
                                              cells_to_replace_by=cells_to_replace_by,
                                              cells_coord=cells_coord_loaded)
                    extracted_cells_indices.extend(cells_to_replace)

                elif verbose and fusion_mode in [self.REPLACE_FUSION, self.ADD_AND_REPLACE_FUSION]:
                    print(f"No cells replaced with {coords_id}")

                if len(cells_to_add) > 0 and fusion_mode in [self.ADD_FUSION, self.ADD_AND_REPLACE_FUSION]:
                    if verbose:
                        print(f"{len(cells_to_add)} cells added with {coords_id}")
                    added_cells_index = cells_coord.add_cells(cells_to_add=cells_to_add,
                                                              cells_coord=cells_coord_loaded)
                    extracted_cells_indices.extend(added_cells_index)

                elif verbose and fusion_mode in [self.ADD_FUSION, self.ADD_AND_REPLACE_FUSION]:
                    print(f"No cells added with {coords_id}")
                # TODO: generate cell type predictions
                if len(cell_type_to_code_dict) > 0:
                    extracted_cell_type = kwargs.get(f"extracted_cell_type Map {coords_index + 1}", "")
                    other_cell_type = kwargs.get(f"other_cell_type Map {coords_index + 1}", "")

                    extracted_cells_indices = np.array(extracted_cells_indices)
                    other_cells_indices = np.setdiff1d(np.arange(cells_coord.n_cells), extracted_cells_indices)

                    if extracted_cell_type.strip() != "" and extracted_cell_type.strip() in cell_type_to_code_dict:
                        # then we set the cells cell type to this one
                        extracted_cell_type_code = cell_type_to_code_dict[extracted_cell_type]
                        for extracted_cell in extracted_cells_indices:
                            cell_type_predictions_dict[extracted_cell] = extracted_cell_type_code

                    if other_cell_type.strip() != "" and other_cell_type.strip() in cell_type_to_code_dict:
                        # then we set the cells cell type to this one
                        other_cell_type_code = cell_type_to_code_dict[other_cell_type]
                        for other_cell in other_cells_indices:
                            # only if the cell has no code
                            if other_cell not in cell_type_predictions_dict:
                                cell_type_predictions_dict[other_cell] = other_cell_type_code

            # lines are cells, columns are cell type, 1 means the cells is predicted as being from this cell type
            # sum of each column should be equal to 1 in our case, even so a cell could have several types
            # depending in the configuration
            if len(cell_type_predictions_dict) > 0:
                cell_type_predictions = np.zeros((cells_coord.n_cells, cell_type_code_max+1), dtype='int8')
                for cell, cell_type_code in cell_type_predictions_dict.items():
                    cell_type_predictions[cell, cell_type_code] = 1
                    print(f"In fusion mode {fusion_mode}, cell {cell} encoded "
                          f"as {cell_type_from_code_dict[cell_type_code]}")

                np.save(os.path.join(self.get_results_path(),
                                     f"{session_identifier}_{fusion_mode}_cell_type_predictions.npy"),
                        cell_type_predictions)

            if verbose:
                print(f"N cells after fusion: {cells_coord.n_cells}")
                print(" ")
            file_name = os.path.join(self.get_results_path(), f"{session_identifier}_new_contours_{fusion_mode}")
            cells_coord.save_coords(file_name=file_name)

        if verbose:
            print(" ")
        self.update_progressbar(self.analysis_start_time, 100)

        print(f"Cells map analysis run in {time() - self.analysis_start_time} sec")
