from cicada.analysis.cicada_analysis import CicadaAnalysis
from time import time
from cicada.utils.shortest_path_seq import read_seq_detection_with_slope_file
from cicada.utils.display.cells_map_utils import CellsCoord
import numpy as np
from cicada.utils.misc import from_timestamps_to_frame_epochs
from cicada.utils.display.rasters import plot_figure_with_map_and_raster_for_sequences
from cicada.utils.display.colors import BREWER_COLORS


class CicadaTripleSeqPlotAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        CicadaAnalysis.__init__(self, name="3x seq plot", family_id="Sequences detection",
                                short_description="Triple plot of sequences", config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

        # contain the name of the arg that contains the file_name to get seq information
        # key: session identifier, value: string
        self.seq_info_file_arg_name_dict = dict()

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaTripleSeqPlotAnalysis(config_handler=self.config_handler)
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
            raster_in_rrs_keys = False
            traces_in_rrs_keys = False
            rrs_names = data_to_analyse.get_roi_response_series_list(keywords_to_exclude=None)
            for rrs_name in rrs_names:
                if 'raster' in rrs_name:
                    raster_in_rrs_keys = True
                else:
                    continue
            for rrs_name in rrs_names:
                if 'trace' in rrs_name:
                    traces_in_rrs_keys = True
                else:
                    continue
            if (raster_in_rrs_keys is False) or (traces_in_rrs_keys is False):
                self.invalid_data_help = f"The analysis requires both spike raster and traces"
                return False

        return True

    def set_arguments_for_gui(self):
        """

        Returns:

        """
        CicadaAnalysis.set_arguments_for_gui(self)

        self.add_roi_response_series_arg_for_gui(short_description="Raster to use", long_description=None,
                                                 arg_name="roi_response_series_raster",
                                                 keywords_to_exclude=["trace"])

        self.add_roi_response_series_arg_for_gui(short_description="Trace to use", long_description=None,
                                                 arg_name="roi_response_series_trace",
                                                 keywords_to_exclude=["raster"])

        self.add_segmentation_arg_for_gui()

        key_names = [data.identifier for data in self._data_to_analyse]
        seq_file_arg = {"arg_name": "seq_file", "value_type": "file",
                        "extensions": "txt",
                        "mandatory": True,
                        "short_description": "Txt file with results from seq analysis (shortest path)",
                        "family_widget": "slopes"}
        if len(key_names) > 1:
            seq_file_arg.update({"key_names": key_names})
        self.add_argument_for_gui(**seq_file_arg)

        self.add_int_values_arg_for_gui(arg_name="slope_in_ms", min_value=50, max_value=2000,
                                        short_description="Slope used in ms",
                                        default_value=1000, family_widget="slopes")

        all_intervals = []
        for data_to_analyse in self._data_to_analyse:
            all_intervals.extend(data_to_analyse.get_intervals_names())
            all_intervals.extend(data_to_analyse.get_behavioral_epochs_names())
        all_intervals = list(np.unique(all_intervals))

        self.add_choices_for_groups_for_gui(arg_name="interval_names", choices=all_intervals,
                                            with_color=True,
                                            mandatory=False,
                                            short_description="Epochs",
                                            long_description="Select epochs you want to color in the raster",
                                            family_widget="epochs")

        self.add_int_values_arg_for_gui(arg_name="intervals_alpha_color", min_value=1, max_value=100,
                                        short_description="Transparency of color bands",
                                        default_value=50, family_widget="epochs")

        # self.add_bool_option_for_gui(arg_name="chronic_session_analysis", true_by_default=False,
        #                              short_description="Apply chronic sessions analysis", family_widget="chronic")
        # self.add_bool_option_for_gui(arg_name="divide_by_total_of_both", true_by_default=True,
        #                              short_description="Common percentage in seq 1",
        #                              long_description="",
        #                              family_widget="chronic")

        # TODO: Add option so the slopes are found using the online algorithm and not the ones already defined

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

        roi_response_series_raster_dict = kwargs["roi_response_series_raster"]

        roi_response_series_trace_dict = kwargs["roi_response_series_trace"]

        segmentation_dict = kwargs['segmentation']

        slope_in_ms = kwargs["slope_in_ms"]

        # ------------- EPOCHS ---------------
        interval_names = kwargs.get("interval_names")

        intervals_alpha_color = kwargs.get("intervals_alpha_color")
        intervals_alpha_color = intervals_alpha_color * 0.01
        # ------------- EPOCHS ---------------

        verbose = kwargs.get("verbose", True)

        # image package format
        save_formats = kwargs.get("save_formats", "pdf")

        dpi = kwargs.get("dpi", 200)

        n_sessions = len(self._data_to_analyse)

        seq_files = kwargs.get("seq_file", None)
        if isinstance(seq_files, str):
            if len(self._data_to_analyse) > 1:
                # not matching the len of the data to analyse
                seq_files = None
            else:
                seq_files = {self._data_to_analyse[0].identifier: seq_files}

        if seq_files is None:
            print(f"No seq file given, end of the analysis")
            self.update_progressbar(time_started=self.analysis_start_time, increment_value=100)
            return

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

            if isinstance(roi_response_series_raster_dict, dict):
                roi_response_serie_raster_info = roi_response_series_raster_dict[session_identifier]
            else:
                roi_response_serie_raster_info = roi_response_series_raster_dict

            if isinstance(roi_response_series_trace_dict, dict):
                roi_response_serie_trace_info = roi_response_series_trace_dict[session_identifier]
            else:
                roi_response_serie_trace_info = roi_response_series_trace_dict

            raster_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_raster_info)

            trace_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_trace_info)

            n_cells = len(trace_data)
            n_frames = trace_data.shape[1]
            n_cells_by_session_dict[session_identifier] = len(trace_data)

            if (session_identifier not in seq_files) or (seq_files[session_identifier] is None):
                print(f"{session_identifier} not in seq_files")
                self.update_progressbar(time_started=self.analysis_start_time, increment_value=100 / n_sessions)
                continue

            # segmentation
            if isinstance(segmentation_dict, dict):
                segmentation_info = segmentation_dict[session_identifier]
            else:
                segmentation_info = segmentation_dict
            pixel_mask = session_data.get_pixel_mask(segmentation_info=segmentation_info)

            if pixel_mask is None:
                print(f"pixel_mask not available in for {session_data.identifier} "
                      f"in {segmentation_info}")
                self.update_progressbar(self.analysis_start_time, 100 / n_sessions)
                continue

            # pixel_mask of type pynwb.core.VectorIndex
            # each element of the list will be a sequences of tuples of 3 floats representing x, y and a float between
            # 0 and 1 (not used in this case)
            pixel_mask_list = [pixel_mask[cell] for cell in range(len(pixel_mask))]
            # TODO: get the real movie dimensions if available
            coord_obj = CellsCoord(pixel_masks=pixel_mask_list, from_matlab=False, invert_xy_coord=True)

            seq_file_name = seq_files[session_identifier]
            cells_best_order, seq_dict = read_seq_detection_with_slope_file(file_name=seq_file_name)
            # cells_best_order (1d np array)
            # seq_dict with key is a tuple of cell indices (int),
            # then key is the slope value (in ms) and value is a list of values:
            # first_cell_spike_time, last_cell_spike_time, range_around, then indices of cells that fire in the sequence

            neuronal_data_timestamps = session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_raster_info)
            sampling_rate_hz = session_data.get_ci_movie_sampling_rate(only_2_photons=True)
            # ------------- EPOCHS ---------------
            span_area_coords = None
            span_area_colors = None

            if (interval_names is not None) and (len(interval_names) > 0) :
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
                            intervals_timestamps = session_data.get_behavioral_epochs_times(epoch_name=interval_name)
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

            # cells_to_highlight = []
            # cells_to_highlight_colors = []
            # cells_added_for_span = []

            for cells_seq, dict_slope in seq_dict.items():
                range_around_slope_in_frames = 0
                # dict that takes for a key a tuple of int representing 2 cells,
                # and as value a list of tuple of 2 float
                # representing the 2 extremities of a line between those 2 cells
                lines_to_display = dict()
                first_cell = cells_seq[0]
                last_cell = cells_seq[-1]
                cells_pair_tuple = (0, len(cells_seq) - 1)
                # number of negatives, synchrone and positive slopes
                for slope, values_list in dict_slope.items():
                    for values in values_list:
                        if cells_pair_tuple not in lines_to_display:
                            lines_to_display[cells_pair_tuple] = []
                        first_cell_spike_time = values[0]
                        last_cell_spike_time = values[1]
                        range_around = values[2]
                        range_around_slope_in_frames = range_around
                        lines_to_display[cells_pair_tuple].append((first_cell_spike_time, last_cell_spike_time))
                n_rep = len(values_list)
                n_cells_in_seq = last_cell - first_cell + 1
                if n_cells_in_seq < 4:
                    continue
                # if (n_rep < 6) or (n_cells_in_seq < 6):
                #     continue

                for first_frame in np.arange(0, n_frames, 2500):
                    frames_to_use = np.arange(first_frame, min(n_frames, first_frame + 2500))
                    file_name = f"{session_identifier}_map_raster_seq_{first_cell}-{last_cell}_frame_{first_frame}"
                    file_name = file_name + f"_slope_{slope_in_ms}_ms"
                    file_name = file_name + f"_{last_cell - first_cell + 1}_cells_{len(values_list)}_rep"

                    # updating coords
                    lines_to_display_update = dict()
                    for cells_pair_tuple, spikes_pair in lines_to_display.items():
                        for spike_pair in spikes_pair:
                            if (spike_pair[0] >= frames_to_use[0]) or (spike_pair[1] <= frames_to_use[1]):
                                if cells_pair_tuple not in lines_to_display_update:
                                    lines_to_display_update[cells_pair_tuple] = []
                                spike_1 = spike_pair[0] - frames_to_use[0]
                                spike_2 = spike_pair[1] - frames_to_use[0]
                                lines_to_display_update[cells_pair_tuple].append((spike_1, spike_2))
                    span_area_coords_update = None
                    if span_area_coords is not None:
                        span_area_coords_update = []
                        for coords in span_area_coords:
                            sub_list = []
                            for coord in coords:
                                # print(f"coord {coord}")
                                if (coord[0] >= frames_to_use[0]) or (coord[1] <= frames_to_use[1]):
                                    if cells_pair_tuple not in span_area_coords_update:
                                        span_area_coords_update[cells_pair_tuple] = []
                                    spike_1 = coord[0] - frames_to_use[0]
                                    spike_2 = coord[1] - frames_to_use[0]
                                    sub_list.append((spike_1, spike_2))
                            span_area_coords_update.append(sub_list)
                    raster_dur = raster_data[:, frames_to_use]
                    plot_figure_with_map_and_raster_for_sequences(raster_dur=raster_dur,
                                                                  raw_traces=trace_data,
                                                                  coord_obj=coord_obj,
                                                                  results_path=self.get_results_path(),
                                                                  cells_in_seq=np.array(cells_best_order)
                                                                  [first_cell:last_cell + 1],
                                                                  file_name=file_name,
                                                                  frames_to_use=frames_to_use,
                                                                  lines_to_display=lines_to_display_update,
                                                                  without_sum_activity_traces=True,
                                                                  range_around_slope_in_frames=
                                                                  range_around_slope_in_frames,
                                                                  span_area_coords=span_area_coords_update,
                                                                  span_area_colors=span_area_colors,
                                                                  save_formats=save_formats,
                                                                  dpi=dpi)

            self.update_progressbar(time_started=self.analysis_start_time, increment_value=100 / n_sessions)

        print(f"Triple seq plot analysis run in {time() - self.analysis_start_time} sec")

