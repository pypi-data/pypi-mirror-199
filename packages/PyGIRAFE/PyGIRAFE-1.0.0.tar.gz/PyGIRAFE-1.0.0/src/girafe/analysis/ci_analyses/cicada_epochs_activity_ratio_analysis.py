from cicada.analysis.cicada_analysis import CicadaAnalysis
from time import time
from cicada.utils.misc import get_continous_time_periods, print_info_dict
import numpy as np
from datetime import datetime
from cicada.utils.display.distribution_plot import plot_hist_distribution, plot_scatter_family
from cicada.utils.misc import from_timestamps_to_frame_epochs, validate_indices_in_string_format, \
    extract_indices_from_string, find_nearest
import pandas as pd
import os
from sortedcontainers import SortedDict
import matplotlib.pyplot as plt
import seaborn as sns


class CicadaEpochsActivityRatioAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        long_description = '<p align="center"><b>Compute activity ratio around an epochs</b></p><br>'
        long_description = long_description + 'For a given type of epochs, compute if an epoch activate or deactivate' \
                                              ' cells.<br><br>'
        CicadaAnalysis.__init__(self, name="Activity ratio around epochs", family_id="Epochs",
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
        analysis_copy = CicadaEpochsActivityRatioAnalysis(config_handler=self.config_handler)
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

        # use age group
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
        self.add_choices_for_groups_for_gui(arg_name="cell_to_use", choices=cell_types,
                                            with_color=False,
                                            mandatory=False,
                                            short_description="Cell type to use",
                                            long_description="Create a group to indicate which cell type to take"
                                                             "in consideration. Only the first group will be taken "
                                                             "into consideration. If more than one group, ",
                                            family_widget="figure_config_celltypes",
                                            add_custom_group_field=False)

        all_epochs = []
        for data_to_analyse in self._data_to_analyse:
            all_epochs.extend(data_to_analyse.get_intervals_names())
            all_epochs.extend(data_to_analyse.get_behavioral_epochs_names())
        all_epochs = list(np.unique(all_epochs))

        self.add_choices_for_groups_for_gui(arg_name="epochs_names", choices=all_epochs,
                                            with_color=False,
                                            mandatory=False,
                                            short_description="Epochs",
                                            long_description="Select epochs to use. ONly one group will be used",
                                            family_widget="epochs")
        # self.add_choices_arg_for_gui(arg_name="epoch_name", choices=all_epochs,
        #                              default_value=all_epochs[0],
        #                              multiple_choices=False,
        #                              short_description="Epochs",
        #                              long_description="Select epochs to use",
        #                              family_widget="epochs")

        epoch_thresholds = ["beginning", "middle", "end"]
        self.add_choices_arg_for_gui(arg_name="start_point_name", choices=epoch_thresholds,
                                     default_value=epoch_thresholds[0],
                                     short_description="Epoch start point",
                                     long_description="Determine from which part of the epoch to look back in time",
                                     multiple_choices=False,
                                     family_widget="epochs")

        epoch_thresholds = ["beginning", "middle", "end"]
        self.add_choices_arg_for_gui(arg_name="end_point_name", choices=epoch_thresholds,
                                     default_value=epoch_thresholds[0],
                                     short_description="Epoch end point",
                                     long_description="Determine from which part of the epoch to look ahead in time",
                                     multiple_choices=False,
                                     family_widget="epochs")

        self.add_int_values_arg_for_gui(arg_name="time_before", min_value=0, max_value=10000,
                                        short_description="Time before epoch (in ms)",
                                        default_value=2000, family_widget="epochs")

        self.add_int_values_arg_for_gui(arg_name="time_after", min_value=0, max_value=10000,
                                        short_description="Time after epoch (in ms)",
                                        default_value=2000, family_widget="epochs")

        self.add_int_values_arg_for_gui(arg_name="inhibition_threshold", min_value=10, max_value=50,
                                        short_description="Inhibition threshold",
                                        long_description="Threshold under which the ratio of activity (%) "
                                                         "is considered as an inhibition ",
                                        default_value=50, family_widget="epochs")

        self.add_int_values_arg_for_gui(arg_name="activation_threshold", min_value=50, max_value=90,
                                        short_description="Activation threshold",
                                        long_description="Threshold above which the ratio of activity (%) "
                                                         "is considered as an activation ",
                                        default_value=50, family_widget="epochs")

        self.add_bool_option_for_gui(arg_name="neutral_mode", true_by_default=True,
                                     short_description="Neutral mode",
                                     long_description="if selected, display the events that are neither inhibitor "
                                                      "nor activator, and put them in the neutral category",
                                     family_widget="epochs")

        self.add_color_arg_for_gui(arg_name="activation_color", default_value=(0, 0, 1, 1.),
                                   short_description="Activation color",
                                   long_description=None, family_widget="epochs")

        self.add_color_arg_for_gui(arg_name="inhibition_color", default_value=(1, 0, 0, 1.),
                                   short_description="Inhibition color",
                                   long_description=None, family_widget="epochs")

        self.add_color_arg_for_gui(arg_name="neutral_color", default_value=(1, 1, 1, 1.),
                                   short_description="Neutral color",
                                   long_description=None, family_widget="epochs")

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

        palettes = ["muted", "deep", "pastel", "Blues"]
        self.add_choices_arg_for_gui(arg_name="palettes", choices=palettes,
                                     default_value="muted",
                                     short_description="Color palette for x-axis subgroups",
                                     long_description="In that case figure facecolor and figure edgecolor are useless",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        # self.add_bool_option_for_gui(arg_name="do_stats", true_by_default=True,
        #                              short_description="Try statistical tests",
        #                              family_widget="figure_config_stats")

        # self.add_int_values_arg_for_gui(arg_name="pvalue", min_value=1, max_value=5,
        #                                 short_description="p-value (%) for statistical test",
        #                                 default_value=5, family_widget="figure_config_stats")

        self.add_image_format_package_for_gui()

        self.add_color_arg_for_gui(arg_name="background_color", default_value=(0, 0, 0, 1.),
                                   short_description="background color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="fig_facecolor", default_value=(0, 0, 1, 1.),
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

        epochs_names = kwargs.get("epochs_names")
        if (epochs_names is None) or len(epochs_names) == 0:
            print(f"No epochs selected, no analysis")
            self.update_progressbar(time_started=self.analysis_start_time, increment_value=100)
            return

        time_before = kwargs.get("time_before")
        # from ms to seconds
        time_before = time_before / 1000

        time_after = kwargs.get("time_after")
        # from ms to seconds
        time_after = time_after / 1000

        start_point_name = kwargs["start_point_name"]
        end_point_name = kwargs["end_point_name"]

        inhibition_threshold = kwargs["inhibition_threshold"]

        activation_threshold = kwargs["activation_threshold"]

        activation_color = kwargs["activation_color"]

        inhibition_color = kwargs["inhibition_color"]

        neutral_color = kwargs["neutral_color"]

        neutral_mode = kwargs["neutral_mode"]

        if (inhibition_threshold == 50) and (activation_threshold == 50):
            # neutral mode doesn't make sense in that case
            neutral_mode = False

        # x_axis_name = kwargs.get("x_axis")
        #
        # hue = kwargs.get("hue")
        #
        # kind = kwargs.get("representation")
        #
        # palette = kwargs.get("palettes")
        #
        # do_stats = kwargs.get("do_stats")
        #
        # cell_types_to_compare = kwargs.get("cell_types_to_compare")
        #
        # pvalue = kwargs.get("pvalue")
        # pvalue = pvalue / 100

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

        groups_by_cell_from_widget = kwargs.get("cell_to_use")

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
            # print(f"groups_by_age_from_widget {groups_by_age_from_widget}")
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

        # list of cell types, if empty, we choose all cells
        cell_types_to_keep = []
        cell_type_group_name = "All"
        # Then deciding on cell types to include
        if len(groups_by_cell_from_widget) > 0:
            for cell_group_id, cell_group_info in groups_by_cell_from_widget.items():
                # cell_group_info is a list with 2 elements, the second one is a color code
                # (4 float between 0 and 1) or None if not color option is activated.
                cell_types_to_keep = cell_group_info[0]
                cell_type_group_name = cell_group_id
                # only one group
                break

        # key is a str or int representing the age group, value is an int
        n_activator_epochs_by_age_group = SortedDict(alpha_numeric_comparator)
        n_inhibitor_epochs_by_age_group = SortedDict(alpha_numeric_comparator)
        n_neutral_epochs_by_age_group = SortedDict(alpha_numeric_comparator)

        global_ratio_df = pd.DataFrame()

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

            # Get Neuronal Data
            neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)
            neuronal_data_timestamps = session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_info)
            raster_dur = neuronal_data
            n_cells, n_frames = raster_dur.shape

            # dict with key the cell_type name and value an array of int representing the cell indices of this type
            cell_indices_by_cell_type = session_data.get_cell_indices_by_cell_type(roi_serie_keys=
                                                                                   roi_response_serie_info)

            if len(cell_types_to_keep) == 0:
                # we use all cells
                cell_indices_in_group = np.arange(n_cells)
            else:
                cell_indices_in_group = []
                for cells_type_name in cell_types_to_keep:
                    # then we extract the cell_indices from the cells_group_name
                    # it is either a string representing the cell_type or a series of indices
                    if cells_type_name in cell_indices_by_cell_type:
                        cell_indices_in_group.extend(cell_indices_by_cell_type[cells_type_name])
            cell_indices_in_group = np.array(cell_indices_in_group)
            # if no cells, we skip it
            if len(cell_indices_in_group) == 0:
                continue

            invalid_times = session_data.get_interval_times(interval_name="invalid_times")
            duration_invalid_times_in_sec = 0

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
                    invalid_times_bool_array[start_frame:stop_frame + 1] = True
                print(
                    f"Number of invalid frames: {np.sum(invalid_times_bool_array)} over {invalid_times.shape[1]} epochs")

            # Get Data Timestamps
            duration_s = neuronal_data_timestamps[len(neuronal_data_timestamps) - 1] - neuronal_data_timestamps[0]
            # removing invalid_times duration
            duration_s -= duration_invalid_times_in_sec
            duration_m = duration_s / 60
            if verbose:
                print(f"Acquisition last for : {duration_s:.2f} seconds // {duration_m:.2f} minutes ")

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

            activity_ratios = []
            name_of_epoch_group_used = ""
            start_frame_list = []
            bhv_names_list = []

            for epoch_group_name, epoch_info in epochs_names.items():
                name_of_epoch_group_used = epoch_group_name
                epochs_names_in_group = epoch_info[0]
                for epoch_name in epochs_names_in_group:
                    # epochs_timestamps : interval times (start and stop in seconds) as a numpy array of 2*n_times.
                    epochs_timestamps = session_data.get_interval_times(interval_name=epoch_name)
                    if epochs_timestamps is None:
                        epochs_timestamps = session_data.get_behavioral_epochs_times(epoch_name=epoch_name)
                    if epochs_timestamps is None:
                        # means this session doesn't have this epoch name
                        continue

                    # list of the ratio of the number of spikes before vs after the epoch
                    # in percentage

                    for epoch_index in range(epochs_timestamps.shape[1]):
                        if start_point_name == "beginning":
                            start_point = epochs_timestamps[0, epoch_index]
                        elif start_point_name == "end":
                            start_point = epochs_timestamps[1, epoch_index]
                        else:
                            start_point = (epochs_timestamps[0, epoch_index] + epochs_timestamps[1, epoch_index]) / 2

                        if end_point_name == "beginning":
                            end_point = epochs_timestamps[0, epoch_index]
                        elif end_point_name == "end":
                            end_point = epochs_timestamps[1, epoch_index]
                        else:
                            end_point = (epochs_timestamps[0, epoch_index] + epochs_timestamps[1, epoch_index]) / 2

                        # first we make sure all range is available
                        if start_point - time_before < neuronal_data_timestamps[0]:
                            continue
                        if end_point + time_after > neuronal_data_timestamps[-1]:
                            continue
                        start_ts = start_point - time_before
                        stop_ts = end_point + time_after
                        # pass it to frame
                        start_frame = find_nearest(array=neuronal_data_timestamps, value=start_ts, is_sorted=True)
                        middle_frame = find_nearest(array=neuronal_data_timestamps, value=epochs_timestamps[0,
                                                                                                            epoch_index],
                                                    is_sorted=True)
                        stop_frame = find_nearest(array=neuronal_data_timestamps, value=stop_ts, is_sorted=True)
                        # we consider this epoch, only if no invalid frames are in the range before, or after
                        if np.sum(invalid_times_bool_array[start_frame:stop_frame + 1]) > 0:
                            continue

                        # sum before the epoch
                        sum_before = np.sum(raster[cell_indices_in_group, start_frame:middle_frame])

                        sum_after = np.sum(raster[cell_indices_in_group, middle_frame:stop_frame + 1])
                        ratio = (sum_after / (sum_after + sum_before)) * 100
                        activity_ratios.append(ratio)
                        start_frame_list.append(middle_frame)
                        bhv_names_list.append(epoch_name)
                # using only one group
                continue

            n_ratios = len(activity_ratios)
            if n_ratios == 0:
                continue
            activity_ratios = np.array(activity_ratios)
            start_frame_list = np.array(start_frame_list)
            np.save(file=os.path.join(self.get_results_path(), f"{session_identifier}_mvt_onsets"),
                    arr=start_frame_list, allow_pickle=True, fix_imports=True)

            group_id = session_identifier
            if session_identifier in session_to_group_id_mapping:
                group_id = session_to_group_id_mapping[session_identifier]

            if group_id not in n_activator_epochs_by_age_group:
                n_activator_epochs_by_age_group[group_id] = 0
                n_inhibitor_epochs_by_age_group[group_id] = 0
                n_neutral_epochs_by_age_group[group_id] = 0

            n_activator_epochs_by_age_group[group_id] += len(np.where(activity_ratios >= activation_threshold)[0])
            n_inhibitor_epochs_by_age_group[group_id] += len(np.where(activity_ratios <= inhibition_threshold)[0])
            if neutral_mode:
                n_neutral_epochs_by_age_group[group_id] += np.sum(np.logical_and(activity_ratios > inhibition_threshold,
                                                                                 activity_ratios < activation_threshold))

            sum_up_data = {'Behavior': bhv_names_list,
                           'Mvt Onset Frame': start_frame_list, 'Activity ratio': activity_ratios,
                           'Celltype': cell_type_group_name,
                           'Session': [session_identifier] * n_ratios,
                           'SubjectID': [info_dict['subject_id']] * n_ratios,
                           'Group': [group_id] * n_ratios}
            ratio_df = pd.DataFrame(sum_up_data)
            global_ratio_df = global_ratio_df.append(ratio_df, ignore_index=True)
            self.update_progressbar(start_time, 100 / n_sessions)

        path_results = self.get_results_path()
        # Save results in table
        if save_table:
            if verbose:
                print(f"----------------------------------- SAVINGS --------------------------------------")
            path_table_xls = os.path.join(f'{path_results}', f'activation_ratio_{name_of_epoch_group_used}_table.xlsx')
            path_table_csv = os.path.join(f'{path_results}', f'activation_ratio_{name_of_epoch_group_used}_table.csv')
            if save_table:
                global_ratio_df.to_excel(path_table_xls)
                global_ratio_df.to_csv(path_table_csv)
                if verbose:
                    print(f"Data save as excel and csv files")

        all_sessions_df = global_ratio_df
        sessions = all_sessions_df.get("Session")
        sessions_list = sessions.values.tolist()
        sessions_list = np.unique(sessions_list)
        n_sessions = len(sessions_list)

        # ploting distribution for each session
        for session in sessions_list:
            session_df = all_sessions_df.query('Session == @session')

            filename = f"activation_ratio_{name_of_epoch_group_used}_{session}"

            activity_ratios = session_df.get("Activity ratio")
            plot_hist_distribution(distribution_data=activity_ratios,
                                   filename=filename,
                                   values_to_scatter=None,
                                   n_bins=10,
                                   use_log=False,
                                   x_range=(0, 100),
                                   labels=None,
                                   scatter_shapes=None,
                                   colors=None,
                                   tight_x_range=False,
                                   twice_more_bins=False,
                                   scale_them_all=False,
                                   background_color=background_color,
                                   hist_facecolor="white",
                                   hist_edgeccolor=fig_facecolor,
                                   axis_labels_color=labels_color,
                                   axis_color="white",
                                   axis_label_font_size=20,
                                   ticks_labels_color="white",
                                   ticks_label_size=14,
                                   xlabel="",
                                   ylabel="Activity ratio (%)",
                                   fontweight=fontweight,
                                   fontfamily=fontfamily,
                                   size_fig=None,
                                   dpi=dpi,
                                   path_results=path_results,
                                   save_formats=save_formats,
                                   ax_to_use=None,
                                   color_to_use=None, legend_str=None,
                                   density=False,
                                   save_figure=True,
                                   with_timestamp_in_file_name=with_timestamp_in_file_name,
                                   max_value=None)

        scatter_dict = dict()
        color_dict = dict()
        x_ticks_labels = []

        activator_label = f"activator {name_of_epoch_group_used} "
        inhibitor_label = f"inhibitor {name_of_epoch_group_used} "
        neutral_label = f"neutral {name_of_epoch_group_used}"

        scatter_dict[activator_label] = [[], [], [], []]
        scatter_dict[inhibitor_label] = [[], [], [], []]

        color_dict[activator_label] = activation_color
        color_dict[inhibitor_label] = inhibition_color

        if neutral_mode:
            scatter_dict[neutral_label] = [[], [], [], []]
            color_dict[neutral_label] = neutral_color

        # for x label
        age_group_index_dict = dict()
        index = 0
        for age_group in n_activator_epochs_by_age_group.keys():
            age_group_index_dict[age_group] = index
            index += 1

        for age_group, n_epochs in n_activator_epochs_by_age_group.items():
            scatter_dict[activator_label][0].append(age_group_index_dict[age_group])
            # we want the proportion of epoch
            n_epochs_total = n_epochs + n_inhibitor_epochs_by_age_group[age_group] + \
                             n_neutral_epochs_by_age_group[age_group]
            scatter_dict[activator_label][1].append((n_epochs / n_epochs_total) * 100)
            scatter_dict[activator_label][3].append('o')
            x_ticks_labels.append(f"{age_group}\n({n_epochs_total})")

        x_ticks_pos = np.arange(len(scatter_dict[activator_label][0]))

        for age_group, n_epochs in n_inhibitor_epochs_by_age_group.items():
            scatter_dict[inhibitor_label][0].append(age_group_index_dict[age_group])
            # we want the proportion of epoch
            n_epochs_total = n_epochs + n_activator_epochs_by_age_group[age_group] + \
                             n_neutral_epochs_by_age_group[age_group]
            scatter_dict[inhibitor_label][1].append((n_epochs / n_epochs_total) * 100)
            scatter_dict[inhibitor_label][3].append('o')
        if neutral_mode:
            for age_group, n_epochs in n_neutral_epochs_by_age_group.items():
                scatter_dict[neutral_label][0].append(age_group_index_dict[age_group])
                # we want the proportion of epoch
                n_epochs_total = n_epochs + n_activator_epochs_by_age_group[age_group] + \
                                 n_inhibitor_epochs_by_age_group[age_group]
                scatter_dict[neutral_label][1].append((n_epochs / n_epochs_total) * 100)
                scatter_dict[neutral_label][3].append('o')

        label_to_legend_dict = dict()
        label_to_legend_dict[activator_label] = activator_label
        label_to_legend_dict[inhibitor_label] = inhibitor_label
        if neutral_mode:
            label_to_legend_dict[neutral_label] = neutral_label

        # now plotting the scatter of the number of events defined as inhibitor or activator
        plot_scatter_family(data_dict=scatter_dict,
                            x_ticks_labels=x_ticks_labels,
                            x_ticks_pos=x_ticks_pos,
                            label_to_legend=label_to_legend_dict,
                            colors_dict=color_dict,
                            filename=f"inhibition_vs_activation_{name_of_epoch_group_used}",
                            y_label=f"{name_of_epoch_group_used} proportion (%)",
                            path_results=path_results, y_lim=[0, 100],
                            x_label="Age",
                            y_log=False,
                            scatter_size=150,
                            scatter_alpha=1,
                            plots_linewidth=1,
                            lines_plot_values=None,
                            background_color=background_color,
                            link_scatter=True,
                            marker_to_legend=None,
                            labels_color=labels_color,
                            with_x_jitter=0,
                            with_y_jitter=None,
                            with_text=False,
                            x_labels_rotation=None,
                            save_formats=save_formats,
                            dpi=dpi,
                            with_timestamp_in_file_name=with_timestamp_in_file_name)


def alpha_numeric_comparator(data):
    """

    :param data: (str)
    :return:
    """
    if len(data) == 1 and data[0].isnumeric():
        return int(data[0])
    if len(data) > 1 and data[:2].isnumeric():
        return int(data[:2])
    return 99999
