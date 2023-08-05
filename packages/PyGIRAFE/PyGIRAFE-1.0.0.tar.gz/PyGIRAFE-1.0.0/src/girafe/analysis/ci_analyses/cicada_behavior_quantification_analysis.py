from cicada.analysis.cicada_analysis import CicadaAnalysis
from cicada.utils.misc import print_info_dict
from datetime import datetime
from time import time
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class CicadaBehaviorQuantificationAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        long_description = '<p align="center"><b>Some quantification of the detected behaviors</b></p><br>'
        long_description = long_description + 'First you need to define groups that include one or multiple behavior(s) ' \
                                              'among the list of behaviors. <br><br>'
        long_description = long_description + 'For each session return: <br><br>'
        long_description = long_description + ' - the number of occurrences of each detected behaviors. <br><br>'
        long_description = long_description + ' - the duration of the behavior at each of its occurrence.<br><br>'
        long_description = long_description + ' - the  total duration each behavior.<br><br>'
        long_description = long_description + 'Data are saved in csv and xlxs formats.<br><br>'
        long_description = long_description + 'Customized categorical plots are done using x-axis group and subgroups'
        CicadaAnalysis.__init__(self, name="Behavior Description", family_id="Behavior",
                                short_description="Basic behavior quantification",
                                long_description=long_description,
                                config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaBehaviorQuantificationAnalysis(config_handler=self.config_handler)
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

        all_epochs = []
        for data_to_analyse in self._data_to_analyse:
            all_epochs.extend(data_to_analyse.get_behavioral_epochs_names())
        all_epochs = list(np.unique(all_epochs))
        if len(all_epochs) == 0:
            self.invalid_data_help = "No behavioral epochs associated to this recording"
            return False

        return True

    def set_arguments_for_gui(self):
        """

        Returns:

        """

        CicadaAnalysis.set_arguments_for_gui(self)

        self.add_roi_response_series_arg_for_gui(short_description="Neural activity to use "
                                                                   "(used to know the duration of the recording)",
                                                 long_description="Use only to know the duration of the recording")

        all_intervals = []
        for data_to_analyse in self._data_to_analyse:
            all_intervals.extend(data_to_analyse.get_intervals_names())
        all_intervals = list(np.unique(all_intervals))
        self.add_choices_for_groups_for_gui(arg_name="removed_intervals", choices=all_intervals,
                                            with_color=False,
                                            mandatory=False,
                                            short_description="Intervals to remove from total recording duration",
                                            long_description=None,
                                            family_widget="intervals")

        all_epochs = []
        for data_to_analyse in self._data_to_analyse:
            all_epochs.extend(data_to_analyse.get_behavioral_epochs_names())
        all_epochs = list(np.unique(all_epochs))

        self.add_choices_for_groups_for_gui(arg_name="epochs_names", choices=all_epochs,
                                            with_color=False,
                                            mandatory=False,
                                            short_description="Behavior groups",
                                            long_description="Group the different behaviors",
                                            family_widget="epochs")

        self.add_bool_option_for_gui(arg_name="save_table", true_by_default=True,
                                     short_description="Save results in table",
                                     family_widget="figure_config_saving")

        self.add_bool_option_for_gui(arg_name="save_figure", true_by_default=True,
                                     short_description="Save figure",
                                     family_widget="figure_config_saving")

        representations = ["strip", "swarm", "violin", "box", "bar", "boxen"]
        self.add_choices_arg_for_gui(arg_name="representation", choices=representations,
                                     default_value="box", short_description="Kind of plot to use",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        x_ax = ["Age", "SubjectID", "Session", "Behavior", "Group"]
        self.add_choices_arg_for_gui(arg_name="x_axis", choices=x_ax,
                                     default_value="Behavior", short_description="Variable to use for x axis groups",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        possible_hues = ["Age", "SubjectID", "Session", "Behavior", "Group", "None"]
        self.add_choices_arg_for_gui(arg_name="hue", choices=possible_hues,
                                     default_value="None",
                                     short_description="Variable to use for x axis sub-groups",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        palettes = ["muted", "deep", "pastel", "Blues"]
        self.add_choices_arg_for_gui(arg_name="palettes", choices=palettes,
                                     default_value="muted", short_description="Color palette for x-axis subgroups",
                                     long_description="In that case figure facecolor and figure edgecolor are useless",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

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

        roi_response_series_dict = kwargs["roi_response_series"]

        removed_intervals = kwargs.get("removed_intervals")

        behaviors_names = kwargs.get("epochs_names")

        x_axis_name = kwargs.get("x_axis")

        hue = kwargs.get("hue")

        kind = kwargs.get("representation")

        palette = kwargs.get("palettes")

        verbose = kwargs.get("verbose", True)

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

        start_time = time()

        print("Behavioral quantification: coming soon...")

        n_sessions = len(self._data_to_analyse)
        n_sessions_to_use = n_sessions
        if verbose:
            print(f"{n_sessions} sessions to analyse")

        session_id_dict = dict()
        animal_age_dict = dict()
        animal_weight_dict = dict()
        all_durations_by_group_by_session_dict = dict()
        sum_duration_by_group_dict_by_session_dict = dict()
        total_events_by_group_by_session_dict = dict()
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

            # Get Data (only to get recording duration)
            if isinstance(roi_response_series_dict, dict):
                roi_response_serie_info = roi_response_series_dict[session_identifier]
            else:
                roi_response_serie_info = roi_response_series_dict

            # Get Data Timestamps (only to get recording duration)
            neuronal_data_timestamps = session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_info)
            duration_s = neuronal_data_timestamps[len(neuronal_data_timestamps) - 1] - neuronal_data_timestamps[0]
            duration_m = duration_s / 60
            if verbose:
                print(f"Acquisition last for : {np.round(duration_s, decimals=2)} seconds // "
                      f"{np.round(duration_m, decimals=2)} minutes ")

            if len(removed_intervals.keys()) > 0:
                if verbose:
                    print(f"Remove {list(removed_intervals.keys())} intervals from the total duration "
                          f"estimated from  neuronal data timestamps")
                all_duration_to_remove = 0
                for group_name, intervals in removed_intervals.items():
                    interval_list = removed_intervals.get(group_name)[0]
                    if verbose:
                        print(f"Remove intervals: {interval_list}")
                    duration_to_remove = 0
                    for interval in interval_list:
                        interval_timestamps = session_data.get_interval_times(interval_name=interval)
                        interval_duration = np.sum(interval_timestamps[1, :] - interval_timestamps[0, :])
                        duration_to_remove = duration_to_remove + interval_duration
                    all_duration_to_remove = all_duration_to_remove + duration_to_remove
                if verbose:
                    print(f"Remove {np.round(all_duration_to_remove, decimals=2)} seconds to the total duration")
                final_duration_s = duration_s - all_duration_to_remove
                final_duration_m = duration_m - (all_duration_to_remove / 60)
            else:
                final_duration_s = duration_s
                final_duration_m = duration_m

            if verbose:
                print(f"Accounted time : {np.round(final_duration_s, decimals=2)} seconds // "
                      f"{np.round(final_duration_m, decimals=2)} minutes ")

            all_epochs = []
            all_epochs.extend(session_data.get_behavioral_epochs_names())
            all_epochs = list(np.unique(all_epochs))
            n_behaviors = len(all_epochs)
            if len(all_epochs) == 0:
                n_sessions_to_use = n_sessions_to_use - 1
                if verbose:
                    print(f"No behavioral epochs in this session, skip it for analysis")
                if n_sessions_to_use == 0:
                    if verbose:
                        print(f"No session can be analyzed for behavior")
                    return
                if n_sessions_to_use > 1:
                    continue

            animal_age_dict[session_identifier] = info_dict['age']
            session_id_dict[session_identifier] = info_dict['subject_id']
            animal_weight_dict[session_identifier] = info_dict['weight']

            if verbose:
                print(f"------------- Start with all behaviors identified for this session -------------")

            if verbose:
                print(f"List of observed behaviors: {all_epochs}")

            n_occurence_by_behavior = []
            durations_by_behavior = [[] for behavior in range(n_behaviors)]
            sum_durations_by_behavior_tmp_dict = dict()
            for behavior in range(n_behaviors):
                behavior_name = all_epochs[behavior]
                if verbose:
                    print(f"Behavior studied: {behavior_name}")
                behavior_timestamps = session_data.get_behavioral_epochs_times(epoch_name=behavior_name)
                before_ci_end = behavior_timestamps[1, :] < neuronal_data_timestamps[len(neuronal_data_timestamps) - 1]
                behavior_timestamps = behavior_timestamps[:, before_ci_end]
                n_occurence_behavior = behavior_timestamps.shape[1]
                durations_behavior = []
                for occurence in range(n_occurence_behavior):
                    duration = behavior_timestamps[1, occurence] - behavior_timestamps[0, occurence]
                    durations_behavior.append(duration)
                tmp_mean = np.mean(durations_behavior)
                tmp_sum = np.sum(durations_behavior)
                durations_by_behavior[behavior] = durations_behavior
                sum_durations_by_behavior_tmp_dict[behavior_name] = np.sum(durations_behavior)
                if verbose:
                    print(f"N={n_occurence_behavior}, mean duration: {tmp_mean}s, total duration"
                          f": {tmp_sum}s")
                n_occurence_by_behavior.append(n_occurence_behavior)
            mean_duration_by_behavior = [np.mean(x) for x in durations_by_behavior]
            sum_duration_by_behavior = [np.sum(x) for x in durations_by_behavior]
            if verbose:
                print(f"---------------------------------- Summary ----------------------------------")
                print(f"List of observed behaviors: {all_epochs}")
                print(f"Number of occurrences by behavior : {n_occurence_by_behavior}")
                print(f"Mean duration by behavior : {mean_duration_by_behavior}")
                print(f"Total time by behavior: {sum_duration_by_behavior}")

            if verbose:
                print(f"---------------------- Work on defined behavior groups ----------------------")

            all_durations_by_group_dict = dict()
            sum_duration_by_group_dict = dict()
            total_events_for_group_dict = dict()
            index = 0
            for behavior_group_name, behavior_info in behaviors_names.items():
                if len(behavior_info) != 2:
                    continue
                index = index + 1
                behaviors_names_by_group = behavior_info[0]
                if verbose:
                    print(f"Group {index}, name: {behavior_group_name}, includes: {behaviors_names_by_group}")

                n_behaviors_in_group = len(behaviors_names_by_group)
                durations_for_group = [[] for behavior in range(n_behaviors_in_group)]
                durations_for_group_dict = dict()
                occurences_for_group = []
                occurences_for_group_dict = dict()
                sum_duration_for_group_dict = dict()
                for behavior, behavior_name in enumerate(behaviors_names_by_group):
                    if behavior_name not in all_epochs:
                        if verbose:
                            print(f"No {behavior_name} to include in group {index} for this animal")
                        continue
                    tmp_index = all_epochs.index(behavior_name)
                    durations_for_group[behavior] = durations_by_behavior[tmp_index]
                    durations_for_group_dict[behavior_name] = durations_by_behavior[tmp_index]
                    occurences_for_group.append(n_occurence_by_behavior[tmp_index])
                    occurences_for_group_dict[behavior_name] = n_occurence_by_behavior[tmp_index]
                    sum_duration_behavior = sum_durations_by_behavior_tmp_dict[behavior_name]
                    sum_duration_for_group_dict[behavior_name] = sum_duration_behavior
                all_durations_for_group = np.concatenate(durations_for_group)
                mean_duration_for_group = np.mean(all_durations_for_group)
                total_events_for_group = np.sum(occurences_for_group)
                all_durations_by_group_dict[behavior_group_name] = durations_for_group_dict
                sum_duration_by_group_dict[behavior_group_name] = sum_duration_for_group_dict
                total_events_for_group_dict[behavior_group_name] = occurences_for_group_dict
                if verbose:
                    print(f"Total events in {behavior_group_name} group: {total_events_for_group}, "
                          f"mean duration: {mean_duration_for_group}s ")

            all_durations_by_group_by_session_dict[session_identifier] = all_durations_by_group_dict
            sum_duration_by_group_dict_by_session_dict[session_identifier] = sum_duration_by_group_dict
            total_events_by_group_by_session_dict[session_identifier] = total_events_for_group_dict
            self.update_progressbar(start_time, 100 / n_sessions)

        column_names_durations = ["Behavior", "Group", "Duration (s)", "Session", "Age", "Weight"]
        column_names_sum_durations = ["Behavior", "Group", "TotalDuration (s)", "RelativeDuration (%)", "Session",
                                      "Age", "Weight"]
        column_names_occurrences = ["Behavior", "Group", "Occurrence", "Frequency (min-1)", "Session", "Age", "Weight"]
        durations_table = pd.DataFrame(columns=column_names_durations)
        sum_duration_table = pd.DataFrame(columns=column_names_sum_durations)
        occurrences_table = pd.DataFrame(columns=column_names_occurrences)
        for session_key, data in all_durations_by_group_by_session_dict.items():
            session_data = all_durations_by_group_by_session_dict.get(session_key)
            sum_duration_data = sum_duration_by_group_dict_by_session_dict.get(session_key)
            animal_age = int(animal_age_dict.get(session_key))
            animal_id = session_id_dict.get(session_key)
            animal_weight = animal_weight_dict.get(session_key)
            if animal_weight not in ["N.A.", "none", "nd"]:
                animal_weight = float(animal_weight)
            for group_key, data_second in session_data.items():
                session_data_group = session_data.get(group_key)
                sum_duration_data_group = sum_duration_data.get(group_key)
                for behavior_key, data_third in session_data_group.items():
                    session_data_goup_behavior = session_data_group.get(behavior_key)
                    sum_duration_data_group_behavior = sum_duration_data_group.get(behavior_key)
                    n_events = len(session_data_goup_behavior)
                    occurrences_table = occurrences_table.append({'Behavior': behavior_key,
                                                                  'Group': group_key, 'Occurrence': n_events,
                                                                  'Frequency (min-1)': n_events / final_duration_m,
                                                                  'Session': session_key,
                                                                  'SubjectID': animal_id, 'Age': animal_age,
                                                                  'Weight': animal_weight}, ignore_index=True)

                    sum_duration_table = sum_duration_table.append({'Behavior': behavior_key,
                                                                    'Group': group_key,
                                                                    'TotalDuration (s)': sum_duration_data_group_behavior,
                                                                    'RelativeDuration (%)': (sum_duration_data_group_behavior / final_duration_s) * 100,
                                                                    'Session': session_key,
                                                                    'SubjectID': animal_id, 'Age': animal_age,
                                                                    'Weight': animal_weight}, ignore_index=True)
                    for event in range(n_events):
                        duration = session_data_goup_behavior[event]
                        durations_table = durations_table.append({'Behavior': behavior_key,
                                                                 'Group': group_key,
                                                                  'Duration (s)': duration, 'Session': session_key,
                                                                  'SubjectID': animal_id, 'Age': animal_age,
                                                                  'Weight': animal_weight}, ignore_index=True)

        path_results = self.get_results_path()
        path_to_occurrence_table = os.path.join(f'{path_results}', f'occurrence_frequency_table.xlsx')
        path_to_duration_table = os.path.join(f'{path_results}', f'duration_table.xlsx')
        path_to_sum_duration_table = os.path.join(f'{path_results}', f'total_relative_duration_table.xlsx')
        if save_table:
            if verbose:
                print(f"--------------------------- GENERAL SUMMARY TABLES ---------------------------")
            occurrences_table.to_excel(path_to_occurrence_table)
            if verbose:
                print(f"Occurences table is built and save")
            durations_table.to_excel(path_to_duration_table)
            if verbose:
                print(f"Durations table is built and save")
            sum_duration_table.to_excel(path_to_sum_duration_table)
            if verbose:
                print(f"Total durations table is built and save")

            if verbose:
                print(f"------------------------------ DO SOME PLOTTING ------------------------------")

        # Do the plot according to GUI requirements
        if hue == "None":
            hue = None
            palette = None

        # Figure1: occurrence
        filename = "occurrences_figure_"

        ylabel = "Number of occurrences (absolute)"

        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(width_fig, height_fig), dpi=dpi)
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)

        svm = sns.catplot(x=x_axis_name, y="Occurrence", hue=hue, data=occurrences_table, hue_order=None,
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
        ax1.tick_params(axis='x', colors=axis_color, rotation=45)

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

        # Figure2: mean duration
        filename = "durations_figure_"

        ylabel = "Behavior mean duration (s)"

        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(width_fig, height_fig), dpi=dpi)
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)

        svm = sns.catplot(x=x_axis_name, y="Duration (s)", hue=hue, data=durations_table, hue_order=None,
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
        ax1.tick_params(axis='x', colors=axis_color, rotation=45)

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

        # Figure3: total duration
        filename = "sum_durations_figure_"

        ylabel = "Behavior total duration (s)"

        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(width_fig, height_fig), dpi=dpi)
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)

        svm = sns.catplot(x=x_axis_name, y="TotalDuration (s)", hue=hue, data=sum_duration_table, hue_order=None,
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
        ax1.tick_params(axis='x', colors=axis_color, rotation=45)

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
