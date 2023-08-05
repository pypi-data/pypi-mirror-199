from cicada.analysis.cicada_analysis import CicadaAnalysis
from cicada.utils.display.videos import load_tiff_movie
from cicada.utils.misc import from_timestamps_to_frame_epochs, print_info_dict
import os
import tifffile as tiff
import numpy as np


class CicadaGenerateTiffMovie(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        CicadaAnalysis.__init__(self, name="Write CI movie to tiff", family_id="Display",
                                short_description="Generate CI movie in tiff format",
                                config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaGenerateTiffMovie(config_handler=self.config_handler)
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

            has_tiff_data = data.contains_ci_movie(consider_only_2_photons=True)

            if has_tiff_data is False:
                self.invalid_data_help = f"No 'TwoPhotonSeries' available to extract 'tiff' movie"
            return has_tiff_data

    def set_arguments_for_gui(self):
        """

        Returns:

        """
        CicadaAnalysis.set_arguments_for_gui(self)

        self.add_ci_movie_arg_for_gui()

        self.add_roi_response_series_arg_for_gui(short_description="Neural activity 'roi response series' ("
                                                                   "only to extract neuronal data timestamps)",
                                                 long_description="May be used to extract timestamps if the 'use epoch'"
                                                                  "option is selected")

        sample_for_tiff = ["Basic option", "Use epochs"]
        self.add_choices_arg_for_gui(arg_name="sampling_tiff_method", choices=sample_for_tiff,
                                     default_value="Basic option",
                                     short_description="Select the method to write tiff movie(s)",
                                     long_description="'Basic option': write all CI frames between selected "
                                                      "first and last frame, 'Use epochs': write multiple CI "
                                                      "tiffs around selected epochs ",
                                     multiple_choices=False,
                                     family_widget="movie type")

        self.add_int_values_arg_for_gui(arg_name="n_examples", min_value=0, max_value=30,
                                        short_description="Number of example to write if  'Use epochs'",
                                        default_value=5, long_description=None, family_widget="movie type")

        self.add_int_values_arg_for_gui(arg_name="first_frame", min_value=0, max_value=10000,
                                        short_description="First frame to write",
                                        default_value=0, long_description=None, family_widget="basic_movie")

        self.add_int_values_arg_for_gui(arg_name="last_frame", min_value=0, max_value=10000,
                                        short_description="Last frame to write",
                                        default_value=10000, long_description=None, family_widget="basic_movie")

        self.add_bool_option_for_gui(arg_name="use_main_epoch", true_by_default=False,
                                     short_description="Sample from one main epoch",
                                     long_description="If yes,sample the behavioral epochs "
                                                      "occurring in this selected main epoch",
                                     family_widget="main epochs")

        all_epochs = []
        for data_to_analyse in self._data_to_analyse:
            all_epochs.extend(data_to_analyse.get_intervals_names())
            all_epochs.extend(data_to_analyse.get_behavioral_epochs_names())
        all_epochs = list(np.unique(all_epochs))
        self.add_choices_for_groups_for_gui(arg_name="main_epoch", choices=all_epochs,
                                            with_color=False,
                                            mandatory=False,
                                            short_description="Select 1 main epoch to sample epochs "
                                                              "from this main epoch only",
                                            family_widget="main epochs")

        self.add_choices_for_groups_for_gui(arg_name="epochs_names", choices=all_epochs,
                                            with_color=False,
                                            mandatory=False,
                                            short_description="Build epoch groups",
                                            family_widget="epochs")

        self.add_bool_option_for_gui(arg_name="filter_consecutive_movements", true_by_default=True,
                                     short_description="Do not sample movements separated by less time than baseline",
                                     long_description=None,
                                     family_widget="epochs")

        self.add_int_values_arg_for_gui(arg_name="baseline_length", min_value=50, max_value=10000,
                                        short_description="Duration of baseline around sampled movement (ms)",
                                        default_value=4000, family_widget="epochs")

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

        verbose = kwargs.get("verbose", True)

        arg_ci_movies_dict = kwargs["ci_movie"]

        sampling_tiff_method = kwargs.get("sampling_tiff_method")

        n_examples = kwargs.get("n_examples")

        use_main_epoch = kwargs.get("use_main_epoch")

        main_epoch = kwargs.get("main_epoch")

        epochs_names = kwargs.get("epochs_names")

        filter_consecutive_movements = kwargs.get("filter_consecutive_movements", False)

        first_frame = kwargs.get("first_frame")

        last_frame = kwargs.get("last_frame")

        baseline_length = kwargs.get("baseline_length")
        baseline_length = baseline_length / 1000

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

            # Get neuronal data for timestamps only:
            if isinstance(roi_response_series_dict, dict):
                roi_response_serie_info = roi_response_series_dict[session_identifier]
            else:
                roi_response_serie_info = roi_response_series_dict

            # Checking for epochs:
            if sampling_tiff_method == 'Use epochs':
                if (epochs_names is None) or len(epochs_names) == 0:
                    print(f"No epochs selected, no analysis")
                    self.update_progressbar(time_started=self.analysis_start_time, increment_value=100)
                    return

            # setting the movie
            session_ci_movie_dict = session_data.get_ci_movies(only_2_photons=True)
            if isinstance(arg_ci_movies_dict, str):
                arg_movie_name = arg_ci_movies_dict
            else:
                arg_movie_name = arg_ci_movies_dict[session_identifier]
            session_ci_movie_data = session_ci_movie_dict[arg_movie_name]
            if isinstance(session_ci_movie_data, str):
                tiff_movie = load_tiff_movie(tiff_file_name=session_ci_movie_data)
            else:
                tiff_movie = session_ci_movie_data

            # Get CI movie sampling rate
            ci_sampling_rate = session_data.get_ci_movie_sampling_rate(only_2_photons=True)
            if ci_sampling_rate is None:
                ci_sampling_rate = session_data.get_rrs_sampling_rate(keys=roi_response_serie_info)

            if verbose:
                print(f"CI movie shape (n_lines x n_cols): {tiff_movie.shape[1]} x {tiff_movie.shape[2]} pixels - "
                      f"{tiff_movie.shape[0]} frames, at {ci_sampling_rate} Hz")

            # Get CI frames in group:
            if sampling_tiff_method == 'Use epochs':
                print(f" ")
                # Get CI frames / neuronal data timestamps (used if 'use epochs' option)
                print(f"get frames timestamps to match them with behavior timestamps")
                ci_frames_ts = np.asarray(session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_info))
                print(f" ")
                print(f"Detect all movements in defined groups")
                epochs_frames_in_group_dict = dict()
                for epoch_group_name, epoch_info in epochs_names.items():
                    if len(epoch_info) != 2:
                        continue
                    epochs_names_in_group = epoch_info[0]
                    # epoch_color = epoch_info[1]

                    # TODO: take into consideration invalid epochs, and remove the one in invalid section
                    epochs_frames_in_group = []
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
                            start_ts = max(0, start_ts - baseline_length)
                            stop_ts = stop_ts + baseline_length
                            extended_invalid_times[0, index] = start_ts
                            extended_invalid_times[1, index] = stop_ts
                    # print(f"session_data.get_intervals_names() {session_data.get_intervals_names()}")
                    if extended_invalid_times is not None:
                        print(f" ")
                        print(f"Among {epoch_group_name}, containing : {epochs_names_in_group} we remove:")
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
                            # TODO: not super efficient, see to make it more efficient
                            filtered_epochs_timestamps = np.zeros(epochs_timestamps.shape)
                            n_epochs_kept = 0
                            last_epoch_kept_index = 0
                            in_invalid = 0
                            to_close_of_previous = 0
                            out_of_main_epoch = 0
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
                                # we can skip it (if we don't do psth on one epoch or filter consecutive movements)
                                if (filter_consecutive_movements is False) and (use_main_epoch is False):
                                    if invalid_times_are_sorted and epochs_are_sorted and \
                                            (epoch_start_ts > extended_invalid_times[1, -1]):
                                        filtered_epochs_timestamps[:, n_epochs_kept] = epochs_timestamps[:, epoch_index]
                                        n_epochs_kept += 1
                                        continue

                                # Filter movements
                                to_filter = False
                                as_invalid = False

                                # Filter based on invalid times
                                if verbose and epoch_index == 0:
                                    print(f"Remove {epoch_name} epochs if they overlap with invalid times")
                                for invalid_index in range(extended_invalid_times.shape[1]):
                                    invalid_start_ts = extended_invalid_times[0, invalid_index]
                                    invalid_stop_ts = extended_invalid_times[1, invalid_index]

                                    if (epoch_start_ts >= invalid_start_ts) and (epoch_start_ts <= invalid_stop_ts):
                                        to_filter = True
                                        as_invalid = True
                                        in_invalid += 1
                                        break
                                    if (epoch_stop_ts >= invalid_start_ts) and (epoch_stop_ts <= invalid_stop_ts):
                                        to_filter = True
                                        as_invalid = True
                                        in_invalid += 1
                                        break
                                    if (epoch_start_ts <= invalid_start_ts) and (epoch_stop_ts >= invalid_stop_ts):
                                        to_filter = True
                                        as_invalid = True
                                        in_invalid += 1
                                        break

                                # Filter based on the main epoch selection
                                if use_main_epoch and as_invalid is False:
                                    keys_list = list(main_epoch.keys())
                                    psth_epoch_name = keys_list[0]
                                    epoch_to_get = main_epoch.get(psth_epoch_name)
                                    epoch_to_get = (epoch_to_get[0])[0]
                                    main_psth_epoch_timestamps = session_data.get_behavioral_epochs_times(
                                        epoch_name=epoch_to_get)
                                    n_epochs_in_main_epoch = main_psth_epoch_timestamps.shape[1]
                                    main_epoch_start = main_psth_epoch_timestamps[0, 0]
                                    main_epoch_stop = main_psth_epoch_timestamps[1, 0]
                                    if verbose and epoch_index == 0:
                                        if n_epochs_in_main_epoch == 1:
                                            print(
                                                f"Remove {epoch_name} epochs if they do not occur during : {epoch_to_get}, "
                                                f"(the main epoch selected) occurring between "
                                                f"t0 = {np.round(main_epoch_start, decimals=2)} s and "
                                                f"t1 = {np.round(main_epoch_stop, decimals=2)} s")
                                        else:
                                            print(
                                                f"Remove {epoch_name} epochs if they do not occur during : {epoch_to_get}, "
                                                f"(the main epoch selected) made of {n_epochs_in_main_epoch} sub-epochs")
                                    epoch_is_in_main_epoch = False
                                    for sub_epoch in range(n_epochs_in_main_epoch):
                                        main_epoch_start = main_psth_epoch_timestamps[0, sub_epoch]
                                        main_epoch_stop = main_psth_epoch_timestamps[1, sub_epoch]
                                        if epoch_start_ts > main_epoch_start and epoch_stop_ts < main_epoch_stop:
                                            epoch_is_in_main_epoch = True
                                            break
                                        else:
                                            continue
                                    if epoch_is_in_main_epoch is False:
                                        to_filter = True
                                        out_of_main_epoch += 1

                                # Filter based on temporal distance from previous movement
                                if filter_consecutive_movements and to_filter is False:
                                    if verbose and epoch_index == 0:
                                        print(f"Remove {epoch_name} epochs if they follow the previous kept {epoch_name}"
                                              f" by less than baseline range ({2*baseline_length} s) ")
                                    if (epoch_start_ts - previous_epoch_start_ts) <= 2 * baseline_length:
                                        to_filter = True
                                        to_close_of_previous += 1

                                if not to_filter:
                                    filtered_epochs_timestamps[:, n_epochs_kept] = epochs_timestamps[:, epoch_index]
                                    n_epochs_kept += 1
                                    last_epoch_kept_index = epoch_index

                            filtered_epochs_timestamps = filtered_epochs_timestamps[:, :n_epochs_kept]
                            n_epochs_filtered = epochs_timestamps.shape[1] - filtered_epochs_timestamps.shape[1]
                            if verbose:
                                print(f"{n_epochs_filtered} {epoch_name} epochs removed: {in_invalid} in invalid frames, "
                                      f"{to_close_of_previous} too close from previous, {out_of_main_epoch} "
                                      f"out of main epoch")
                                print(f"{filtered_epochs_timestamps.shape[1]} {epoch_name} epochs left")
                            epochs_timestamps = filtered_epochs_timestamps

                        # session_data.get_interval_times()
                        # now we want to get the intervals time_stamps and convert them in frames
                        # list of list of 2 int
                        intervals_frames = from_timestamps_to_frame_epochs(time_stamps_array=epochs_timestamps,
                                                                           frames_timestamps=ci_frames_ts,
                                                                           as_list=True)

                        epochs_frames_in_group.extend(intervals_frames)

                    epochs_frames_in_group_dict[epoch_group_name] = epochs_frames_in_group

            if verbose:
                print(f" ")
                print(f"---------- Generate tiffs -----------")
                print(f" ")

            if sampling_tiff_method == "Use epochs":
                baseline_in_ci_frames = int(baseline_length * ci_sampling_rate)
                if verbose:
                    print(f"Extend tiff with {baseline_in_ci_frames} CI frames before onset and after offset of movement")
                for group, frames_in_group in epochs_frames_in_group_dict.items():
                    n_trials = len(frames_in_group)
                    if n_trials == 0:
                        if verbose:
                            print(f"No {group} try next group")
                        continue
                    if n_examples > n_trials:
                        n_examples_to_take = n_trials
                    else:
                        n_examples_to_take = n_examples
                    if verbose:
                        print(f" ")
                        print(f"Select {n_examples_to_take} random epochs among {group}")
                    rnd_indexes = np.random.choice(a=n_trials, size=n_examples_to_take, replace=False, p=None)
                    for sample in range(n_examples_to_take):
                        ind = rnd_indexes[sample]
                        onset = frames_in_group[ind][0]
                        offset = frames_in_group[ind][1]
                        first_frame = max(0, (onset - baseline_in_ci_frames))
                        last_frame = min((offset + baseline_in_ci_frames), tiff_movie.shape[0])
                        saving_path = os.path.join(self.get_results_path(),
                                                   f"{session_identifier}_"
                                                   f"{group}_{sample}_frames_{first_frame}_{last_frame}.tiff")
                        movie_to_write = tiff_movie[first_frame: last_frame, :, :]

                        print(
                            f"Generating tiff movie file with first frame: {first_frame}, last frame: {last_frame}")

                        tiff.imsave(saving_path, movie_to_write)

            if sampling_tiff_method == "Basic option":
                saving_path = os.path.join(self.get_results_path(), f"{session_identifier}.tiff")

                last_frame_to_take = min(last_frame, tiff_movie.shape[0])

                movie_to_write = tiff_movie[first_frame: last_frame_to_take, :, :]

                print(f"Generating tiff movie file with first frame: {first_frame}, last frame: {last_frame_to_take}")

                tiff.imsave(saving_path, movie_to_write)

        print(f" ")
        print(f"ANALYSIS DONE")




