from cicada.analysis.cicada_analysis import CicadaAnalysis
from time import time
from datetime import datetime
from cicada.utils.misc import from_timestamps_to_frame_epochs, print_info_dict
from cicada.utils.sce_stats_utils import detect_sce_on_traces
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.signal as sci_si
import pandas as pd
import os


class CicadaSceDescriptionTraces(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        long_description = '<p align="center"><b>Describe Synchronous Calcium Events (SCEs)</b></p><br>'

        long_description = long_description + 'First detect SCEs using the raw calcium traces.' \
                                              ' SCEs are defined as frames with more co-active cells than ' \
                                              'a threshold defined by the user (same as Malvache 2016).<br><br>'

        CicadaAnalysis.__init__(self, name="SCE description from traces", family_id="Descriptive statistics",
                                short_description="Basic SCE statistics (from traces)",
                                long_description=long_description,
                                config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaSceDescriptionTraces(config_handler=self.config_handler)
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

        return True

    def set_arguments_for_gui(self):
        """

        Returns:

        """
        CicadaAnalysis.set_arguments_for_gui(self)

        self.add_roi_response_series_arg_for_gui(short_description="Neuronal activity to use: select calcium traces",
                                                 long_description=None)

        self.add_bool_option_for_gui(arg_name="verbose", true_by_default=True,
                                     short_description="Verbose: show prints",
                                     long_description=None, family_widget="prints")

        all_epochs = []
        for data_to_analyse in self._data_to_analyse:
            all_epochs.extend(data_to_analyse.get_behavioral_epochs_names())
        all_epochs = list(np.unique(all_epochs))

        possibilities = ['full_recording', 'Use_epoch']
        self.add_choices_arg_for_gui(arg_name="epochs_to_use", choices=possibilities,
                                     default_value="full_recording",
                                     short_description="Use the full recording or a specific epoch to compute SCE "
                                                       "threshold from surrogates",
                                     multiple_choices=False,
                                     family_widget="epochs_for_sce_threshold")

        self.add_choices_for_groups_for_gui(arg_name="epochs_names_sce_threshold", choices=all_epochs,
                                            with_color=False,
                                            mandatory=False,
                                            short_description="Define 1 epoch to compute SCE threshold",
                                            long_description="Define 1 epoch to restrict SCE threshold determination "
                                                             "from surrogates",
                                            family_widget="epochs_for_sce_threshold")

        self.add_choices_for_groups_for_gui(arg_name="epochs_names", choices=all_epochs,
                                            with_color=False,
                                            mandatory=False,
                                            short_description="Define epochs to see to which epochs belong SCEs",
                                            long_description="Define epoch name and composition",
                                            family_widget="epochs_for_stats")

        self.add_int_values_arg_for_gui(arg_name="synchronous_time", min_value=50, max_value=300,
                                        short_description="Max time between two 'co-active' cells in a single SCE (ms)",
                                        default_value=200, family_widget="figure_config_method_to_use")

        self.add_bool_option_for_gui(arg_name="use_speed", true_by_default=False,
                                     short_description="Use mouse speed to restrict SCEs detection to period "
                                                       "of immobility",
                                     family_widget="speed_epochs")

        self.add_int_values_arg_for_gui(arg_name="speed_threshold", min_value=1, max_value=10,
                                        short_description="Speed below which consider the mouse immobile (cm/s)",
                                        default_value=1, family_widget="speed_epochs")

        self.add_int_values_arg_for_gui(arg_name="min_sce_distance", min_value=1, max_value=10,
                                        short_description="Minimal number of frames between 2 SCEs",
                                        default_value=5, family_widget="figure_config_method_to_use")

        self.add_int_values_arg_for_gui(arg_name="sce_n_cells_threshold", min_value=1, max_value=10,
                                        short_description="Minimal number of co-active cells in SCEs defined on traces",
                                        default_value=5, family_widget="figure_config_method_to_use")

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

        verbose = kwargs.get("verbose", True)

        roi_response_series_dict = kwargs["roi_response_series"]

        epochs_names = kwargs.get("epochs_names")

        epochs_to_use = kwargs.get("epochs_to_use")

        sces_epoch = kwargs.get("epochs_names_sce_threshold")

        use_speed = kwargs.get("use_speed")

        speed_threshold = kwargs.get("speed_threshold")

        sce_n_cells_threshold = kwargs.get("sce_n_cells_threshold")

        min_sce_distance = kwargs.get("min_sce_distance")

        synchronous_time = kwargs.get("synchronous_time")
        synchronous_time = synchronous_time / 1000

        start_time = time()
        if verbose:
            print("SCE description: coming soon...")
        n_sessions = len(self._data_to_analyse)

        if verbose:
            print(f"{n_sessions} sessions to analyse")
        general_sce_recruitment_table = pd.DataFrame()
        general_cell_recruitment_table = pd.DataFrame()
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

            # Get Data Timestamps
            neuronal_data_timestamps = session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_info)
            duration_s = neuronal_data_timestamps[len(neuronal_data_timestamps) - 1] - neuronal_data_timestamps[0]
            duration_m = duration_s / 60
            if verbose:
                print(f"Acquisition last for : {np.round(duration_s, decimals=2)} seconds // "
                      f"{np.round(duration_m, decimals=2)} minutes ")

            # Get Neuronal Data
            neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)
            traces = neuronal_data
            n_cells, n_frames = traces.shape

            # Check Neuronal Data is a traces array:
            if len(np.unique(traces[0, :])) < 3:
                if verbose:
                    print(f"Selected RoiResponseSeries is not calcium traces, go to next session. "
                          f"To run SCEs description on a raster-plot run: 'SCE description from raster'")
                continue

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

            # Get the 'epoch' of each frame #
            group_names = []
            frames_in_epoch_dict = dict()
            for epoch_group_name, epoch_info in epochs_names.items():
                if len(epoch_info) != 2:
                    continue
                group_names.append(epoch_group_name)

                epochs_names_in_group = epoch_info[0]

                # Loop on all the epochs included in the main epoch
                epochs_frames_in_group = []
                for epoch_name in epochs_names_in_group:
                    # looking in behavior or intervals
                    epochs_timestamps = session_data.get_interval_times(interval_name=epoch_name)
                    if epochs_timestamps is None:
                        epochs_timestamps = session_data.get_behavioral_epochs_times(epoch_name=epoch_name)
                    if epochs_timestamps is None:
                        # means this session doesn't have this epoch name
                        continue

                    # now we want to get the intervals time_stamps and convert them in frames
                    intervals_frames = from_timestamps_to_frame_epochs(time_stamps_array=epochs_timestamps,
                                                                       frames_timestamps=neuronal_data_timestamps,
                                                                       as_list=True)
                    epochs_frames_in_group.extend(intervals_frames)

                group_name_bool = np.zeros(n_frames, dtype=int)
                n_events = len(epochs_frames_in_group)
                for event in range(n_events):
                    event_start = epochs_frames_in_group[event][0]
                    event_stop = epochs_frames_in_group[event][1] + 1
                    group_name_bool[event_start: event_stop] = 1
                frames_in_epoch_dict[epoch_group_name] = group_name_bool

            # Follow GUI requirements if ask to compute the threshold value from specified epoch
            if epochs_to_use == "full_recording":
                if verbose:
                    print(f"Do the determination of SCE threshold using the full recording")
                traces_for_sce_threshold = traces
                if verbose:
                    print(
                        f"Shape of data for SCE threshold determination: "
                        f"NCells: {traces_for_sce_threshold.shape[0]} , "
                        f"NFrames: {traces_for_sce_threshold.shape[1]}")
            else:
                keys_list = list(sces_epoch.keys())
                sce_epoch_name = keys_list[0]
                behaviors_to_get = sces_epoch.get(sce_epoch_name)
                behaviors_to_get = behaviors_to_get[0]
                if verbose:
                    print(f"Do the SCE threshold determination on "
                          f"{sce_epoch_name} epoch, that includes: {behaviors_to_get}")

                interval_frames_in_bhv = []
                frames_to_take = []
                for behavior_to_get in behaviors_to_get:
                    behavior_timestamps = session_data.get_behavioral_epochs_times(epoch_name=behavior_to_get)
                    intervals_frames = from_timestamps_to_frame_epochs(time_stamps_array=behavior_timestamps,
                                                                       frames_timestamps=neuronal_data_timestamps,
                                                                       as_list=True)
                    interval_frames_in_bhv.extend(intervals_frames)

                n_periods = len(interval_frames_in_bhv)
                for event in range(n_periods):
                    start = interval_frames_in_bhv[event][0]
                    end = interval_frames_in_bhv[event][1]
                    frames_to_take.extend(np.arange(start, end + 1))

                if len(frames_to_take) == 0:
                    if verbose:
                        print(f"No imaging frames in the {sce_epoch_name} "
                              f"epoch selected for SCE threshold determination. Skip this session from analysis")
                    continue

                traces_for_sce_threshold = traces[:, frames_to_take]

                if verbose:
                    print(
                        f"Shape of data for SCE threshold determination: "
                        f"NCells: {traces_for_sce_threshold.shape[0]}, "
                        f"NFrames: {traces_for_sce_threshold.shape[1]}")

            # Get mouse speed
            speed = session_data.get_mouse_speed_info()

            # Detect SCEs
            if verbose:
                print(f"Detection of SCEs location based on the calcium traces")
            sampling_rate_hz = session_data.get_rrs_sampling_rate(keys=roi_response_serie_info)
            n_synchronous_frames = int(np.round(synchronous_time * sampling_rate_hz))
            [cells_in_sce, sce_times, raster] = detect_sce_on_traces(raw_traces=traces_for_sce_threshold,
                                                                     speed=speed, use_speed=use_speed,
                                                                     speed_threshold=speed_threshold,
                                                                     sce_n_cells_threshold=sce_n_cells_threshold,
                                                                     sce_min_distance=min_sce_distance,
                                                                     n_synchronous_frames=n_synchronous_frames,
                                                                     use_median_norm=True,
                                                                     use_bleaching_correction=False,
                                                                     use_savitzky_golay_filt=True)
            # Put sce_times as a list of tuple, not single frame list
            sce_times = [(frame, frame) for frame in sce_times]
            n_sces = len(sce_times)

            # Just count
            sce_cell_count = np.sum(cells_in_sce, axis=0)
            sce_cell_prop = (sce_cell_count / n_cells) * 100
            sce_cell_part = np.sum(cells_in_sce, axis=1)
            sce_cell_part_prop = (sce_cell_part / n_sces) * 100

            # List cell index in SCE
            cell_index_in_sce = [list(np.where(cells_in_sce[:, i])[0]) for i in range(n_sces)]

            # For all SCE look at the epoch during which it is occurring #
            sce_epoch = []
            for sce in range(n_sces):
                sce_epoch.append("No epoch specified")
            for sce in range(n_sces):
                sce_time = sce_times[sce][0]
                for group_key, data in frames_in_epoch_dict.items():
                    epoch_frames_bool = frames_in_epoch_dict.get(group_key)
                    if epoch_frames_bool[sce_time] == 1:
                        sce_epoch[sce] = group_key
                    else:
                        continue

            # Get 'cells_in_sce' matrices for each cell types #
            type_in_sce_dict = dict()
            count_type_in_sce_dict = dict()
            prop_type_in_sce_dict = dict()
            for key, info in cell_indices_by_cell_type.items():
                indexes = cell_indices_by_cell_type.get(key)
                type_in_sce = cells_in_sce[indexes, :]
                type_in_sce_dict[key] = type_in_sce
                count_type_in_sce_dict[key] = np.sum(type_in_sce, axis=0)
                prop_type_in_sce_dict[key] = (np.sum(type_in_sce, axis=0) / len(indexes)) * 100

            # Make a table in which each line is a SCE:
            age_list_sce = [info_dict['age'] for k in range(n_sces)]
            weight_list_sce = [info_dict['weight'] for k in range(n_sces)]
            session_identifier_list_sce = [info_dict['identifier'] for k in range(n_sces)]
            animal_id_list_sce = [info_dict['subject_id'] for k in range(n_sces)]
            sce_frames = [sce_times[i][0] for i in range(n_sces)]
            sum_up_data_1 = {'Age': age_list_sce, 'SubjectID': animal_id_list_sce, 'Weight': weight_list_sce,
                             'Session': session_identifier_list_sce, 'SCE#': np.arange(n_sces), 'SCE_frame': sce_frames,
                             'SCE_epoch': sce_epoch, 'Recruited_cells': list(cell_index_in_sce),
                             'AllCells_Recruitment_Count': sce_cell_count, 'AllCells_Recruitment_Prop': sce_cell_prop}

            for key, info in cell_indices_by_cell_type.items():
                sum_up_data_1[f"Recruitment_Count_{key}"] = count_type_in_sce_dict.get(key)
                sum_up_data_1[f"Recruitment_Prop_{key}"] = prop_type_in_sce_dict.get(key)

            sce_recruitment_table = pd.DataFrame(sum_up_data_1)

            general_sce_recruitment_table = general_sce_recruitment_table.append(sce_recruitment_table,
                                                                                 ignore_index=True)

            # Make a table in which each line is a cell:
            age_list_sce = [info_dict['age'] for k in range(n_cells)]
            weight_list_sce = [info_dict['weight'] for k in range(n_cells)]
            session_identifier_list_sce = [info_dict['identifier'] for k in range(n_cells)]
            animal_id_list_sce = [info_dict['subject_id'] for k in range(n_cells)]
            sum_up_data_2 = {'Age': age_list_sce, 'SubjectID': animal_id_list_sce, 'Weight': weight_list_sce,
                             'Session': session_identifier_list_sce, 'Cell#': np.arange(n_cells),
                             'Cell_type': cell_type_list, 'SCE_participation_count': sce_cell_part,
                             'SCE_participation_prop': sce_cell_part_prop}

            cell_participation_table = pd.DataFrame(sum_up_data_2)

            general_cell_recruitment_table = general_cell_recruitment_table.append(cell_participation_table,
                                                                                   ignore_index=True)

            self.update_progressbar(start_time, 100 / (n_sessions+1))

        # Savings
        if verbose:
            print(f"Save results table")
        sce_table_filename = 'SCE_recruitment_table'
        path_results = self.get_results_path()
        general_sce_recruitment_table.to_excel(os.path.join(path_results, f"{sce_table_filename}.xlsx"))

        cells_table_filename = 'SCE_cell_participation_table'
        path_results = self.get_results_path()
        general_cell_recruitment_table.to_excel(os.path.join(path_results, f"{cells_table_filename}.xlsx"))

        if verbose:
            print(f"ANALYSIS DONE")

