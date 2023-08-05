from cicada.analysis.cicada_analysis import CicadaAnalysis
from time import time
from cicada.utils.display.rasters import plot_raster
import numpy as np
# from cicada.utils.display.colors import rgb_to_name
from cicada.utils.misc import from_timestamps_to_frame_epochs, from_timestamps_array_to_list, \
    validate_indices_in_string_format, \
    extract_indices_from_string, print_info_dict


class CicadaDisplayRasterAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        long_description = '<p align="center"><b>Display neuronal data</b></p><br>'
        long_description = long_description + 'Save plots of neuronal data as a cells by times raster of discrete ' \
                                              '(like spikes) or continuous data (like fluorescence signal).<br><br>'
        long_description = long_description + 'It is possible to specify epochs that will be colored accordingly.'
        CicadaAnalysis.__init__(self, name="Display activity", family_id="Display",
                                short_description="Display Raster / Traces",
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
        analysis_copy = CicadaDisplayRasterAnalysis(config_handler=self.config_handler)
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

        return True

    def set_arguments_for_gui(self):
        """

        Returns:

        """
        CicadaAnalysis.set_arguments_for_gui(self)

        self.add_roi_response_series_arg_for_gui(short_description="Neural activity to use", long_description=None)

        # choices_dict = dict()
        # for index, data in enumerate(self._data_to_analyse):
        #     if index < 2:
        #         choices_dict[data.identifier] = ["test_1", "test_2"]
        #     else:
        #         choices_dict[data.identifier] = ["test_3", "test_4", "test_6"]
        #
        # test_arg = {"arg_name": "test_multiple_choices", "choices": choices_dict,
        #             "short_description": "Test choices for each session",
        #             "multiple_choices": True}
        #
        # self.add_argument_for_gui(**test_arg)

        all_intervals = []
        for data_to_analyse in self._data_to_analyse:
            all_intervals.extend(data_to_analyse.get_intervals_names())
            all_intervals.extend(data_to_analyse.get_behavioral_epochs_names())
        all_intervals = list(np.unique(all_intervals))
        # print(f"all_intervals {all_intervals}")

        if len(all_intervals) > 0:
            self.add_choices_for_groups_for_gui(arg_name="interval_names", choices=all_intervals,
                                                with_color=True,
                                                mandatory=False,
                                                short_description="Epochs",
                                                long_description="Select epochs you want to color in the raster",
                                                family_widget="epochs")

            self.add_int_values_arg_for_gui(arg_name="intervals_alpha_color", min_value=1, max_value=100,
                                            short_description="Transparency of color bands",
                                            default_value=50, family_widget="epochs")

            self.add_bool_option_for_gui(arg_name="span_area_only_on_raster", true_by_default=False,
                                         short_description="Span only on raster",
                                         long_description="If checked, means the span will also be displayed in "
                                                          "the sum of activity plot if existing",
                                         family_widget="epochs")

        if len(self._data_to_analyse) == 1 and self._data_to_analyse[0].has_epoch_table():
            self.add_bool_option_for_gui(arg_name="use_epoch_table", true_by_default=False,
                                         short_description="Use epoch table for display",
                                         family_widget="epochs_table")
            self.add_epoch_dict_arg_for_gui(short_description="Define epochs to group from epoch table for display",
                                            long_description=None,
                                            multiple_choices=True,
                                            arg_name='epoch_table', family_widget="epochs_table")
            self.add_color_arg_for_gui(arg_name="epoch_table_color", default_value=(1, 1, 1, 1.),
                                       short_description="Color of the epochs selected from table",
                                       long_description=None, family_widget="epochs_table")

        if len(self._data_to_analyse) == 1 and self._data_to_analyse[0].has_trial_table():
            self.add_bool_option_for_gui(arg_name="use_trial_table", true_by_default=False,
                                         short_description="Use trial table for display",
                                         family_widget="trials_table")
            self.add_trial_dict_arg_for_gui(short_description="Define trials to group from trial table for display",
                                            long_description=None,
                                            multiple_choices=True,
                                            arg_name='trial_table', family_widget="trials_table")
            self.add_color_arg_for_gui(arg_name="trial_table_color", default_value=(1, 1, 1, 1.),
                                       short_description="Color of the epochs selected from table",
                                       long_description=None, family_widget="trials_table")

        all_cell_types = []
        for data_to_analyse in self._data_to_analyse:
            all_cell_types.extend(data_to_analyse.get_all_cell_types())

        all_cell_types = list(set(all_cell_types))

        self.add_choices_for_groups_for_gui(arg_name="cells_groups", choices=all_cell_types,
                                            with_color=True,
                                            mandatory=False,
                                            short_description="Groups of cells",
                                            long_description="Select cells's groups you want to color in the raster",
                                            family_widget="cell_type",
                                            add_custom_group_field=True,
                                            custom_group_validation_fct=validate_indices_in_string_format,
                                            custom_group_processor_fct=None)
        self.add_bool_option_for_gui(arg_name="sort_raster_by_cell_type", true_by_default=False,
                                     short_description="Sort raster cells' groups ",
                                     family_widget="cell_type")

        self.add_bool_option_for_gui(arg_name="pick_n_random_cells", true_by_default=False,
                                     short_description="Plot only 'n' random cells",
                                     family_widget="cells_to_plot")

        self.add_int_values_arg_for_gui(arg_name="n_rnd_cells", min_value=1, max_value=500,
                                        short_description="Number of random cells to plot",
                                        default_value=5, long_description=None, family_widget="cells_to_plot")

        self.add_bool_option_for_gui(arg_name="subplot_frames", true_by_default=False,
                                     short_description="Plot sample of frames",
                                     family_widget="frames_to_plot")

        frames_meth = ["block", "define_first_last"]
        self.add_choices_arg_for_gui(arg_name="sample_frames_selection", choices=frames_meth,
                                     default_value="block", short_description="Method to sample CI frames",
                                     multiple_choices=False,
                                     family_widget="frames_to_plot")

        self.add_int_values_arg_for_gui(arg_name="n_frames", min_value=10, max_value=15000,
                                        short_description="Size of the block to pick in frames",
                                        default_value=5000, long_description=None, family_widget="frames_to_plot_block")

        self.add_int_values_arg_for_gui(arg_name="first_frame", min_value=0, max_value=50000,
                                        short_description="First CI frame to plot",
                                        default_value=0, long_description=None, family_widget="frames_to_plot_frames")

        self.add_int_values_arg_for_gui(arg_name="last_frame", min_value=0, max_value=100000,
                                        short_description="Last CI frame to plot",
                                        default_value=10000, long_description=None, family_widget="frames_to_plot_frames")

        spike_shapes = ["|", "o", ".", "*"]
        self.add_choices_arg_for_gui(arg_name="spike_shape", choices=spike_shapes,
                                     default_value="|", short_description="Spikes shape",
                                     multiple_choices=False,
                                     family_widget="spikes")

        self.add_int_values_arg_for_gui(arg_name="spike_size", min_value=5, max_value=500,
                                        short_description="Spike size",
                                        default_value=5, long_description=None, family_widget="spikes")

        self.add_color_arg_for_gui(arg_name="spikes_color", default_value=(1, 1, 1, 1.),
                                   short_description="spikes color",
                                   long_description=None, family_widget="spikes")

        norm = ["z-score", "df/f", "raw"]
        self.add_choices_arg_for_gui(arg_name="trace_normalization", choices=norm,
                                     default_value="df/f", short_description="Traces normalization method",
                                     multiple_choices=False,
                                     family_widget="traces")

        self.add_int_values_arg_for_gui(arg_name="traces_lw", min_value=1, max_value=500,
                                        short_description="Traces line width",
                                        default_value=30, family_widget="traces")

        self.add_bool_option_for_gui(arg_name="use_brewer_colors_for_traces", true_by_default=True,
                                     short_description="Use brewer colors for traces",
                                     long_description="If False, will use spikes color",
                                     family_widget="traces")

        self.add_bool_option_for_gui(arg_name="display_dashed_line_with_traces", true_by_default=False,
                                     short_description="Dashlines with traces",
                                     long_description="Display a dashline representing the mean value of each cell "
                                                      "fluoresence' signal",
                                     family_widget="traces")

        self.add_color_arg_for_gui(arg_name="background_color", default_value=(0, 0, 0, 1.),
                                   short_description="background color",
                                   long_description=None, family_widget="raster_config")

        self.add_color_arg_for_gui(arg_name="activity_sum_plot_color", default_value=(1, 1, 1, 1.),
                                   short_description="Activity sum plot color",
                                   long_description=None, family_widget="raster_config")

        self.add_color_arg_for_gui(arg_name="y_ticks_labels_color", default_value=(1, 1, 1, 1.),
                                   short_description="Y axis ticks labels color",
                                   long_description=None, family_widget="raster_config")

        self.add_color_arg_for_gui(arg_name="x_ticks_labels_color", default_value=(1, 1, 1, 1.),
                                   short_description="X axis ticks labels color",
                                   long_description=None, family_widget="raster_config")

        self.add_field_text_option_for_gui(arg_name="raster_y_axis_label", default_value="",
                                           short_description="Raster y axis label",
                                           long_description=None, family_widget="raster_config")

        self.add_int_values_arg_for_gui(arg_name="raster_y_axis_label_size", min_value=1, max_value=100,
                                        short_description="Raster y axis label size",
                                        default_value=10, family_widget="raster_config")

        self.add_color_arg_for_gui(arg_name="axes_label_color", default_value=(1, 1, 1, 1.),
                                   short_description="Axes label color",
                                   long_description=None, family_widget="raster_config")

        self.add_int_values_arg_for_gui(arg_name="x_axis_ticks_label_size", min_value=1, max_value=50,
                                        short_description="X axis ticks label size",
                                        default_value=8, family_widget="raster_config")

        self.add_int_values_arg_for_gui(arg_name="y_axis_ticks_label_size", min_value=1, max_value=50,
                                        short_description="Y axis ticks label size",
                                        default_value=8, family_widget="raster_config")

        self.add_int_values_arg_for_gui(arg_name="bin_size_ms_for_spikes_sum", min_value=10, max_value=500,
                                        short_description="Bin size in ms for activity sum",
                                        default_value=150, family_widget="raster_config")

        self.add_bool_option_for_gui(arg_name="hide_x_ticks_labels", true_by_default=False,
                                     short_description="Hide x ticks labels",
                                     family_widget="raster_config")

        self.add_bool_option_for_gui(arg_name="hide_raster_y_ticks_labels", true_by_default=True,
                                     short_description="Hide raster y ticks labels",
                                     family_widget="raster_config")

        self.add_bool_option_for_gui(arg_name="with_ticks", true_by_default=False,
                                     short_description="Ticks on plots",
                                     family_widget="raster_config")

        self.add_bool_option_for_gui(arg_name="with_activity_sum", true_by_default=True,
                                     short_description="With activity sum plot",
                                     long_description=None, family_widget="raster_activity_sum_config")

        self.add_bool_option_for_gui(arg_name="sum_as_percentage", true_by_default=True,
                                     short_description="Show sum of active cell as percentage",
                                     long_description=None, family_widget="raster_activity_sum_config")

        self.add_bool_option_for_gui(arg_name="activity_sum_specified_y_lim", true_by_default=False,
                                     short_description="Manually set y-axis limit on activity sum plot",
                                     family_widget="raster_activity_sum_config")

        self.add_int_values_arg_for_gui(arg_name="activity_sum_yaxis_lim", min_value=5, max_value=40,
                                        short_description="Max value on activity sum plot",
                                        default_value=20, family_widget="raster_activity_sum_config")

        self.add_bool_option_for_gui(arg_name="show_activity_sum_label", true_by_default=False,
                                     short_description="Show Y-axis label on activity sum plot",
                                     long_description=None, family_widget="raster_activity_sum_config")

        self.add_bool_option_for_gui(arg_name="show_y_scale", true_by_default=False,
                                     short_description="Show Y-axis scale (only if plot Traces)",
                                     family_widget="raster_scale_config")

        self.add_bool_option_for_gui(arg_name="show_x_scale", true_by_default=False,
                                     short_description="Show X-axis scale",
                                     family_widget="raster_scale_config")

        self.add_field_text_option_for_gui(arg_name="y_scale_label", default_value='dF/F',
                                           short_description="Label for Y axis scale bar",
                                           long_description="To use if the RoiResponseSeries to plot is 'Traces'",
                                           family_widget="raster_scale_config")

        self.add_int_values_arg_for_gui(arg_name="y_scale_value", min_value=1, max_value=10,
                                        short_description="Length of the Y-axis scale bar",
                                        long_description="To use if the RoiResponseSeries to plot is 'Traces'",
                                        default_value=1, family_widget="raster_scale_config")

        x_scale_units = ["sec", "min"]
        self.add_choices_arg_for_gui(arg_name="x_scale_unit", choices=x_scale_units,
                                     default_value="min", short_description="Unit of X scale bar",
                                     multiple_choices=False,
                                     family_widget="raster_scale_config")

        self.add_int_values_arg_for_gui(arg_name="x_scale_value", min_value=1, max_value=60,
                                        short_description="Length of the X-axis scale bar (in min or sec)",
                                        default_value=1, family_widget="raster_scale_config")

        self.add_image_format_package_for_gui()

        self.add_verbose_arg_for_gui()

        self.add_with_timestamp_in_filename_arg_for_gui()

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

        subplot_frames = kwargs.get("subplot_frames")

        sample_frames_selection = kwargs.get("sample_frames_selection")

        frame_block_size = kwargs.get("n_frames")

        first_given_ci_frame = kwargs.get("first_frame")

        last_given_ci_frame = kwargs.get("last_frame")

        pick_n_random_cells = kwargs.get("pick_n_random_cells")

        hide_x_ticks_labels = kwargs.get("hide_x_ticks_labels")

        hide_raster_y_ticks_labels = kwargs.get("hide_raster_y_ticks_labels")

        with_ticks = kwargs.get("with_ticks")

        spike_shape = kwargs.get("spike_shape", "|")

        spike_size = kwargs.get("spike_size", "5")
        spike_size = spike_size * 0.01

        use_brewer_colors_for_traces = kwargs.get("use_brewer_colors_for_traces", True)

        trace_normalization = kwargs.get("trace_normalization")

        background_color = kwargs.get("background_color")

        spikes_color = kwargs.get("spikes_color")

        activity_sum_plot_color = kwargs.get("activity_sum_plot_color")

        axes_label_color = kwargs.get("axes_label_color")

        with_activity_sum = kwargs.get("with_activity_sum")

        sum_as_percentage = kwargs.get("sum_as_percentage")

        activity_sum_specified_y_lim = kwargs.get("activity_sum_specified_y_lim")

        activity_sum_yaxis_lim = kwargs.get("activity_sum_yaxis_lim")

        show_activity_sum_label = kwargs.get("show_activity_sum_label")

        display_dashed_line_with_traces = kwargs.get("display_dashed_line_with_traces")

        xkcd_mode = kwargs.get("xkcd_mode", False)

        # ------------- CELL TYPES ---------------
        sort_raster_by_cell_type = kwargs.get("sort_raster_by_cell_type", False)

        cells_groups_dict = kwargs.get("cells_groups")
        # ------------- CELL TYPES ---------------

        # ------------- EPOCHS ---------------
        interval_names = kwargs.get("interval_names")

        intervals_alpha_color = kwargs.get("intervals_alpha_color", 100)
        intervals_alpha_color = intervals_alpha_color * 0.01

        span_area_only_on_raster = kwargs.get("span_area_only_on_raster", False)

        # epoch from epoch table
        use_epoch_table = kwargs.get("use_epoch_table")
        epoch_table = kwargs.get("epoch_table")
        epoch_table_color = kwargs.get('epoch_table_color')

        # trial from trial table
        use_trial_table = kwargs.get("use_trial_table")
        trial_table = kwargs.get("trial_table")
        trial_table_color = kwargs.get('trial_table_color')
        # ------------- EPOCHS ---------------

        traces_lw = kwargs.get("traces_lw")
        traces_lw = traces_lw * 0.01

        bin_size_ms_for_spikes_sum = kwargs.get("bin_size_ms_for_spikes_sum")

        raster_y_axis_label = kwargs.get("raster_y_axis_label")
        if raster_y_axis_label.strip() == "":
            raster_y_axis_label = None
        raster_y_axis_label_size = kwargs.get("raster_y_axis_label_size")

        y_axis_ticks_label_size = kwargs.get("y_axis_ticks_label_size")
        x_axis_ticks_label_size = kwargs.get("x_axis_ticks_label_size")

        y_ticks_labels_color = kwargs.get("y_ticks_labels_color")
        x_ticks_labels_color = kwargs.get("x_ticks_labels_color")

        # image package format
        save_formats = kwargs["save_formats"]
        if save_formats is None:
            save_formats = "pdf"

        save_raster = True

        dpi = kwargs.get("dpi", 100)

        width_fig = kwargs.get("width_fig")

        height_fig = kwargs.get("height_fig")

        with_timestamps_in_file_name = kwargs.get("with_timestamp_in_file_name", True)

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
            if np.isnan(neuronal_data).any():
                print(f"Only 'nan' in this neuronal activity matrix. Go to next session")
                continue
            if not np.any(neuronal_data):
                print(f"Only null values in this neuronal activity matrix. Go to next session")
                continue

            neuronal_data_timestamps = np.asarray(session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_info))

            frame_times = None
            if len(neuronal_data_timestamps) > 2:
                # if the timestamps is 2? then it means it is not really timestamps, but just the frame index
                if neuronal_data_timestamps[2] != 2:
                    frame_times = neuronal_data_timestamps

            # In NWB file imaging data should be (times x cells) and transposed to (cells x times) in CICADA wrapper
            # Check that neuronal data 2nd dimension is of same length than the length of timestamps
            if neuronal_data.shape[0] == len(frame_times):
                neuronal_data = np.transpose(neuronal_data)
                if verbose:
                    print(f"Seems like imaging data from the NWB file were (cells x times) instead of (times x cells), "
                          f"data have been transposed")

            # ------------- EPOCHS ---------------
            span_area_coords = None
            span_area_colors = None
            if (interval_names is not None) and (len(interval_names) > 0):
                span_area_coords = []
                span_area_colors = []
                # print(f"Behavioral epochs names: {session_data.get_behavioral_epochs_names()}")
                # print(f"Interval names: {session_data.get_intervals_names()}")
                for interval_group_name, interval_info in interval_names.items():
                    if len(interval_info) != 2:
                        continue
                    interval_names_in_group = interval_info[0]
                    interval_color = interval_info[1]
                    # print(f"Interval {interval_group_name}, color: "
                    #       f"{rgb_to_name(interval_color, with_float_values=True)}")
                    rdb_values = [int(np.round(c*255)) for c in interval_color]
                    rdb_values = rdb_values[:-1]
                    print(f"Interval {interval_group_name}, color: {rdb_values}")

                    intervals_in_group = []
                    # TODO: See for fusioning epochs from a same group so there are extended
                    for interval_name in interval_names_in_group:
                        # looking in behavior or intervals
                        intervals_timestamps = session_data.get_interval_times(interval_name=interval_name)
                        if intervals_timestamps is None:
                            intervals_timestamps = session_data.get_behavioral_epochs_times(epoch_name=interval_name)
                        if intervals_timestamps is None:
                            # means this session doesn't have this epoch name
                            print(f"{interval_name}: intervals_timestamps is None")
                            continue

                        if frame_times is None:
                            # means we don't know the timestamps
                            continue

                        # putting it as a list format, listof tuple of float
                        intervals_timestamps = from_timestamps_array_to_list(time_stamps_array=intervals_timestamps,
                                                                             frames_timestamps=neuronal_data_timestamps)
                        intervals_in_group.extend(intervals_timestamps)
                        # # now we want to get the intervals time_stamps and convert them in frames
                        # intervals_frames = from_timestamps_to_frame_epochs(time_stamps_array=intervals_timestamps,
                        #                                                    frames_timestamps=neuronal_data_timestamps,
                        #                                                    as_list=True)
                        # intervals_in_group.extend(intervals_frames)
                    span_area_coords.append(intervals_in_group)
                    span_area_colors.append(interval_color)
            if epoch_table is not None and use_epoch_table:
                if len(epoch_table) == 0:
                    continue
                else:
                    span_area_coords = []
                    span_area_colors = []
                    print(f" ")
                    print(f"Epochs build on: ")
                    print_info_dict(epoch_table)
                    epoch_timestamps, time_unit = session_data.get_epochs_timestamps_from_table(requirements_dict=epoch_table)
                    if time_unit == "frames":
                        print(f"Convert 'start_time' and 'stop_time' from frames to seconds")
                        epoch_timestamps = np.array(epoch_timestamps).astype(int)
                        epoch_timestamps[0, :] = neuronal_data_timestamps[epoch_timestamps[0, :]]
                        epoch_timestamps[1, :] = neuronal_data_timestamps[epoch_timestamps[1, :]]
                    intervals_in_group = from_timestamps_array_to_list(time_stamps_array=epoch_timestamps,
                                                                       frames_timestamps=neuronal_data_timestamps)
                    print(f"Total of {epoch_timestamps.shape[1]} epochs")
                    span_area_coords.append(intervals_in_group)
                    span_area_colors.append(epoch_table_color)
            if trial_table is not None and use_trial_table:
                if len(trial_table) == 0:
                    continue
                else:
                    span_area_coords = []
                    span_area_colors = []
                    print(f"Trials build on: ")
                    print_info_dict(trial_table)
                    epoch_timestamps, time_unit = session_data.get_trials_timestamps_from_table(requirements_dict=trial_table)
                    if time_unit == "frames":
                        print(f"Convert 'start_time' and 'stop_time' from frames to seconds")
                        epoch_timestamps = np.array(epoch_timestamps).astype(int)
                        epoch_timestamps[0, :] = neuronal_data_timestamps[epoch_timestamps[0, :]]
                        epoch_timestamps[1, :] = neuronal_data_timestamps[epoch_timestamps[1, :]]
                    intervals_in_group = from_timestamps_array_to_list(time_stamps_array=epoch_timestamps,
                                                                       frames_timestamps=neuronal_data_timestamps)
                    print(f"Total of {epoch_timestamps.shape[1]} trials")
                    span_area_coords.append(intervals_in_group)
                    span_area_colors.append(trial_table_color)
            # ------------- END EPOCHS ---------------
            # print(f"timestamps[:5] {timestamps[:5]}")
            cells_to_highlight = None
            cells_to_highlight_colors = None

            cells_order = np.arange(len(neuronal_data))

            if (cells_groups_dict is not None) and (len(cells_groups_dict) > 0):
                cell_indices_by_cell_type = session_data.get_cell_indices_by_cell_type(roi_serie_keys=
                                                                                       roi_response_serie_info)
                cells_to_highlight = []
                cells_to_highlight_colors = []
                if sort_raster_by_cell_type:
                    # ordering the data by cell type
                    last_index = 0
                    cells_added = []
                    new_neuronal_data = np.zeros(neuronal_data.shape)
                # TODO: See to check if groups don't contain some of the cells
                #  so far if that's the case it won't crash but some cells will be displayed several times
                # for cell_type, cell_indices in cell_indices_by_cell_type.items():
                for cells_group_name, cells_group_info in cells_groups_dict.items():
                    if len(cells_group_info) != 2:
                        continue
                    cells_names_in_group = cells_group_info[0]
                    cells_group_color = cells_group_info[1]
                    for cells_name in cells_names_in_group:
                        # then we extract the cell_indices from the cells_group_name
                        # it is either a string representing the cell_type or a series of indices
                        if cells_name in cell_indices_by_cell_type:
                            cell_indices = cell_indices_by_cell_type[cells_name]
                        else:
                            cell_indices = np.array(extract_indices_from_string(cells_name))
                        print(f"N cells in {cells_name}: {len(cell_indices)}")
                        if len(cell_indices) == 0:
                            continue
                        # making sure we are on the boundaries
                        cell_indices = cell_indices[np.logical_and(cell_indices >= 0,
                                                                   cell_indices < len(neuronal_data))]
                        if sort_raster_by_cell_type:
                            new_neuronal_data[last_index:last_index+len(cell_indices)] = neuronal_data[cell_indices]
                        # coloring the cells
                        cells_to_highlight_colors.extend([cells_group_color]*len(cell_indices))
                        if sort_raster_by_cell_type:
                            cells_to_highlight.extend(list(np.arange(last_index, last_index+len(cell_indices))))
                            last_index = last_index + len(cell_indices)
                            cells_added.extend(list(cell_indices))
                        else:
                            cells_to_highlight.extend(list(cell_indices))

                if sort_raster_by_cell_type:
                    cells_left = np.setdiff1d(np.arange(len(neuronal_data)), cells_added)
                    cells_order = cells_added + list(cells_left)
                    if len(cells_left) > 0:
                        new_neuronal_data[last_index:last_index+len(cells_left)] = neuronal_data[cells_left]
                    neuronal_data = new_neuronal_data

            # Default parameters without scale on plot
            show_y_scale = kwargs.get("show_y_scale")
            show_x_scale = kwargs.get("show_x_scale")
            y_scale_label = None
            y_scale_value = None
            x_scale_unit = None
            x_scale_length = None
            x_scale_init_value = None
            # to decide if we display the neuronal data as trace or as a binary raster
            # we look at how the data looks like, if there more than 10 different values, then it will be a trace mode
            unique_values = np.unique(neuronal_data)
            # if "trace" in roi_response_serie_info[-1]:
            if len(unique_values) > 10:
                # Display traces
                if verbose:
                    print(f"Display Traces")
                display_traces = True
                display_spike_nums = False
                traces = neuronal_data
                spike_nums = None
                if trace_normalization == 'z-score':
                    if verbose:
                        print(f"Use {roi_response_serie_info[2]} and do 'z-score' normalization")
                    # we normalize the traces with z-score
                    for trace_index, trace in enumerate(traces):
                        traces[trace_index] = (trace - np.mean(trace)) / np.std(trace)
                elif trace_normalization == 'df/f':
                    if verbose:
                        print(f"Use {roi_response_serie_info[2]} and do 'median' normalization")
                    for trace_index, trace in enumerate(traces):
                        traces[trace_index] = (trace - np.median(trace)) / np.median(trace)
                else:
                    traces = traces
                    if verbose:
                        print(f"Use {roi_response_serie_info[2]} without normalization")
                if pick_n_random_cells:
                    n_rnd_cells = kwargs.get("n_rnd_cells")
                    if n_rnd_cells > traces.shape[0]:
                        n_rnd_cells = traces.shape[0]
                    rnd_cell_index = np.random.choice(a=traces.shape[0], size=n_rnd_cells, replace=False, p=None)
                    traces = traces[rnd_cell_index, :]
                    cells_order = rnd_cell_index
                if subplot_frames:
                    if sample_frames_selection == 'block':
                        first_frame_to_take = np.random.randint(1, max((traces.shape[1] - frame_block_size), 0))
                        last_frame_to_take = first_frame_to_take + frame_block_size
                        traces = traces[:, first_frame_to_take: last_frame_to_take]
                        frame_times = frame_times[first_frame_to_take: last_frame_to_take]
                    if sample_frames_selection == 'define_first_last':
                        first_frame_to_take = first_given_ci_frame
                        last_frame_to_take = min(last_given_ci_frame, traces.shape[1])
                        traces = traces[:, first_frame_to_take: last_frame_to_take]
                        frame_times = frame_times[first_frame_to_take: last_frame_to_take]
                if verbose:
                    print(f"Traces: {traces.shape[0]} cells, {traces.shape[1]} frames")
                # Get the scale parameters
                if show_y_scale:
                    y_scale_label = kwargs.get("y_scale_label")
                    y_scale_value = kwargs.get("y_scale_value")
                if show_x_scale:
                    x_scale_unit = kwargs.get("x_scale_unit")
                    x_scale_init_value = kwargs.get("x_scale_value")
                    x_scale_length = x_scale_init_value if x_scale_unit == 'sec' else x_scale_init_value * 60
            else:
                # Display raster plot
                if verbose:
                    print(f"Display Spike Raster")
                display_traces = False
                display_spike_nums = True
                spike_nums = neuronal_data
                traces = None
                if pick_n_random_cells:
                    n_rnd_cells = kwargs.get("n_rnd_cells")
                    if n_rnd_cells > spike_nums.shape[0]:
                        n_rnd_cells = spike_nums.shape[0]
                    rnd_cell_index = np.random.choice(a=spike_nums.shape[0], size=n_rnd_cells, replace=False, p=None)
                    spike_nums = spike_nums[rnd_cell_index, :]
                    cells_order = rnd_cell_index
                if subplot_frames:
                    if sample_frames_selection == 'block':
                        first_frame_to_take = np.random.randint(1, max((spike_nums.shape[1] - frame_block_size), 0))
                        last_frame_to_take = first_frame_to_take + frame_block_size
                        spike_nums = spike_nums[:, first_frame_to_take: last_frame_to_take]
                        frame_times = frame_times[first_frame_to_take: last_frame_to_take]
                    if sample_frames_selection == 'define_first_last':
                        first_frame_to_take = first_given_ci_frame
                        last_frame_to_take = min(last_given_ci_frame, spike_nums.shape[1])
                        spike_nums = spike_nums[:, first_frame_to_take: last_frame_to_take]
                        frame_times = frame_times[first_frame_to_take: last_frame_to_take]
                if verbose:
                    print(f"Raster: {spike_nums.shape[0]} cells, {spike_nums.shape[1]} frames")
                # Get the scale parameters
                if show_x_scale:
                    x_scale_unit = kwargs.get("x_scale_unit")
                    x_scale_init_value = kwargs.get("x_scale_value")
                    x_scale_length = x_scale_init_value if x_scale_unit == 'sec' else x_scale_init_value * 60

            if hide_raster_y_ticks_labels:
                y_ticks_labels = None
            else:
                y_ticks_labels = cells_order
            plot_raster(spike_nums=spike_nums,
                        frame_times=frame_times, traces=traces, display_traces=display_traces,
                        bin_size_ms_for_spikes_sum=bin_size_ms_for_spikes_sum,
                        display_dashed_line_with_traces=display_dashed_line_with_traces,
                        traces_lw=traces_lw,
                        file_name="raster_" + session_data.identifier,
                        display_spike_nums=display_spike_nums,
                        with_timestamp_in_file_name=with_timestamps_in_file_name,
                        path_results=self.get_results_path(),
                        save_raster=save_raster,
                        show_raster=False,
                        use_brewer_colors_for_traces=use_brewer_colors_for_traces,
                        dpi=dpi,
                        xkcd_mode=xkcd_mode,
                        show_sum_spikes_as_percentage=sum_as_percentage,
                        show_activity_sum_label=show_activity_sum_label,
                        spike_shape=spike_shape,
                        spike_shape_size=spike_size,
                        without_ticks=not with_ticks,
                        without_activity_sum=not with_activity_sum,
                        activity_sum_specified_y_lim=activity_sum_specified_y_lim,
                        y_lim_sum_activity=activity_sum_yaxis_lim,
                        cell_spikes_color=spikes_color,
                        figure_background_color=background_color,
                        raster_face_color=background_color,
                        activity_sum_plot_color=activity_sum_plot_color,
                        activity_sum_face_color=background_color,
                        axes_label_color=axes_label_color,
                        hide_x_ticks_labels=hide_x_ticks_labels,
                        hide_raster_y_ticks_labels=hide_raster_y_ticks_labels,
                        raster_y_axis_label=raster_y_axis_label,
                        raster_y_axis_label_size=raster_y_axis_label_size,
                        y_ticks_labels=y_ticks_labels,
                        y_ticks_labels_size=y_axis_ticks_label_size,
                        x_ticks_labels_size=x_axis_ticks_label_size,
                        y_ticks_labels_color=y_ticks_labels_color,
                        x_ticks_labels_color=x_ticks_labels_color,
                        cells_to_highlight=cells_to_highlight,
                        cells_to_highlight_colors=cells_to_highlight_colors,
                        span_area_coords=span_area_coords,
                        span_area_colors=span_area_colors,
                        span_area_only_on_raster=span_area_only_on_raster,
                        alpha_span_area=intervals_alpha_color,
                        size_fig=(width_fig, height_fig),
                        show_y_scale=show_y_scale,
                        show_x_scale=show_x_scale,
                        y_scale_unit=y_scale_label,
                        y_scale_length=y_scale_value,
                        x_scale_unit=x_scale_unit,
                        x_scale_length=x_scale_length,
                        x_scale_label=x_scale_init_value,
                        save_formats=save_formats)

            if verbose:
                print(" ")
            self.update_progressbar(time_started=self.analysis_start_time, increment_value=100 / n_sessions)

        print(f"Raster analysis run in {np.round(time() - self.analysis_start_time, 3)} sec")
