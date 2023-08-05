from cicada.analysis.cicada_analysis import CicadaAnalysis
from time import time
from cicada.utils.misc import get_continous_time_periods, print_info_dict
import numpy as np
from datetime import datetime
from cicada.utils.stats import compare_two_distributions
from cicada.utils.stats import multiple_comparison_one_factor_effect
from cicada.utils.misc import from_timestamps_to_frame_epochs, validate_indices_in_string_format, \
    extract_indices_from_string, find_nearest
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


class CicadaTransientFrequencyAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        long_description = '<p align="center"><b>Compute calcium event frequency for all cells</b></p><br>'
        long_description = long_description + 'Use the raster to return the transient frequency of each cell' \
                                              ' and save in csv and xlxs formats.<br><br>'
        long_description = long_description + 'Do some customized plots with groups and subgroups that can be defined'
        CicadaAnalysis.__init__(self, name="Transients' frequency", family_id="Descriptive statistics",
                                short_description="",
                                long_description=long_description, config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

        # each key is an int representing the age, the value is a list of session_data
        self.sessions_by_age = dict()

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaTransientFrequencyAnalysis(config_handler=self.config_handler)
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

        for data_to_analyse in self._data_to_analyse:
            roi_response_series = data_to_analyse.get_roi_response_series()
            if len(roi_response_series) == 0:
                self.invalid_data_help = f"No roi response series available in " \
                                         f"{data_to_analyse.identifier}"
                return False
            rrs_names = data_to_analyse.get_roi_response_series_list(keywords_to_exclude=None)
            raster_in_rrs_keys = False
            for rrs_name in rrs_names:
                if 'raster' in rrs_name:
                    raster_in_rrs_keys = True
                    return True
                else:
                    continue
            if raster_in_rrs_keys is False:
                self.invalid_data_help = f"Analysis is so far based on inferred raster plot, " \
                                         f"not implemented on traces yet"
                return False

        return True

    def set_arguments_for_gui(self):
        """

        Returns:

        """
        CicadaAnalysis.set_arguments_for_gui(self)

        self.add_roi_response_series_arg_for_gui(short_description="Neuronal activity to use",
                                                 long_description=None)

        ages = []
        for session_index, session_data in enumerate(self._data_to_analyse):
            age = session_data.age
            if age not in self.sessions_by_age:
                self.sessions_by_age[age] = []
            self.sessions_by_age[age].append(session_data)
            ages.append(age)
        self.add_choices_for_groups_for_gui(arg_name="sessions_grouped_by_age", choices=np.unique(ages),
                                            with_color=False,
                                            mandatory=False,
                                            short_description="Grouped by age",
                                            long_description="If you select group of ages, stat will be produced "
                                                             "over the sessions in that age. "
                                                             "You can indicate the "
                                                             "ages in text field, such as '1-4 6 15-17'to "
                                                             "make a group "
                                                             "with age 1 to 4, 6 and 15 to 17. If None are selected, "
                                                             "then a stat will be produce for each session.",
                                            family_widget="session_selection",
                                            add_custom_group_field=True,
                                            custom_group_validation_fct=validate_indices_in_string_format,
                                            custom_group_processor_fct=None)

        cell_types = []
        for session_index, session_data in enumerate(self._data_to_analyse):
            cell_types.extend(session_data.get_all_cell_types())
        cell_types = list(set(cell_types))
        self.add_choices_for_groups_for_gui(arg_name="cell_type_groups", choices=cell_types,
                                            with_color=False,
                                            mandatory=False,
                                            short_description="Define groups of cell type",
                                            long_description="Create groups to indicate which for each cell"
                                                             "in which group ID there are. "
                                                             "Ideally, each cell type should be in a group",
                                            family_widget="figure_config_celltypes",
                                            add_custom_group_field=False)

        cell_types = []
        for session_index, session_data in enumerate(self._data_to_analyse):
            cell_types.extend(session_data.get_all_cell_types())
            cell_types = list(np.unique(cell_types))
        cell_types.insert(0, "all_cells")
        self.add_choices_arg_for_gui(arg_name="cell_to_use", choices=cell_types,
                                     default_value="all_cells",
                                     short_description="Cell type to use to plots and do statistics",
                                     multiple_choices=False,
                                     family_widget="figure_config_celltypes")

        self.add_bool_option_for_gui(arg_name="do_not_show_unclassified", true_by_default=False,
                                     short_description="Do not include 'Unclassified' as a cell-type",
                                     family_widget="figure_config_celltypes")

        time_unity = ["seconds", "minutes"]
        self.add_choices_arg_for_gui(arg_name="time_unit", choices=time_unity,
                                     default_value="minutes",
                                     short_description="Time unity for frequency",
                                     multiple_choices=False,
                                     family_widget="figure_config_data_to_use")

        self.add_bool_option_for_gui(arg_name="save_table", true_by_default=True,
                                     short_description="Save results in table",
                                     family_widget="figure_config_saving")

        self.add_bool_option_for_gui(arg_name="save_figure", true_by_default=True,
                                     short_description="Save figure",
                                     family_widget="figure_config_saving")

        representations = ["strip", "swarm", "violin", "box", "bar", "boxen"]
        self.add_choices_arg_for_gui(arg_name="representation", choices=representations,
                                     default_value="box",
                                     short_description="Kind of plot to use",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        x_ax = ["Age", "Group", "SubjectID", "Session", "Celltype", "Weight"]
        self.add_choices_arg_for_gui(arg_name="x_axis", choices=x_ax,
                                     default_value="Age",
                                     short_description="Variable to use for x axis groups",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        possible_hues = ["Age", "SubjectID", "Session", "Celltype", "Weight", "None"]
        self.add_choices_arg_for_gui(arg_name="hue", choices=possible_hues,
                                     default_value="Celltype",
                                     short_description="Variable to use for x axis sub-groups",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        palettes = ["muted", "deep", "pastel", "Blues"]
        self.add_choices_arg_for_gui(arg_name="palettes", choices=palettes,
                                     default_value="muted",
                                     short_description="Color palette for x-axis subgroups",
                                     long_description="In that case figure facecolor and figure edgecolor are useless",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        cell_comp = []
        for session_index, session_data in enumerate(self._data_to_analyse):
            cell_comp.extend(session_data.get_all_cell_types())
            cell_comp = list(np.unique(cell_comp))
        self.add_choices_arg_for_gui(arg_name="cell_types_to_compare", choices=cell_comp,
                                     default_value="",
                                     short_description="Cell types to compare (all sessions merged)",
                                     multiple_choices=True,
                                     family_widget="figure_config_stats")

        self.add_bool_option_for_gui(arg_name="do_stats", true_by_default=False,
                                     short_description="Try statistical tests",
                                     family_widget="figure_config_stats")

        self.add_int_values_arg_for_gui(arg_name="pvalue", min_value=1, max_value=5,
                                        short_description="p-value (%) for statistical test",
                                        default_value=5, family_widget="figure_config_stats")

        self.add_image_format_package_for_gui()

        self.add_color_arg_for_gui(arg_name="background_color", default_value=(0, 0, 0, 1.),
                                   short_description="background color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="fig_facecolor", default_value=(1, 1, 1, 1.),
                                   short_description="Figure face color",
                                   long_description="Useless if a 'hue' is specified, in such a case use 'palette'",
                                   family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="axis_color", default_value=(1, 1, 1, 1.),
                                   short_description="Axes color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="labels_color", default_value=(1, 1, 1, 1.),
                                   short_description="Label color",
                                   long_description=None, family_widget="figure_config_color")

        policies = ["Arial", "Cambria", "Rosa", "Times", "Calibri"]
        self.add_choices_arg_for_gui(arg_name="font_type", choices=policies,
                                     default_value="Arial", short_description="Font type",
                                     multiple_choices=False,
                                     family_widget="figure_config_label")

        weights = ["light", "normal", "bold", "extra bold"]
        self.add_choices_arg_for_gui(arg_name="fontweight", choices=weights,
                                     default_value="normal", short_description="Font Weight",
                                     multiple_choices=False,
                                     family_widget="figure_config_label")

        self.add_int_values_arg_for_gui(arg_name="font_size", min_value=1, max_value=100,
                                        short_description="Font size",
                                        default_value=10, family_widget="figure_config_label")

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
        print("Transients' frequency: coming soon...")

        roi_response_series_dict = kwargs["roi_response_series"]

        groups_by_cell_from_widget = kwargs.get("cell_type_groups")

        cell_to_use = kwargs.get("cell_to_use")

        do_not_show_unclassified = kwargs.get("do_not_show_unclassified")

        x_axis_name = kwargs.get("x_axis")

        hue = kwargs.get("hue")

        kind = kwargs.get("representation")

        palette = kwargs.get("palettes")

        do_stats = kwargs.get("do_stats")

        cell_types_to_compare = kwargs.get("cell_types_to_compare")

        pvalue = kwargs.get("pvalue")
        pvalue = pvalue / 100

        verbose = kwargs.get("verbose", True)

        time_unit = kwargs.get("time_unit")

        background_color = kwargs.get("background_color")

        fig_facecolor = kwargs.get("fig_facecolor")

        axis_color = kwargs.get("axis_color")

        labels_color = kwargs.get("labels_color")

        font_size = kwargs.get("font_size")

        fontweight = kwargs.get("fontweight")

        fontfamily = kwargs.get("font_type")

        # image package format
        save_formats = kwargs["save_formats"]
        if save_formats is None:
            save_formats = "pdf"

        save_table = kwargs.get("save_table")

        save_figure = kwargs.get("save_figure")

        dpi = kwargs.get("dpi", 100)

        width_fig = kwargs.get("width_fig")

        height_fig = kwargs.get("height_fig")

        with_timestamp_in_file_name = kwargs.get("with_timestamp_in_file_name", True)

        # dict results from widget
        groups_by_age_from_widget = kwargs.get("sessions_grouped_by_age")

        # first we create a dict that will identify group of session by an id
        # a group could be just a session
        # dict key is a string, value is a list of CicadaAnalysisWrapper instances
        session_group_ids_dict = dict()

        # take as key a session identifier and return the group_id it is part of
        session_to_group_id_mapping = dict()

        start_time = time()

        n_sessions = len(self._data_to_analyse)
        if verbose:
            print(f"{n_sessions} sessions to analyse")

        # first building the groups
        if len(groups_by_age_from_widget) > 0:
            x_axis_name = "Group"
            for session_group_id, session_group_info in groups_by_age_from_widget.items():
                # session_group_info is a list with 2 elements, the second one is a color code
                # (4 float between 0 and 1) or None if not color option is activated.
                # For exemple: {'5-6': [['5', '6'], (1.0, 1.0, 1.0, 1.0)], '7-10': [['7-10'], (1.0, 1.0, 1.0, 1.0)]}
                # the first element is either a list of string representing int, or a list of more complex int like
                # 7-10 meaning from p7 to p10
                ages_in_group = []
                age_codes_in_group = session_group_info[0]
                group_color = session_group_info[1]
                for age_code in age_codes_in_group:
                    try:
                        age = int(age_code)
                        ages_in_group.append(age)
                    except ValueError:
                        ages_in_group.extend(extract_indices_from_string(age_code))
                session_group_ids_dict[session_group_id] = []
                for age in ages_in_group:
                    if age in self.sessions_by_age:
                        sessions = self.sessions_by_age[age]
                        for session_data in sessions:
                            session_identifier = session_data.identifier
                            session_to_group_id_mapping[session_identifier] = session_group_id
                            session_group_ids_dict[session_group_id].append(session_data)

        else:
            # each session is its own group
            for session_index, session_data in enumerate(self._data_to_analyse):
                session_identifier = session_data.identifier
                session_to_group_id_mapping[session_identifier] = session_identifier
                session_group_ids_dict[session_identifier] = [session_data]

        # Dict with key the name of cell type group, value is the cell types in (list of str)
        cell_types_groups_dict = dict()
        # key is the name of a cell type, value is the name of the group it belongs
        cell_type_to_cell_type_group_dict = dict()
        # print(f"groups_by_cell_from_widget {groups_by_cell_from_widget}")
        # Then deciding on cell types to include
        if len(groups_by_cell_from_widget) > 0:
            for cell_group_id, cell_group_info in groups_by_cell_from_widget.items():
                # cell_group_info is a list with 2 elements, the second one is a color code
                # (4 float between 0 and 1) or None if not color option is activated.
                cell_types_groups_dict[cell_group_id] = cell_group_info[0]
                for cell_type in cell_group_info[0]:
                    cell_type_to_cell_type_group_dict[cell_type] = cell_group_id
        # print(f"cell_type_to_cell_type_group_dict {cell_type_to_cell_type_group_dict}")

        global_frequence_data_table = pd.DataFrame()
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

            # Get Data
            if isinstance(roi_response_series_dict, dict):
                roi_response_serie_info = roi_response_series_dict[session_identifier]
            else:
                roi_response_serie_info = roi_response_series_dict

            invalid_times = session_data.get_interval_times(interval_name="invalid_times")
            duration_invalid_times_in_sec = 0
            # Get Neuronal Data
            neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)
            neuronal_data_timestamps = session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_info)
            raster_dur = neuronal_data
            n_cells, n_frames = raster_dur.shape

            # each index correspond to a frame of CI, and indicate if it is considered as invalid frame
            invalid_times_bool_array = np.zeros(n_frames, dtype="bool")

            if verbose:
                print(f"N cells: {n_cells}, N frames: {n_frames}")

            if invalid_times is not None:
                for index in range(invalid_times.shape[1]):
                    start_ts = invalid_times[0, index]
                    stop_ts = invalid_times[1, index]
                    duration_invalid_times_in_sec += (stop_ts - start_ts)
                    # for each epoch, we update invalid_times_bool_array
                    start_frame = find_nearest(array=neuronal_data_timestamps, value=start_ts, is_sorted=True)
                    stop_frame = find_nearest(array=neuronal_data_timestamps, value=stop_ts, is_sorted=True)
                    invalid_times_bool_array[start_frame:stop_frame+1] = True
                print(f"Number of invalid frames: {np.sum(invalid_times_bool_array)} over {invalid_times.shape[1]} epochs")

            # Get Data Timestamps
            duration_s = neuronal_data_timestamps[len(neuronal_data_timestamps)-1] - neuronal_data_timestamps[0]
            # removing invalid_times duration
            duration_s -= duration_invalid_times_in_sec
            duration_m = duration_s / 60
            if verbose:
                print(f"Acquisition last for : {duration_s:.2f} seconds // {duration_m:.2f} minutes ")

            # Get Cell-type data and build cell-type list
            cell_indices_by_cell_type = session_data.get_cell_indices_by_cell_type(roi_serie_keys=
                                                                                   roi_response_serie_info)
            cell_type_list = []
            cell_type_group_list = []
            for cell in range(n_cells):
                cell_type_list.append("Unclassified")
                cell_type_group_list.append("Unclassified")

            for key, info in cell_indices_by_cell_type.items():
                cell_type = key.capitalize()
                indexes = cell_indices_by_cell_type.get(key)
                tmp_n_cell = len(indexes)
                for cell in range(tmp_n_cell):
                    tmp_ind = indexes[cell]
                    cell_type_list[tmp_ind] = cell_type
                    if key in cell_type_to_cell_type_group_dict:
                        cell_type_group_list[tmp_ind] = cell_type_to_cell_type_group_dict[key]
                    # else:
                    #     print(f"Key {key} not in cell_type_to_cell_type_group_dict")

            # Check Data with respect to the specific analysis
            type_required = cell_to_use.capitalize()
            if type_required != "All_cells":
                if type_required not in cell_type_list:
                    if verbose:
                        print(f"No {type_required} identified in this session")
                        print(f"Session: {session_identifier} not included in plots and statistics")

            # Building raster plot from rasterdur
            raster = np.zeros((n_cells, n_frames))
            for cell in range(n_cells):
                tmp_tple = get_continous_time_periods(raster_dur[cell, :])
                for tple in range(len(tmp_tple)):
                    onset = tmp_tple[tple][0]
                    # if the onset is in an invalid epoch, we skip it
                    if invalid_times_bool_array[onset]:
                        continue
                    raster[cell, onset] = 1

            # Building spike frequency vector
            n_onsets = np.sum(raster, axis=1)
            transient_frequeny_second = n_onsets / duration_s
            transient_frequeny_minute = n_onsets / duration_m
            if time_unit == "seconds":
                distribution_all_cells = transient_frequeny_second
            else:
                distribution_all_cells = transient_frequeny_minute

            # Generate pd.DataFrame table #
            age_list = [info_dict['age'] for k in range(n_cells)]
            weight_list = [info_dict['weight'] for k in range(n_cells)]
            session_identifier_list = [info_dict['identifier'] for k in range(n_cells)]
            animal_id_list = [info_dict['subject_id'] for k in range(n_cells)]
            group_id = session_identifier
            if session_identifier in session_to_group_id_mapping:
                group_id = session_to_group_id_mapping[session_identifier]
            group_id_list = [group_id] * n_cells
            sum_up_data = {'N_transients': n_onsets, 'Frequence': distribution_all_cells, 'Cell#': np.arange(n_cells),
                           'Celltype': cell_type_list,
                           'Celltype_group': cell_type_group_list,
                           'Session': session_identifier_list, 'SubjectID': animal_id_list, f'Age': age_list,
                           'Group': group_id_list,
                           'Weight': weight_list}
            frequence_data_table = pd.DataFrame(sum_up_data)

            # If possible compare across cell types for this session:
            unique_types = np.unique(cell_type_list)
            unique_types_list = unique_types.tolist()
            frequencies_lists = []
            if do_stats and len(unique_types_list) > 1:
                for index, name in enumerate(unique_types_list):
                    table = frequence_data_table.query('Celltype == @name')
                    frequencies = table.get("Frequence")
                    frequencies_list = frequencies.values.tolist()
                    frequencies_lists.append(frequencies_list)
                if verbose:
                    print(f"--------------------- Basic stats: {session_identifier} ---------------------")
                    print(f"Compare transient frequency across the different cell-types: {unique_types_list}")
                if len(unique_types_list) == 2:
                    compare_two_distributions(frequencies_lists[0], frequencies_lists[1],
                                              pvalues=pvalue, verbose=verbose)
                if len(unique_types_list) > 2:
                    multiple_comparison_one_factor_effect(frequencies_lists, pvalues=pvalue, verbose=verbose,
                                                          sessions_ids=unique_types_list)

            # Generate / append global pd.DataFrame table #
            global_frequence_data_table = global_frequence_data_table.append(frequence_data_table, ignore_index=True)

            self.update_progressbar(start_time, 100 / n_sessions)

        if verbose:
            print(f" ")
            print(f"------------------------------- GENERATE SUMMARY ----------------------------------")
            print(f"Generate simplest tables to keep one value per session or one value per animal")

        # Generate a simplest table that keep one value per session #
        by_session_data_table_with_celltype = \
            global_frequence_data_table.groupby(['SubjectID', 'Session', 'Celltype'])\
                .agg({f'Age': 'mean', 'Cell#': 'size', 'Weight': 'mean',
                      'Frequence': ['mean', 'std', 'min', 'median', 'max']})\
                .rename(columns={'Cell#': 'N_Cells', 'Frequence': 'Frequency_description'})
        by_session_data_table_without_celltype = \
            global_frequence_data_table.groupby(['SubjectID', 'Session'])\
                .agg({f'Age': 'mean', 'Cell#': 'size', 'Weight': 'mean',
                      'Frequence': ['mean', 'std', 'min', 'median', 'max']})\
                .rename(columns={'Cell#': 'N_Cells', 'Frequence': 'Frequency_description'})

        # Generate a simplest table that keep one value per animal #
        by_animal_data_table_with_celltype = \
            global_frequence_data_table.groupby(['SubjectID', 'Celltype']) \
                .agg({f'Age': 'mean', 'Cell#': 'size', 'Weight': 'mean',
                      'Frequence': ['mean', 'std', 'min', 'median', 'max']})\
                .rename(columns={'Cell#': 'N_Cells', 'Frequence': 'Frequency_description'})
        by_animal_data_table_without_celltype = \
            global_frequence_data_table.groupby(['SubjectID']) \
                .agg({f'Age': 'mean', 'Cell#': 'size', 'Weight': 'mean',
                      'Frequence': ['mean', 'std', 'min', 'median', 'max']})\
                .rename(columns={'Cell#': 'N_Cells', 'Frequence': 'Frequency_description'})

        # Save results in table
        if save_table:
            if verbose:
                print(f" ")
                print(f"----------------------------------- SAVINGS --------------------------------------")

        path_results = self.get_results_path()

        # Path for xlxs files #
        path_table_xls = os.path.join(f'{path_results}',
                                      f'transient_frequencies_table.xlsx')
        path_table_session_type_xls = os.path.join(f'{path_results}',
                                                   f'by_session_celltypes_transient_frequencies_table.xlsx')
        path_table_session_xls = os.path.join(f'{path_results}',
                                              f'by_session_transient_frequencies_table.xlsx')
        path_table_animal_type_xls = os.path.join(f'{path_results}',
                                                  f'by_animal_celltypes_transient_frequencies_table.xlsx')
        path_table_animal_xls = os.path.join(f'{path_results}',
                                             f'by_animal_transient_frequencies_table.xlsx')

        # Path for csv files #
        path_table_csv = os.path.join(f'{path_results}',
                                      'transient_frequencies_table.csv')
        path_table_session_type_csv = os.path.join(f'{path_results}',
                                                   f'by_session_celltypes_transient_frequencies_table.csv')
        path_table_session_csv = os.path.join(f'{path_results}',
                                              f'by_session_transient_frequencies_table.csv')
        path_table_animal_type_csv = os.path.join(f'{path_results}',
                                                  f'by_animal_celltypes_transient_frequencies_table.csv')
        path_table_animal_csv = os.path.join(f'{path_results}',
                                             f'by_animal_transient_frequencies_table.csv')

        # Do the savings #
        # save full table #
        global_frequence_data_table.to_excel(path_table_xls)
        global_frequence_data_table.to_csv(path_table_csv)
        # save table by session with cell type #
        by_session_data_table_with_celltype.to_excel(path_table_session_type_xls)
        by_session_data_table_with_celltype.to_csv(path_table_session_type_csv)
        # save table by session without cell type #
        by_session_data_table_without_celltype.to_excel(path_table_session_xls)
        by_session_data_table_without_celltype.to_csv(path_table_session_csv)
        # save table by animal with cell type #
        by_animal_data_table_with_celltype.to_excel(path_table_animal_type_xls)
        by_animal_data_table_with_celltype.to_csv(path_table_animal_type_csv)
        # save table by animal without cell type #
        by_animal_data_table_without_celltype.to_excel(path_table_animal_xls)
        by_animal_data_table_without_celltype.to_csv(path_table_animal_csv)

        if verbose:
            print(f"Data save as excel and csv files")

        # Filter general table on query from the GUI
        if cell_to_use == "all_cells":
            data_table = global_frequence_data_table
        else:
            type_to_use = cell_to_use.capitalize()
            data_table = global_frequence_data_table.query('Celltype == @type_to_use')

        if do_not_show_unclassified:
            data_table.drop(data_table.loc[data_table['Celltype'] == "Unclassified"].index, inplace=True)
        n_cells_stats = len(data_table.index)

        # Get Info
        ages = data_table.get(f"Age")
        ages_list = ages.values.tolist()
        ages_list = np.unique(ages_list)
        n_ages = len(ages_list)

        animals = data_table.get("SubjectID")
        animals_list = animals.values.tolist()
        animals_list = np.unique(animals_list)
        n_animals = len(animals_list)

        sessions = data_table.get("Session")
        sessions_list = sessions.values.tolist()
        sessions_list = np.unique(sessions_list)
        n_sessions = len(sessions_list)

        # Do Some Statistics
        if do_stats:
            if verbose:
                print(f" ")
                print(f"----------------------------------- DO STATS --------------------------------------")
            if cell_to_use == "all_cells":
                if verbose:
                    print(f"N pups: {n_animals}, N sessions: {n_sessions}, N cells: {n_cells_stats}")

                if n_ages > 1:
                    if verbose:
                        print(f"------------------- Compare {cell_to_use} frequency across ages --------------------")
                    distribution_by_age = [[] for k in range(n_ages)]
                    for index in range(n_ages):
                        age = ages_list[index]
                        tmp_table = data_table[data_table.Age == age]
                        data = tmp_table.get("Frequence")
                        data_list = data.values.tolist()
                        distribution_by_age[index] = data_list
                    multiple_comparison_one_factor_effect(distribution_by_age, pvalues=pvalue, verbose=verbose,
                                                          sessions_ids=ages_list)

                if len(cell_types_to_compare) > 1:
                    frequencies_lists = []
                    for index, key in enumerate(cell_types_to_compare):
                        name = key.capitalize()
                        table = data_table.query('Celltype == @name')
                        frequencies = table.get("Frequence")
                        frequencies_list = frequencies.values.tolist()
                        frequencies_lists.append(frequencies_list)
                    if verbose:
                        print(f"------------- Compare {cell_types_to_compare}: all data set --------------")
                    if len(cell_types_to_compare) == 2:
                        compare_two_distributions(frequencies_lists[0], frequencies_lists[1],
                                                  pvalues=pvalue, verbose=verbose)
                    if len(cell_types_to_compare) > 2:
                        multiple_comparison_one_factor_effect(frequencies_lists, pvalues=pvalue, verbose=verbose,
                                                              sessions_ids=cell_types_to_compare)

            else:
                if verbose:
                    print(f"N pups: {n_animals}, N sessions: {n_sessions}, N {cell_to_use}: {n_cells_stats}")
                if n_ages > 1:
                    if verbose:
                        print(f"------------------- Compare {cell_to_use} frequency across ages --------------------")
                    distribution_by_age = [[] for k in range(n_ages)]
                    for index in range(n_ages):
                        age = ages_list[index]
                        tmp_table = data_table[data_table.Age == age]
                        data = tmp_table.get("Frequence")
                        data_list = data.values.tolist()
                        distribution_by_age[index] = data_list
                    multiple_comparison_one_factor_effect(distribution_by_age, pvalues=pvalue, verbose=verbose,
                                                          sessions_ids=ages_list)

        # Do Some Plots
        if verbose:
            print(f" ")
            print(f"----------------------------------- DO PLOTS --------------------------------------")

        # Do the plots according to GUI requirements #

        if hue == "None":
            hue = None
            palette = None

        ylabel = "Frequency  (Transients / " + time_unit + ")"

        filename = "transient_frequency_"

        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(width_fig, height_fig), dpi=dpi)
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)

        svm = sns.catplot(x=x_axis_name, y="Frequence", hue=hue, data=data_table, hue_order=None,
                          kind=kind, orient=None, color=fig_facecolor, palette=palette, ax=ax1)

        ax1.set_ylabel(ylabel, fontsize=font_size, labelpad=20, fontweight=fontweight, fontfamily=fontfamily)
        ax1.yaxis.label.set_color(labels_color)
        ax1.xaxis.label.set_color(labels_color)
        ax1.spines['left'].set_color(axis_color)
        ax1.spines['right'].set_color(background_color)
        ax1.spines['bottom'].set_color(background_color)
        ax1.spines['top'].set_color(background_color)
        ax1.yaxis.set_tick_params(labelsize=font_size)
        ax1.xaxis.set_tick_params(labelsize=font_size)
        ax1.tick_params(axis='y', colors=axis_color)
        ax1.tick_params(axis='x', colors=axis_color)

        fig.tight_layout()
        if save_figure and (path_results is not None):
            # transforming a string in a list
            if isinstance(save_formats, str):
                save_formats = [save_formats]
            time_str = ""
            if with_timestamp_in_file_name:
                time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
            for save_format in save_formats:
                if not with_timestamp_in_file_name:
                    fig.savefig(os.path.join(f'{path_results}', f'{filename}.{save_format}'),
                                format=f"{save_format}",
                                facecolor=fig.get_facecolor())
                else:
                    fig.savefig(os.path.join(f'{path_results}', f'{filename}{time_str}.{save_format}'),
                                format=f"{save_format}",
                                facecolor=fig.get_facecolor())
        plt.close()

        if verbose:
            print(f"Plots are done")

