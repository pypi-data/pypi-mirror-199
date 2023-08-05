from cicada.analysis.cicada_analysis import CicadaAnalysis
from cicada.utils.sce_stats_utils import get_sce_threshold
from cicada.utils.sce_stats_utils import detect_sce_on_traces
from cicada.utils.misc import get_continous_time_periods, get_yang_frames, from_timestamps_to_frame_epochs, \
    print_info_dict
from cicada.utils.cell_assemblies.malvache.utils import compute_and_plot_clusters_raster_kmean_version
from time import time
import numpy as np
import scipy.signal as sci_si


class CicadaAssembliesMalvacheAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        long_description = '<p align="center"><b>Assembly detection (Malvache method)</b></p><br>'
        long_description = long_description + 'Assembly detection is done as follow: <br><br>'
        long_description = long_description + '<b>- Step#1: SCEs detection </b><br><br>'
        long_description = long_description + 'Detection can be done on the full recording or on a specific epoch: <br><br>'
        long_description = long_description + ' --> choose between options: full recording or epoch <br><br>'
        long_description = long_description + ' If specific epoch is chosen then define its name and the behavior to ' \
                                              'include in the group (for example restrict SCE detection to rest).<br><br>'
        long_description = long_description + ' SCEs can be defined in different manners: <br><br>'
        long_description = long_description + ' - Defined on the raster: either peak of synchrony or all frames with' \
                                              ' more co-active cells than expected by chance. <br><br>'
        long_description = long_description + ' - Defined on traces: as originally defined (Malvache et al. 2016)' \
                                              ' more co-active cells than a defined threshold (default is 5) <br><br>'
        long_description = long_description + '<b>- Step#2: Kmean clustering </b><br><br>'
        long_description = long_description + '<b>- Step#3: Statistical definition of cell assemblies </b><br><br>'
        long_description = long_description + '<b>- Step#4: Do some plots </b><br><br>'
        CicadaAnalysis.__init__(self, name="Malvache's assemblies detection", family_id="Assemblies detection",
                                short_description="Malvache et al. 2016 Science",
                                long_description=long_description,
                                config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaAssembliesMalvacheAnalysis(config_handler=self.config_handler)
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

        self.add_roi_response_series_arg_for_gui(short_description="Neuronal activity to use", long_description=None)

        sce_detection_methods = ["Peaks", "All frames", "Traces"]
        self.add_choices_arg_for_gui(arg_name="method", choices=sce_detection_methods,
                                     default_value="peaks", short_description="Method used to detect SCEs",
                                     long_description="If 'Peaks': find SCEs using find-peaks with parameters below, "
                                                      "SCE will be define by a single frame. "
                                                      "If 'All frames': define SCEs as all continuous frame periods"
                                                      " with more active cells than the statistical threshold.",
                                     multiple_choices=False,
                                     family_widget="figure_config_method_to_use")

        self.add_int_values_arg_for_gui(arg_name="sce_n_cells_threshold", min_value=1, max_value=10,
                                        short_description="Minimal number of co-active cells in SCEs defined on traces",
                                        default_value=5, family_widget="figure_config_method_to_use")

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

        possibilities = ['full_recording', 'Use_epoch']
        self.add_choices_arg_for_gui(arg_name="epochs_to_use", choices=possibilities,
                                     default_value="all_recording",
                                     short_description="Detect SCEs over the full recording or on a specific epoch",
                                     multiple_choices=False,
                                     family_widget="epochs")

        all_available_epochs = []
        for data_to_analyse in self._data_to_analyse:
            all_available_epochs.extend(data_to_analyse.get_behavioral_epochs_names())
            all_available_epochs = list(np.unique(all_available_epochs))
        all_epochs = [name.lower() for name in all_available_epochs]
        if len(all_epochs) >= 1:
            if 'rest' not in all_epochs:
                all_epochs.insert(0, 'rest')
        self.add_choices_for_groups_for_gui(arg_name="epochs_names", choices=all_epochs,
                                            with_color=True,
                                            mandatory=False,
                                            short_description="Do SCE detection on a specific epoch that you define",
                                            long_description="Here you need to specify which individual behaviors "
                                                             "belong to the epoch used for SCE detection",
                                            family_widget="epochs")

        self.add_int_values_arg_for_gui(arg_name="n_surrogates", min_value=10, max_value=10000,
                                        short_description="Number of surrogates raster to compute SCE threshold",
                                        default_value=100, family_widget="figure_config_surrogate")

        self.add_int_values_arg_for_gui(arg_name="percentile", min_value=95, max_value=100,
                                        short_description="Percentile of surrogate distribution to compute SCE threshold",
                                        default_value=99, family_widget="figure_config_surrogate")

        self.add_int_values_arg_for_gui(arg_name="min_sce_distance", min_value=1, max_value=10,
                                        short_description="Minimal number of frames between 2 SCEs",
                                        default_value=5, family_widget="figure_config_surrogate")

        self.add_int_values_arg_for_gui(arg_name="min_ncl", min_value=2, max_value=20,
                                        short_description="Minimal number of clusters to test with k-means",
                                        default_value=2, family_widget="figure_config_kmean_param")

        self.add_int_values_arg_for_gui(arg_name="max_ncl", min_value=2, max_value=20,
                                        short_description="Maximal number of clusters to test with k-means",
                                        default_value=18, family_widget="figure_config_kmean_param")

        self.add_int_values_arg_for_gui(arg_name="n_kmean_surrogate", min_value=10, max_value=1000,
                                        short_description="Number of surrogates in K-mean",
                                        default_value=50, family_widget="figure_config_kmean_param")

        self.add_bool_option_for_gui(arg_name="keep_only_the_best", true_by_default=False,
                                     short_description="Keep the number of clusters giving the best median silhouette value",
                                     family_widget="figure_config_kmean_param")

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

        verbose = True

        roi_response_series_dict = kwargs["roi_response_series"]

        epochs_to_use = kwargs.get("epochs_to_use")

        use_speed = kwargs.get("use_speed")

        speed_threshold = kwargs.get("speed_threshold")

        epochs_names = kwargs.get("epochs_names")

        n_surrogates = kwargs.get("n_surrogates")

        percentile = kwargs.get("percentile")

        sce_n_cells_threshold = kwargs.get("sce_n_cells_threshold")

        sce_detection_method = kwargs.get("method")

        min_sce_distance = kwargs.get("min_sce_distance")

        synchronous_time = kwargs.get("synchronous_time")
        synchronous_time = synchronous_time / 1000

        min_ncl = kwargs.get("min_ncl")

        max_ncl = kwargs.get("max_ncl")

        n_kmean_surrogate = kwargs.get("n_kmean_surrogate")

        keep_only_the_best = kwargs.get("keep_only_the_best")

        start_time = time()
        print("Malvache assemblies detection: coming soon...")

        n_sessions = len(self._data_to_analyse)
        if verbose:
            print(f"{n_sessions} sessions to analyse")

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
                print(f"Acquisition last for : {duration_s} seconds // {duration_m} minutes ")

            # Get mouse speed
            speed = session_data.get_mouse_speed_info()

            # Get Neuronal Data
            neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)
            raster_dur = neuronal_data

            [n_cells, n_frames] = raster_dur.shape
            if verbose:
                print(f"Raster : N cells: {n_cells}, N frames: {n_frames}")

            trace_neuronal_data = session_data.get_roi_response_serie_data_by_keyword(keys=roi_response_serie_info[:-1],
                                                                                      keyword="trace")
            for key, data in trace_neuronal_data.items():
                traces = trace_neuronal_data.get(key)

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
            unique_types = np.unique(cell_type_list)
            unique_types_list = unique_types.tolist()

            # Get the rest frames of this session if 'rest' is not already defined as a behavior
            data_behaviors_list = session_data.get_behavioral_epochs_names()
            behaviors_list = [name.lower() for name in data_behaviors_list]
            if 'rest' not in behaviors_list:
                active_frames = []
                for behavior in behaviors_list:
                    # looking in behavior or intervals
                    epochs_timestamps = session_data.get_interval_times(interval_name=behavior)
                    if epochs_timestamps is None:
                        epochs_timestamps = session_data.get_behavioral_epochs_times(epoch_name=behavior)
                    if epochs_timestamps is None:
                        # means this session doesn't have this epoch name
                        continue
                    # now we want to get the intervals time_stamps and convert them in frames
                    intervals_frames = from_timestamps_to_frame_epochs(time_stamps_array=epochs_timestamps,
                                                                       frames_timestamps=neuronal_data_timestamps,
                                                                       as_list=True)
                    active_frames.extend(intervals_frames)

                deducted_rest_frames = get_yang_frames(total_frames=n_frames, yin_frames=active_frames)[1]

            # Follow GUI requirements to get the data on specified epoch
            if epochs_to_use == "full_recording":
                if verbose:
                    print(f"Do the SCE detection over the full recording")
            else:
                keys_list = list(epochs_names.keys())
                epoch_name = keys_list[0]
                behaviors_to_get = epochs_names.get(epoch_name)[0]
                if verbose:
                    print(f"Do the SCE detection on {epoch_name} epoch, that includes: {behaviors_to_get}")

                interval_frames_in_bhv = []
                frames_to_take = []
                for behavior_to_get in behaviors_to_get:
                    if behavior_to_get == 'rest' and 'rest' not in behaviors_list:
                        frames_to_take = deducted_rest_frames
                    else:
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

                if verbose:
                    print(f"{frames_to_take} frames remaining for analysis")

                traces = traces[:, frames_to_take]
                raster_dur = raster_dur[:, frames_to_take]
                speed = speed[frames_to_take]

            if use_speed is True and sce_detection_method != "Traces":
                # use of speed already included for traces method, see below
                if verbose:
                    print(f"Use speed to restrict raster to immobility periods")
                if speed is None:
                    if verbose:
                        print(f"Speed is not provided do not use it")
                else:
                    frames_to_take = np.where(speed <= speed_threshold)[0]
                    raster_dur = raster_dur[:, frames_to_take]
                    if verbose:
                        print(f"{len(frames_to_take)} frames with speed below speed threshold ({speed_threshold} cm/s)")

            if verbose:
                print(f"Shape of data for SCE detection: NCells: {raster_dur.shape[0]} , NFrames: {raster_dur.shape[1]}")

            # Get the SCE locations based on surrogate on rasterdur: 2 options to define SCE #
            if sce_detection_method == "Peaks" or sce_detection_method == "All frames":
                if verbose:
                    print(f"Detection of SCEs location based on the rasterdur")
                sum_active_cells = np.sum(raster_dur, axis=0)
                sce_thresh = get_sce_threshold(raster_dur, n_surrogates=n_surrogates, percentile=percentile,
                                               verbose=verbose)[1]

                # With 'peaks' method: SCE are at a single frame which is the peak of synchrony
                if sce_detection_method == "Peaks":
                    if verbose:
                        print(f"Detection of SCEs location using the '{sce_detection_method}' method")
                    sce_times = sci_si.find_peaks(sum_active_cells, height=sce_thresh, distance=min_sce_distance)[0]
                    n_sce = len(sce_times)
                    if verbose:
                        print(f"Minimal distance between 2 SCEs: {min_sce_distance} frames")
                        print(f"SCE detection found: {n_sce} SCEs")
                    cells_in_sce = raster_dur[:, sce_times]
                    # Put sce_times as a list of tuple, not single frame list
                    sce_times = [(frame, frame) for frame in sce_times]

                # With 'all frames' method: SCE are at all frames with more co-active cells is higher than the threshold
                if sce_detection_method == "All frames":
                    if verbose:
                        print(f"Detection of SCEs location using the '{sce_detection_method}' method")
                    sce_periods = np.array(np.where(sum_active_cells >= sce_thresh)[0])
                    sce_periods_bool = np.zeros(n_frames, dtype="bool")
                    sce_periods_bool[sce_periods] = True
                    sce_times = get_continous_time_periods(sce_periods_bool)
                    n_sce = len(sce_times)
                    if verbose:
                        print(f"SCE detection found: {n_sce} SCEs")
                    cells_in_sce = np.zeros((n_cells, n_sce), dtype=int)
                    for cell in range(n_cells):
                        for sce in range(n_sce):
                            if sce_times[sce][0] < sce_times[sce][1]:
                                cells_in_sce[cell, sce] = np.max(
                                    raster_dur[cell, sce_times[sce][0]: sce_times[sce][1]])
                            else:
                                cells_in_sce[cell, sce] = raster_dur[cell, sce_times[sce][0]]

            # With 'traces' method: SCE are defined as in Malvache paper (2016)
            if sce_detection_method == "Traces":
                if verbose:
                    print(f"Detection of SCEs location based on the calcium traces")
                sampling_rate_hz = session_data.get_rrs_sampling_rate(keys=roi_response_serie_info)
                n_synchronous_frames = int(np.round(synchronous_time * sampling_rate_hz))
                [cells_in_sce, sce_times, raster] = detect_sce_on_traces(raw_traces=traces,
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
                sce_thresh = sce_n_cells_threshold
                raster_dur = raster

            if verbose:
                print(f"Matrix Cells by SCEs obtained")

            # Check number of SCE to stop the analysis if not more than 10
            if cells_in_sce.shape[1] < 10:
                if verbose:
                    print(f"Less than 10 SCEs detected, stop analysis here, go to next session")
                continue
            else:
                if verbose:
                    print(f"Start clustering on this matrix to look for cell-assemblies")

            labels = np.arange(raster_dur.shape[0])
            compute_and_plot_clusters_raster_kmean_version(labels=labels,
                                                           activity_threshold=sce_thresh,
                                                           range_n_clusters_k_mean=np.arange(min_ncl, max_ncl+1),
                                                           n_surrogate_k_mean=n_kmean_surrogate,
                                                           spike_nums_to_use=raster_dur,
                                                           cellsinpeak=cells_in_sce,
                                                           data_descr=session_identifier,
                                                           path_results=self.get_results_path(),
                                                           sliding_window_duration=0,
                                                           sce_times_numbers=None,
                                                           SCE_times=sce_times,
                                                           perc_threshold=sce_thresh,
                                                           n_surrogate_activity_threshold=n_surrogates,
                                                           with_shuffling=False,
                                                           sce_times_bool=None,
                                                           debug_mode=False,
                                                           keep_only_the_best=keep_only_the_best,
                                                           with_cells_in_cluster_seq_sorted=False,
                                                           fct_to_keep_best_silhouettes=np.mean)

            self.update_progressbar(start_time, 100 / n_sessions)
