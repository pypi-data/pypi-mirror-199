from cicada.analysis.cicada_analysis import CicadaAnalysis
from time import time
from cicada.utils.shortest_path_seq import find_sequences_using_graph_main, \
    plot_rasters_with_sequences_slope_by_slope, get_seq_times_from_raster_with_slopes
import numpy as np
from cicada.utils.misc import from_timestamps_to_frame_epochs, get_stability_among_cell_assemblies
from cicada.utils.display.distribution_plot import plot_box_plots
from cicada.utils.display.colors import BREWER_COLORS
from sortedcontainers import SortedDict
import matplotlib.pyplot as plt
import os
import random


class CicadaSeqGraphAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        long_description = '<p align="center"><b>Shortest path & sequences</b></p><br>'
        long_description = long_description + 'The goal of this analysis is to find group of cells strongly connected' \
                                              ' and look for sequences after ordering those cells.<br><br>'
        long_description = long_description + 'Discrete neuronal activity (such as spikes). ' \
                                              'There are several steps :<br><br>'
        long_description = long_description + '- Building adjacency matrix based on parameters such as the minimum ' \
                                              ' and maximum time between two connected spikes<br><br>'
        long_description = long_description + '- Using n surrogates, we build surrogates adjacency matrices in ' \
                                              'to remove non significant connection (p > 0.05)<br><br>'
        long_description = long_description + '- We then use this matrix to build a connectivity graph, linking ' \
                                              'each cell to its xth strongest connected cell (parameter ' \
                                              '"Max connections by cell")<br><br>'
        long_description = long_description + '- From the graph, we extract the longest shortest paths<br><br>'
        long_description = long_description + '- Then for different slopes, we look for sequences among those ' \
                                              'shortest paths, according to a given error rate, meaning how ' \
                                              'many cells from the shortest path can be missing ' \
                                              'in a sequence instance<br><br>'
        long_description = long_description + 'It is also possible to specify a number of global surrogates. In ' \
                                              'that case the same analysis will be apply to the original neuronal ' \
                                              'data after rolling each of the cell s activity. We can then apply a ' \
                                              'statistical threshold on the number of repetitions of a ' \
                                              'given sequence<br><br> '
        long_description = long_description + 'It will produce several outputs:<br><br>'
        long_description = long_description + '- Two text files for each slope explored, with information ' \
                                              'such as the cells in each shortest path, the sequence ' \
                                              'positions and so on.<br><br>'
        long_description = long_description + '- If raster option is checked, a raster will be plot ordered ' \
                                              'by chunck of shortest path, each one with its color and with ' \
                                              'sequence marked with a line. <br><br>'
        long_description = long_description + '- If global surrogates are configured, then differents figures ' \
                                              'will be plotted regarding the surrogates vs real data for the ' \
                                              'number of repetition in sequences, the error rate and the ratio ' \
                                              'negative/positive slopes.<br><br>'
        CicadaAnalysis.__init__(self, name="Shortest path", family_id="Sequences detection",
                                long_description=long_description,
                                short_description="Using connectivity graph", config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaSeqGraphAnalysis(config_handler=self.config_handler)
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
            roi_response_series = data_to_analyse.get_roi_response_series(keywords_to_exclude=["trace"])
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

        self.add_roi_response_series_arg_for_gui(short_description="Neural activity to use", long_description=None,
                                                 keywords_to_exclude=["trace"])

        all_intervals = []
        for data_to_analyse in self._data_to_analyse:
            all_intervals.extend(data_to_analyse.get_intervals_names())
            all_intervals.extend(data_to_analyse.get_behavioral_epochs_names())
        all_intervals = list(np.unique(all_intervals))

        #
        self.add_int_values_arg_for_gui(arg_name="n_global_surrogates", min_value=0, max_value=1000,
                                        short_description="Number of global surrogates",
                                        long_description="Rolling the original raster before looking for sequences",
                                        default_value=0, family_widget="config")

        self.add_int_values_arg_for_gui(arg_name="n_surrogates", min_value=0, max_value=1000,
                                        short_description="Number of surrogates",
                                        long_description="Number of surrogates on the transition matrix",
                                        default_value=10, family_widget="config")

        self.add_int_values_arg_for_gui(arg_name="min_time_bw_2_spikes", min_value=1, max_value=10,
                                        short_description="Min frames between 2 spikes",
                                        default_value=2, family_widget="config")

        self.add_int_values_arg_for_gui(arg_name="max_time_bw_2_spikes", min_value=1, max_value=20,
                                        short_description="Max frames between 2 spikes",
                                        default_value=10, family_widget="config")

        self.add_int_values_arg_for_gui(arg_name="max_connex_by_cell", min_value=1, max_value=20,
                                        short_description="Max connections by cell",
                                        default_value=5, family_widget="config")

        self.add_int_values_arg_for_gui(arg_name="min_nb_of_rep", min_value=1, max_value=20,
                                        short_description="Min number of repetitions",
                                        default_value=3, family_widget="config")

        self.add_int_values_arg_for_gui(arg_name="min_duration_intra_seq", min_value=1, max_value=5,
                                        short_description="min_duration_intra_seq",
                                        default_value=1, family_widget="config")

        self.add_int_values_arg_for_gui(arg_name="error_rate", min_value=5, max_value=90,
                                        short_description="Error rate (%)",
                                        default_value=70, family_widget="config")

        self.add_int_values_arg_for_gui(arg_name="min_slope_by_cell_in_ms", min_value=-1500, max_value=1400,
                                        short_description="Min slope in ms",
                                        default_value=-1500, family_widget="config")

        self.add_int_values_arg_for_gui(arg_name="max_slope_by_cell_in_ms", min_value=-1400, max_value=1500,
                                        short_description="Max slope in ms",
                                        default_value=1500, family_widget="config")

        self.add_int_values_arg_for_gui(arg_name="slope_step_in_ms", min_value=10, max_value=500,
                                        short_description="Slope step in ms",
                                        default_value=150, family_widget="config")

        self.add_bool_option_for_gui(arg_name="plot_raster", true_by_default=True,
                                     short_description="Plot raster ?",
                                     family_widget="config")

        self.add_choices_for_groups_for_gui(arg_name="interval_names", choices=all_intervals,
                                            with_color=True,
                                            mandatory=False,
                                            short_description="Epochs",
                                            long_description="Select epochs you want to color in the raster",
                                            family_widget="epochs")

        self.add_int_values_arg_for_gui(arg_name="intervals_alpha_color", min_value=1, max_value=100,
                                        short_description="Transparency of color bands",
                                        default_value=50, family_widget="epochs")

        self.add_bool_option_for_gui(arg_name="chronic_session_analysis", true_by_default=False,
                                     short_description="Apply chronic sessions analysis", family_widget="chronic")
        self.add_bool_option_for_gui(arg_name="divide_by_total_of_both", true_by_default=True,
                                     short_description="Common percentage in seq 1",
                                     family_widget="chronic")

        self.add_bool_option_for_gui(arg_name="crop_raster", true_by_default=False,
                                     short_description="Crop raster",
                                     long_description="If check will use only the n first frames indicated to"
                                                      "look for sequences",
                                     family_widget="crop_raster")

        self.add_int_values_arg_for_gui(arg_name="n_frames_to_crop", min_value=1000, max_value=10000,
                                        short_description="Number of frames to use",
                                        default_value=50, family_widget="crop_raster")

        self.add_image_format_package_for_gui()

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

        roi_response_series_dict = kwargs["roi_response_series"]

        crop_raster = kwargs.get("crop_raster", False)

        n_frames_to_crop = kwargs.get("n_frames_to_crop", 12500)

        # if False, the rasters are not plotted
        plot_raster = kwargs.get("plot_raster", True)

        # config algo
        min_time_bw_2_spikes = kwargs.get("min_time_bw_2_spikes", 2)
        max_time_bw_2_spikes = kwargs.get("max_time_bw_2_spikes", 10)
        max_connex_by_cell = kwargs.get("max_connex_by_cell", 5)
        min_nb_of_rep = kwargs.get("min_nb_of_rep", 3)
        min_duration_intra_seq = kwargs.get("min_duration_intra_seq", 1)
        error_rate = kwargs.get("error_rate", 70)
        error_rate = error_rate / 100
        # number of surrogates to filter the transition matrix
        n_surrogates = kwargs.get("n_surrogates", 10)
        # how many surrogates at the first step, meaning we roll the data before even building the matrix transition
        n_global_surrogates = kwargs.get("n_global_surrogates", 0)
        min_slope_by_cell_in_ms = kwargs.get("min_slope_by_cell_in_ms", -1500)
        max_slope_by_cell_in_ms = kwargs.get("max_slope_by_cell_in_ms", 1500)
        slope_step_in_ms = kwargs.get("slope_step_in_ms", 150)

        # ------------- EPOCHS ---------------
        interval_names = kwargs.get("interval_names")

        intervals_alpha_color = kwargs.get("intervals_alpha_color")
        intervals_alpha_color = intervals_alpha_color * 0.01
        # ------------- EPOCHS ---------------

        chronic_session_analysis = kwargs.get("chronic_session_analysis", False)

        verbose = kwargs.get("verbose", True)

        # image package format
        save_formats = kwargs.get("save_formats", "pdf")

        start_time = time()

        n_sessions = len(self._data_to_analyse)

        # key is session_id, value is a list of list of int (sequence of cells)
        seq_indices_list_dict = dict()

        # useful for the seq stat
        n_cells_by_session_dict = dict()

        for session_index, session_data in enumerate(self._data_to_analyse):
            # Get Session Info
            info_dict = session_data.get_sessions_info()
            session_identifier = info_dict['identifier']

            if verbose:
                print(f" ")
                print(f"------------------ ONGOING SESSION: {session_identifier} -------------------- ")
                print(f"SESSION INFO: {info_dict}")

            if isinstance(roi_response_series_dict, dict):
                roi_response_serie_info = roi_response_series_dict[session_identifier]
            else:
                roi_response_serie_info = roi_response_series_dict

            neuronal_data_from_session = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)

            # compare results in nomber of seq (n cells & n rep) for real and surrogates data
            # key: int slope
            # key: "surrogate" or "real"
            # key list of (int, int) == (n_cells, n_repetition)
            real_vs_surrogates_results_dict = dict()

            for index_global_surrogate in np.arange(-1, n_global_surrogates):
                # if index_global_surrogate >= 0 it means we build a surrogate
                if index_global_surrogate >= 0:
                    print(f"-------------- {session_identifier}, "
                          f"surrogate n° {index_global_surrogate + 1} / {n_global_surrogates} -------------- ")
                neuronal_data = neuronal_data_from_session.copy()
                if index_global_surrogate >= 0:
                    # TODO: roll the data
                    n_frames = neuronal_data.shape[1]
                    for cell, data in enumerate(neuronal_data):
                        # roll the data to a random displace number
                        neuronal_data[cell, :] = np.roll(data, np.random.randint(1, n_frames))

                # croping the raster, so only the n_frames_to_crop first frames will be used
                if crop_raster:
                    original_neuronal_data = np.copy(neuronal_data)
                    n_frames = neuronal_data.shape[1]
                    # making sure we don't exceed the number of frames in data
                    n_frames_to_crop_in_session = min(n_frames, n_frames_to_crop)
                    print(f"// Building shortest path using the first {n_frames_to_crop_in_session} frames //")
                    neuronal_data = neuronal_data[:, :n_frames_to_crop_in_session]

                n_cells_by_session_dict[session_identifier] = len(neuronal_data)

                neuronal_data_timestamps = session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_info)
                sampling_rate_hz = session_data.get_ci_movie_sampling_rate()
                # ------------- EPOCHS ---------------
                span_area_coords = None
                span_area_colors = None

                # TODO: allows epochs when crop_raster, need to remove epoch that are over the limit
                if (interval_names is not None) and (len(interval_names) > 0) and (not crop_raster):
                    span_area_coords = []
                    span_area_colors = []

                    for interval_group_name, interval_info in interval_names.items():
                        if len(interval_info) != 2:
                            continue
                        interval_names_in_group = interval_info[0]
                        interval_color = interval_info[1]
                        # print(f"Interval {interval_group_name}, color: "
                        #       f"{rgb_to_name(interval_color, with_float_values=True)}")
                        rdb_values = [int(np.round(c * 255)) for c in interval_color]
                        rdb_values = rdb_values[:-1]
                        print(f"Interval {interval_group_name}, color: {rdb_values}")

                        intervals_frames_in_group = []
                        # TODO: See for fusioning epochs from a same group so there are extended
                        for interval_name in interval_names_in_group:
                            # looking in behavior or intervals
                            intervals_timestamps = session_data.get_interval_times(interval_name=interval_name)
                            if intervals_timestamps is None:
                                intervals_timestamps = session_data.get_behavioral_epochs_times(
                                    epoch_name=interval_name)
                            if intervals_timestamps is None:
                                # means this session doesn't have this epoch name
                                continue
                            # now we want to get the intervals time_stamps and convert them in frames
                            intervals_frames = from_timestamps_to_frame_epochs(time_stamps_array=intervals_timestamps,
                                                                               frames_timestamps=neuronal_data_timestamps,
                                                                               as_list=True)
                            intervals_frames_in_group.extend(intervals_frames)
                        span_area_coords.append(intervals_frames_in_group)
                        span_area_colors.append(interval_color)
                # ------------- END EPOCHS ---------------
                descr = session_identifier
                if crop_raster:
                    descr = descr + "_cropped"
                if index_global_surrogate >= 0:
                    descr = descr + f"_surrogate_{index_global_surrogate}"
                    # used to be 1 and 10
                # seq_indices_list is a list of list of int, representing the cell indices of a same sequence
                seq_indices_list, long_seq_list, short_seq_cells, isolates_cell = find_sequences_using_graph_main(
                    neuronal_data, min_time_bw_2_spikes=min_time_bw_2_spikes,
                    max_time_bw_2_spikes=max_time_bw_2_spikes,
                    max_connex_by_cell=max_connex_by_cell,
                    min_nb_of_rep=min_nb_of_rep,
                    min_duration_intra_seq=min_duration_intra_seq,
                    error_rate=error_rate,
                    n_surrogates=n_surrogates,
                    sampling_rate=sampling_rate_hz,
                    debug_mode=False, descr=descr,
                    results_path=self.get_results_path(),
                    plot_raster=plot_raster,
                    raster_dur_version=True,
                    span_area_coords=span_area_coords,
                    span_area_colors=span_area_colors,
                    min_slope_by_cell_in_ms=min_slope_by_cell_in_ms,
                    max_slope_by_cell_in_ms=max_slope_by_cell_in_ms,
                    slope_step_in_ms=slope_step_in_ms,
                    save_formats=save_formats)

                if crop_raster and plot_raster:
                    # plotting the full raster, see if there is still sequences after the n first_frames
                    descr = session_identifier + "_full"
                    if index_global_surrogate >= 0:
                        descr = descr + f"_surrogate_{index_global_surrogate}"
                    plot_rasters_with_sequences_slope_by_slope(spike_nums=original_neuronal_data,
                                                               raster_dur_version=True,
                                                               seq_indices_list=seq_indices_list,
                                                               long_seq_list=long_seq_list,
                                                               short_seq_cells=short_seq_cells,
                                                               isolates_cell=isolates_cell,
                                                               colors=BREWER_COLORS,
                                                               span_area_coords=span_area_coords,
                                                               span_area_colors=span_area_colors,
                                                               descr=descr,
                                                               error_rate=error_rate,
                                                               sampling_rate=sampling_rate_hz,
                                                               results_path=self.get_results_path(),
                                                               debug_mode=False,
                                                               save_formats=save_formats)

                seq_indices_list_dict[session_identifier] = long_seq_list

                # min_slope_by_cell_in_ms = -1500
                # max_slope_by_cell_in_ms = 1500
                # slope_step_in_ms = 150
                range_around_slope_in_ms = 600
                range_around_slope_in_frames = max(1, int(range_around_slope_in_ms / (1000 / sampling_rate_hz)))

                for slope_ms in np.arange(min_slope_by_cell_in_ms, max_slope_by_cell_in_ms, slope_step_in_ms):
                    # finding sequences for given slopes
                    for seq_indices in seq_indices_list:
                        for seq_index in seq_indices:
                            seq = np.array(long_seq_list[seq_index])
                            # if n_cells_in_seq < 3:
                            #     short_seq_cells.extend(list(seq))
                            # dict with key a tuple of int representing cell_index and a spike_time (in frame)
                            # value is a dict with key as tuple of int (slope, range_around) and value the number of cells in this slope
                            # one key will be "max" and the value the best (slope, range_around) and a key "spikes_in_seq" representing
                            # the a boolean 2d-array same dimension as raster, eing True every where the cell is participating to the the seq
                            slope_result = get_seq_times_from_raster_with_slopes(neuronal_data[seq],
                                                                                 raster_dur_version=True,
                                                                                 sampling_rate=sampling_rate_hz,
                                                                                 only_on_slope_in_ms=slope_ms,
                                                                                 range_around_slope_in_ms=range_around_slope_in_ms,
                                                                                 error_rate=error_rate)
                            # number of slopes (sequences)
                            n_repetitions = len(slope_result)
                            # now we measure the error_rate for each repetition
                            # meaning how many cells from the seq are active in each repetition
                            # 1 means all cells are active, while 0 mean 0 and 0.5 50% etc...
                            error_rates = []
                            for rep_dict in slope_result.values():
                                for key_dict, cells_in_slope in rep_dict.items():
                                    if key_dict not in ["max", "spikes_in_seq"]:
                                        # print(f"key_dict {key_dict}")
                                        # print(f"cells_in_slope {cells_in_slope}")
                                        # print(f"seq {seq}")
                                        # print(f"len(cells_in_slope) / len(seq) {np.round(len(cells_in_slope) / len(seq), 2)}")
                                        error_rates.append(1 - (len(cells_in_slope) / len(seq)))
                            # print(f"error_rates {error_rates}")
                            # comment of the line filling slope_result in get_seq_times_from_raster_with_slopes()
                            # slope_result[(cell, spike_time)][(actual_slope, range_around_slope_in_frames)] = cells_in_slope

                            key_result = "real"
                            if index_global_surrogate >= 0:
                                key_result = "surrogate"
                            if slope_ms not in real_vs_surrogates_results_dict:
                                real_vs_surrogates_results_dict[slope_ms] = dict()
                            if key_result not in real_vs_surrogates_results_dict[slope_ms]:
                                real_vs_surrogates_results_dict[slope_ms][key_result] = list()
                            real_vs_surrogates_results_dict[slope_ms][key_result].append((len(seq), n_repetitions,
                                                                                          error_rates))

                if not chronic_session_analysis:
                    self.update_progressbar(time_started=self.analysis_start_time,
                                            increment_value=100 / ((n_sessions + 1) * (n_global_surrogates + 1)))
                else:
                    self.update_progressbar(time_started=self.analysis_start_time,
                                            increment_value=100 / (n_sessions * (n_global_surrogates + 1)))
            # then we plot scatter (one by slope) representing the the number of seq found (n_cells * n_repetition)
            # we also plot the ratio nb positive slopes / negative slopes
            plot_scatter_seq_real_vs_surrogate(real_vs_surrogates_results_dict=real_vs_surrogates_results_dict,
                                               session_identifier=session_identifier, save_formats=save_formats,
                                               results_path=self.get_results_path(),
                                               n_surrogates=n_global_surrogates + 1,
                                               labels_to_threshold=["surrogate"],
                                               threshold_value=95)
        if not chronic_session_analysis:
            print(f"Shortest path seq analysis run in {time() - self.analysis_start_time} sec")
            return

        # ---------- Chronic session comparison -----------------
        divide_by_total_of_both = kwargs.get("divide_by_total_of_both", True)
        # compare composition of sequences between the session (should be chronic recording)
        len_seq_by_session_dict = SortedDict()
        for session_identifier, seq_indices_list in seq_indices_list_dict.items():
            # TODO: remove seq that are less than 4 cells
            if len(seq_indices_list) == 0:
                print(f"No shortest path in {session_identifier}")
                continue
            len_sequences = []
            n_cells_in_seq = 0
            for seq in seq_indices_list:
                len_sequences.append(len(seq))
                n_cells_in_seq += len(seq)
            n_cells_in_session = n_cells_by_session_dict[session_identifier]
            # we add in id how many cells are in shortest path vs total cells
            len_seq_by_session_dict[session_identifier[:3] + f'\n({n_cells_in_seq} / {n_cells_in_session})'] = \
                len_sequences

        plot_box_plots(data_dict=len_seq_by_session_dict, title="",
                       filename=f"chronic_seq_lengths",
                       path_results=self.get_results_path(), with_scatters=True,
                       scatter_size=200,
                       x_labels_rotation=45,
                       y_label=f"N cells in sequences", colors=BREWER_COLORS,
                       save_formats=save_formats)

        box_plot_stability_dict = dict()
        # key is session_identifier, value is the stability of the percentage between cell in assemblies from
        # on session to the other
        box_plot_cells_in_shortest_path_dict = dict()
        scatter_text_shortest_path_cells_dict = dict()

        # for each assembly, display a value, in our case we want to put the number of cells
        scatter_text_dict = dict()
        # we want to order session by age
        session_indexes = np.arange(n_sessions)
        session_ages = []
        session_identifiers = []
        for session_index, session_data in enumerate(self._data_to_analyse):
            session_ages.append(session_data.age)
            session_identifiers.append(session_data.identifier)
        arg_order = np.argsort(session_ages)
        # ordering them by age
        session_indexes = session_indexes[arg_order]

        for i, session_1_index in enumerate(session_indexes[:-1]):
            for session_2_index in session_indexes[i + 1:]:
                assemblies_1 = seq_indices_list_dict[session_identifiers[session_1_index]]
                assemblies_2 = seq_indices_list_dict[session_identifiers[session_2_index]]
                """
                   divide_by_total_of_both: if True, we divide the number of cell in common by the total amount
                   of different cells represented by the two assemblies that has been compared, otherwise we divide it
                   just by the number of cell in assembly_1

                   Returns: list of the same size as assembly_1, of integers representing the percentage of cells in each
                   assembly that are part of a same assembly in assemblies_2

                """

                stabilities = get_stability_among_cell_assemblies(assemblies_1, assemblies_2,
                                                                  divide_by_total_of_both=divide_by_total_of_both)
                identifier_box_plot = f"{session_identifiers[session_1_index][:3]}\n" \
                                      f"vs\n{session_identifiers[session_2_index][:3]}"
                # extracting just the first 3 values of the session id, to get the age (like p13)
                box_plot_stability_dict[identifier_box_plot] = stabilities
                n_cells_in_assemblies = [len(cells_in_assembly) for cells_in_assembly in assemblies_1]
                scatter_text_dict[identifier_box_plot] = n_cells_in_assemblies

                cells_in_shortest_path_session_1 = []
                for cells in assemblies_1:
                    cells_in_shortest_path_session_1.extend(cells)
                cells_in_shortest_path_session_2 = []
                for cells in assemblies_2:
                    cells_in_shortest_path_session_2.extend(cells)
                stabilities = get_stability_among_cell_assemblies([cells_in_shortest_path_session_1],
                                                                  [cells_in_shortest_path_session_2],
                                                                  divide_by_total_of_both=False)
                scatter_text_shortest_path_cells_dict[identifier_box_plot] = [len(cells_in_shortest_path_session_1)]
                box_plot_cells_in_shortest_path_dict[identifier_box_plot] = stabilities

        plot_box_plots(data_dict=box_plot_cells_in_shortest_path_dict, title="",
                       scatter_text_dict=scatter_text_shortest_path_cells_dict,
                       filename=f"chronic_seq_cells_in_shortest_path_stability",
                       path_results=self.get_results_path(), with_scatters=True,
                       scatter_size=200,
                       x_labels_rotation=45,
                       y_label=f"stability (%)", colors=BREWER_COLORS,
                       save_formats=save_formats)

        plot_box_plots(data_dict=box_plot_stability_dict, title="",
                       scatter_text_dict=scatter_text_dict,
                       filename=f"chronic_seq_stability",
                       path_results=self.get_results_path(), with_scatters=True,
                       scatter_size=200,
                       x_labels_rotation=45,
                       y_label=f"stability (%)", colors=BREWER_COLORS,
                       save_formats=save_formats)
        # plot_box_plots(data_dict, title, filename,
        #                y_label, param, colors=None,
        #                path_results=None, y_lim=None,
        #                x_label=None, with_scatters=True,
        #                y_log=False,
        #                scatters_with_same_colors=None,
        #                scatter_size=20,
        #                scatter_alpha=0.5,
        #                n_sessions_dict=None,
        #                background_color="black",
        #                link_medians=True,
        #                color_link_medians="red",
        #                labels_color="white",
        #                with_y_jitter=None,
        #                x_labels_rotation=None,
        #                fliers_symbol=None,
        #                save_formats="pdf")
        self.update_progressbar(time_started=self.analysis_start_time, increment_value=100 / (n_sessions + 1))
        print(f"Shortest path seq analysis run in {time() - self.analysis_start_time} sec")


