from cicada.analysis.cicada_analysis import CicadaAnalysis
from cicada.utils.display.cells_map_utils import CellsCoord
import sys
from time import sleep, time
import numpy as np
import matplotlib.cm as cm
from cicada.utils.display.colors import BREWER_COLORS
import matplotlib.colors as plt_colors
from cicada.utils.cell_assemblies.malvache.utils import load_cell_assemblies_data
from cicada.utils.display.videos import load_tiff_movie
from cicada.utils.misc import get_continous_time_periods, print_info_dict
from cicada.utils.misc import validate_indices_in_string_format, extract_indices_from_string


class CicadaCellsMapAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        CicadaAnalysis.__init__(self, name="Cells map", family_id="Display",
                                short_description="Plot map of the cells",
                                config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaCellsMapAnalysis(config_handler=self.config_handler)
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

        self.add_segmentation_arg_for_gui()

        self.add_ci_movie_arg_for_gui(long_description="Only useful if the average calcium imaging is displayed "
                                                       "on the background")

        self.add_int_values_arg_for_gui(arg_name="n_sample_frame",
                                        default_value=2000, min_value=100, max_value=5000,
                                        short_description="Number of movie frames used to produce image background",
                                        family_widget='background')

        avg_methods = ["avg", "std"]
        self.add_choices_arg_for_gui(arg_name="bckground_method", choices=avg_methods,
                                     default_value="block", short_description="Method to produce background image",
                                     multiple_choices=False,
                                     family_widget="background")

        cell_numbers_arg = {"arg_name": "with_cell_numbers", "value_type": "bool",
                            "default_value": True, "short_description": "Display cell numbers"}

        self.add_argument_for_gui(**cell_numbers_arg)

        self.add_save_formats_arg_for_gui(family_widget="image_format")

        self.add_dpi_arg_for_gui(family_widget="image_format")

        self.add_bool_option_for_gui(arg_name="xkcd_mode", true_by_default=False,
                                     short_description="Turn on xkcd sketch-style drawing mode",
                                     long_description="For best results, the 'Humor Sans' font should be installed: "
                                                      "it is not included with matplotlib.",
                                     family_widget="image_format")

        pixels_mask_polygon_arg = {"arg_name": "polygon_or_pixel_mask", "choices": ["polygons", "pixel masks"],
                                   "default_value": "polygons", "short_description": "Technique use to draw the cells",
                                   "long_description": "if both are selected, then 2 figures will be produce",
                                   "multiple_choices": True, "family_widget": "contours"}

        self.add_argument_for_gui(**pixels_mask_polygon_arg)

        self.add_bool_option_for_gui(arg_name="use_open_cv_approx_for_contours", true_by_default=True,
                                     short_description="Open cv contours",
                                     long_description="Use open cv to approximate contours drawn. approximates a curve "
                                                      "or a polygon with another curve/polygon with less vertices so "
                                                      "that the distance between them is less or equal to "
                                                      "the specified precision. It uses the Douglas-Peucker "
                                                      "algorithm "
                                                      "<http://en.wikipedia.org/wiki/Ramer-Douglas-Peucker_algorithm>",

                                     family_widget="contours")
        self.add_int_values_arg_for_gui(arg_name="epsilon_factor_for_open_cv_approx",
                                        default_value=10, min_value=1, max_value=1000,
                                        short_description="Contours approximation",
                                        long_description="Specifying the approximation accuracy for open cv contours, "
                                                         "the smaller the more precise.",
                                        family_widget="contours")

        all_cell_types = []
        for data_to_analyse in self._data_to_analyse:
            all_cell_types.extend(data_to_analyse.get_all_cell_types())

        all_cell_types = list(set(all_cell_types))

        self.add_choices_for_groups_for_gui(arg_name="cells_groups", choices=all_cell_types,
                                            with_color=True,
                                            mandatory=False,
                                            short_description="Groups of cells to color",
                                            long_description="Select cells's groups you want to color in the map. "
                                                             "It has priority on other options, except cell assemblies",
                                            family_widget="cell_type",
                                            add_custom_group_field=True,
                                            custom_group_validation_fct=validate_indices_in_string_format,
                                            custom_group_processor_fct=None)

        cells_color_arg = {"arg_name": "cells_color", "value_type": "color_with_alpha",
                           "default_value": (1, 1, 1, 1.), "short_description": "Cells' color",
                           "family_widget": "colors"}
        self.add_argument_for_gui(**cells_color_arg)

        fill_cells_arg = {"arg_name": "dont_fill_cells_not_in_groups", "value_type": "bool",
                          "default_value": False, "short_description": "Display only edges for cells not in a group",
                          "family_widget": "colors"}

        self.add_argument_for_gui(**fill_cells_arg)

        edge_color_arg = {"arg_name": "edge_color", "value_type": "color_with_alpha",
                          "default_value": (1, 1, 1, 1.), "short_description": "Cells' edge color",
                          "family_widget": "colors"}
        self.add_argument_for_gui(**edge_color_arg)

        # dimgray is the default color
        cell_numbers_color_arg = {"arg_name": "cell_numbers_color", "value_type": "color",
                                  "default_value": (0.412, 0.412, 0.412, 1.),
                                  "short_description": "Cells' number color",
                                  "family_widget": "colors"}
        self.add_argument_for_gui(**cell_numbers_color_arg)

        bg_color_arg = {"arg_name": "background_color", "value_type": "color_with_alpha",
                        "default_value": (0, 0, 0, 1.), "short_description": "Background color",
                        "long_description": "If calcium imaging movie background selected, the background won't matter",
                        "family_widget": "colors"}
        self.add_argument_for_gui(**bg_color_arg)

        img_on_background_arg = {"arg_name": "display_img_on_background", "value_type": "bool",
                                 "default_value": False, "short_description": "Use average movie image as background",
                                 "family_widget": "colors"}

        self.add_argument_for_gui(**img_on_background_arg)

        self.add_bool_option_for_gui(arg_name="adjust_brightness",
                                     short_description="Adjust contrast of CI movie average in background",
                                     true_by_default=False, family_widget="colors")

        self.add_int_values_arg_for_gui(arg_name="max_img_sat",
                                        default_value=1, min_value=1, max_value=5,
                                        short_description="Per thousand of saturating pixels",
                                        long_description="How many saturating pixels are in the image after brigthness"
                                                         "adjustment",
                                        family_widget="colors")

        real_size_image_on_bg_arg = {"arg_name": "real_size_image_on_bg", "value_type": "bool",
                                     "default_value": True, "short_description": "Scale the figure to the background "
                                                                                 "image resolution",
                                     "family_widget": "colors"}

        self.add_argument_for_gui(**real_size_image_on_bg_arg)

        welsh_arg = {"arg_name": "use_welsh_powell_coloring", "value_type": "bool",
                     "default_value": False, "short_description": "Use welsh powell algorithm to color cells",
                     "long_description": "If chosen, then groups of cells will be decide by the algorithm. "
                                         "As well as colors, "
                                         "except for isolated cell, whose color will be the cells' color choosen.",
                     "family_widget": "colors"}

        self.add_argument_for_gui(**welsh_arg)

        self.add_bool_option_for_gui(arg_name="gradient_color_by_firing_rate",
                                     short_description="Color cell by firing rate",
                                     true_by_default=False, family_widget="gradient_color")
        self.add_roi_response_series_arg_for_gui(short_description="Raster to encode color",
                                                 family_widget="gradient_color",
                                                 long_description=None)

        key_names = [data.identifier for data in self._data_to_analyse]
        cell_ass_arg = {"arg_name": "cell_assemblies_file", "value_type": "file",
                        "extensions": "txt",
                        "mandatory": False,
                        "short_description": "Txt file with results from kmean cell assemblies analysis",
                        "family_widget": "cell assemblies"}
        if len(key_names) > 1:
            cell_ass_arg.update({"key_names": key_names})
        self.add_argument_for_gui(**cell_ass_arg)

        self.add_choices_arg_for_gui(arg_name="color_cell_assemblies", choices=["cmap nipy_spectral", "brewer"],
                                     default_value="brewer", short_description="Set of colors for cell assemblies",
                                     multiple_choices=False,
                                     family_widget="cell assemblies")

        show_polygons_arg = {"arg_name": "show_polygons", "value_type": "bool",
                             "default_value": False, "short_description": "Show a polygon that covers "
                                                                          "the cells of a same cell assembly",
                             "family_widget": "cell assemblies"}

        self.add_argument_for_gui(**show_polygons_arg)

        fill_polygons_arg = {"arg_name": "fill_polygons", "value_type": "bool",
                             "default_value": False, "short_description": "Fill the polygon that covers "
                                                                          "the cells of a same cell assembly",
                             "family_widget": "cell assemblies"}

        self.add_argument_for_gui(**fill_polygons_arg)

        invert_xy_coord_arg = {"arg_name": "invert_xy_coord", "value_type": "bool",
                               "default_value": False, "short_description": "Invert xy coords",
                               "long_description": "Could be useful if the coordinates are inverted"}

        self.add_argument_for_gui(**invert_xy_coord_arg)

        self.add_verbose_arg_for_gui()

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

        # use if a gradient of color is using neuronal activity
        roi_response_series_dict = kwargs.get("roi_response_series", None)

        gradient_color_by_firing_rate = kwargs.get("gradient_color_by_firing_rate", False)

        n_sessions = len(self._data_to_analyse)

        segmentation_dict = kwargs['segmentation']

        with_cell_numbers = kwargs["with_cell_numbers"]

        n_sample_frame = kwargs.get("n_sample_frame")

        bckground_method = kwargs.get("bckground_method")

        save_formats = kwargs["save_formats"]
        if save_formats is None:
            save_formats = "pdf"

        cells_groups_dict = kwargs.get("cells_groups")

        cells_color = kwargs.get("cells_color", None)

        dont_fill_cells_not_in_groups = kwargs.get("dont_fill_cells_not_in_groups", False)

        edge_color = kwargs.get("edge_color", None)

        background_color = kwargs.get("background_color", None)

        display_img_on_background = kwargs.get("display_img_on_background", None)

        adjust_brightness = kwargs.get("adjust_brightness")

        max_img_sat = kwargs.get("max_img_sat")
        max_img_sat = max_img_sat / 1000

        real_size_image_on_bg = kwargs.get("real_size_image_on_bg", True)

        cell_numbers_color = kwargs.get("cell_numbers_color", None)

        use_welsh_powell_coloring = kwargs.get("use_welsh_powell_coloring", False)

        use_open_cv_approx_for_contours = kwargs.get("use_open_cv_approx_for_contours", False)
        epsilon_factor_for_open_cv_approx = kwargs.get("epsilon_factor_for_open_cv_approx", 10)
        epsilon_factor_for_open_cv_approx = epsilon_factor_for_open_cv_approx / 10000

        invert_xy_coord = kwargs.get("invert_xy_coord", False)

        verbose = kwargs.get("verbose", True)

        xkcd_mode = kwargs.get("xkcd_mode", False)

        dpi = kwargs.get("dpi", 200)

        use_pixel_masks_values = []
        if "polygon_or_pixel_mask" in kwargs:
            option_args = kwargs['polygon_or_pixel_mask']
            if option_args is None:
                use_pixel_masks_values = []
            else:
                if isinstance(option_args, str):
                    option_args = [option_args]
                for option_arg in option_args:
                    if option_arg == "polygons":
                        use_pixel_masks_values.append(False)
                    else:  # "pixel masks"
                        use_pixel_masks_values.append(True)

        cell_assemblies_file = kwargs.get("cell_assemblies_file", None)
        if isinstance(cell_assemblies_file, str):
            if len(self._data_to_analyse) > 1:
                # not matching the len of the data to analyse
                cell_assemblies_file = None
            else:
                cell_assemblies_file = {self._data_to_analyse[0].identifier: cell_assemblies_file}
        # else it should be a dict if not None

        fill_polygons = kwargs.get("fill_polygons", False)

        show_polygons = kwargs.get("show_polygons", False)

        color_cell_assemblies = kwargs.get("color_cell_assemblies", None)
        if color_cell_assemblies is None:
            color_cell_assemblies = "cmap nipy_spectral"

        if display_img_on_background:
            arg_ci_movies_dict = kwargs["ci_movie"]

        for session_index, session_data in enumerate(self._data_to_analyse):
            # Get Session Info
            info_dict = session_data.get_sessions_info()
            session_identifier = info_dict['identifier']

            if verbose:
                print(f" ")
                print(f"------------------ ONGOING SESSION: {session_identifier} -------------------- ")
                print(f"----------------------------- SESSION INFO ---------------------------------- ")
                print_info_dict(info_dict)
                print(f" ")

            if isinstance(segmentation_dict, dict):
                segmentation_info = segmentation_dict[session_identifier]
            else:
                segmentation_info = segmentation_dict

            if roi_response_series_dict is None:
                roi_response_serie_info = None
            elif isinstance(roi_response_series_dict, dict):
                roi_response_serie_info = roi_response_series_dict[session_identifier]
            else:
                roi_response_serie_info = roi_response_series_dict

            if verbose:
                print(f"Get pixels masks for plot")
            pixel_mask = session_data.get_pixel_mask(segmentation_info=segmentation_info)

            if pixel_mask is None:
                print(f"Pixel mask not available in for {session_data.identifier} "
                      f"in {segmentation_info}")
                self.update_progressbar(self.analysis_start_time, 100 / n_sessions)
                continue

            # pixel_mask of type pynwb.core.VectorIndex
            # each element of the list will be a sequences of tuples of 3 floats representing x, y and a float between
            # 0 and 1 (not used in this case)
            pixel_mask_list = [pixel_mask[cell] for cell in range(len(pixel_mask))]
            if verbose:
                print(f" ")
                print(f"Get CI movie dimensions")
                print(f"Try first to get dimensions from 'TwoPhotonSeries'")
            # Try to get CI movie dimensions from the 'TwoPhotonSeries'
            is_ci_movie = session_data.contains_ci_movie(consider_only_2_photons=True)
            if is_ci_movie:
                n_lines, n_cols = session_data.get_ci_movie_dimension(only_2_photons=True)
                if (n_lines is not None) and (n_cols is not None):
                    print(f"Dimension of calcium imaging movie (n_lines x n_cols) is {n_lines}x{n_cols} pixels")
            else:
                n_lines = None
                n_cols = None
                print(f"No dimension of calcium imaging movie found yet, try from 'PlanSegmentation'")
            # If it does not return n_lines and n_cols try to get them from 'image mask' in PlanSegmentation
            if (n_lines is None) and (n_cols is None):
                n_lines, n_cols = session_data.get_ci_dimension_from_img_mask(segmentation_info=segmentation_info)
                if (n_lines is not None) and (n_cols is not None):
                    print(f"Dimension of calcium imaging movie (n_lines x n_cols) is {n_lines}x{n_cols} pixels")
                else:
                    print(f"Image size was not found from the 'TwoPhotonSeries' or from 'image_mask'")

            cells_coord = CellsCoord(pixel_masks=pixel_mask_list,  nb_lines=n_lines, nb_col=n_cols,
                                     from_matlab=False, invert_xy_coord=invert_xy_coord)
            if verbose:
                print(f" ")
                print(f"N cells: {cells_coord.n_cells}")
            args_to_add = dict()
            if cells_color is not None:
                args_to_add["default_cells_color"] = cells_color
            if background_color is not None:
                args_to_add["background_color"] = background_color

            if edge_color is not None:
                args_to_add["default_edge_color"] = edge_color

            if cell_numbers_color is not None:
                args_to_add["cell_numbers_color"] = cell_numbers_color

            cells_groups = None
            cells_groups_colors = None
            cell_assemblies_on = False
            gradient_color_on = False
            if (cell_assemblies_file is not None) and (session_identifier in cell_assemblies_file) \
                    and (cell_assemblies_file[session_identifier] is not None):
                cell_assemblies_on = True
                assemblies_results = load_cell_assemblies_data(data_file_name=cell_assemblies_file[session_identifier])
                cell_assemblies = assemblies_results[0]
                n_assemblies = len(cell_assemblies)
                cells_groups_colors = []
                cells_groups = cell_assemblies
                for i in np.arange(n_assemblies):
                    if color_cell_assemblies == "cmap nipy_spectral":
                        color = cm.nipy_spectral(float(i + 1) / (n_assemblies + 1))
                    else:
                        # brewer
                        color_hex = BREWER_COLORS[i % len(BREWER_COLORS)]
                        # putting it with value from 0.0 to 1.0
                        color_rgb = plt_colors.hex2color(color_hex)
                        # adding the alpha
                        color_rgba = [c for c in color_rgb]
                        color_rgba.append(0.8)
                        color = color_rgba
                    cells_groups_colors.append(color)
            elif (cells_groups_dict is not None) and (len(cells_groups_dict) > 0):
                cell_indices_by_cell_type = session_data.get_cell_indices_by_cell_type(roi_serie_keys=
                                                                                       roi_response_serie_info)
                # cells_to_highlight = []
                # cells_to_highlight_colors = []
                cells_groups = []
                cells_groups_colors = []

                # TODO: See to check if groups don't contain some of the cells
                #  so far if that's the case it won't crash but some cells will be displayed several times
                for cells_group_name, cells_group_info in cells_groups_dict.items():
                    if len(cells_group_info) != 2:
                        continue
                    cells_names_in_group = cells_group_info[0]
                    cells_group_color = cells_group_info[1]
                    for cells_name in cells_names_in_group:
                        # then we extract the cell_indices from the cells_group_name
                        # it is either a string representing the cell_type or a series of indices
                        if cells_name in cell_indices_by_cell_type:
                            cell_indices = cell_indices_by_cell_type[cells_name]
                        else:
                            cell_indices = np.array(extract_indices_from_string(cells_name))
                        if len(cell_indices) == 0:
                            continue
                        # making sure we are on the boundaries
                        if roi_response_serie_info is not None:
                            neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)
                            cell_indices = cell_indices[np.logical_and(cell_indices >= 0,
                                                                       cell_indices < len(neuronal_data))]
                        # coloring the cells
                        cells_groups_colors.append(cells_group_color)
                        cells_groups.append(list(cell_indices))
            elif gradient_color_by_firing_rate and roi_response_serie_info is not None:
                # coloring each cell according to its firing rate (aka number of transients)
                gradient_color_on = True
                neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)
                number_of_transients_by_cell = np.zeros(len(neuronal_data), dtype="int16")
                for cell in np.arange(len(neuronal_data)):
                    # firing_rate == number of transients
                    number_of_transients_by_cell[cell] = len(get_continous_time_periods(neuronal_data[cell]))
                max_n_transients = np.max(number_of_transients_by_cell)
                if max_n_transients > 0:
                    cells_groups = []
                    cells_groups_colors = []
                    color_map = cm.Reds
                    for cell in np.arange(len(neuronal_data)):
                        cells_groups.append([cell])
                        color = color_map(number_of_transients_by_cell[cell] / max_n_transients)
                        cells_groups_colors.append(color)

            avg_cell_map_img = None
            if display_img_on_background:
                # setting the movie
                if verbose:
                    print(f" ")
                    print(f"Use CI movie as background image")
                    print(f"Loading the first {n_sample_frame} frames of the movie to build image background ... ")
                session_ci_movie_dict = session_data.get_ci_movies_sample(only_2_photons=False, n_frames=n_sample_frame)
                if isinstance(arg_ci_movies_dict, str):
                    arg_movie_name = arg_ci_movies_dict
                else:
                    arg_movie_name = arg_ci_movies_dict[session_identifier]
                session_ci_movie_data = session_ci_movie_dict[arg_movie_name]
                if isinstance(session_ci_movie_data, str):
                    tiff_movie = load_tiff_movie(tiff_file_name=session_ci_movie_data)
                else:
                    tiff_movie = session_ci_movie_data
                if bckground_method == 'std':
                    avg_cell_map_img = np.std(tiff_movie, axis=0)
                if bckground_method == 'avg':
                    avg_cell_map_img = np.mean(tiff_movie, axis=0)
                if verbose:
                    print(f"Background image is obtained")

            for use_pixel_masks in use_pixel_masks_values:
                if use_pixel_masks:
                    title_option = "all_cells_pixel_masks"
                else:
                    title_option = "all_cells_polygons"

                use_welsh_powell_coloring = (not cell_assemblies_on) and \
                                            (not gradient_color_on) and \
                                            (not ((cells_groups_dict is not None)
                                                  and (len(cells_groups_dict) > 0))) and use_welsh_powell_coloring

                cells_coord.plot_cells_map(path_results=self.get_results_path(),
                                           data_id=session_identifier, show_polygons=show_polygons,
                                           fill_polygons=fill_polygons,
                                           use_pixel_masks=use_pixel_masks,
                                           title_option=title_option, connections_dict=None,
                                           use_welsh_powell_coloring=use_welsh_powell_coloring,
                                           verbose=verbose,
                                           cells_groups=cells_groups,
                                           cells_groups_colors=cells_groups_colors,
                                           img_on_background=avg_cell_map_img,
                                           real_size_image_on_bg=real_size_image_on_bg,
                                           cells_groups_edge_colors=None,
                                           with_edge=True, cells_groups_alpha=None,
                                           dont_fill_cells_not_in_groups=dont_fill_cells_not_in_groups,
                                           with_cell_numbers=with_cell_numbers, save_formats=save_formats,
                                           dpi=dpi,
                                           xkcd_mode=xkcd_mode,
                                           use_open_cv_approx_for_contours=use_open_cv_approx_for_contours,
                                           epsilon_factor_for_open_cv_approx=epsilon_factor_for_open_cv_approx,
                                           save_plot=True, return_fig=False, adjust_brightness=adjust_brightness,
                                           max_saturation=max_img_sat,
                                           **args_to_add)

            if verbose:
                print(" ")
            self.update_progressbar(time_started=self.analysis_start_time, increment_value=100 / n_sessions)
        print(f"Cells map analysis run in {time() - self.analysis_start_time} sec")
