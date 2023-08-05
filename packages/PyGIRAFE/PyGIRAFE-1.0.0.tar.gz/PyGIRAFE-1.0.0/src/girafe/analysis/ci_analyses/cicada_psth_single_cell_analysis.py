from cicada.analysis.cicada_analysis import CicadaAnalysis
from cicada.utils.misc import from_timestamps_to_frame_epochs, validate_indices_in_string_format, \
    extract_indices_from_string, get_continous_time_periods, print_info_dict
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from cicada.utils.display.rasters import plot_raster


class CicadaPsthSingleCellAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        A list of
        :param data_to_analyse: list of data_structure
        :param family_id: family_id indicated to which family of analysis this class belongs. If None, then
        the analysis is a family in its own.
        :param data_format: indicate the type of data structure. for NWB, NIX
        """
        CicadaAnalysis.__init__(self, name="Single-cell level PSTH", family_id="Epochs",
                                short_description="Build PeriStimuli Time Histogram at single cell level",
                                config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

        # each key is an int representing the age, the value is a list of session_data
        self.sessions_by_age = dict()

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaPsthSingleCellAnalysis(config_handler=self.config_handler)
        self.transfer_attributes_to_tabula_rasa_copy(analysis_copy=analysis_copy)
        return analysis_copy

    def check_data(self):
        """
        Check the data given one initiating the class and return True if the data given allows the analysis
        implemented, False otherwise.
        :return: a boolean
        """
        super().check_data()

        if len(self._data_to_analyse) > 1:
            self.invalid_data_help = f"This analysis can be done only one session at a time"
            return False

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

        # It is also necessary to have epoch to work with, but if None is available, then it won't just be possible
        # to run the analysis

        return True

    def set_arguments_for_gui(self):
        """

        Returns:

        """
        CicadaAnalysis.set_arguments_for_gui(self)

        self.add_roi_response_series_arg_for_gui(short_description="Neural activity to use", long_description=None)

        data_kind = ['Traces', 'Raster']
        self.add_choices_arg_for_gui(arg_name="data_type", choices=data_kind,
                                     default_value="Raster",
                                     short_description="Format of the selected Roi response Series (RRS)",
                                     long_description="Specify here the format of the selected RRS in "
                                                      "'neural activity to use' (usually 'Traces' (raw, df/f,...) or "
                                                      "'Raster' (binary matrix)",
                                     multiple_choices=False,
                                     family_widget="data_type")

        self.add_bool_option_for_gui(arg_name="has_traces", true_by_default=False,
                                     short_description="Traces available in RRS ?",
                                     long_description="If the selected RRS is not 'Traces', is there traces accessible "
                                                      "among the others RRS ? If yes specify a keyword below",
                                     family_widget="data_type")
        self.add_field_text_option_for_gui(arg_name="trace_keyword", default_value='raw_trace',
                                           short_description="Keyword to find 'Traces'",
                                           long_description="To use if 'Traces' is not the format selected, keyword to "
                                                            "select the 'Traces' among RRS",
                                           family_widget="data_type")

        self.add_bool_option_for_gui(arg_name="has_raster", true_by_default=False,
                                     short_description="Raster available in RRS ?",
                                     long_description="If selected RRS is not 'Raster', is there a raster accessible "
                                                      "among the others RRS ?If yes specify a keyword below",
                                     family_widget="data_type")
        self.add_field_text_option_for_gui(arg_name="raster_keyword", default_value='raster',
                                           short_description="Keyword to find 'Raster'",
                                           long_description="To use if 'Raster' is not the format selected keyword to "
                                                            "select the 'Raster' among RRS",
                                           family_widget="data_type")

        self.add_bool_option_for_gui(arg_name="do_psth_on_one_epoch", true_by_default=False,
                                     short_description="Build PSTH from ONE main epoch ?",
                                     long_description="If yes, build the PSTH only from the behavioral epochs "
                                                      "occurring in this selected main epoch",
                                     family_widget="main epochs")

        all_epochs = []
        for data_to_analyse in self._data_to_analyse:
            all_epochs.extend(data_to_analyse.get_intervals_names())
            all_epochs.extend(data_to_analyse.get_behavioral_epochs_names())
        all_epochs = list(np.unique(all_epochs))

        self.add_bool_option_for_gui(arg_name="do_psth_on_one_epoch", true_by_default=False,
                                     short_description="Build PSTH from ONE main epoch ?",
                                     long_description="If yes, build the PSTH only from the behavioral epochs "
                                                      "occurring in this selected main epoch",
                                     family_widget="main epochs")

        self.add_choices_for_groups_for_gui(arg_name="psth_period", choices=all_epochs,
                                            with_color=False,
                                            mandatory=False,
                                            short_description="Select 1 epoch to build PSTH on this main epoch",
                                            long_description="Select 1 epoch to restrict PSTH analysis to the "
                                                             "behavioral epochs occurring during this epoch",
                                            family_widget="main epochs")

        psth_center_possibilities = ["behavioral epochs"]
        for data_to_analyse in self._data_to_analyse:
            acquisitions_series = data_to_analyse.get_acquisition_names()
            if "ogen_stim" in acquisitions_series:
                if "optogenetics" in psth_center_possibilities:
                    continue
                else:
                    psth_center_possibilities.append("optogenetics")
            if data_to_analyse.has_epoch_table():
                psth_center_possibilities.append("epochs table")
            if data_to_analyse.has_trial_table():
                psth_center_possibilities.append("trials table")
        self.add_choices_arg_for_gui(arg_name="psth_on", choices=psth_center_possibilities,
                                     default_value="behavior",
                                     short_description="Nature of the epochs to use to build the PSTH",
                                     multiple_choices=False,
                                     family_widget="epochs")

        self.add_choices_for_groups_for_gui(arg_name="epochs_names", choices=all_epochs,
                                            with_color=False,
                                            mandatory=False,
                                            short_description="Behavioral Epochs",
                                            long_description="Select epochs for which you want to build PSTH",
                                            family_widget="epochs")

        if len(self._data_to_analyse) == 1 and self._data_to_analyse[0].has_epoch_table():
            self.add_epoch_dict_arg_for_gui(short_description="Define epochs to group from epoch table",
                                            long_description=None,
                                            multiple_choices=True,
                                            arg_name='epoch_table', family_widget="epochs_table")

        if len(self._data_to_analyse) == 1 and self._data_to_analyse[0].has_trial_table():
            self.add_trial_dict_arg_for_gui(short_description="Define trials to group from trial table",
                                            long_description=None,
                                            multiple_choices=True,
                                            arg_name='trial_table', family_widget="trials_table")

        self.add_bool_option_for_gui(arg_name="do_fusion_epochs", true_by_default=False,
                                     short_description="Fusion epochs ?",
                                     long_description="If checked, within a group epochs that overlap "
                                                      "will be fused so they represent "
                                                      "then one epoch.",
                                     family_widget="general_epochs")

        self.add_bool_option_for_gui(arg_name="filter_consecutive_movements", true_by_default=True,
                                     short_description="Remove movements separated by less time than psth range",
                                     long_description=None,
                                     family_widget="general_epochs")

        cells_to_analyse = ["all cells", "custom list", "cell-type group"]
        self.add_choices_arg_for_gui(arg_name="cells_to_include", choices=cells_to_analyse,
                                     default_value="custom list",
                                     short_description="Cells to analyse",
                                     multiple_choices=False,
                                     family_widget="cell_group")
        all_cell_types = []
        for data_to_analyse in self._data_to_analyse:
            all_cell_types.extend(data_to_analyse.get_all_cell_types())

        all_cell_types = list(set(all_cell_types))
        self.add_choices_for_groups_for_gui(arg_name="cells_groups", choices=all_cell_types,
                                            with_color=False,
                                            mandatory=False,
                                            short_description="Indexes of cells to analyse",
                                            long_description="If you select cells's groups, a PSTH will be created "
                                                             "for each cells'group and session. You can indicate the "
                                                             "cell indices in text field, such as '1-4 6 15-17'to "
                                                             "make a group "
                                                             "with cell 1 to 4, 6 and 15 to 17.",
                                            family_widget="cell_group",
                                            add_custom_group_field=True,
                                            custom_group_validation_fct=validate_indices_in_string_format,
                                            custom_group_processor_fct=None)

        self.add_int_values_arg_for_gui(arg_name="psth_range", min_value=50, max_value=10000,
                                        short_description="Range of the PSTH (ms)",
                                        default_value=10000, family_widget="psth_config")

        self.add_int_values_arg_for_gui(arg_name="low_percentile", min_value=1, max_value=49,
                                        short_description="Low percentile",
                                        default_value=25, family_widget="psth_config")

        self.add_int_values_arg_for_gui(arg_name="high_percentile", min_value=51, max_value=99,
                                        short_description="High percentile",
                                        default_value=75, family_widget="psth_config")

        self.add_choices_arg_for_gui(arg_name="ref_in_epoch", choices=["start", "end", "middle"],
                                     short_description="Reference point to center PSTH",
                                     long_description="Determine which part of the epoch to center the PSTH on",
                                     default_value="start",
                                     multiple_choices=False, family_widget="psth_config")

        self.add_bool_option_for_gui(arg_name="do_surrogates", true_by_default=False,
                                     short_description="Do surrogates",
                                     long_description=None, family_widget="psth_config")

        self.add_int_values_arg_for_gui(arg_name="n_surrogates", min_value=10, max_value=1000,
                                        short_description="Number of surrogates",
                                        default_value=20, family_widget="psth_config")

        self.add_int_values_arg_for_gui(arg_name="alpha", min_value=1, max_value=5,
                                        short_description="Alpha risk value",
                                        default_value=5, family_widget="psth_config")

        traces_normalization = ["raw", "df/f", "z-score"]
        self.add_choices_arg_for_gui(arg_name="traces_norm", choices=traces_normalization,
                                     default_value="df/f",
                                     short_description="Traces normalization method",
                                     multiple_choices=False,
                                     family_widget="traces_normalization")

        self.add_color_arg_for_gui(arg_name="background_color", default_value=(1, 1, 1, 1.),
                                   short_description="background color",
                                   long_description=None, family_widget="figure1_config_color")

        self.add_color_arg_for_gui(arg_name="median_color", default_value=(0, 0, 0, 1.),
                                   short_description="Median color",
                                   long_description=None, family_widget="figure1_config_color")

        self.add_color_arg_for_gui(arg_name="prctl_color", default_value=(0.73, 0.73, 0.73, 1.),
                                   short_description="Percentile colors",
                                   long_description=None, family_widget="figure1_config_color")

        self.add_color_arg_for_gui(arg_name="rnd_color", default_value=(0.72, 0.04, 0.06, 1.),
                                   short_description="Color for surrogate",
                                   long_description=None, family_widget="figure1_config_color")

        self.add_color_arg_for_gui(arg_name="axis_color", default_value=(0, 0, 0, 1.),
                                   short_description="Axes color",
                                   long_description=None, family_widget="figure1_config_color")

        self.add_color_arg_for_gui(arg_name="labels_color", default_value=(0, 0, 0, 1.),
                                   short_description="Label color",
                                   long_description=None, family_widget="figure1_config_color")

        sequential_cmaps = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd',
                            'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
        self.add_choices_arg_for_gui(arg_name="colormap", choices=sequential_cmaps,
                                     short_description="Colormap in superimposed trace trials",
                                     default_value="Purples",
                                     multiple_choices=False, family_widget="figure2_config_color")

        self.add_bool_option_for_gui(arg_name="show_raster", true_by_default=True,
                                     short_description="Show Raster",
                                     long_description=None, family_widget="figure3_config_color")

        self.add_bool_option_for_gui(arg_name="show_traces", true_by_default=False,
                                     short_description="Show Traces",
                                     long_description=None, family_widget="figure3_config_color")

        spike_shapes = ["|", "o", ".", "*"]
        self.add_choices_arg_for_gui(arg_name="spike_shape", choices=spike_shapes,
                                     default_value="o", short_description="Raster spikes shape",
                                     multiple_choices=False,
                                     family_widget="figure3_config_color")

        self.add_int_values_arg_for_gui(arg_name="spike_size", min_value=5, max_value=500,
                                        short_description="Raster spike size",
                                        default_value=50, long_description=None, family_widget="figure3_config_color")

        self.add_color_arg_for_gui(arg_name="spikes_color", default_value=(0, 0, 0, 1.),
                                   short_description="Raster spikes color",
                                   long_description=None, family_widget="figure3_config_color")

        self.add_bool_option_for_gui(arg_name="with_activity_sum", true_by_default=True,
                                     short_description="With activity sum plot",
                                     long_description=None, family_widget="figure3_config_color")

        self.add_bool_option_for_gui(arg_name="sum_as_percentage", true_by_default=True,
                                     short_description="Show sum of active cell as percentage",
                                     long_description=None, family_widget="figure3_config_color")

        self.add_color_arg_for_gui(arg_name="activity_sum_plot_color", default_value=(0, 0, 0, 1.),
                                   short_description="Activity sum plot color",
                                   long_description=None, family_widget="figure3_config_color")

        self.add_bool_option_for_gui(arg_name="with_ticks", true_by_default=False,
                                     short_description="Ticks on plots",
                                     family_widget="figure3_config_color")

        self.add_color_arg_for_gui(arg_name="y_ticks_labels_color", default_value=(0, 0, 0, 1.),
                                   short_description="Y axis ticks labels color",
                                   long_description=None, family_widget="figure3_config_color")

        self.add_bool_option_for_gui(arg_name="hide_raster_y_ticks_labels", true_by_default=False,
                                     short_description="Hide raster y ticks labels",
                                     family_widget="figure3_config_color")

        self.add_color_arg_for_gui(arg_name="x_ticks_labels_color", default_value=(0, 0, 0, 1.),
                                   short_description="X axis ticks labels color",
                                   long_description=None, family_widget="figure3_config_color")

        self.add_bool_option_for_gui(arg_name="hide_x_ticks_labels", true_by_default=False,
                                     short_description="Hide x ticks labels",
                                     family_widget="figure3_config_color")

        self.add_image_format_package_for_gui()

        self.add_bool_option_for_gui(arg_name="verbose", true_by_default=True,
                                     short_description="With verbose",
                                     family_widget="verbose")

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
        :return:
        """
        CicadaAnalysis.run_analysis(self, **kwargs)

        roi_response_series_dict = kwargs["roi_response_series"]

        data_type = kwargs.get("data_type")

        has_traces = kwargs.get("has_traces")

        trace_keyword = kwargs.get("trace_keyword")

        has_raster = kwargs.get("has_raster")

        raster_keyword = kwargs.get("raster_keyword")

        verbose = kwargs.get("verbose", True)

        cells_to_do = kwargs.get("cells_groups")

        cells_choice = kwargs.get("cells_to_include")

        psth_range_in_ms = kwargs.get("psth_range")
        psth_range_in_sec = psth_range_in_ms / 1000

        do_psth_on_one_epoch = kwargs.get("do_psth_on_one_epoch")

        psth_period = kwargs.get("psth_period")

        psth_on = kwargs.get("psth_on")

        filter_consecutive_movements = kwargs.get("filter_consecutive_movements", False)

        traces_norm = kwargs.get("traces_norm")

        ref_in_epoch = kwargs.get("ref_in_epoch")

        low_percentile = kwargs.get("low_percentile", 25)
        high_percentile = kwargs.get("high_percentile", 75)

        do_surrogates = kwargs.get("do_surrogates", False)

        n_surrogates = kwargs.get("n_surrogates")

        alpha = kwargs.get("alpha")

        epochs_names = kwargs.get("epochs_names")
        if psth_on == "behavior":
            if (epochs_names is None) or len(epochs_names) == 0:
                print(f"No epochs selected, no analysis")
                self.update_progressbar(time_started=self.analysis_start_time, increment_value=100)
                return

        epoch_table = kwargs.get("epoch_table")
        trial_table = kwargs.get("trial_table")

        path_results = self.get_results_path()

        # ------- figures config part -------
        save_formats = kwargs["save_formats"]
        if save_formats is None:
            save_formats = "png"

        dpi = kwargs.get("dpi", 100)

        width_fig = kwargs.get("width_fig")

        height_fig = kwargs.get("height_fig")

        background_color = kwargs.get("background_color")

        median_color = kwargs.get("median_color")

        prctil_color = kwargs.get("prctl_color")

        rnd_trace_color = kwargs.get("rnd_color")

        axis_color = kwargs.get("axis_color")

        labels_color = kwargs.get("labels_color")

        colormap = kwargs.get("colormap")

        show_raster = kwargs.get("show_raster")

        show_traces = kwargs.get("show_traces")

        spike_shape = kwargs.get("spike_shape", "|")

        spike_size = kwargs.get("spike_size", "5")
        spike_size = spike_size * 0.01

        spikes_color = kwargs.get("spikes_color")

        with_activity_sum = kwargs.get("with_activity_sum")

        sum_as_percentage = kwargs.get("sum_as_percentage")

        activity_sum_plot_color = kwargs.get("activity_sum_plot_color")

        with_ticks = kwargs.get("with_ticks")

        y_ticks_labels_color = kwargs.get("y_ticks_labels_color")

        hide_raster_y_ticks_labels = kwargs.get("hide_raster_y_ticks_labels")

        x_ticks_labels_color = kwargs.get("x_ticks_labels_color")

        hide_x_ticks_labels = kwargs.get("hide_x_ticks_labels")

        font_size = kwargs.get("font_size")

        fontweight = kwargs.get("fontweight")

        fontfamily = kwargs.get("font_type")

        print(f"Run PSTH analysis at single cell level")
        for session_index, session in enumerate(self._data_to_analyse):
            session_data = session

        # Get Session Info
        info_dict = session_data.get_sessions_info()
        session_identifier = info_dict['identifier']

        if verbose:
            print(f" ")
            print(f"------------------ ONGOING SESSION: {session_identifier} -------------------- ")
            print(f"----------------------------- SESSION INFO ---------------------------------- ")
            print_info_dict(info_dict)
            print(f" ")

        # GET RASTER AND TRACES #
        if isinstance(roi_response_series_dict, dict):
            roi_response_serie_info = roi_response_series_dict[session_identifier]
        else:
            roi_response_serie_info = roi_response_series_dict

        neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)
        neuronal_data_timestamps = session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_info)

        n_cells, n_frames = neuronal_data.shape

        if data_type == 'Raster':
            if verbose:
                print(f"Initially selected ROI response serie: {roi_response_serie_info[2]}")
            raster = neuronal_data
            has_raster = True
            if has_traces:
                if verbose:
                    print(f"Traces also available")
                trace_neuronal_data = session_data.get_roi_response_serie_data_by_keyword(
                    keys=roi_response_serie_info[:-1],
                    keyword=trace_keyword)
                for key, data in trace_neuronal_data.items():
                    traces = trace_neuronal_data.get(key)
                    if verbose:
                        print(f"Looking for 'Traces' got a RRS with name: {key}")
                    break
                if traces_norm == "raw":
                    traces = traces
                if traces_norm == "df/f":
                    if verbose:
                        print(f"Do median normalization on traces")
                    for cell, trace in enumerate(traces):
                        traces[cell] = (trace - np.median(trace)) / np.median(trace)
                if traces_norm == "z-score":
                    if verbose:
                        print(f"Do Z-score normalization on traces")
                    for cell, trace in enumerate(traces):
                        traces[cell] = (trace - np.mean(trace)) / np.std(trace)
        elif data_type == 'Traces':
            traces = neuronal_data
            has_traces = True
            if verbose:
                print(f"Initially selected ROI response serie: {roi_response_serie_info[2]}")
            if traces_norm == "raw":
                traces = traces
            if traces_norm == "df/f":
                if verbose:
                    print(f"Do median normalization on traces")
                for cell, trace in enumerate(traces):
                    traces[cell] = (trace - np.median(trace)) / np.median(trace)
            if traces_norm == "z-score":
                if verbose:
                    print(f"Do Z-score normalization on traces")
                for cell, trace in enumerate(traces):
                    traces[cell] = (trace - np.mean(trace)) / np.std(trace)
            if has_raster:
                if verbose:
                    print(f"Raster also available")
                raster_neuronal_data = session_data.get_roi_response_serie_data_by_keyword(
                    keys=roi_response_serie_info[:-1],
                    keyword=raster_keyword)
                for key, data in raster_neuronal_data.items():
                    raster = raster_neuronal_data.get(key)
                    if verbose:
                        print(f"Looking for 'Raster' got a RRS with name: {key}")

        # GET THE CELLS TO DO #
        if cells_choice == "all cells":
            if verbose:
                print(f"Run the analysis on all cells")
            cell_indexes_to_do = np.arange(n_cells)
        if cells_choice == "custom list":
            if verbose:
                print(f"Run the analysis on a custom set of cells")
            group_name = cells_to_do.keys()
            group_name = list(group_name)
            if len(group_name) == 0:
                if verbose:
                    print(f"No group defined, stop analysis")
                return
            group_name = group_name[0]
            if verbose:
                print(f"Group name of the cells to use: {group_name}")
            txt_indexes = cells_to_do.get(group_name)
            txt_indexes = txt_indexes[0]
            txt_indexes = txt_indexes[0]
            cell_indexes_to_do = extract_indices_from_string(txt_indexes)
        if cells_choice == "cell-type group":
            if verbose:
                print(f"Run the analysis on a group of cells defined on cell type")
            cell_indices_by_cell_type = session_data.get_cell_indices_by_cell_type(roi_serie_keys=
                                                                                   roi_response_serie_info)
            group_name = cells_to_do.keys()
            group_name = list(group_name)
            if len(group_name) == 0:
                if verbose:
                    print(f"No group defined, stop analysis")
                return
            group_name = group_name[0]
            cell_types_in_group = cells_to_do.get(group_name)[0]
            if verbose:
                print(f"Group named: '{group_name}' that contains: {cell_types_in_group}")
            cell_indexes_to_do = []
            for celltype in cell_types_in_group:
                cell_indexes_to_do.extend(list(cell_indices_by_cell_type.get(celltype)))

        n_cells_to_do = len(cell_indexes_to_do)
        if n_cells_to_do == 0:
            if verbose:
                print(f" No cell to analyse, stop the analysis")
            return
        else:
            if verbose:
                print(f"Total of {n_cells_to_do} cells to analyse")
                print(f"Indexes of cells to analyse: {cell_indexes_to_do}")

        # GET THE EPOCH FRAMES IN GROUP
        if verbose:
            print(f" ")
            print(f"## Getting the frames in each epochs group ##")
            print(f" ")

        epochs_frames_in_group_dict = dict()

        if psth_on == "optogenetics":
            if verbose:
                print(f"Do PSTH on otpogenetic stimulation")
            opto_stimulus = session_data.get_opto_stimulation_time_serie()[0]
            otpo_timestamps = session_data.get_opto_stimulation_time_serie()[1]
            opto_stim_ts = otpo_timestamps
            opto_stim_ts[(np.where(opto_stimulus == 0)[0])] = 0

            opto_stim_periods = get_continous_time_periods(opto_stim_ts)
            n_stims = len(opto_stim_periods)
            if verbose:
                print(f"N stimulations: {n_stims}")

            opto_stim_ts_period = np.zeros((2, n_stims), dtype=float)
            for stim in range(n_stims):
                start_period = opto_stim_periods[stim][0]
                stop_period = opto_stim_periods[stim][1]
                start_period_ts = otpo_timestamps[start_period]
                stop_period_ts = otpo_timestamps[stop_period]
                opto_stim_ts_period[0, stim] = start_period_ts
                opto_stim_ts_period[1, stim] = stop_period_ts

            intervals_frames = from_timestamps_to_frame_epochs(time_stamps_array=opto_stim_ts_period,
                                                               frames_timestamps=neuronal_data_timestamps,
                                                               as_list=True)
            epochs_frames_in_group_dict['Opto_stim'] = intervals_frames
        elif psth_on == "behavioral epochs":
            if verbose:
                print(f"Do PSTH on behavioral epochs")
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
                        start_ts = max(0, start_ts - psth_range_in_sec)
                        stop_ts = stop_ts + psth_range_in_sec
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
                            # we can skip it
                            if (filter_consecutive_movements is False) and (do_psth_on_one_epoch is False):
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
                            if do_psth_on_one_epoch and as_invalid is False:
                                keys_list = list(psth_period.keys())
                                psth_epoch_name = keys_list[0]
                                epoch_to_get = psth_period.get(psth_epoch_name)
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
                                    print(
                                        f"Remove {epoch_name} epochs if they follow the previous kept {epoch_name}"
                                        f" by less than PSTH range ({2*psth_range_in_ms / 1000} s) ")
                                if (epoch_start_ts - previous_epoch_start_ts) <= 2 * psth_range_in_sec:
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
                                                                       frames_timestamps=neuronal_data_timestamps,
                                                                       as_list=True)

                    epochs_frames_in_group.extend(intervals_frames)

                epochs_frames_in_group_dict[epoch_group_name] = epochs_frames_in_group
        elif psth_on == "epochs table":
            print(f" ")
            print(f"Epochs build on: ")
            print_info_dict(epoch_table)
            epoch_timestamps, time_unit = session_data.get_epochs_timestamps_from_table(requirements_dict=epoch_table)
            if time_unit == "frames":
                intervals_frames = [[int(epoch_timestamps[0, i]), int(epoch_timestamps[1, i])]
                                    for i in range(epoch_timestamps.shape[1])]
            else:
                intervals_frames = from_timestamps_to_frame_epochs(time_stamps_array=epoch_timestamps,
                                                                   frames_timestamps=neuronal_data_timestamps,
                                                                   as_list=True)
            epochs_frames_in_group_dict['Selected_epochs'] = intervals_frames
            print(f"Total of {epoch_timestamps.shape[1]} epochs")
        elif psth_on == 'trials table':
            print(f"Trials build on: ")
            print_info_dict(trial_table)
            epoch_timestamps, time_unit = session_data.get_trials_timestamps_from_table(requirements_dict=trial_table)
            if time_unit == "frames":
                intervals_frames = [(int(epoch_timestamps[0, i]), int(epoch_timestamps[1, i]))
                                    for i in range(epoch_timestamps.shape[1])]
            else:
                intervals_frames = from_timestamps_to_frame_epochs(time_stamps_array=epoch_timestamps,
                                                                   frames_timestamps=neuronal_data_timestamps,
                                                                   as_list=True)
            epochs_frames_in_group_dict['Selected_trials'] = intervals_frames
            print(f"Total of {epoch_timestamps.shape[1]} trials")
        # DEFINE PSTH RANGE #
        # Get CI movie sampling rate
        two_p_sampling_rate = session_data.get_ci_movie_sampling_rate(only_2_photons=True)
        if two_p_sampling_rate is None:
            two_p_sampling_rate = session_data.get_rrs_sampling_rate(keys=roi_response_serie_info)
        # Define PSTH range
        psth_range_in_frames = np.ceil(two_p_sampling_rate * psth_range_in_sec)
        n_psth_frames = int(2*psth_range_in_frames + 1)
        psth_frames_zero_centered = np.arange(n_psth_frames) - psth_range_in_frames
        psth_times_zero_centered = psth_frames_zero_centered / two_p_sampling_rate

        # LOOP ON ALL THE CELLS TO DO TO GENERATE ALL RESULTS#
        if verbose:
            print(f" ")
            print(f"## Building psth on data ##")
        for ind, index_cell_to_analyse in enumerate(cell_indexes_to_do):
            if verbose:
                print(f" ")
                print(f"Starting analysis for cell: {index_cell_to_analyse}")
            if has_raster:
                cell_binary_activity = raster[index_cell_to_analyse, :]
                aligned_raster_by_group_dict = dict()
            if has_traces:
                cell_trace = traces[index_cell_to_analyse, :]

            for group, frames_in_group in epochs_frames_in_group_dict.items():
                n_trials = len(frames_in_group)
                sorted_frames_in_group = sorted(frames_in_group, key=lambda x: x[0])

                if verbose:
                    print(f"On {group} epoch, with total: {n_trials} 'trials' ")

                if has_raster:
                    aligned_raster = np.zeros((n_trials, n_psth_frames), dtype=int)
                    all_trials_raster = dict()
                    all_trials_raster['Time (s)'] = psth_times_zero_centered
                    all_trials_raster['Frames'] = psth_frames_zero_centered

                if has_traces:
                    aligned_traces = np.zeros((n_trials, n_psth_frames), dtype=float)
                    all_trials_traces = dict()
                    all_trials_traces['Time (s)'] = psth_times_zero_centered
                    all_trials_traces['Frames'] = psth_frames_zero_centered

                kept_trials = []
                trials_to_keep = [True for trial in range(n_trials)]
                last_kept_trial = 0
                for trial in range(n_trials):
                    mvt_period = sorted_frames_in_group[trial]
                    if ref_in_epoch == "end":
                        psth_center = mvt_period[1]
                    elif ref_in_epoch == "start":
                        psth_center = mvt_period[0]
                    else:
                        psth_center = int((mvt_period[0] + mvt_period[1]) / 2)

                    if (psth_center - psth_range_in_frames) < 0 or (psth_center + psth_range_in_frames) > n_frames:
                        if verbose:
                            print(f"Trial #{trial} removed (too close of first or last imaging frame)")
                        trials_to_keep[trial] = False
                        continue

                    if filter_consecutive_movements and trial >= 1:
                        if (mvt_period[0] - 2 * psth_range_in_frames) < sorted_frames_in_group[last_kept_trial][0]:
                            if verbose:
                                print(f"Trial #{trial} removed (too close from Trial #{last_kept_trial} "
                                      f"the last kept one (less than {2*psth_range_in_ms / 1000} s))")
                            trials_to_keep[trial] = False
                            continue

                    kept_trials.append(f'Trial_{trial}')
                    last_kept_trial = trial

                    start_frame = int((psth_center - psth_range_in_frames))
                    stop_frame = int(psth_center + psth_range_in_frames)

                    if has_raster:
                        all_trials_raster[f'Trial_{trial}'] = cell_binary_activity[start_frame: stop_frame + 1]
                        aligned_raster[trial] = cell_binary_activity[start_frame: stop_frame + 1]
                    if has_traces:
                        all_trials_traces[f'Trial_{trial}'] = cell_trace[start_frame: stop_frame + 1]
                        aligned_traces[trial] = cell_trace[start_frame: stop_frame + 1]

                if has_raster:
                    aligned_raster = aligned_raster[trials_to_keep, :]
                    sum_activation_raster = np.sum(aligned_raster, axis=0)
                    perc_activation_raster = np.sum(aligned_raster, axis=0) / n_trials
                    aligned_raster_by_group_dict[group] = aligned_raster

                if has_traces:
                    aligned_traces = aligned_traces[trials_to_keep, :]
                    med_trace = np.median(aligned_traces, axis=0)
                    low_perc_trace = np.percentile(aligned_traces, low_percentile, axis=0)
                    high_perc_trace = np.percentile(aligned_traces, high_percentile, axis=0)

                if verbose:
                    print(f"Remaining 'trials': {len(kept_trials)}")

                # GENERATE TABLES
                if verbose:
                    print(f"Generating and saving result: tables and figures")

                # Path
                cell_path_results = os.path.join(path_results, f'cell_{index_cell_to_analyse}', f'{group}')
                if os.path.isdir(cell_path_results) is False:
                    os.makedirs(cell_path_results)

                if has_raster:
                    # rasterplot all trials
                    all_trials_raster_df = pd.DataFrame(all_trials_raster)
                    trials_raster_filename = f"cell_{index_cell_to_analyse}_raster_{group}_trials"
                    path_trials_raster_to_save = os.path.join(f'{cell_path_results}', f'{trials_raster_filename}.xlsx')
                    all_trials_raster_df.to_excel(path_trials_raster_to_save)

                    # sum of raster plot
                    sumury_trials_raster = dict()
                    sumury_trials_raster['Time (s)'] = psth_times_zero_centered
                    sumury_trials_raster['Frames'] = psth_frames_zero_centered
                    sumury_trials_raster['Sum of trial activation'] = sum_activation_raster
                    sumury_trials_raster['% of trial activation'] = perc_activation_raster
                    sumury_trials_raster_df = pd.DataFrame(sumury_trials_raster)
                    sum_raster_filename = f"cell_{index_cell_to_analyse}_raster_sum_{group}_trials"
                    path_sum_raster_to_save = os.path.join(f'{cell_path_results}', f'{sum_raster_filename}.xlsx')
                    sumury_trials_raster_df.to_excel(path_sum_raster_to_save)

                if has_traces:
                    # traces all trials
                    all_trials_traces_df = pd.DataFrame(all_trials_traces)
                    trials_traces_filename = f"cell_{index_cell_to_analyse}_traces_{group}_trials"
                    path_trials_traces_to_save = os.path.join(f'{cell_path_results}', f'{trials_traces_filename}.xlsx')
                    all_trials_traces_df.to_excel(path_trials_traces_to_save)

                    # median and percentiles traces
                    sumury_trials_traces = dict()
                    sumury_trials_traces['Time (s)'] = psth_times_zero_centered
                    sumury_trials_traces['Frames'] = psth_frames_zero_centered
                    sumury_trials_traces['Median trace'] = med_trace
                    sumury_trials_traces[f'Percentile_{low_percentile}'] = low_perc_trace
                    sumury_trials_traces[f'Percentile_{high_percentile}'] = high_perc_trace
                    sumury_trials_traces_df = pd.DataFrame(sumury_trials_traces)
                    sumup_traces_filename = f"cell_{index_cell_to_analyse}_traces_summary_{group}_trials"
                    path_sumup_traces_to_save = os.path.join(f'{cell_path_results}', f'{sumup_traces_filename}.xlsx')
                    sumury_trials_traces_df.to_excel(path_sumup_traces_to_save)

                # DO SOME PLOTS
                if has_traces:
                    # PLOT 1: median and percentiles traces #
                    sumury_trials_traces_df_to_plot = sumury_trials_traces_df.drop(columns=['Frames'])

                    fig, ax = plt.subplots(
                                        ncols=1,
                                        nrows=1,
                                        figsize=(width_fig, height_fig), dpi=dpi)

                    fig_title = f'cell_{index_cell_to_analyse}_{group}_data'
                    colors = [median_color, prctil_color, prctil_color]

                    sumury_trials_traces_df_to_plot.plot(x="Time (s)", y=["Median trace", f'Percentile_{low_percentile}',
                                                         f'Percentile_{high_percentile}'],
                                                         kind='line', ax=ax, color=colors, linewidth=2,
                                                         subplots=False, sharex=None,
                                                         sharey=False, layout=None, figsize=(width_fig, height_fig),
                                                         use_index=True, title=fig_title, grid=None,
                                                         legend=False, style=None, logx=False,
                                                         logy=False, loglog=False, xticks=None, yticks=None, xlim=None,
                                                         ylim=None, rot=None, fontsize=None, table=False,
                                                         yerr=None, xerr=None, secondary_y=False, sort_columns=False)
                    if traces_norm == "df/f":
                        ylabel = "df/f"
                    elif traces_norm == "z-score":
                        ylabel = "z-score"
                    elif traces_norm == "raw":
                        ylabel = "raw fluorescence"

                    ax.set_ylabel(ylabel, fontsize=font_size, labelpad=20, fontweight=fontweight, fontfamily=fontfamily)
                    ax.yaxis.label.set_color(labels_color)
                    ax.xaxis.label.set_color(labels_color)
                    ax.spines['left'].set_color(axis_color)
                    ax.spines['right'].set_color(background_color)
                    ax.spines['bottom'].set_color(axis_color)
                    ax.spines['top'].set_color(background_color)
                    ax.yaxis.set_tick_params(labelsize=font_size)
                    ax.xaxis.set_tick_params(labelsize=font_size)
                    ax.tick_params(axis='y', colors=axis_color)
                    ax.tick_params(axis='x', colors=axis_color)

                    fig.tight_layout()

                    file_name = f'cell_{index_cell_to_analyse}_summary_from_traces_{group}_median_pctl{low_percentile}_' \
                                f'prctl_{high_percentile}'
                    if isinstance(save_formats, str):
                        save_formats = [save_formats]
                    for save_format in save_formats:
                        fig.savefig(f'{cell_path_results}/{file_name}.{save_format}',
                                    format=f"{save_format}",
                                    facecolor=fig.get_facecolor())
                    plt.close()

                    # PLOT 2: all trials traces superimposed #
                    all_trials_traces_df_to_plot = all_trials_traces_df.drop(columns=['Frames'])

                    fig, ax = plt.subplots(
                        ncols=1,
                        nrows=1,
                        figsize=(width_fig, height_fig), dpi=dpi)

                    fig_title = f'cell_{index_cell_to_analyse}_{group}_indiv_trials'
                    trials = kept_trials
                    all_trials_traces_df_to_plot.plot(x="Time (s)", y=trials,
                                                      kind='line', ax=ax, linewidth=1,
                                                      subplots=False, sharex=None,
                                                      sharey=False, layout=None, figsize=(width_fig, height_fig),
                                                      use_index=True, title=fig_title, grid=None,
                                                      legend=False, style=None, logx=False,
                                                      logy=False, loglog=False, xticks=None, yticks=None, xlim=None,
                                                      ylim=None, rot=None, fontsize=None, colormap=colormap, table=False,
                                                      yerr=None, xerr=None, secondary_y=False, sort_columns=False)
                    if traces_norm == "df/f":
                        ylabel = "df/f"
                    elif traces_norm == "z-score":
                        ylabel = "z-score"
                    elif traces_norm == "raw":
                        ylabel = "raw fluorescence"

                    ax.set_ylabel(ylabel, fontsize=font_size, labelpad=20, fontweight=fontweight, fontfamily=fontfamily)
                    ax.yaxis.label.set_color(labels_color)
                    ax.xaxis.label.set_color(labels_color)
                    ax.spines['left'].set_color(axis_color)
                    ax.spines['right'].set_color(background_color)
                    ax.spines['bottom'].set_color(axis_color)
                    ax.spines['top'].set_color(background_color)
                    ax.yaxis.set_tick_params(labelsize=font_size)
                    ax.xaxis.set_tick_params(labelsize=font_size)
                    ax.tick_params(axis='y', colors=axis_color)
                    ax.tick_params(axis='x', colors=axis_color)

                    fig.tight_layout()

                    file_name = f'cell_{index_cell_to_analyse}_all_trials_traces_{group}'
                    if isinstance(save_formats, str):
                        save_formats = [save_formats]
                    for save_format in save_formats:
                        fig.savefig(f'{cell_path_results}/{file_name}.{save_format}',
                                    format=f"{save_format}",
                                    facecolor=fig.get_facecolor())
                    plt.close()

                if has_raster:
                    # PLOT 3: all trials rasterplot #
                    if hide_raster_y_ticks_labels:
                        y_ticks_labels = None
                    else:
                        y_ticks_labels = kept_trials
                    if show_raster and show_traces is True:
                        show_traces = False
                    if show_raster and show_traces is False:
                        show_raster = True
                    if show_traces is True:
                        with_activity_sum = False
                        sum_as_percentage = False

                    if any(np.sum(aligned_raster, axis=0)) is False:
                        with_activity_sum = False
                        sum_as_percentage = False

                    plot_raster(spike_nums=aligned_raster,
                                frame_times=psth_times_zero_centered, traces=None, display_traces=False,
                                bin_size_ms_for_spikes_sum=150,
                                file_name=f'cell_{index_cell_to_analyse}_all_trials_raster_{group}',
                                display_spike_nums=show_raster,
                                with_timestamp_in_file_name=False,
                                path_results=f'{cell_path_results}',
                                save_raster=True,
                                show_raster=False,
                                dpi=dpi,
                                show_sum_spikes_as_percentage=sum_as_percentage,
                                spike_shape=spike_shape,
                                spike_shape_size=spike_size,
                                without_ticks=not with_ticks,
                                without_activity_sum=not with_activity_sum,
                                cell_spikes_color=spikes_color,
                                figure_background_color=background_color,
                                raster_face_color=background_color,
                                activity_sum_plot_color=activity_sum_plot_color,
                                activity_sum_face_color=background_color,
                                axes_label_color=spikes_color,
                                hide_x_ticks_labels=hide_x_ticks_labels,
                                hide_raster_y_ticks_labels=hide_raster_y_ticks_labels,
                                raster_y_axis_label="Trial #",
                                raster_y_axis_label_size=font_size,
                                y_ticks_labels=y_ticks_labels,
                                y_ticks_labels_size=font_size,
                                x_ticks_labels_size=font_size,
                                y_ticks_labels_color=y_ticks_labels_color,
                                x_ticks_labels_color=x_ticks_labels_color,
                                size_fig=(width_fig, height_fig),
                                save_formats=save_formats)

            if do_surrogates is False:
                self.update_progressbar(time_started=self.analysis_start_time, increment_value=100/(n_cells_to_do + 1))

            if do_surrogates:
                significant_prctile = 100 - alpha
                if verbose:
                    print(f" ")
                    print(f"## Building psth from {n_surrogates} surrogate data ##")

                for group, frames_in_group in epochs_frames_in_group_dict.items():
                    n_trials = len(frames_in_group)
                    sorted_frames_in_group = sorted(frames_in_group, key=lambda x: x[0])

                    if verbose:
                        print(f" ")
                        print(f"On {group} epoch, with total: {n_trials} 'trials' ")

                    # Matrices
                    if has_raster:
                        all_surrogates_raster = np.zeros((n_trials, n_psth_frames, n_surrogates), dtype=int)
                    if has_traces:
                        all_surrogates_traces = np.zeros((n_trials, n_psth_frames, n_surrogates), dtype=float)

                    # Dictionaries for future pd.Dataframe
                    if has_raster:
                        all_trials_surrogate_raster = dict()
                        all_trials_surrogate_raster['Time (s)'] = psth_times_zero_centered
                        all_trials_surrogate_raster['Frames'] = psth_frames_zero_centered
                    if has_traces:
                        all_trials_surrogate_traces = dict()
                        all_trials_surrogate_traces['Time (s)'] = psth_times_zero_centered
                        all_trials_surrogate_traces['Frames'] = psth_frames_zero_centered

                    for surrogate in range(n_surrogates):
                        if verbose:
                            print(f"Ongoing for surrogate #{surrogate}")

                        roll_value = np.random.randint(n_frames, size=1)[0]

                        if has_raster:
                            rolled_cell_binary_activity = np.roll(cell_binary_activity, shift=roll_value)
                        if has_traces:
                            rolled_cell_trace = np.roll(cell_trace, shift=roll_value)

                        kept_surrogate_trials = []
                        surrogate_trials_to_keep = [True for k in range(n_trials)]
                        last_kept_surrogate_trial = 0
                        for trial in range(n_trials):
                            mvt_period = sorted_frames_in_group[trial]
                            if ref_in_epoch == "end":
                                psth_center = mvt_period[1]
                            elif ref_in_epoch == "start":
                                psth_center = mvt_period[0]
                            else:
                                psth_center = int((mvt_period[0] + mvt_period[1]) / 2)

                            if (psth_center - psth_range_in_frames) < 0 or \
                                    (psth_center + psth_range_in_frames) > n_frames:
                                surrogate_trials_to_keep[trial] = False
                                continue

                            if filter_consecutive_movements and trial >= 1:
                                if (mvt_period[0] - 2 * psth_range_in_frames) < sorted_frames_in_group[last_kept_surrogate_trial][0]:
                                    surrogate_trials_to_keep[trial] = False
                                    continue

                            kept_surrogate_trials.append(f'Trial_{trial}')
                            last_kept_surrogate_trial = trial

                            start_frame = int((psth_center - psth_range_in_frames))
                            stop_frame = int(psth_center + psth_range_in_frames)

                            if has_raster:
                                all_surrogates_raster[trial, :, surrogate] = \
                                    rolled_cell_binary_activity[start_frame: stop_frame + 1]
                            if has_traces:
                                all_surrogates_traces[trial, :, surrogate] = \
                                    rolled_cell_trace[start_frame: stop_frame + 1]
                            if has_raster:
                                all_trials_surrogate_raster[f'Surrogate_{surrogate}_Trial_{trial}'] = \
                                    rolled_cell_binary_activity[start_frame: stop_frame + 1]
                            if has_traces:
                                all_trials_surrogate_traces[f'Surrogate_{surrogate}_Trial_{trial}'] = \
                                    rolled_cell_trace[start_frame: stop_frame + 1]
                    if has_raster:
                        all_surrogates_raster = all_surrogates_raster[surrogate_trials_to_keep, :, :]
                    if has_traces:
                        all_surrogates_traces = all_surrogates_traces[surrogate_trials_to_keep, :, :]

                    # raster:
                    if has_raster:
                        all_surrogate_raster_two_d = np.sum(all_surrogates_raster, axis=0)
                        all_surrogate_raster_one_d = np.nanpercentile(all_surrogate_raster_two_d, significant_prctile, axis=1)

                    # traces
                    if has_traces:
                        all_surrogate_traces_two_d = np.nanmedian(all_surrogates_traces, axis=0)
                        all_surrogate_traces_one_d = np.nanpercentile(all_surrogate_traces_two_d, significant_prctile, axis=1)

                    # Table results
                    if verbose:
                        print(f"Generate and save surrogate tables")

                    # raster
                    if has_raster:
                        all_trials_surrogate_raster_df = pd.DataFrame(all_trials_surrogate_raster)
                        trials_surrogate_raster_filename = f"cell_{index_cell_to_analyse}_surrogate_rasters_{group}"
                        path_trials_surrogate_raster_to_save = os.path.join(f'{cell_path_results}',
                                                                            f'{trials_surrogate_raster_filename}.xlsx')
                        all_trials_surrogate_raster_df.to_excel(path_trials_surrogate_raster_to_save)

                    # traces
                    if has_traces:
                        all_trials_surrogate_traces_df = pd.DataFrame(all_trials_surrogate_traces)
                        trials_surrogate_traces_filename = f"cell_{index_cell_to_analyse}_surrogates_traces_{group}"
                        path_trials_surro_traces_to_save = os.path.join(f'{cell_path_results}',
                                                                        f'{trials_surrogate_traces_filename}.xlsx')
                        all_trials_surrogate_traces_df.to_excel(path_trials_surro_traces_to_save)

                        sumury_trials_rnd_traces = dict()
                        sumury_trials_rnd_traces['Time (s)'] = psth_times_zero_centered
                        sumury_trials_rnd_traces['Frames'] = psth_frames_zero_centered
                        sumury_trials_rnd_traces[f'Median from surrogates'] = all_surrogate_traces_one_d
                        sumury_trials_rnd_traces_df = pd.DataFrame(sumury_trials_rnd_traces)
                        sumary_rnd_traces_filename = f"cell_{index_cell_to_analyse}_median_surrogate_{group}"
                        path_sumary_rnd_traces_to_save = os.path.join(f'{cell_path_results}',
                                                                      f'{sumary_rnd_traces_filename}.xlsx')
                        sumury_trials_rnd_traces_df.to_excel(path_sumary_rnd_traces_to_save)

                    # DO SOME PLOTS
                    if verbose:
                        print(f"Do some plots")
                    # pick one surrogate for illustration:
                    selected_surrogate = np.random.randint(n_surrogates, size=1)
                    if has_traces:
                        # PLOT 1: median trace from all surrogates #
                        fig, ax = plt.subplots(
                            ncols=1,
                            nrows=1,
                            figsize=(width_fig, height_fig), dpi=dpi)

                        fig_title = f'cell_{index_cell_to_analyse}_{group}_surrogate'

                        sumury_trials_rnd_traces_df.plot(x="Time (s)",
                                                         y="Median from surrogates",
                                                         kind='line', ax=ax, color=rnd_trace_color, linewidth=2,
                                                         subplots=False, sharex=None,
                                                         sharey=False, layout=None, figsize=(width_fig, height_fig),
                                                         use_index=True, title=fig_title, grid=None,
                                                         legend=False, style=None, logx=False,
                                                         logy=False, loglog=False, xticks=None, yticks=None, xlim=None,
                                                         ylim=None, rot=None, fontsize=None, table=False,
                                                         yerr=None, xerr=None, secondary_y=False, sort_columns=False)
                        if traces_norm == "df/f":
                            ylabel = "df/f"
                        elif traces_norm == "z-score":
                            ylabel = "z-score"
                        elif traces_norm == "raw":
                            ylabel = "raw fluorescence"

                        ax.set_ylabel(ylabel, fontsize=font_size, labelpad=20, fontweight=fontweight, fontfamily=fontfamily)
                        ax.yaxis.label.set_color(labels_color)
                        ax.xaxis.label.set_color(labels_color)
                        ax.spines['left'].set_color(axis_color)
                        ax.spines['right'].set_color(background_color)
                        ax.spines['bottom'].set_color(axis_color)
                        ax.spines['top'].set_color(background_color)
                        ax.yaxis.set_tick_params(labelsize=font_size)
                        ax.xaxis.set_tick_params(labelsize=font_size)
                        ax.tick_params(axis='y', colors=axis_color)
                        ax.tick_params(axis='x', colors=axis_color)

                        fig.tight_layout()

                        file_name = f'cell_{index_cell_to_analyse}_median_from_rnd_traces_{group}'
                        if isinstance(save_formats, str):
                            save_formats = [save_formats]
                        for save_format in save_formats:
                            fig.savefig(f'{cell_path_results}/{file_name}.{save_format}',
                                        format=f"{save_format}",
                                        facecolor=fig.get_facecolor())
                        plt.close()

                        # PLOT 2: median/prctiles data + median trace from all surrogates #
                        # get previous data
                        cell_path_results = os.path.join(path_results, f'cell_{index_cell_to_analyse}', f'{group}')
                        data_name = f"cell_{index_cell_to_analyse}_traces_summary_{group}_trials.xlsx"
                        full_path_to_load = os.path.join(cell_path_results, data_name)
                        trace_summury_df = pd.read_excel(full_path_to_load)

                        to_plot = dict()
                        to_plot['Time (s)'] = psth_times_zero_centered
                        to_plot['Median trace'] = trace_summury_df['Median trace']
                        to_plot[f'Percentile_{low_percentile}'] = trace_summury_df[f'Percentile_{low_percentile}']
                        to_plot[f'Percentile_{high_percentile}'] = trace_summury_df[f'Percentile_{high_percentile}']
                        to_plot['Surrogate results'] = sumury_trials_rnd_traces[f'Median from surrogates']
                        df_to_plot = pd.DataFrame(to_plot)
                        fig, ax = plt.subplots(
                            ncols=1,
                            nrows=1,
                            figsize=(width_fig, height_fig), dpi=dpi)

                        fig_title = f'cell_{index_cell_to_analyse}_{group}_data_and_surrogate'
                        with_surrogates_colors = [median_color, prctil_color, prctil_color, rnd_trace_color]

                        df_to_plot.plot(x="Time (s)",
                                        y=['Median trace', f'Percentile_{low_percentile}', f'Percentile_{high_percentile}',
                                           "Surrogate results"],
                                        kind='line', ax=ax, color=with_surrogates_colors, linewidth=2,
                                        subplots=False, sharex=None,
                                        sharey=False, layout=None, figsize=(width_fig, height_fig),
                                        use_index=True, title=fig_title, grid=None,
                                        legend=False, style=None, logx=False,
                                        logy=False, loglog=False, xticks=None, yticks=None, xlim=None,
                                        ylim=None, rot=None, fontsize=None, table=False,
                                        yerr=None, xerr=None, secondary_y=False, sort_columns=False)
                        if traces_norm == "df/f":
                            ylabel = "df/f"
                        elif traces_norm == "z-score":
                            ylabel = "z-score"
                        elif traces_norm == "raw":
                            ylabel = "raw fluorescence"

                        ax.set_ylabel(ylabel, fontsize=font_size, labelpad=20, fontweight=fontweight, fontfamily=fontfamily)
                        ax.yaxis.label.set_color(labels_color)
                        ax.xaxis.label.set_color(labels_color)
                        ax.spines['left'].set_color(axis_color)
                        ax.spines['right'].set_color(background_color)
                        ax.spines['bottom'].set_color(axis_color)
                        ax.spines['top'].set_color(background_color)
                        ax.yaxis.set_tick_params(labelsize=font_size)
                        ax.xaxis.set_tick_params(labelsize=font_size)
                        ax.tick_params(axis='y', colors=axis_color)
                        ax.tick_params(axis='x', colors=axis_color)

                        fig.tight_layout()

                        file_name = f'cell_{index_cell_to_analyse}_data_with_median_from_rnd_traces_{group}'
                        if isinstance(save_formats, str):
                            save_formats = [save_formats]
                        for save_format in save_formats:
                            fig.savefig(f'{cell_path_results}/{file_name}.{save_format}',
                                        format=f"{save_format}",
                                        facecolor=fig.get_facecolor())
                        plt.close()

                        # PLOT 3: all trials traces superimposed from one random surrogate #
                        all_trials_surrogate_traces_df_to_plot = all_trials_surrogate_traces_df.drop(columns=['Frames'])

                        fig, ax = plt.subplots(
                            ncols=1,
                            nrows=1,
                            figsize=(width_fig, height_fig), dpi=dpi)

                        fig_title = f'cell_{index_cell_to_analyse}_{group}_indiv_trials_surrogate_{selected_surrogate[0]}'
                        rnd_trials = ["no_name" for k in range(len(kept_surrogate_trials))]
                        for trial in range(len(kept_surrogate_trials)):
                            name = f'Surrogate_{selected_surrogate[0]}'
                            name = name + '_' + kept_surrogate_trials[trial]
                            rnd_trials[trial] = name
                        all_trials_surrogate_traces_df_to_plot.plot(x="Time (s)", y=rnd_trials,
                                                                    kind='line', ax=ax, linewidth=1,
                                                                    subplots=False, sharex=None,
                                                                    sharey=False, layout=None, figsize=(width_fig, height_fig),
                                                                    use_index=True, title=fig_title, grid=None,
                                                                    legend=False, style=None, logx=False,
                                                                    logy=False, loglog=False, xticks=None, yticks=None, xlim=None,
                                                                    ylim=None, rot=None, fontsize=None, colormap=colormap,
                                                                    table=False,
                                                                    yerr=None, xerr=None, secondary_y=False, sort_columns=False)
                        if traces_norm == "df/f":
                            ylabel = "df/f"
                        elif traces_norm == "z-score":
                            ylabel = "z-score"
                        elif traces_norm == "raw":
                            ylabel = "raw fluorescence"

                        ax.set_ylabel(ylabel, fontsize=font_size, labelpad=20, fontweight=fontweight, fontfamily=fontfamily)
                        ax.yaxis.label.set_color(labels_color)
                        ax.xaxis.label.set_color(labels_color)
                        ax.spines['left'].set_color(axis_color)
                        ax.spines['right'].set_color(background_color)
                        ax.spines['bottom'].set_color(axis_color)
                        ax.spines['top'].set_color(background_color)
                        ax.yaxis.set_tick_params(labelsize=font_size)
                        ax.xaxis.set_tick_params(labelsize=font_size)
                        ax.tick_params(axis='y', colors=axis_color)
                        ax.tick_params(axis='x', colors=axis_color)

                        fig.tight_layout()

                        file_name = f'cell_{index_cell_to_analyse}_all_trials_traces_{group}_surrogate_' \
                                    f'{selected_surrogate[0]}'
                        if isinstance(save_formats, str):
                            save_formats = [save_formats]
                        for save_format in save_formats:
                            fig.savefig(f'{cell_path_results}/{file_name}.{save_format}',
                                        format=f"{save_format}",
                                        facecolor=fig.get_facecolor())
                        plt.close()

                    if has_raster:
                        # PLOT 4: raster from one random surrogate #
                        if hide_raster_y_ticks_labels:
                            y_ticks_labels = None
                        else:
                            y_ticks_labels = kept_surrogate_trials

                        plot_raster(spike_nums=all_surrogates_raster[:, :, selected_surrogate],
                                    frame_times=psth_times_zero_centered,
                                    traces=None,
                                    display_traces=False,
                                    bin_size_ms_for_spikes_sum=150,
                                    file_name=f'cell_{index_cell_to_analyse}_all_trials_raster_{group}_'
                                              f'surrogate_{selected_surrogate[0]}',
                                    display_spike_nums=show_raster,
                                    with_timestamp_in_file_name=False,
                                    path_results=f'{cell_path_results}',
                                    save_raster=True,
                                    show_raster=False,
                                    dpi=dpi,
                                    show_sum_spikes_as_percentage=sum_as_percentage,
                                    spike_shape=spike_shape,
                                    spike_shape_size=spike_size,
                                    without_ticks=not with_ticks,
                                    without_activity_sum=not with_activity_sum,
                                    cell_spikes_color=spikes_color,
                                    figure_background_color=background_color,
                                    raster_face_color=background_color,
                                    activity_sum_plot_color=activity_sum_plot_color,
                                    activity_sum_face_color=background_color,
                                    axes_label_color=spikes_color,
                                    hide_x_ticks_labels=hide_x_ticks_labels,
                                    hide_raster_y_ticks_labels=hide_raster_y_ticks_labels,
                                    raster_y_axis_label="Trial #",
                                    raster_y_axis_label_size=font_size,
                                    y_ticks_labels=y_ticks_labels,
                                    y_ticks_labels_size=font_size,
                                    x_ticks_labels_size=font_size,
                                    y_ticks_labels_color=y_ticks_labels_color,
                                    x_ticks_labels_color=x_ticks_labels_color,
                                    size_fig=(width_fig, height_fig),
                                    save_formats=save_formats)

                        # PLOT 5: sum of raster for all surrogates #
                        if hide_raster_y_ticks_labels:
                            y_ticks_labels = None
                        else:
                            y_ticks_labels = np.arange(n_surrogates)
                        if sum_as_percentage:
                            ylabel_name = "Percentage of active cells in each surrogate"
                        else:
                            ylabel_name = "Sum of active cells in each surrogate"

                        plot_raster(spike_nums=None,
                                    frame_times=psth_times_zero_centered,
                                    traces=np.transpose(all_surrogate_raster_two_d),
                                    display_traces=True,
                                    bin_size_ms_for_spikes_sum=150,
                                    file_name=f'cell_{index_cell_to_analyse}_all_surrogate_raster_{group}',
                                    display_spike_nums=False,
                                    with_timestamp_in_file_name=False,
                                    path_results=f'{cell_path_results}',
                                    save_raster=True,
                                    show_raster=False,
                                    dpi=dpi,
                                    show_sum_spikes_as_percentage=sum_as_percentage,
                                    spike_shape=spike_shape,
                                    spike_shape_size=spike_size,
                                    without_ticks=not with_ticks,
                                    without_activity_sum=True,
                                    cell_spikes_color=spikes_color,
                                    figure_background_color=background_color,
                                    raster_face_color=background_color,
                                    activity_sum_plot_color=activity_sum_plot_color,
                                    activity_sum_face_color=background_color,
                                    axes_label_color=spikes_color,
                                    hide_x_ticks_labels=hide_x_ticks_labels,
                                    hide_raster_y_ticks_labels=True,
                                    raster_y_axis_label=ylabel_name,
                                    raster_y_axis_label_size=font_size,
                                    y_ticks_labels=y_ticks_labels,
                                    y_ticks_labels_size=font_size,
                                    x_ticks_labels_size=font_size,
                                    y_ticks_labels_color=y_ticks_labels_color,
                                    x_ticks_labels_color=x_ticks_labels_color,
                                    size_fig=(width_fig, height_fig),
                                    save_formats=save_formats)

                        # PLOT 6: raster from data and sum from surrogate data on activity sum #
                        aligned_data_raster = aligned_raster_by_group_dict.get(group)
                        if hide_raster_y_ticks_labels:
                            y_ticks_labels = None
                        else:
                            y_ticks_labels = kept_surrogate_trials
                        if show_raster and show_traces is True:
                            show_traces = False
                        if show_raster and show_traces is False:
                            show_raster = True
                        if show_traces is True:
                            with_activity_sum = False
                            sum_as_percentage = False

                        if any(np.sum(aligned_data_raster, axis=0)) is False:
                            with_activity_sum = False
                            sum_as_percentage = False
                        plot_raster(spike_nums=aligned_data_raster,
                                    frame_times=psth_times_zero_centered, traces=None, display_traces=False,
                                    bin_size_ms_for_spikes_sum=150,
                                    file_name=f'cell_{index_cell_to_analyse}_all_trials_raster_{group}_and_sum_surrogate',
                                    display_spike_nums=True,
                                    with_timestamp_in_file_name=False,
                                    path_results=f'{cell_path_results}',
                                    save_raster=True,
                                    show_raster=False,
                                    dpi=dpi,
                                    show_sum_spikes_as_percentage=sum_as_percentage,
                                    spike_shape=spike_shape,
                                    spike_shape_size=spike_size,
                                    without_ticks=not with_ticks,
                                    without_activity_sum=not with_activity_sum,
                                    activity_threshold=all_surrogate_raster_one_d,
                                    cell_spikes_color=spikes_color,
                                    figure_background_color=background_color,
                                    raster_face_color=background_color,
                                    activity_sum_plot_color=activity_sum_plot_color,
                                    activity_sum_face_color=background_color,
                                    axes_label_color=spikes_color,
                                    hide_x_ticks_labels=hide_x_ticks_labels,
                                    hide_raster_y_ticks_labels=hide_raster_y_ticks_labels,
                                    raster_y_axis_label="Trial #",
                                    raster_y_axis_label_size=font_size,
                                    y_ticks_labels=y_ticks_labels,
                                    y_ticks_labels_size=font_size,
                                    x_ticks_labels_size=font_size,
                                    y_ticks_labels_color=y_ticks_labels_color,
                                    x_ticks_labels_color=x_ticks_labels_color,
                                    size_fig=(width_fig, height_fig),
                                    save_formats=save_formats)

            self.update_progressbar(time_started=self.analysis_start_time, increment_value=100/(n_cells_to_do + 1))

        if verbose:
            print(f" ")
            print(f"ANALYSIS DONE, OPEN RESULT FOLDER")