def plot_scatter_seq_real_vs_surrogate(real_vs_surrogates_results_dict, session_identifier, save_formats,
                                       results_path, n_surrogates, labels_to_threshold,
                                       threshold_value):
    """

    Args:
        real_vs_surrogates_results_dict:
        session_identifier:
        save_formats:
        results_path:
        n_surrogates:
        labels_to_threshold: list of string, will display a threshold line for each label in the list
        threshold_value: threshold (percentile value) at which to display the limit

    Returns:

    """

    lines_width = 1

    # compare results in nomber of seq (n cells & n rep) for real and surrogates data
    # key: int slope
    # key: "surrogate" or "real"
    # key list of (int, int) == (n_cells, n_repetition)
    # real_vs_surrogates_results_dict = dict()
    for slope_ms, data_dict in real_vs_surrogates_results_dict.items():
        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(15, 15))
        background_color = "black"
        labels_color = "white"
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)
        min_rep = 1
        max_rep = 10
        min_len = 4
        max_len = 10

        with_text = True

        # key: label_index
        # vaue: list of the float: n_cells_threshold value, n_rep_threshold value
        threshold_lines_dict = dict()

        label_index = 0
        # print(f"SLOPE {slope_ms}: {data_dict}")
        colors = ["red", "cornflowerblue", "yellow", "green"]
        for label, seq_values in data_dict.items():
            # seq_values is a list of (n_cells, n_rep)
            n_cells_in_seq = np.array([seq_value[0] for seq_value in seq_values])
            n_rep_for_seq = np.array([seq_value[1] for seq_value in seq_values])

            if label in labels_to_threshold:
                n_cells_threshold = np.percentile(n_cells_in_seq, threshold_value)
                n_rep_threshold = np.percentile(n_rep_for_seq, threshold_value)
                threshold_lines_dict[label_index] = [n_cells_threshold, n_rep_threshold]

            # then we filter them to remove those too small
            new_n_cells_in_seq = []
            new_n_rep_for_seq = []
            for n_cells_index, n_cells in enumerate(n_cells_in_seq):
                n_rep = n_rep_for_seq[n_cells_index]
                if n_cells < 4 or n_rep <= 0:
                    continue
                new_n_cells_in_seq.append(n_cells)
                new_n_rep_for_seq.append(n_rep)
            if len(new_n_cells_in_seq) == 0:
                continue
            n_cells_in_seq = np.array(new_n_cells_in_seq)
            n_rep_for_seq = np.array(new_n_rep_for_seq)

            min_len = min(min_len, np.min(n_cells_in_seq))
            max_len = max(max_len, np.max(n_cells_in_seq))
            min_rep = min(min_rep, np.min(n_rep_for_seq))
            max_rep = max(max_rep, np.max(n_rep_for_seq))

            n_jitter = len(n_cells_in_seq)
            jitter_range_x = 0.25
            n_cells_in_seq = [x + random.uniform(-jitter_range_x, jitter_range_x) for x in n_cells_in_seq]
            # jitter_range_y = 0.25
            # n_rep_for_seq = [y + random.uniform(-jitter_range_y, jitter_range_y) for y in n_rep_for_seq]

            if label == "surrogate":
                zorder = 1
            else:
                zorder = 2
            ax1.scatter(n_cells_in_seq,
                        n_rep_for_seq,
                        color=colors[label_index],
                        marker="o", zorder=zorder,
                        s=300, alpha=0.7, edgecolors='white',
                        label=label)

            if with_text:
                for index in np.arange(len(n_cells_in_seq)):
                    ax1.text(x=n_cells_in_seq[index], y=n_rep_for_seq[index],
                             s=f"{int(n_rep_for_seq[index])}", color="black", zorder=22,
                             ha='center', va="center", fontsize=4, fontweight='bold')
            label_index += 1

        use_log_scale = True
        if use_log_scale:
            ax1.set_yscale("log")
            if max_rep < 100:
                y_lim = (0, 100)
            else:
                y_lim = (0, 1100)
        else:
            y_lim = (min_rep - 2, max_rep + 2)
        x_lim = (min_len - 2, max_len + 2)

        for label_index, threshold_lines in threshold_lines_dict.items():
            ax1.vlines(threshold_lines[0], y_lim[0], y_lim[1], lw=lines_width, linestyles="dashed",
                       color=colors[label_index], zorder=5)
            ax1.hlines(threshold_lines[1], x_lim[0], x_lim[1], lw=lines_width, linestyles="dashed",
                       color=colors[label_index], zorder=5)
        ax1.legend()

        # plt.title(title)
        ax1.set_ylabel(f"Repetition (#)", fontsize=20)
        ax1.set_xlabel("Cells (#)", fontsize=20)

        ax1.set_xlim(x_lim[0], x_lim[1])
        ax1.set_ylim(y_lim[0], y_lim[1])

        ax1.xaxis.label.set_color(labels_color)
        ax1.yaxis.label.set_color(labels_color)

        ax1.tick_params(axis='y', colors=labels_color)
        ax1.tick_params(axis='x', colors=labels_color)
        # xticks = np.arange(0, len(data_dict))
        # ax1.set_xticks(xticks)
        # # sce clusters labels
        # ax1.set_xticklabels(labels)

        if isinstance(save_formats, str):
            save_formats = [save_formats]
        for save_format in save_formats:
            fig.savefig(os.path.join(results_path,
                                     f'{session_identifier}_real_vs_{n_surrogates}_surrogates_seq_slope_{slope_ms}.{save_format}'),
                        format=f"{save_format}",
                        facecolor=fig.get_facecolor())
        plt.close()


        # ------------------------------------------------------------------------
        # ------------------------------------------------------------------------
        # ------------------------------------------------------------------------

        # compare results in nomber of seq (n cells & n rep) for real and surrogates data
        # but combining the negative and positive side of a slope
        # key: int slope
        # key: "surrogate" or "real"
        # key list of (int, int) == (n_cells, n_repetition)
        # real_vs_surrogates_results_dict = dict()
        if (slope_ms > 0) and (-slope_ms in real_vs_surrogates_results_dict):
            negative_data_dict = real_vs_surrogates_results_dict[-slope_ms]
            fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                    gridspec_kw={'height_ratios': [1]},
                                    figsize=(15, 15))
            background_color = "black"
            labels_color = "white"
            ax1.set_facecolor(background_color)
            fig.patch.set_facecolor(background_color)
            min_rep = 1
            max_rep = 10
            min_len = 4
            max_len = 10

            with_text = True

            # key: label_index
            # vaue: list of the float: n_cells_threshold value, n_rep_threshold value
            threshold_lines_dict = dict()

            label_index = 0
            # print(f"SLOPE {slope_ms}: {data_dict}")
            colors = ["red", "cornflowerblue", "yellow", "green"]
            for label, seq_values in data_dict.items():
                # seq_values is a list of (n_cells, n_rep)
                n_cells_in_seq = [seq_value[0] for seq_value in seq_values]
                n_rep_for_seq = [seq_value[1] for seq_value in seq_values]

                # adding negative values
                n_cells_in_seq.extend([seq_value[0] for seq_value in negative_data_dict[label]])
                n_rep_for_seq.extend([seq_value[1] for seq_value in negative_data_dict[label]])

                if label in labels_to_threshold:
                    n_cells_threshold = np.percentile(n_cells_in_seq, threshold_value)
                    n_rep_threshold = np.percentile(n_rep_for_seq, threshold_value)
                    threshold_lines_dict[label_index] = [n_cells_threshold, n_rep_threshold]

                # then we filter them to remove those too small
                new_n_cells_in_seq = []
                new_n_rep_for_seq = []
                for n_cells_index, n_cells in enumerate(n_cells_in_seq):
                    n_rep = n_rep_for_seq[n_cells_index]
                    if n_cells < 4 or n_rep <= 0:
                        continue
                    new_n_cells_in_seq.append(n_cells)
                    new_n_rep_for_seq.append(n_rep)
                if len(new_n_cells_in_seq) == 0:
                    continue
                n_cells_in_seq = np.array(new_n_cells_in_seq)
                n_rep_for_seq = np.array(new_n_rep_for_seq)

                min_len = min(min_len, np.min(n_cells_in_seq))
                max_len = max(max_len, np.max(n_cells_in_seq))
                min_rep = min(min_rep, np.min(n_rep_for_seq))
                max_rep = max(max_rep, np.max(n_rep_for_seq))

                n_jitter = len(n_cells_in_seq)
                jitter_range_x = 0.25
                n_cells_in_seq = [x + random.uniform(-jitter_range_x, jitter_range_x) for x in n_cells_in_seq]
                # jitter_range_y = 0.25
                # n_rep_for_seq = [y + random.uniform(-jitter_range_y, jitter_range_y) for y in n_rep_for_seq]
                if label == "surrogate":
                    zorder = 1
                else:
                    zorder = 2
                ax1.scatter(n_cells_in_seq,
                            n_rep_for_seq,
                            color=colors[label_index],
                            marker="o",
                            zorder=zorder,
                            s=300, alpha=0.7, edgecolors='white',
                            label=label)

                if with_text:
                    for index in np.arange(len(n_cells_in_seq)):
                        ax1.text(x=n_cells_in_seq[index], y=n_rep_for_seq[index],
                                 s=f"{int(n_rep_for_seq[index])}", color="black", zorder=22,
                                 ha='center', va="center", fontsize=4, fontweight='bold')
                label_index += 1

            use_log_scale = True
            if use_log_scale:
                ax1.set_yscale("log")
                if max_rep < 100:
                    y_lim = (0, 100)
                else:
                    y_lim = (0, 1100)
            else:
                y_lim = (min_rep - 2, max_rep + 2)
            x_lim = (min_len - 2, max_len + 2)

            for label_index, threshold_lines in threshold_lines_dict.items():
                ax1.vlines(threshold_lines[0], y_lim[0], y_lim[1], lw=lines_width, linestyles="dashed",
                           color=colors[label_index], zorder=5)
                ax1.hlines(threshold_lines[1], x_lim[0], x_lim[1], lw=lines_width, linestyles="dashed",
                           color=colors[label_index], zorder=5)
            ax1.legend()

            # plt.title(title)
            ax1.set_ylabel(f"Repetition (#)", fontsize=20)
            ax1.set_xlabel("Cells (#)", fontsize=20)

            ax1.set_xlim(x_lim[0], x_lim[1])
            ax1.set_ylim(y_lim[0], y_lim[1])

            ax1.xaxis.label.set_color(labels_color)
            ax1.yaxis.label.set_color(labels_color)

            ax1.tick_params(axis='y', colors=labels_color)
            ax1.tick_params(axis='x', colors=labels_color)
            # xticks = np.arange(0, len(data_dict))
            # ax1.set_xticks(xticks)
            # # sce clusters labels
            # ax1.set_xticklabels(labels)

            if isinstance(save_formats, str):
                save_formats = [save_formats]
            for save_format in save_formats:
                fig.savefig(os.path.join(results_path,
                                         f'{session_identifier}_real_vs_{n_surrogates}_surrogates_seq_slope_pos_&_neg_{slope_ms}.{save_format}'),
                            format=f"{save_format}",
                            facecolor=fig.get_facecolor())
            plt.close()

        # ------------------------------------------------------------------------
        # ------------------------------------------------------------------------
        # ------------------------------------------------------------------------

        # now we display error rate for each group and seq, as a boxplot
        # values range from 0 to 1
        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(15, 15))
        background_color = "black"
        labels_color = "white"
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)
        min_rep = 1
        max_rep = 10
        min_len = 4
        max_len = 10

        with_text = True

        # key: label_index
        # vaue: list of the float: n_cells_threshold value, n_rep_threshold value
        threshold_lines_dict = dict()

        label_index = 0
        # print(f"SLOPE {slope_ms}: {data_dict}")
        colors = ["red", "cornflowerblue", "yellow", "green"]
        bplots = []
        labels = []
        for label, seq_values in data_dict.items():
            # seq_values is a list of (n_cells, n_rep)
            # list of list
            n_cells_in_seq = np.array([seq_value[0] for seq_value in seq_values])
            n_rep_for_seq = np.array([seq_value[1] for seq_value in seq_values])
            error_rates = [np.array(seq_value[2]) * 100 for seq_value in seq_values]

            # then we filter them to remove those too small
            new_n_cells_in_seq = []
            new_n_rep_for_seq = []
            new_error_rates = []
            for n_cells_index, n_cells in enumerate(n_cells_in_seq):
                n_rep = n_rep_for_seq[n_cells_index]
                if n_cells < 4 or n_rep <= 3:
                    continue
                new_error_rates.append(error_rates[n_cells_index])
                new_n_cells_in_seq.append(n_cells)
                new_n_rep_for_seq.append(n_rep)
            if len(new_error_rates) == 0:
                continue
            n_cells_in_seq = np.array(new_n_cells_in_seq)
            n_rep_for_seq = np.array(new_n_rep_for_seq)
            error_rates = new_error_rates

            if label in labels_to_threshold:
                error_rates_threshold = np.percentile([np.median(er) for er in error_rates], threshold_value)
                error_rates_invert_threshold = np.percentile([np.median(er) for er in error_rates], 100 - threshold_value)
                threshold_lines_dict[label_index] = [error_rates_threshold, error_rates_invert_threshold]

            min_len = min(min_len, np.min(n_cells_in_seq))
            max_len = max(max_len, np.max(n_cells_in_seq))

            n_jitter = len(n_cells_in_seq)
            jitter_range_x = 0.25
            n_cells_in_seq = [np.round(x + random.uniform(-jitter_range_x, jitter_range_x), 2) for x in n_cells_in_seq]
            # jitter_range_y = 0.25
            # n_rep_for_seq = [y + random.uniform(-jitter_range_y, jitter_range_y) for y in n_rep_for_seq]
            colorfull = True
            if label == "surrogate":
                zorder = 5
            else:
                zorder = 11
            bplot = ax1.boxplot(error_rates, positions=n_cells_in_seq, patch_artist=colorfull,
                                sym='', widths=[0.5] * len(error_rates), zorder=zorder)
            bplots.append(bplot)
            labels.append(label)

            for element in ['boxes', 'whiskers', 'fliers', 'caps']:
                # if white_background:
                #     plt.setp(bplot[element], color="black")
                # else:
                plt.setp(bplot[element], color="white")

            for element in ['means', 'medians']:
                # if white_background:
                #     plt.setp(bplot[element], color="black")
                # else:
                plt.setp(bplot[element], color="black")

            if colorfull:
                colors_boxplot = [colors[label_index]] * len(error_rates)

                for patch, color_boxplot in zip(bplot['boxes'], colors_boxplot):
                    patch.set_facecolor(color_boxplot)

            if label == "surrogate":
                zorder = 6
            else:
                zorder = 12

            ax1.scatter(n_cells_in_seq,
                        [np.median(er) for er in error_rates],
                        color=colors[label_index],
                        marker="o",
                        zorder=zorder,
                        s=300, alpha=0.7, edgecolors='white',
                        label=label)

            # if with_text:
            #     for index in np.arange(len(n_cells_in_seq)):
            #         ax1.text(x=n_cells_in_seq[index], y=n_rep_for_seq[index],
            #                  s=f"{int(n_rep_for_seq[index])}", color="black", zorder=22,
            #                  ha='center', va="center", fontsize=4, fontweight='bold')
            label_index += 1

        y_lim = (0, 100)
        x_lim = (min_len - 2, max_len + 2)

        for label_index, threshold_lines in threshold_lines_dict.items():
            ax1.hlines(threshold_lines[0], x_lim[0], x_lim[1], lw=lines_width, linestyles="dashed",
                       color=colors[label_index], zorder=5)
            ax1.hlines(threshold_lines[1], x_lim[0], x_lim[1], lw=lines_width, linestyles="dashed",
                       color=colors[label_index], zorder=5)

        ax1.legend([bp["boxes"][0] for bp in bplots], labels, loc='upper right')

        # plt.title(title)
        ax1.set_ylabel(f"Error rate (%)", fontsize=20)
        ax1.set_xlabel("Cells (#)", fontsize=20)

        ax1.set_xlim(x_lim[0], x_lim[1])
        ax1.set_ylim(y_lim[0], y_lim[1])

        ax1.xaxis.label.set_color(labels_color)
        ax1.yaxis.label.set_color(labels_color)

        ax1.tick_params(axis='y', colors=labels_color)
        ax1.tick_params(axis='x', colors=labels_color)
        # xticks = np.arange(0, len(data_dict))
        # ax1.set_xticks(xticks)
        # # sce clusters labels
        # ax1.set_xticklabels(labels)

        if isinstance(save_formats, str):
            save_formats = [save_formats]
        for save_format in save_formats:
            fig.savefig(os.path.join(results_path,
                                     f'{session_identifier}_real_vs_{n_surrogates}_surrogates_error_rate_slope_{slope_ms}.{save_format}'),
                        format=f"{save_format}",
                        facecolor=fig.get_facecolor())
        plt.close()

        # ------------------------------------------------------------------------
        # ------------------------------------------------------------------------
        # ------------------------------------------------------------------------

        # now ratio positive / negative
        if (slope_ms >= 0) or (-slope_ms not in real_vs_surrogates_results_dict):
            # means there is no symetric
            continue

        negative_slope_ms = slope_ms
        positive_slope_ms = -slope_ms
        negative_data_dict = data_dict
        positive_data_dict = real_vs_surrogates_results_dict[positive_slope_ms]

        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(15, 15))
        background_color = "black"
        labels_color = "white"
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)
        min_rep = 1
        max_rep = 3
        min_len = 4
        max_len = 6

        label_index = 0

        # key: label_index
        # vaue: list of the float: n_cells_threshold value, n_rep_threshold value
        threshold_lines_dict = dict()

        colors = ["red", "cornflowerblue", "yellow", "green"]
        # in our case label will be surrogate or real
        for label, negative_seq_values in negative_data_dict.items():
            if label not in positive_data_dict:
                continue
            positive_seq_values = positive_data_dict[label]
            # seq_values is a list of (n_cells, n_rep)
            n_cells_in_negative_seq = np.array([seq_value[0] for seq_value in negative_seq_values])
            n_rep_for_negative_seq = np.array([seq_value[1] for seq_value in negative_seq_values])

            n_cells_in_positive_seq = np.array([seq_value[0] for seq_value in positive_seq_values])
            n_rep_for_positive_seq = np.array([seq_value[1] for seq_value in positive_seq_values])

            # ratio_n_cells_in_seq = n_cells_in_positive_seq / n_cells_in_negative_seq
            # ratio_n_rep_for_seq = []
            # new_ratio_n_cells_in_seq = []
            # for index_rep in np.arange(len(n_rep_for_positive_seq)):

            # now we want to filter some
            new_n_cells_in_positive_seq = []
            new_n_rep_for_positive_seq = []
            new_n_rep_for_negative_seq = []
            for index, n_cells in enumerate(n_cells_in_positive_seq):
                if n_cells < 4:
                    continue
                if n_rep_for_negative_seq[index] <= 1 and n_rep_for_positive_seq[index] <= 1:
                    continue
                new_n_cells_in_positive_seq.append(n_cells)
                new_n_rep_for_positive_seq.append(n_rep_for_positive_seq[index])
                new_n_rep_for_negative_seq.append(n_rep_for_negative_seq[index])

            n_cells_in_positive_seq = np.array(new_n_cells_in_positive_seq)
            n_rep_for_positive_seq = np.array(new_n_rep_for_positive_seq)
            n_rep_for_negative_seq = np.array(new_n_rep_for_negative_seq)

            # replacing the 0 by 1 to avoid error when dividing
            n_rep_for_positive_seq[n_rep_for_positive_seq == 0] = 1
            n_rep_for_negative_seq[n_rep_for_negative_seq == 0] = 1
            ratio_n_rep_for_seq = n_rep_for_negative_seq / n_rep_for_positive_seq

            if label in labels_to_threshold:
                ratio_n_rep_threshold = np.percentile(ratio_n_rep_for_seq, threshold_value)
                ratio_n_rep_inver_threshold = np.percentile(ratio_n_rep_for_seq, 100 - threshold_value)
                threshold_lines_dict[label_index] = [ratio_n_rep_threshold, ratio_n_rep_inver_threshold]

            min_len = min(min_len, np.min(n_cells_in_positive_seq))
            max_len = max(max_len, np.max(n_cells_in_positive_seq))
            min_rep = min(min_rep, np.min(ratio_n_rep_for_seq))
            max_rep = max(max_rep, np.max(ratio_n_rep_for_seq))

            # n_jitter = len(n_cells_in_seq)
            jitter_range_x = 0.25
            n_cells_in_positive_seq = [x + random.uniform(-jitter_range_x, jitter_range_x)
                                       for x in n_cells_in_positive_seq]
            # jitter_range_y = 0.25
            # ratio_n_rep_for_seq = [y + random.uniform(-jitter_range_y, jitter_range_y) for y in ratio_n_rep_for_seq]
            if label == "surrogate":
                zorder = 1
            else:
                zorder = 2

            ax1.scatter(n_cells_in_positive_seq,
                        ratio_n_rep_for_seq,
                        color=colors[label_index],
                        marker="o", zorder=zorder,
                        s=300, alpha=0.7, edgecolors='white',
                        label=label)
            label_index += 1

        ax1.legend()

        use_log_scale = False
        if use_log_scale:
            ax1.set_yscale("log")
            if max_rep < 100:
                y_lim = (0, 100)
            else:
                y_lim = (0, 1100)
        else:
            y_lim = (min_rep - 2, max_rep + 2)
        x_lim = (min_len - 2, max_len + 2)

        for label_index, threshold_lines in threshold_lines_dict.items():
            ax1.hlines(threshold_lines[0], x_lim[0], x_lim[1], lw=lines_width, linestyles="dashed",
                       color=colors[label_index], zorder=5)
            ax1.hlines(threshold_lines[1], x_lim[0], x_lim[1], lw=lines_width, linestyles="dashed",
                       color=colors[label_index], zorder=5)

        # plt.title(title)
        ax1.set_ylabel(f"Ratio repetition negative/positive", fontsize=20)
        ax1.set_xlabel("Cells (#)", fontsize=20)

        ax1.set_xlim(x_lim[0], x_lim[1])
        ax1.set_ylim(y_lim[0], y_lim[1])

        ax1.xaxis.label.set_color(labels_color)
        ax1.yaxis.label.set_color(labels_color)

        ax1.tick_params(axis='y', colors=labels_color)
        ax1.tick_params(axis='x', colors=labels_color)
        # xticks = np.arange(0, len(data_dict))
        # ax1.set_xticks(xticks)
        # # sce clusters labels
        # ax1.set_xticklabels(labels)

        if isinstance(save_formats, str):
            save_formats = [save_formats]
        for save_format in save_formats:
            fig.savefig(os.path.join(results_path,
                                     f'{session_identifier}_real_vs_{n_surrogates}_surrogates_ratio_neg_pos_slope_{slope_ms}.{save_format}'),
                        format=f"{save_format}",
                        facecolor=fig.get_facecolor())
        plt.close()

