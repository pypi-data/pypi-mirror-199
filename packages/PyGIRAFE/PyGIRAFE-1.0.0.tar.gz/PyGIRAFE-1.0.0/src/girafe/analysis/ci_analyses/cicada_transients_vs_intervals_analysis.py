from cicada.analysis.cicada_analysis import CicadaAnalysis
from cicada.utils.misc import get_continous_time_periods
from cicada.utils.misc import from_timestamps_to_frame_epochs, print_info_dict
from time import time
import os
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class CicadaTransientsVsIntervalsAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        long_description = '<p align="center"><b>Rate of calcium event for each cell in defined epochs</b></p><br>'
        long_description = long_description + 'Allows the user to defined epochs. For each epoch we then count the ' \
                                              'number of calcium events for each cell and divide it by the total' \
                                              ' duration of the considered epoch. <br><br>'
        long_description = long_description + 'Return an activation rate for each cell for each defined epoch.<br><br>'
        long_description = long_description + 'Data are saved in table (one line per cell) in csv and xlxs formats.' \
                                              ' Customized categorical plots are done'
        CicadaAnalysis.__init__(self, name="Epochs' transient frequency", family_id="Epochs",
                                short_description="Transient frequency in different time epochs",
                                long_description=long_description,
                                config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaTransientsVsIntervalsAnalysis(config_handler=self.config_handler)
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

        self.add_roi_response_series_arg_for_gui(short_description="Neuronal activity to use", long_description=None)

        epoch_def = ["auto", "manual"]
        self.add_choices_arg_for_gui(arg_name="epoch_definition", choices=epoch_def,
                                     default_value="auto", short_description="How to define epoch",
                                     multiple_choices=False,
                                     family_widget="epochs")

        all_epochs = []
        for data_to_analyse in self._data_to_analyse:
            all_epochs.extend(data_to_analyse.get_behavioral_epochs_names())
            all_epochs.extend(data_to_analyse.get_intervals_names())
        all_epochs = list(np.unique(all_epochs))
        self.add_choices_for_groups_for_gui(arg_name="epochs_names", choices=all_epochs,
                                            with_color=False,
                                            mandatory=False,
                                            short_description="Epochs composition",
                                            long_description="Define epoch name and composition",
                                            family_widget="epochs")

        self.add_int_values_arg_for_gui(arg_name="first_epoch_start", min_value=0, max_value=100,
                                        short_description="Percentage of recording to start epoch 1",
                                        default_value=0, family_widget="epochs")

        self.add_int_values_arg_for_gui(arg_name="first_epoch_stop", min_value=0, max_value=100,
                                        short_description="Percentage of recording to stop epoch 1",
                                        default_value=25, family_widget="epochs")

        self.add_int_values_arg_for_gui(arg_name="second_epoch_start", min_value=0, max_value=100,
                                        short_description="Percentage of recording to start epoch 2",
                                        default_value=75, family_widget="epochs")

        self.add_int_values_arg_for_gui(arg_name="second_epoch_stop", min_value=0, max_value=100,
                                        short_description="Percentage of recording to stop epoch 2",
                                        default_value=100, family_widget="epochs")

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
                                     default_value="minutes", short_description="Time unity for frequency",
                                     multiple_choices=False,
                                     family_widget="figure_config_data_to_use")

        self.add_bool_option_for_gui(arg_name="specify_twitches_duration", true_by_default=False,
                                     short_description="Arbitrary set twitch duration",
                                     family_widget="figure_config_twitches_duration")

        self.add_int_values_arg_for_gui(arg_name="twitches_duration", min_value=100, max_value=1500,
                                        short_description="Duration after twitch to define 'twitch-related' transient (ms)",
                                        default_value=1000, family_widget="figure_config_twitches_duration")

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

        x_ax = ["Age", "SubjectID", "Session", "Celltype"]
        self.add_choices_arg_for_gui(arg_name="x_axis", choices=x_ax,
                                     default_value="Age", short_description="Variable to use for x axis groups",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        possible_hues = ["Age", "SubjectID", "Session", "Celltype", "None"]
        self.add_choices_arg_for_gui(arg_name="hue", choices=possible_hues,
                                     default_value="Celltype",
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
        testa
        :param kwargs:
          segmentation

        :return:
        """
        CicadaAnalysis.run_analysis(self, **kwargs)

        verbose = kwargs.get("verbose", True)

        roi_response_series_dict = kwargs["roi_response_series"]

        epoch_definition = kwargs.get('epoch_definition')

        epochs_names = kwargs.get("epochs_names")
        if epoch_definition == "auto":
            if (epochs_names is None) or len(epochs_names) == 0:
                print(f"No epochs selected, no analysis")
                self.update_progressbar(time_started=self.analysis_start_time, increment_value=100)
                return

        first_epoch_start = kwargs.get("first_epoch_start")

        first_epoch_stop = kwargs.get("first_epoch_stop")

        second_epoch_start = kwargs.get("second_epoch_start")

        second_epoch_stop = kwargs.get("second_epoch_stop")

        cell_to_use = kwargs.get("cell_to_use")

        do_not_show_unclassified = kwargs.get("do_not_show_unclassified")

        time_unit = kwargs.get("time_unit")

        specify_twitches_duration = kwargs.get("specify_twitches_duration")

        save_table = kwargs.get("save_table")

        save_figure = kwargs.get("save_figure")

        x_axis_name = kwargs.get("x_axis")

        hue = kwargs.get("hue")

        kind = kwargs.get("representation")

        palette = kwargs.get("palettes")

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

        dpi = kwargs.get("dpi", 100)

        width_fig = kwargs.get("width_fig")

        height_fig = kwargs.get("height_fig")

        with_timestamp_in_file_name = kwargs.get("with_timestamp_in_file_name", True)

        start_time = time()
        print("Transients frequency in multiple epochs: coming soon...")
        n_sessions = len(self._data_to_analyse)

        global_epoch_frequency_table = pd.DataFrame()
        group_name_list = []
        for session_index, session_data in enumerate(self._data_to_analyse):
            # Get Session Info
            info_dict = session_data.get_sessions_info()
            session_identifier = info_dict['identifier']

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

            # Get Data Timestamps
            neuronal_data_timestamps = session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_info)
            duration_s = neuronal_data_timestamps[len(neuronal_data_timestamps)-1] - neuronal_data_timestamps[0]
            duration_m = duration_s / 60
            if verbose:
                print(f"Acquisition last for : {duration_s} seconds // {duration_m} minutes ")

            # Get Neuronal Data
            neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)
            raster_dur = neuronal_data
            [n_cells, n_frames] = raster_dur.shape
            if verbose:
                print(f"N cells: {n_cells}, N frames: {n_frames}")

            # Get Cell-type Data and build cell-type list
            cell_indices_by_cell_type = session_data.get_cell_indices_by_cell_type(roi_serie_keys=
                                                                                   roi_response_serie_info)
            cell_type_list = []
            for cell in range(n_cells):
                cell_type_list.append("Unclassified")

            for key, info in cell_indices_by_cell_type.items():
                cell_type = key.capitalize()
                indexes = cell_indices_by_cell_type.get(key)
                tmp_n_cell = len(indexes)
                for cell in range(tmp_n_cell):
                    tmp_ind = indexes[cell]
                    cell_type_list[tmp_ind] = cell_type

            # Check Data with respect to the specific analysis
            type_required = cell_to_use.capitalize()
            if type_required != "All_cells":
                if type_required not in cell_type_list:
                    if verbose:
                        print(f"No {type_required} identified in this session")
                        print(f"Session: {session_identifier} not included in plots")

            # Building raster plot from rasterdur
            raster = np.zeros((n_cells, n_frames))
            for cell in range(n_cells):
                tmp_tple = get_continous_time_periods(raster_dur[cell, :])
                for tple in range(len(tmp_tple)):
                    onset = tmp_tple[tple][0]
                    raster[cell, onset] = 1

            # Get total spike
            total_spikes = np.sum(raster, axis=1)

            # Get the sampling rate and number of frames to consider after twitches
            sampling_rate = session_data.get_ci_movie_sampling_rate(only_2_photons=True)
            twitches_duration = kwargs.get("twitches_duration")
            twitches_duration = twitches_duration / 1000
            frames_delay = int(np.round(twitches_duration * sampling_rate))

            # Building spike frequency vector for each main epoch
            # Loop on each defined main epoch
            n_spikes_by_epoch_dict = dict()
            spike_frequency_by_epoch = dict()
            group_duration_seconds = []
            group_duration_minutes = []
            group_names = []
            spikes_in_epoch = np.zeros((n_cells, ), dtype=int)
            if epoch_definition == 'auto':
                for epoch_group_name, epoch_info in epochs_names.items():
                    if len(epoch_info) != 2:
                        continue
                    group_names.append(epoch_group_name)

                    # Check whether this main epoch is the one of twitches
                    name_to_check = epoch_group_name.lower()
                    twitches_group = False
                    if name_to_check.find('twi') != -1:
                        twitches_group = True

                    epochs_names_in_group = epoch_info[0]
                    if verbose:
                        print(f"Group name: {epoch_group_name}")
                        print(f"Includes: {epochs_names_in_group}")

                    # Loop on all the epochs included in the main epoch
                    epochs_frames_in_group = []
                    epochs_duration_group = []
                    for epoch_name in epochs_names_in_group:
                        # looking in behavior or intervals
                        epochs_timestamps = session_data.get_interval_times(interval_name=epoch_name)
                        if epochs_timestamps is None:
                            epochs_timestamps = session_data.get_behavioral_epochs_times(epoch_name=epoch_name)
                        if epochs_timestamps is None:
                            # means this session doesn't have this epoch name
                            continue
                        # Take the durations:
                        epoch_durations = []
                        n_events = epochs_timestamps.shape[1]
                        for event in range(n_events):
                            if twitches_group is True and specify_twitches_duration is True:
                                duration = twitches_duration
                            else:
                                duration = epochs_timestamps[1, event] - epochs_timestamps[0, event]
                            epoch_durations.append(duration)
                        epoch_total_duration = np.sum(epoch_durations)
                        epochs_duration_group.append(epoch_total_duration)
                        # now we want to get the intervals time_stamps and convert them in frames
                        intervals_frames = from_timestamps_to_frame_epochs(time_stamps_array=epochs_timestamps,
                                                                           frames_timestamps=neuronal_data_timestamps,
                                                                           as_list=True)
                        epochs_frames_in_group.extend(intervals_frames)

                    main_epoch_total_duration = np.sum(epochs_duration_group)
                    main_epoch_total_duration_min = main_epoch_total_duration / 60
                    if verbose:
                        print(f"Total duration in minutes: {main_epoch_total_duration_min}")
                    group_duration_seconds.append(main_epoch_total_duration)
                    group_duration_minutes.append(main_epoch_total_duration_min)

                    n_events_in_main_epoch = len(epochs_frames_in_group)
                    n_spikes_in_main_epoch = np.zeros((n_cells, ), dtype=int)
                    for event in range(n_events_in_main_epoch):
                        start = epochs_frames_in_group[event][0]
                        if twitches_group is True and specify_twitches_duration is True:
                            end = epochs_frames_in_group[event][0] + frames_delay
                        else:
                            end = epochs_frames_in_group[event][1]
                        frames_to_take = np.arange(start, end + 1)
                        n_spikes = np.sum(raster[:, frames_to_take], axis=1)
                        n_spikes_in_main_epoch = n_spikes_in_main_epoch + n_spikes
                    n_spikes_by_epoch_dict[epoch_group_name] = n_spikes_in_main_epoch
                    spikes_in_epoch = spikes_in_epoch + n_spikes_in_main_epoch

                    if time_unit == "seconds":
                        frequency_in_main_epoch = n_spikes_in_main_epoch / main_epoch_total_duration
                    else:
                        frequency_in_main_epoch = n_spikes_in_main_epoch / main_epoch_total_duration_min
                    spike_frequency_by_epoch[epoch_group_name] = frequency_in_main_epoch

                rest_duration_seconds = duration_s - np.sum(group_duration_seconds)
                rest_duration_minutes = rest_duration_seconds / 60
                if verbose:
                    print(f"Total 'Movements' duration: {np.sum(group_duration_minutes)} minutes")
                    print(f"Total 'Rest' duration: {rest_duration_minutes} minutes")
                # Spike frequency during rest
                spikes_in_rest = total_spikes - spikes_in_epoch
                if time_unit == "seconds":
                    rest_frequency = spikes_in_rest / rest_duration_seconds
                else:
                    rest_frequency = spikes_in_rest / rest_duration_minutes
            if epoch_definition == 'manual':
                # Do the first epoch
                first_epoch_start_ts = neuronal_data_timestamps[np.round((first_epoch_start / 100) * len(neuronal_data_timestamps))]
                first_epoch_stop_ts = neuronal_data_timestamps[np.round((first_epoch_stop / 100) * len(neuronal_data_timestamps))]

                first_epoch_total_duration = first_epoch_stop_ts - first_epoch_start_ts
                first_epoch_total_duration_min = first_epoch_total_duration / 60

                first_epoch_timestamps = np.vstack((first_epoch_start_ts, first_epoch_stop_ts))


                first_intervals_frames = from_timestamps_to_frame_epochs(time_stamps_array=first_epoch_timestamps,
                                                                         frames_timestamps=neuronal_data_timestamps,
                                                                         as_list=True)
                frames_to_take = np.arange(first_intervals_frames[0][0], first_intervals_frames[0][1])

                first_epoch_n_spikes = np.sum(raster[:, frames_to_take], axis=1)
                n_spikes_by_epoch_dict[f'Epoch1_{first_epoch_start}%_{first_epoch_stop}%'] = first_epoch_n_spikes

                if time_unit == "seconds":
                    frequency_in_first_epoch = first_epoch_n_spikes / first_epoch_total_duration
                else:
                    frequency_in_first_epoch = first_epoch_n_spikes / first_epoch_total_duration_min
                spike_frequency_by_epoch[f'Epoch1_{first_epoch_start}%_{first_epoch_stop}%'] = frequency_in_first_epoch

                # Do the second epoch
                second_epoch_start_ts = neuronal_data_timestamps[np.round((second_epoch_start / 100) * len(neuronal_data_timestamps))]
                second_epoch_stop_ts = neuronal_data_timestamps[np.round((second_epoch_stop / 100) * len(neuronal_data_timestamps)) - 1]

                second_epoch_total_duration = second_epoch_stop_ts - second_epoch_stop_ts
                second_epoch_total_duration_min = first_epoch_total_duration / 60

                second_epoch_timestamps = np.vstack((second_epoch_start_ts, second_epoch_stop_ts))
                second_intervals_frames = from_timestamps_to_frame_epochs(time_stamps_array=second_epoch_timestamps,
                                                                          frames_timestamps=neuronal_data_timestamps,
                                                                          as_list=True)
                frames_to_take = np.arange(second_intervals_frames[0][0], second_intervals_frames[0][1])

                second_epoch_n_spikes = np.sum(raster[:, frames_to_take], axis=1)
                n_spikes_by_epoch_dict[f'Epoch2_{second_epoch_start}%_{second_epoch_stop}%'] = second_epoch_n_spikes

                if time_unit == "seconds":
                    frequency_in_second_epoch = second_epoch_n_spikes / second_epoch_total_duration
                else:
                    frequency_in_second_epoch = second_epoch_n_spikes / second_epoch_total_duration_min
                spike_frequency_by_epoch[f'Epoch2_{second_epoch_start}%_{second_epoch_stop}%'] = frequency_in_second_epoch

                spikes_in_rest = ['NA'] * n_cells
                rest_frequency = ['NA'] * n_cells

            # Build pd.DataFrame table
            age_list = [info_dict['age'] for k in range(n_cells)]
            weight_list = [info_dict['weight'] for k in range(n_cells)]
            session_identifier_list = [session_identifier for k in range(n_cells)]
            animal_id_list = [info_dict['subject_id'] for k in range(n_cells)]
            sum_up_data = {'Age': age_list, 'Weight': weight_list, 'SubjectID': animal_id_list,
                           'Session': session_identifier_list, 'Cell#': np.arange(n_cells),
                           'Celltype': cell_type_list, 'N_Rest_transients': spikes_in_rest, 'Rest': rest_frequency}
            epoch_frequency_table = pd.DataFrame(sum_up_data)

            # Append a new column of each group define in the GUI
            for group_key, data in spike_frequency_by_epoch.items():
                frequencies = spike_frequency_by_epoch.get(group_key)
                n_spikes = n_spikes_by_epoch_dict.get(group_key)
                fz_name = group_key
                spikes_name = 'n_' + group_key + '_transients'
                epoch_frequency_table[spikes_name] = n_spikes
                epoch_frequency_table[fz_name] = frequencies

            global_epoch_frequency_table = global_epoch_frequency_table.append(epoch_frequency_table, ignore_index=True)
            group_name_list.append(group_names)
            self.update_progressbar(start_time, 100 / n_sessions)

        if verbose:
            print(f"------------------------------- GENERATE SUMMARY ----------------------------------")
            print(f"Generate simplest tables to keep one value per session or one value per animal")

        # Generate a simplest table that keep one value per session #
        by_session_data_table_with_celltype = \
            global_epoch_frequency_table.groupby(['SubjectID', 'Session', 'Celltype']) \
                .agg({'mean', 'median', 'std', 'size'})
        by_session_data_table_without_celltype = \
            global_epoch_frequency_table.groupby(['SubjectID', 'Session']) \
                .agg({'mean', 'median', 'std', 'size'})

        # Generate a simplest table that keep one value per animal #
        by_animal_data_table_with_celltype = \
            global_epoch_frequency_table.groupby(['SubjectID', 'Celltype']) \
                .agg({'mean', 'median', 'std', 'size'})
        by_animal_data_table_without_celltype = \
            global_epoch_frequency_table.groupby(['SubjectID']) \
                .agg({'mean', 'median', 'std', 'size'})

        # Save results in table
        if save_table:
            if verbose:
                print(f"----------------------------------- SAVINGS --------------------------------------")

        path_results = self.get_results_path()

        # Path for xlxs files #
        path_table_xls = os.path.join(f'{path_results}',
                                      f'transient_epoch_frequencies_table.xlsx')
        path_table_session_type_xls = os.path.join(f'{path_results}',
                                                   f'by_session_celltypes_epoch_transient_frequencies_table.xlsx')
        path_table_session_xls = os.path.join(f'{path_results}',
                                              f'by_session_transient_epoch_frequencies_table.xlsx')
        path_table_animal_type_xls = os.path.join(f'{path_results}',
                                                  f'by_animal_celltypes_transient_epoch_frequencies_table.xlsx')
        path_table_animal_xls = os.path.join(f'{path_results}',
                                             f'by_animal_transient_epoch_frequencies_table.xlsx')

        # Path for csv files #
        path_table_csv = os.path.join(f'{path_results}',
                                      'transient_epoch_frequencies_table.csv')
        path_table_session_type_csv = os.path.join(f'{path_results}',
                                                   f'by_session_celltypes_transient_epoch_frequencies_table.csv')
        path_table_session_csv = os.path.join(f'{path_results}',
                                              f'by_session_transient_epoch_frequencies_table.csv')
        path_table_animal_type_csv = os.path.join(f'{path_results}',
                                                  f'by_animal_celltypes_transient_epoch_frequencies_table.csv')
        path_table_animal_csv = os.path.join(f'{path_results}',
                                             f'by_animal_transient_epoch_frequencies_table.csv')

        # Do the savings #
        # save full table #
        global_epoch_frequency_table.to_excel(path_table_xls)
        global_epoch_frequency_table.to_csv(path_table_csv)
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
            data_table = global_epoch_frequency_table
        else:
            type_to_use = cell_to_use.capitalize()
            data_table = global_epoch_frequency_table.query('Celltype == @type_to_use')

        if do_not_show_unclassified:
            data_table.drop(data_table.loc[data_table['Celltype'] == "Unclassified"].index, inplace=True)
        n_cells_stats = len(data_table.index)

        # Get Info
        ages = data_table.get("Age")
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

        group_name_list = np.unique(group_name_list)
        my_set = set(group_name_list)
        new_group_name_list = list(my_set)
        new_group_name_list.append('Rest')

        if verbose:
            print(f"N pups: {n_animals}, N sessions: {n_sessions}, N cells: {n_cells_stats}")

        # Do Some Plots
        if verbose:
            print(f"----------------------------------- DO PLOTS --------------------------------------")

        # Do the plot according to GUI requirements
        if hue == "None":
            hue = None
            palette = None

        for index, name in enumerate(new_group_name_list):

            ylabel = " Transient's frequency in " + name + " (Transients / " + time_unit + ")"

            filename = "transient_frequency_in_" + name

            y_axis_name = name

            fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                    gridspec_kw={'height_ratios': [1]},
                                    figsize=(width_fig, height_fig), dpi=dpi)
            ax1.set_facecolor(background_color)
            fig.patch.set_facecolor(background_color)

            svm = sns.catplot(x=x_axis_name, y=y_axis_name, hue=hue, data=data_table,
                              hue_order=None,
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


