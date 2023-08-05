from cicada.analysis.cicada_analysis import CicadaAnalysis
from cicada.utils.misc import print_info_dict, from_timestamps_to_frame_epochs
from cicada.utils.pairwise_correlation_analysis import compute_similarity_matrix, plot_similarity_matrix
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import compress
from datetime import datetime
import os


class CicadaTwitchesActivityAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        long_description = '<p align="center"><b>Analyze twitch-related activity</b></p><br>'
        long_description = long_description + 'Look at whether the cells recruited in twitches are similar or not' \
                                              '.<br><br>'
        CicadaAnalysis.__init__(self, name="Twitches Activity", family_id="Epochs",
                                short_description="Focus on twitch-related activity",
                                long_description=long_description,
                                config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

        # key is the cell type name, value is the name of the arg to get the color from the widget
        self.cell_type_color_arg_name = dict()

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaTwitchesActivityAnalysis(config_handler=self.config_handler)
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
                self.invalid_data_help = f"No Roi Response Series available in " \
                    f"{data_to_analyse.identifier}"
                return False

        for session_index, session_data in enumerate(self._data_to_analyse):
            experimenter = session_data.experimenter
            if (experimenter not in ['RD', 'MR', 'EL', 'RD_EL']) or (experimenter is None):
                self.invalid_data_help = f"Analysis restricted to specific experiments on twitching mouse pups"
                return False
            else:
                continue

        return True

    def set_arguments_for_gui(self):
        """

        Returns:

        """
        CicadaAnalysis.set_arguments_for_gui(self)

        self.add_roi_response_series_arg_for_gui(short_description="Neural activity to use", long_description=None)

        all_intervals = []
        for data_to_analyse in self._data_to_analyse:
            all_intervals.extend(data_to_analyse.get_intervals_names())
            all_intervals.extend(data_to_analyse.get_behavioral_epochs_names())
        all_intervals = list(np.unique(all_intervals))
        # print(f"all_intervals {all_intervals}")

        if len(all_intervals) > 0:
            self.add_choices_for_groups_for_gui(arg_name="interval_names", choices=all_intervals,
                                                with_color=False,
                                                mandatory=False,
                                                short_description="Build a group containing all the 'twitches' epochs",
                                                long_description="",
                                                family_widget="epochs")

        self.add_int_values_arg_for_gui(arg_name="twitch_activity_delay", min_value=100, max_value=10000,
                                        short_description="Delay after twitch onset to link activity (ms)",
                                        default_value=2000, family_widget="twitch_config")

        self.add_bool_option_for_gui(arg_name="filter_consecutive_movements", true_by_default=True,
                                     short_description="Remove movements if separated by less than selected delay",
                                     long_description=None, family_widget="twitch_config")

        self.add_bool_option_for_gui(arg_name="verbose", true_by_default=True,
                                     short_description="Verbose: show prints",
                                     long_description=None, family_widget="prints")

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

        similarity_methods = ["Pearson", "Jacquard", "Hamming"]
        self.add_choices_arg_for_gui(arg_name="similarity_method", choices=similarity_methods,
                                     default_value="Jacquard",
                                     short_description="Epoch similarity metric",
                                     multiple_choices=False,
                                     family_widget="similarity")

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

        epochs_names = kwargs.get("interval_names")

        twitch_activity_delay = kwargs.get("twitch_activity_delay")
        twitch_activity_delay = twitch_activity_delay / 1000

        filter_consecutive_movements = kwargs.get("filter_consecutive_movements")

        verbose = kwargs.get("verbose", True)

        kind = kwargs.get("representation")

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

        similarity_method = kwargs.get("similarity_method")

        with_timestamp_in_file_name = kwargs.get("with_timestamp_in_file_name", True)

        n_sessions = len(self._data_to_analyse)

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

            if isinstance(roi_response_series_dict, dict):
                roi_response_serie_info = roi_response_series_dict[session_identifier]
            else:
                roi_response_serie_info = roi_response_series_dict

            neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)

            n_cells, n_frames = neuronal_data.shape

            neuronal_data_timestamps = session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_info)
            if verbose:
                print(f" ")

            # Build 2 dict:
            # - epochs_frames_in_group_dict: key is the group name data is a list of tuples of interval frames
            # - epochs_names_in_group_dict: key is the group name data is a list the name of the epoch
            epochs_frames_in_group_dict = dict()
            epochs_names_in_group_dict = dict()
            for epoch_group_name, epoch_info in epochs_names.items():
                if len(epoch_info) != 2:
                    continue
                epochs_names_in_group = epoch_info[0]
                # epoch_color = epoch_info[1]

                # TODO: take into consideration invalid epochs, and remove the one in invalid section
                epochs_frames_in_group = []
                epoch_name_in_group = []
                invalid_times = session_data.get_interval_times(interval_name="invalid_times")
                extended_invalid_times = None
                invalid_times_are_sorted = False

                # first we extent the invalid times to take into consideration the range of PSTH
                if invalid_times is not None:
                    invalid_times_are_sorted = np.all(np.diff(invalid_times[1]) >= 0)
                    extended_invalid_times = np.zeros(invalid_times.shape)
                    for index in range(invalid_times.shape[1]):
                        start_ts = invalid_times[0, index]
                        stop_ts = invalid_times[1, index]
                        stop_ts = stop_ts + twitch_activity_delay
                        extended_invalid_times[0, index] = start_ts
                        extended_invalid_times[1, index] = stop_ts
                # print(f"session_data.get_intervals_names() {session_data.get_intervals_names()}")
                if extended_invalid_times is not None:
                    print(f"Among {epoch_group_name}, we remove:")
                for epoch_name in epochs_names_in_group:
                    # looking in behavior or intervals
                    epochs_timestamps = session_data.get_interval_times(interval_name=epoch_name)
                    if epochs_timestamps is None:
                        epochs_timestamps = session_data.get_behavioral_epochs_times(epoch_name=epoch_name)
                    if epochs_timestamps is None:
                        # means this session doesn't have this epoch name
                        continue
                    epochs_are_sorted = np.all(np.diff(epochs_timestamps[1]) >= 0)
                    if extended_invalid_times is not None:
                        # now we want to filter epochs_timestamps
                        # we loop over each invalid epoch to remove the epoch that overlap it
                        filtered_epochs_timestamps = np.zeros(epochs_timestamps.shape)
                        n_epochs_kept = 0
                        last_epoch_kept_index = 0
                        in_invalid = 0
                        to_close_of_previous = 0
                        if verbose:
                            print(f"Before removing epochs we have: {epochs_timestamps.shape[1]} {epoch_name}")
                        for epoch_index in range(epochs_timestamps.shape[1]):
                            epoch_start_ts = epochs_timestamps[0, epoch_index]
                            epoch_stop_ts = epochs_timestamps[1, epoch_index]
                            if epoch_index == 0:
                                previous_epoch_start_ts = 0
                            else:
                                previous_epoch_start_ts = epochs_timestamps[0, last_epoch_kept_index]
                            # if ordered, and the epoch if superior at the last invalid frames known
                            # we can skip it
                            if filter_consecutive_movements is False:
                                if invalid_times_are_sorted and epochs_are_sorted and \
                                        (epoch_start_ts > extended_invalid_times[1, -1]):
                                    filtered_epochs_timestamps[:, n_epochs_kept] = epochs_timestamps[:, epoch_index]
                                    n_epochs_kept += 1
                                    continue
                            # Filter movements
                            to_filter = False
                            # Filter based on invalid times
                            if verbose and epoch_index == 0:
                                print(f"Remove {epoch_name} epochs if they overlap with invalid times")
                            for invalid_index in range(extended_invalid_times.shape[1]):
                                invalid_start_ts = extended_invalid_times[0, invalid_index]
                                invalid_stop_ts = extended_invalid_times[1, invalid_index]

                                if (epoch_start_ts >= invalid_start_ts) and (epoch_start_ts <= invalid_stop_ts):
                                    to_filter = True
                                    in_invalid += 1
                                    break
                                if (epoch_stop_ts >= invalid_start_ts) and (epoch_stop_ts <= invalid_stop_ts):
                                    to_filter = True
                                    in_invalid += 1
                                    break
                                if (epoch_start_ts <= invalid_start_ts) and (epoch_stop_ts >= invalid_stop_ts):
                                    to_filter = True
                                    in_invalid += 1
                                    break
                            # Filter based on temporal distance from previous movement
                            if filter_consecutive_movements and to_filter is False:
                                if verbose and epoch_index == 0:
                                    print(
                                        f"Remove {epoch_name} epochs if they follow the previous kept {epoch_name}"
                                        f" by less than ({np.round(twitch_activity_delay / 1000, decimals=2)} s) ")
                                if (epoch_start_ts - previous_epoch_start_ts) <= twitch_activity_delay:
                                    to_filter = True
                                    to_close_of_previous += 1

                            if not to_filter:
                                filtered_epochs_timestamps[:, n_epochs_kept] = epochs_timestamps[:, epoch_index]
                                n_epochs_kept += 1
                                last_epoch_kept_index = epoch_index
                                epoch_name_in_group.append(epoch_name)

                        filtered_epochs_timestamps = filtered_epochs_timestamps[:, :n_epochs_kept]
                        n_epochs_filtered = epochs_timestamps.shape[1] - filtered_epochs_timestamps.shape[1]
                        if verbose:
                            print(f"{n_epochs_filtered} {epoch_name} epochs removed: {in_invalid} in invalid frames, "
                                  f"{to_close_of_previous} too close from previous")
                            print(f"{filtered_epochs_timestamps.shape[1]} {epoch_name} epochs left")
                        epochs_timestamps = filtered_epochs_timestamps

                    # Modify epoch_timestamps based on defined delay instead of 'true' epoch duration
                    n_epochs = epochs_timestamps.shape[1]
                    for epoch in range(n_epochs):
                        epochs_timestamps[1, epoch] = epochs_timestamps[0, epoch] + twitch_activity_delay
                    # session_data.get_interval_times()
                    # now we want to get the intervals time_stamps and convert them in frames
                    # list of list of 2 int
                    intervals_frames = from_timestamps_to_frame_epochs(time_stamps_array=epochs_timestamps,
                                                                       frames_timestamps=neuronal_data_timestamps,
                                                                       as_list=True)
                    epochs_frames_in_group.extend(intervals_frames)

                # Order all intervals
                start_epoch = [epochs_frames_in_group[i][0] for i in range(len(epochs_frames_in_group))]
                order = np.argsort(start_epoch)
                epochs_frames_in_group.sort(key=lambda tup: tup[0])
                epoch_name_in_group = [epoch_name_in_group[i] for i in order]

                # Filter if end of epoch n-1 is after beginning of epoch n
                epochs_to_keep = [True for epoch in range(len(epochs_frames_in_group))]
                last_kept_epoch = 0
                for epoch in range(len(epochs_frames_in_group)):
                    if epochs_frames_in_group[epoch][1] > n_frames:
                        epochs_to_keep[epoch] = False
                        continue

                    if filter_consecutive_movements and epoch >= 1:
                        if epochs_frames_in_group[epoch][0] < epochs_frames_in_group[last_kept_epoch][1]:
                            epochs_to_keep[epoch] = False
                            continue
                    last_kept_epoch = epoch
                epochs_frames_in_group = list(compress(epochs_frames_in_group, epochs_to_keep))
                epoch_name_in_group = list(compress(epoch_name_in_group, epochs_to_keep))
                epochs_frames_in_group_dict[epoch_group_name] = epochs_frames_in_group
                epochs_names_in_group_dict[epoch_group_name] = epoch_name_in_group
                if verbose:
                    print(f" ")
                    print(f"Total of {len(epochs_frames_in_group)} remaining epochs in {epoch_group_name} group")

            # Loop on group to build an 'epoch recruitment' table
            if verbose:
                print(f" ")
                print(f"Compute the proportion of active cells in the {twitch_activity_delay} s after epoch")
            for group_name, interval_in_group in epochs_frames_in_group_dict.items():
                epoch_names_list = epochs_names_in_group_dict[group_name]
                n_epochs = len(interval_in_group)
                epoch_matrix = np.zeros((n_cells, n_epochs), dtype=int)
                for epoch in range(n_epochs):
                    epoch_matrix[:, epoch] = np.amax(neuronal_data[:,
                                                     np.arange(interval_in_group[epoch][0], interval_in_group[epoch][1])],
                                                     axis=1)
                n_cells_by_twitch = np.sum(epoch_matrix, axis=0)
                prop_cell_by_twitch = (n_cells_by_twitch / n_cells) * 100

                age_list = [info_dict['age'] for k in range(n_epochs)]
                weight_list = [info_dict['weight'] for k in range(n_epochs)]
                session_identifier_list = [info_dict['identifier'] for k in range(n_epochs)]
                animal_id_list = [info_dict['subject_id'] for k in range(n_epochs)]
                group_id_list = [group_name for k in range(n_epochs)]
                sum_up_data_1 = {'Age': age_list, 'SubjectID': animal_id_list, 'Session': session_identifier_list,
                                 'Weight': weight_list,
                                 'Epoch#': np.arange(n_epochs), 'Group': group_id_list, 'Epoch type': epoch_names_list,
                                 'Recruited cells (%)': prop_cell_by_twitch}
                epoch_recruitment_data_table = pd.DataFrame(sum_up_data_1)

                # Save a table:
                filename = session_identifier + '_epochs_recruitment'
                path_results = self.get_results_path()
                # Path for xlxs files #
                if verbose:
                    print(f"Save results in a table")
                path_table_xls = os.path.join(f'{path_results}', f'{filename}.xlsx')
                epoch_recruitment_data_table.to_excel(path_table_xls)

                # Figure from table:
                if verbose:
                    print(f"Plot a figure")
                legend_time = np.round(twitch_activity_delay, decimals=2)
                ylabel = f"% of cell in the {legend_time} s after epoch"

                filename = f"{session_identifier}_epochs_recruitment_"

                fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                        gridspec_kw={'height_ratios': [1]},
                                        figsize=(width_fig, height_fig), dpi=dpi)
                ax1.set_facecolor(background_color)
                fig.patch.set_facecolor(background_color)

                svm = sns.catplot(x="Epoch type", y="Recruited cells (%)", data=epoch_recruitment_data_table,
                                  hue_order=None, kind=kind, orient=None, color=fig_facecolor, ax=ax1)

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
                plt.close('all')

            # Loop on group to build an 'epoch similarity' table
            if verbose:
                print(f" ")
                print(f"Compute the similarity in the recruited cells between each pair of epochs")
            for group_name, interval_in_group in epochs_frames_in_group_dict.items():
                epoch_names_list = epochs_names_in_group_dict[group_name]
                n_epochs = len(interval_in_group)
                epoch_matrix = np.zeros((n_cells, n_epochs), dtype=int)
                for epoch in range(n_epochs):
                    epoch_matrix[:, epoch] = np.amax(neuronal_data[:,
                                                     np.arange(interval_in_group[epoch][0],
                                                               interval_in_group[epoch][1])],
                                                     axis=1)

                # Measure similarity between each pair of columns and output in table
                # (transpose data to put twitches in lines and use already made function)
                similarity_matrix = compute_similarity_matrix(neuronal_data=np.transpose(epoch_matrix),
                                                              method=similarity_method, verbose=verbose)
                if verbose:
                    print(f"Plot similarity matrix")
                plot_similarity_matrix(similarity_matrix,
                                       filename=f"{session_identifier}_{group_name}_similarity_matrix",
                                       background_color=background_color,
                                       size_fig=(width_fig, height_fig),
                                       save_figure=True,
                                       path_results=self.get_results_path(),
                                       save_formats=save_formats,
                                       with_timestamp_in_file_name=with_timestamp_in_file_name)

                # Put the result in a table:
                epoch_one_index = []
                epoch_one_types = []
                epoch_two_index = []
                epoch_two_types = []
                epoch_pair_type = []
                similarity_values = []
                identical_epoch = []
                for epoch_one in range(n_epochs):
                    for epoch_two in np.arange((epoch_one + 1), n_epochs):
                        epoch_one_type = epoch_names_list[epoch_one]
                        epoch_one_types.append(epoch_one_type)
                        epoch_two_type = epoch_names_list[epoch_two]
                        epoch_two_types.append(epoch_two_type)
                        epoch_one_index.append(epoch_one)
                        epoch_two_index.append(epoch_two)
                        if epoch_one_type == epoch_two_type:
                            identical_epoch.append('Identical pair')
                        else:
                            identical_epoch.append('Different pair')
                        if f'{epoch_two_type}_vs_{epoch_one_type}' in epoch_pair_type:
                            epoch_pair_type.append(f'{epoch_two_type}_vs_{epoch_one_type}')
                        else:
                            epoch_pair_type.append(f'{epoch_one_type}_vs_{epoch_two_type}')
                        similarity_value = similarity_matrix[epoch_one, epoch_two]
                        similarity_values.append(similarity_value)
                age_list = [info_dict['age'] for k in range(len(similarity_values))]
                weight_list = [info_dict['weight'] for k in range(len(similarity_values))]
                session_identifier_list = [info_dict['identifier'] for k in range(len(similarity_values))]
                animal_id_list = [info_dict['subject_id'] for k in range(len(similarity_values))]
                sum_up_data_2 = {'Age': age_list, 'SubjectID': animal_id_list, 'Session': session_identifier_list,
                                 'Weight': weight_list,
                                 'Epoch1#': epoch_one_index, 'Epoch1 type': epoch_one_types,
                                 'Epoch2#': epoch_two_index, 'Epoch2 type': epoch_two_types,
                                 'Epoch pair type': epoch_pair_type, 'Pair type': identical_epoch,
                                 'Similarity': similarity_values}
                epoch_similarity_data_table = pd.DataFrame(sum_up_data_2)

                # Save a table:
                if verbose:
                    print(f"Save results in a table")
                filename = session_identifier + '_epochs_similarity'
                path_results = self.get_results_path()
                # Path for xlxs files #
                path_table_xls = os.path.join(f'{path_results}', f'{filename}.xlsx')
                epoch_similarity_data_table.to_excel(path_table_xls)

                # Figure 1 from table:
                if verbose:
                    print(f"Plot a figure")
                ylabel = f"Epoch {similarity_method} similarity "

                filename = f"{session_identifier}_epochs_similarity_v1_"

                fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                        gridspec_kw={'height_ratios': [1]},
                                        figsize=(width_fig, height_fig), dpi=dpi)
                ax1.set_facecolor(background_color)
                fig.patch.set_facecolor(background_color)

                svm = sns.catplot(x="Epoch pair type", y="Similarity", data=epoch_similarity_data_table,
                                  hue_order=None, kind=kind, orient=None, color=fig_facecolor, ax=ax1)

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
                ax1.tick_params(axis='x', colors=axis_color, labelrotation=90)

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
                plt.close('all')

                # Figure 2 from table:
                if verbose:
                    print(f"Plot a figure")
                ylabel = f"Epoch {similarity_method} similarity "

                filename = f"{session_identifier}_epochs_similarity_v2_"

                fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                        gridspec_kw={'height_ratios': [1]},
                                        figsize=(width_fig, height_fig), dpi=dpi)
                ax1.set_facecolor(background_color)
                fig.patch.set_facecolor(background_color)

                svm = sns.catplot(x="Pair type", y="Similarity", data=epoch_similarity_data_table,
                                  hue_order=None, kind=kind, orient=None, color=fig_facecolor, ax=ax1)

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
                ax1.tick_params(axis='x', colors=axis_color, labelrotation=45)

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
                plt.close('all')

            self.update_progressbar(time_started=self.analysis_start_time, increment_value=100 / n_sessions)
        if verbose:
            print(f" ")
            print(f"ANALYSIS DONE")

