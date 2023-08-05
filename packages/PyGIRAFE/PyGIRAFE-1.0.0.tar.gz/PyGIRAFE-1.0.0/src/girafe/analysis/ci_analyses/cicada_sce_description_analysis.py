from cicada.analysis.cicada_analysis import CicadaAnalysis
from time import time
from datetime import datetime
from cicada.utils.misc import get_continous_time_periods, print_info_dict
from cicada.utils.misc import give_unique_id_to_each_transient_of_raster_dur
from cicada.utils.misc import from_timestamps_to_frame_epochs
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.signal as sci_si
from cicada.utils.sce_stats_utils import get_sce_threshold
from cicada.utils.stats import multiple_comparison_one_factor_effect
import pandas as pd
import os


class CicadaSceDescriptionAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        long_description = '<p align="center"><b>Describe Synchronous Calcium Events (SCEs)</b></p><br>'
        long_description = long_description + 'First detect SCEs using the raster. SCEs are defined as frames with more' \
                                              ' co-active cells than expected by chance (same as Modol 2020).<br><br>'
        long_description = long_description + 'SCE definition: <br><br>'
        long_description = long_description + ' - Peak method: SCE are defined as a single frame (peak of synchrony)<br><br>'
        long_description = long_description + ' - All frame method: SCE are defined as all continuous frame periods ' \
                                              'with more active cells than the statistical threshold. <br><br>'
        long_description = long_description + 'Return: <br><br>'
        long_description = long_description + '- a cell table (each line is a cell) containing information on the cell' \
                                              ' and the ratio of its event in SCE over total events.<br><br>'
        long_description = long_description + '- a SCE table (each line is a SCE) containing information on the SCE:' \
                                              ' the proportion of cell recruited.<br><br>'
        long_description = long_description + '- a SCE table (each line is a SCE) containing information on the SCE:' \
                                              ' the mean calcium event amplitude of the cells involved.<br><br>'
        long_description = long_description + 'Data are saved in several csv and xlxs files. Customized categorical plots' \
                                              ' can be done'
        CicadaAnalysis.__init__(self, name="SCE description from raster", family_id="Descriptive statistics",
                                short_description="Basic SCE statistics (from raster-plot)",
                                long_description=long_description,
                                config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaSceDescriptionAnalysis(config_handler=self.config_handler)
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
                if 'raster' in rrs_name.lower():
                    raster_in_rrs_keys = True
                    return True
                else:
                    continue
            if raster_in_rrs_keys is False:
                self.invalid_data_help = f"'SCEs descriptions' is so far based on inferred raster plot, " \
                                         f"not implemented on traces yet (will be)"
                return False

        return True

    def set_arguments_for_gui(self):
        """

        Returns:

        """
        CicadaAnalysis.set_arguments_for_gui(self)

        self.add_roi_response_series_arg_for_gui(short_description="Neuronal activity to use: select a raster-plot",
                                                 long_description=None)

        threshold_methods = ["Surrogate", "Arbitrary percentage", "Arbitrary number"]
        self.add_choices_arg_for_gui(arg_name="thr_method", choices=threshold_methods,
                                     default_value="Surrogate", short_description="Method used to get SCEs threshold",
                                     long_description="Define the method to obtain the minimal number of cell in a SCE",
                                     multiple_choices=False,
                                     family_widget="figure_config_thr_method_to_use")

        self.add_int_values_arg_for_gui(arg_name="arbitrary_perc_threshold", min_value=10, max_value=200,
                                        short_description="Arbitrary threshold (in proportion of cell) "
                                                          "in SCE (in 1/1000)",
                                        default_value=50, family_widget="figure_config_thr_method_to_use")

        self.add_int_values_arg_for_gui(arg_name="arbitrary_numb_threshold", min_value=1, max_value=1500,
                                        short_description="Arbitrary threshold (in absolute number of cell) in SCE",
                                        default_value=25, family_widget="figure_config_thr_method_to_use")

        self.add_int_values_arg_for_gui(arg_name="n_surrogates", min_value=10, max_value=10000,
                                        short_description="Number of surrogates raster to compute SCE threshold",
                                        default_value=100, family_widget="figure_config_thr_method_to_use")

        self.add_int_values_arg_for_gui(arg_name="percentile", min_value=95, max_value=100,
                                        short_description="Percentile of surrogate distribution "
                                                          "to compute SCE threshold",
                                        default_value=99, family_widget="figure_config_thr_method_to_use")

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

        self.add_bool_option_for_gui(arg_name="do_single_epoch_analysis", true_by_default=False,
                                     short_description="Do (spikes in sce / total spikes) epoch by epoch",
                                     family_widget="epochs_for_stats")

        methods = ["Peaks", "All frames"]
        self.add_choices_arg_for_gui(arg_name="method", choices=methods,
                                     default_value="peaks", short_description="Method used to detect SCEs",
                                     long_description="If 'Peaks': find SCEs using find-peaks with parameters below, "
                                                      "SCE will be define by a single frame (the 'peak' of synchrony). "
                                                      "If 'All frames': define SCEs as all continuous frame periods"
                                                      " with more active cells than the statistical threshold.",
                                     multiple_choices=False,
                                     family_widget="figure_config_method_to_use")

        self.add_int_values_arg_for_gui(arg_name="min_sce_distance", min_value=1, max_value=10,
                                        short_description="Minimal number of frames between 2 SCEs",
                                        default_value=5, family_widget="figure_config_findpeaks")

        time_unity = ["seconds", "minutes"]
        self.add_choices_arg_for_gui(arg_name="time_unit", choices=time_unity,
                                     default_value="minutes", short_description="Time unit for SCE frequency",
                                     multiple_choices=False,
                                     family_widget="figure_config_time")

        self.add_bool_option_for_gui(arg_name="do_stats", true_by_default=False,
                                     short_description="Try statistical tests",
                                     family_widget="figure_config_stats")

        self.add_int_values_arg_for_gui(arg_name="pvalue", min_value=1, max_value=5,
                                        short_description="p-value (%) for statistical test",
                                        default_value=5, family_widget="figure_config_stats")

        self.add_bool_option_for_gui(arg_name="save_table", true_by_default=True,
                                     short_description="Save results in tables",
                                     family_widget="figure_config_saving")

        self.add_bool_option_for_gui(arg_name="save_figure", true_by_default=True,
                                     short_description="Save figures",
                                     family_widget="figure_config_saving")

        cell_types = []
        for session_index, session_data in enumerate(self._data_to_analyse):
            cell_types.extend(session_data.get_all_cell_types())
            cell_types = list(np.unique(cell_types))
        cell_types.insert(0, "all_cells")
        self.add_choices_arg_for_gui(arg_name="cell_to_use", choices=cell_types,
                                     default_value="all_cells",
                                     short_description="Cell type to plots on 'in-SCE spike ratio' figure",
                                     multiple_choices=False,
                                     family_widget="figure_ratio_config_representation")

        self.add_bool_option_for_gui(arg_name="do_not_show_unclassified", true_by_default=False,
                                     short_description="Do not include 'Unclassified' as a cell-type",
                                     family_widget="figure_ratio_config_representation")

        representations = ["strip", "swarm", "violin", "box", "bar", "boxen"]
        self.add_choices_arg_for_gui(arg_name="representation_ratio", choices=representations,
                                     default_value="box",
                                     short_description="Plot to use for 'in-SCE spike ratio' figure",
                                     multiple_choices=False,
                                     family_widget="figure_ratio_config_representation")

        x_ax = ["Age", "SubjectID", "Session", "Celltype", "Weight"]
        self.add_choices_arg_for_gui(arg_name="x_axis_ratio", choices=x_ax,
                                     default_value="Age", short_description="Variable to use for x axis groups",
                                     multiple_choices=False,
                                     family_widget="figure_ratio_config_representation")

        possible_hues = ["Age", "SubjectID", "Session", "Celltype", "None"]
        self.add_choices_arg_for_gui(arg_name="hue_ratio", choices=possible_hues,
                                     default_value="None",
                                     short_description="Variable to use for x axis sub-groups",
                                     multiple_choices=False,
                                     family_widget="figure_ratio_config_representation")

        palettes = ["muted", "deep", "pastel", "Blues"]
        self.add_choices_arg_for_gui(arg_name="palettes_ratio", choices=palettes,
                                     default_value="muted", short_description="Color palette for subgroups",
                                     long_description="In that case figure facecolor and figure edgecolor are useless",
                                     multiple_choices=False,
                                     family_widget="figure_ratio_config_representation")

        representations = ["strip", "swarm", "violin", "box", "bar", "boxen"]
        self.add_choices_arg_for_gui(arg_name="representation_recruitment", choices=representations,
                                     default_value="box", short_description="Plot to use for 'SCE recruitment' figure",
                                     multiple_choices=False,
                                     family_widget="figure_recruitment_config_representation")

        x_ax = ["Age", "SubjectID", "Session", "Weight", "SCE_epoch"]
        self.add_choices_arg_for_gui(arg_name="x_axis_recruitment", choices=x_ax,
                                     default_value="Age", short_description="Variable to use for x axis groups",
                                     multiple_choices=False,
                                     family_widget="figure_recruitment_config_representation")

        possible_hues = ["Age", "SubjectID", "Session", "SCE_epoch", "None"]
        self.add_choices_arg_for_gui(arg_name="hue_recruitment", choices=possible_hues,
                                     default_value="None",
                                     short_description="Variable to use for x axis sub-groups",
                                     multiple_choices=False,
                                     family_widget="figure_recruitment_config_representation")

        palettes = ["muted", "deep", "pastel", "Blues"]
        self.add_choices_arg_for_gui(arg_name="palettes_recruitment", choices=palettes,
                                     default_value="muted", short_description="Color palette for subgroups",
                                     long_description="In that case figure facecolor and figure edgecolor are useless",
                                     multiple_choices=False,
                                     family_widget="figure_recruitment_config_representation")

        representations = ["strip", "swarm", "violin", "box", "bar", "boxen"]
        self.add_choices_arg_for_gui(arg_name="representation_amplitude", choices=representations,
                                     default_value="box",
                                     short_description="Plot to use for 'SCE transient amplitude' figure",
                                     multiple_choices=False,
                                     family_widget="figure_amplitude_config_representation")

        x_ax = ["Age", "SubjectID", "Session", "Weight", "SCE_epoch"]
        self.add_choices_arg_for_gui(arg_name="x_axis_amplitude", choices=x_ax,
                                     default_value="Age", short_description="Variable to use for x axis groups",
                                     multiple_choices=False,
                                     family_widget="figure_amplitude_config_representation")

        possible_hues = ["Age", "SubjectID", "Session", "SCE_epoch", "None"]
        self.add_choices_arg_for_gui(arg_name="hue_amplitude", choices=possible_hues,
                                     default_value="None",
                                     short_description="Variable to use for x axis sub-groups",
                                     multiple_choices=False,
                                     family_widget="figure_amplitude_config_representation")

        palettes = ["muted", "deep", "pastel", "Blues"]
        self.add_choices_arg_for_gui(arg_name="palettes_amplitude", choices=palettes,
                                     default_value="muted", short_description="Color palette for subgroups",
                                     long_description="In that case figure facecolor and figure edgecolor are useless",
                                     multiple_choices=False,
                                     family_widget="figure_amplitude_config_representation")

        self.add_image_format_package_for_gui()

        self.add_color_arg_for_gui(arg_name="background_color", default_value=(0, 0, 0, 1.),
                                   short_description="background color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="fig_facecolor", default_value=(1, 1, 1, 1.),
                                   short_description="Figure face color",
                                   long_description="Useless if a 'hue' is specified, in that case use 'palette'",
                                   family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="axis_color", default_value=(1, 1, 1, 1.),
                                   short_description="Axes color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="axes_label_color", default_value=(1, 1, 1, 1.),
                                   short_description="Axes label color",
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

        self.add_int_values_arg_for_gui(arg_name="axis_label_size", min_value=1, max_value=100,
                                        short_description="Font size",
                                        default_value=18, family_widget="figure_config_label")

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

        epochs_to_use = kwargs.get("epochs_to_use")

        n_surrogates = kwargs.get("n_surrogates")

        percentile = kwargs.get("percentile")

        thr_method = kwargs.get("thr_method")

        arbitrary_percentage_threshold = kwargs.get("arbitrary_perc_threshold")

        arbitrary_number_threshold = kwargs.get("arbitrary_numb_threshold")

        method = kwargs.get("method")

        min_sce_distance = kwargs.get("min_sce_distance")

        time_unit = kwargs.get("time_unit")

        epochs_names = kwargs.get("epochs_names")

        do_single_epoch_analysis = kwargs.get("do_single_epoch_analysis")

        sces_epoch = kwargs.get("epochs_names_sce_threshold")

        do_stats = kwargs.get("do_stats")

        pvalue = kwargs.get("pvalue")
        pvalue = pvalue / 100

        verbose = kwargs.get("verbose", True)

        cell_to_use = kwargs.get("cell_to_use")

        do_not_show_unclassified = kwargs.get("do_not_show_unclassified")

        x_axis_name_ratio = kwargs.get("x_axis_ratio")

        kind_ratio = kwargs.get("representation_ratio")

        hue_ratio = kwargs.get("hue_ratio")

        palette_ratio = kwargs.get("palettes_ratio")

        x_axis_name_recruitment = kwargs.get("x_axis_recruitment")

        kind_recruitment = kwargs.get("representation_recruitment")

        hue_recruitment = kwargs.get("hue_recruitment")

        palette_recruitment = kwargs.get("palettes_recruitment")

        x_axis_name_amplitude = kwargs.get("x_axis_amplitude")

        kind_amplitude = kwargs.get("representation_amplitude")

        hue_amplitude = kwargs.get("hue_amplitude")

        palette_amplitude = kwargs.get("palettes_amplitude")

        background_color = kwargs.get("background_color")

        fig_facecolor = kwargs.get("fig_facecolor")

        labels_color = kwargs.get("axes_label_color")

        axis_color = kwargs.get("axis_color")

        font_size = kwargs.get("axis_label_size", 20)

        fontweight = kwargs.get("fontweight")

        fontfamily = kwargs.get("font_type")

        # image package format
        save_formats = kwargs["save_formats"]
        if save_formats is None:
            save_formats = "pdf"

        save_figure = True

        path_results = self.get_results_path()

        save_table = kwargs.get("save_table")

        dpi = kwargs.get("dpi", 100)

        width_fig = kwargs.get("width_fig")

        height_fig = kwargs.get("height_fig")

        with_timestamp_in_file_name = kwargs.get("with_timestamp_in_file_name", True)

        start_time = time()
        if verbose:
            print("SCE description: coming soon...")
        n_sessions = len(self._data_to_analyse)

        if verbose:
            print(f"{n_sessions} sessions to analyse")

        gobal_spike_ratio_data_table = pd.DataFrame()
        gobal_sce_recruitment_data_table = pd.DataFrame()
        global_sce_transient_amplitude_data_table = pd.DataFrame()
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

            # Get Neuronal Data
            neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)
            raster_dur = neuronal_data

            # Check Neuronal Data is a raster-plot:
            if len(np.unique(raster_dur[0, :])) > 2:
                if verbose:
                    print(f"Selected RoiResponseSeries is not a raster plot (ie not binary activity), "
                          f"go to next session. To run SCEs description on traces run: 'SCE description from traces'")
                continue

            # ID each transient:
            spike_nums_dur_numbers = give_unique_id_to_each_transient_of_raster_dur(raster_dur)

            [n_cells, n_frames] = raster_dur.shape
            if verbose:
                print(f"N cells: {n_cells}, N frames: {n_frames}")

            trace_neuronal_data = session_data.get_roi_response_serie_data_by_keyword(keys=roi_response_serie_info[:-1],
                                                                                      keyword="raw_trace")
            for key, data in trace_neuronal_data.items():
                traces = trace_neuronal_data.get(key)

            for trace_index, trace in enumerate(traces):
                traces[trace_index] = (trace - np.median(trace)) / np.median(trace)

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
                        print(f"Session: {session_identifier} not included in plots and statistics")

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

            # Get the SCE locations : 2 options to define SCE #
            sum_active_cells = np.sum(raster_dur, axis=0)

            # Get SCE threshold (3 options)#

            # SCEs threshold from surrogates
            if thr_method == "Surrogate":
                if verbose:
                    print(f"Define threshold for SCE detection using surrogate")

                # Follow GUI requirements if ask to get the threshold value from surrogates on specified epoch
                if epochs_to_use == "full_recording":
                    if verbose:
                        print(f"Do the determination of SCE threshold using the full recording")
                    raster_for_sce_threshold = raster_dur
                    if verbose:
                        print(
                            f"Shape of data for SCE threshold determination: "
                            f"NCells: {raster_for_sce_threshold.shape[0]} , "
                            f"NFrames: {raster_for_sce_threshold.shape[1]}")

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

                    raster_for_sce_threshold = raster_dur[:, frames_to_take]

                    if verbose:
                        print(
                            f"Shape of data for SCE threshold determination: "
                            f"NCells: {raster_for_sce_threshold.shape[0]}, "
                            f"NFrames: {raster_for_sce_threshold.shape[1]}")

                # Finally get the threshold
                sce_thresh = get_sce_threshold(raster_for_sce_threshold, n_surrogates=n_surrogates, percentile=percentile,
                                               verbose=verbose)[1]

            # SCEs threshold from arbitrary % of active cell
            if thr_method == "Arbitrary percentage":
                thresh = arbitrary_percentage_threshold / 10
                sce_thresh = (n_cells * thresh) / 100
                sce_thresh = np.floor(sce_thresh)
                if verbose:
                    print(f"Use {thresh} % of cells ({sce_thresh} cells) as threshold for SCE detection")

            # SCEs threshold from arbitrary number of active cell
            if thr_method == "Arbitrary number":
                sce_thresh = arbitrary_number_threshold
                if verbose:
                    print(f"Use {arbitrary_number_threshold} cells as threshold for SCE detection "
                          f"representing {np.round((arbitrary_number_threshold / n_cells) * 100, decimals=1)} %"
                          f" of the detected cells")

            # With 'peaks' method: SCE are at a single frame which is the peak of synchrony
            if verbose:
                print(f"Detection of SCEs location using the {method} method")
            if method == "Peaks":
                sce_times = sci_si.find_peaks(sum_active_cells, height=sce_thresh, distance=min_sce_distance)[0]
                n_sce = len(sce_times)
                if verbose:
                    print(f"Minimal distance between 2 SCEs: {min_sce_distance} frames")
                    print(f"SCE detection found: {n_sce} SCEs")
                cells_in_sce = raster_dur[:, sce_times]
                cell_transient_in_sce = np.ones((n_cells, n_sce), dtype=int)
                cell_transient_in_sce = cell_transient_in_sce * (-1)
                for cell in range(n_cells):
                    for sce in range(n_sce):
                        if cells_in_sce[cell, sce] == 1:
                            cell_transient_in_sce[cell, sce] = spike_nums_dur_numbers[cell, sce_times[sce]]
                # for all SCE look at the epoch during which it is occurring #
                sce_epoch = []
                for sce in range(n_sce):
                    sce_epoch.append("No epoch specified")
                for sce in range(n_sce):
                    sce_time = sce_times[sce]
                    for group_key, data in frames_in_epoch_dict.items():
                        epoch_frames_bool = frames_in_epoch_dict.get(group_key)
                        if epoch_frames_bool[sce_time] == 1:
                            sce_epoch[sce] = group_key
                        else:
                            continue
                # Build a cells in SCE matrix epoch group by epoch group
                if do_single_epoch_analysis:
                    if verbose:
                        print(f"Build a cells by SCEs matrix for each epoch")
                    cells_in_sce_by_epoch = dict()
                    cells_spikes_in_sce_by_epoch = dict()
                    for epoch, frames_in_epoch in frames_in_epoch_dict.items():
                        if len(np.where(frames_in_epoch)[0]) == 0:
                            if verbose:
                                print(f"No {epoch} frames in this session, skip this epoch")
                            continue
                        if verbose:
                            print(f"Ongoing epoch: {epoch}, with {len(np.where(frames_in_epoch)[0])} frames")
                        sce_times_in_epoch = list(frames_in_epoch[sce_times])
                        sce_times_in_epoch_bool = [bool(x) for x in sce_times_in_epoch]
                        n_sces_in_epoch = len(np.where(sce_times_in_epoch_bool)[0])
                        if verbose:
                            print(f"{n_sces_in_epoch} SCEs in {epoch} epoch")
                        cells_in_sce_in_epoch = cells_in_sce[:, sce_times_in_epoch_bool]
                        cells_spikes_in_sce_in_epoch = np.sum(cells_in_sce_in_epoch, axis=1)
                        cells_in_sce_by_epoch[epoch] = cells_in_sce_in_epoch
                        cells_spikes_in_sce_by_epoch[epoch] = cells_spikes_in_sce_in_epoch

            # With 'all frames' method: SCE are at all frames with more co-active cells is higher than the threshold
            if method == "All frames":
                sce_times = np.array(np.where(sum_active_cells >= sce_thresh)[0])
                sce_times_bool = np.zeros(n_frames, dtype="bool")
                sce_times_bool[sce_times] = True
                sce_periods = get_continous_time_periods(sce_times_bool)
                n_sce = len(sce_periods)
                if verbose:
                    print(f"SCE detection found: {len(sce_periods)} SCEs")
                cells_in_sce = np.zeros((n_cells, n_sce), dtype=int)
                cell_transient_in_sce = np.ones((n_cells, n_sce), dtype=int)
                cell_transient_in_sce = cell_transient_in_sce * (-1)
                for cell in range(n_cells):
                    for sce in range(n_sce):
                        if sce_periods[sce][0] < sce_periods[sce][1]:
                            cells_in_sce[cell, sce] = np.max(raster_dur[cell, sce_periods[sce][0]: sce_periods[sce][1]])
                            cell_transient_in_sce[cell, sce] = \
                                np.max(spike_nums_dur_numbers[cell, sce_periods[sce][0]: sce_periods[sce][1]])
                        else:
                            cells_in_sce[cell, sce] = raster_dur[cell, sce_periods[sce][0]]
                            cell_transient_in_sce[cell, sce] = spike_nums_dur_numbers[cell, sce_periods[sce][0]]
                # for all SCE look at the epoch during which it is occurring #
                sce_epoch = []
                for sce in range(n_sce):
                    sce_epoch.append("No epoch specified")
                for sce in range(n_sce):
                    sce_tpl = sce_periods[sce]
                    frames_to_check = range(sce_tpl[0], sce_tpl[1]+1)
                    frames_to_check = np.array(frames_to_check)
                    for group_key, data in frames_in_epoch_dict.items():
                        epoch_frames_bool = frames_in_epoch_dict.get(group_key)
                        if len(np.where(epoch_frames_bool[frames_to_check] == 1)[0]) > 0:
                            sce_epoch[sce] = group_key
                # Build a cells in SCE matrix epoch group by epoch group
                if do_single_epoch_analysis:
                    if verbose:
                        print(f"Build a cells by SCEs matrix for each epoch")
                    cells_in_sce_by_epoch = dict()
                    cells_spikes_in_sce_by_epoch = dict()
                    for epoch, frames_in_epoch in frames_in_epoch_dict.items():
                        if len(np.where(frames_in_epoch)[0]) == 0:
                            if verbose:
                                print(f"No {epoch} frames in this session, skip this epoch")
                            continue
                        if verbose:
                            print(f"Ongoing epoch: {epoch}, with {len(np.where(frames_in_epoch)[0])} frames")
                        frames_in_epoch = list(frames_in_epoch)
                        frames_in_epoch_bool = [bool(x) for x in frames_in_epoch]
                        sces_in_epoch_bool = [False for sce in range(n_sce)]
                        for sce in range(n_sce):
                            sce_tpl = sce_periods[sce]
                            sce_logicals = frames_in_epoch_bool[sce_tpl[0]: sce_tpl[1] + 1]
                            sce_logical = all(sce_logicals)
                            if sce_logical is True:
                                sces_in_epoch_bool[sce] = True
                        n_sces_in_epoch = len(np.where(sces_in_epoch_bool)[0])
                        if verbose:
                            print(f"{n_sces_in_epoch} SCEs in {epoch} epoch")
                        cells_in_sce_in_epoch = cells_in_sce[:, sces_in_epoch_bool]
                        cells_spikes_in_sce_in_epoch = np.sum(cells_in_sce_in_epoch, axis=1)
                        cells_in_sce_by_epoch[epoch] = cells_in_sce_in_epoch
                        cells_spikes_in_sce_by_epoch[epoch] = cells_spikes_in_sce_in_epoch

            # Get 'cells_in_sce' matrices for each cell types #
            type_in_sce_dict = dict()
            for key, info in cell_indices_by_cell_type.items():
                indexes = cell_indices_by_cell_type.get(key)
                type_in_sce = cells_in_sce[indexes, :]
                type_in_sce_dict[key] = type_in_sce

            # Print SCE frequency #
            sce_frequeny_second = n_sce / duration_s
            sce_frequeny_minute = n_sce / duration_m

            if time_unit == "seconds":
                sce_frequeny = sce_frequeny_second
            else:
                sce_frequeny = sce_frequeny_minute

            if verbose:
                print(f"Over full recording SCE frequency is: {sce_frequeny} SCEs / {time_unit}")

            # PART 1 :Get the 2 ratios spikes in SCE / total spikes and spike out SCE / total spikes #
            if verbose:
                print(f"Computing in-SCE and out-SCE spikes / total spike ratios for each cell")
            raster = np.zeros((n_cells, n_frames))
            for cell in range(n_cells):
                tmp_tple = get_continous_time_periods(raster_dur[cell, :])
                for tple in range(len(tmp_tple)):
                    onset = tmp_tple[tple][0]
                    raster[cell, onset] = 1
            n_spikes = np.sum(raster, axis=1)
            if verbose:
                print(f"N cells without spike: {len(np.where(n_spikes == 0)[0])}")

            n_spikes_sce = np.sum(cells_in_sce, axis=1)
            n_spikes_in_sce = np.minimum(n_spikes_sce, n_spikes)
            n_spikes_out_sce = n_spikes - n_spikes_in_sce
            spike_in_sce_ratio = n_spikes_in_sce / n_spikes
            spike_out_sce_ratio = n_spikes_out_sce / n_spikes

            # Build a pd.DataFrame to summarize the 2 ratios (each row is a cell)
            age_list = [info_dict['age'] for k in range(n_cells)]
            weight_list = [info_dict['weight'] for k in range(n_cells)]
            session_identifier_list = [info_dict['identifier'] for k in range(n_cells)]
            animal_id_list = [info_dict['subject_id'] for k in range(n_cells)]
            sum_up_data_0 = {'Age': age_list, 'SubjectID': animal_id_list, 'Weight': weight_list,
                             'Session': session_identifier_list, 'Celltype': cell_type_list,
                             'Cell#': np.arange(n_cells), 'N_spikes': n_spikes, 'N_spikes_in_SCEs': n_spikes_in_sce,
                             'In_SCE_spike_ratio': spike_in_sce_ratio, 'Out_SCE_spike_ratio': spike_out_sce_ratio}
            spike_ratio_data_table = pd.DataFrame(sum_up_data_0)
            if verbose:
                print(f"Data table is built")

            if do_single_epoch_analysis:
                if verbose:
                    print(f"Computing in-SCE and out-SCE spikes / total spike ratios for each cell for each epoch")

                sum_up_data_0_epoch = {'Age': age_list, 'SubjectID': animal_id_list, 'Weight': weight_list,
                                       'Session': session_identifier_list, 'Celltype': cell_type_list,
                                       'Cell#': np.arange(n_cells),
                                       'N_spikes': n_spikes}

                for epoch, frames_in_epoch in frames_in_epoch_dict.items():
                    if verbose:
                        print(f"Ongoing epoch: {epoch}")
                    if len(np.where(frames_in_epoch)[0]) == 0:
                        if verbose:
                            print(f"No {epoch} frames in this session, skip this epoch")
                        continue
                    frames_in_epoch = list(frames_in_epoch)
                    frames_in_epoch_bool = [bool(x) for x in frames_in_epoch]
                    epoch_raster = raster[:, frames_in_epoch_bool]
                    n_spikes_epoch = np.sum(epoch_raster, axis=1)
                    n_spikes_in_sce_epoch = cells_spikes_in_sce_by_epoch.get(epoch)
                    n_spikes_out_sce_epoch = n_spikes_epoch - n_spikes_in_sce_epoch
                    spike_in_sce_epoch_ratio = n_spikes_in_sce_epoch / n_spikes_epoch
                    spike_out_sce_epoch_ratio = n_spikes_out_sce_epoch / n_spikes_epoch
                    sum_up_data_0_epoch[f'N_spikes_in_{epoch}'] = n_spikes_epoch
                    sum_up_data_0_epoch[f'N_spikes_in_sce_{epoch}'] = n_spikes_in_sce_epoch
                    sum_up_data_0_epoch[f'%_spikes_in_sce_{epoch}'] = spike_in_sce_epoch_ratio
                    sum_up_data_0_epoch[f'N_spikes_out_sce_{epoch}'] = n_spikes_out_sce_epoch
                    sum_up_data_0_epoch[f'%_spikes_out_sce_{epoch}'] = spike_out_sce_epoch_ratio

                # general table
                spike_ratio_data_table_epoch = pd.DataFrame(sum_up_data_0_epoch)
                # summary table
                by_animal_in_sce_epoch_with_celltype = \
                    spike_ratio_data_table_epoch.groupby(['SubjectID', 'Celltype']) \
                        .agg({'mean', 'size'})
                by_animal_in_sce_epoch_without_celltype = \
                    spike_ratio_data_table_epoch.groupby(['SubjectID']) \
                        .agg({'mean', 'size'})
                # Savings
                path_results = self.get_results_path()
                # general
                path_ratio_epoch_table_xls = os.path.join(f'{path_results}',
                                                          f'{session_identifier}_inSCE_spikes_ratio_epochs_table.xlsx')
                spike_ratio_data_table_epoch.to_excel(path_ratio_epoch_table_xls)
                # summary
                path_ratio_epoch_table_animal_celltype = os.path.join(
                    f'{path_results}', f'{session_identifier}_inSCE_spikes_ratio_epochs_table_summary1.xlsx')
                by_animal_in_sce_epoch_with_celltype.to_excel(path_ratio_epoch_table_animal_celltype)

                path_by_animal_in_sce_epoch_without_celltype = os.path.join(
                    f'{path_results}', f'{session_identifier}_inSCE_spikes_ratio_epochs_table_summary2.xlsx')
                by_animal_in_sce_epoch_without_celltype.to_excel(path_by_animal_in_sce_epoch_without_celltype)

                if verbose:
                    print(f"Data tables are built and saved")

            # PART 2: Get the % of cell (for each type) participating in each SCE #
            if verbose:
                print(f"Computing SCE recruitment for each SCE")
            n_cells_by_sce = np.sum(cells_in_sce, axis=0)
            all_cell_participation_sce = (n_cells_by_sce / n_cells) * 100

            sce_participation_by_cell_type = dict()
            for key, info in type_in_sce_dict.items():
                cells_in_sce_type = type_in_sce_dict.get(key)
                n_cells_by_sce_type = np.sum(cells_in_sce_type, axis=0)
                participation_sce_type = (n_cells_by_sce_type / cells_in_sce_type.shape[0]) * 100
                sce_participation_by_cell_type[key] = participation_sce_type

            # Build a pd.DataFrame to summarize the SCE recruitment (each row is a SCE)
            age_list_sce = [info_dict['age'] for k in range(n_sce)]
            weight_list_sce = [info_dict['weight'] for k in range(n_sce)]
            session_identifier_list_sce = [info_dict['identifier'] for k in range(n_sce)]
            animal_id_list_sce = [info_dict['subject_id'] for k in range(n_sce)]
            sum_up_data_1 = {'Age': age_list_sce, 'SubjectID': animal_id_list_sce, 'Weight': weight_list_sce,
                             'Session': session_identifier_list_sce, 'SCE#': np.arange(n_sce), 'SCE_epoch': sce_epoch,
                             'AllCells_Recruitment': all_cell_participation_sce}
            for key, info in sce_participation_by_cell_type.items():
                if key not in sum_up_data_1.keys():
                    column_name = str(key.capitalize()) + '_Recruitment'
                    sum_up_data_1[column_name] = sce_participation_by_cell_type.get(key)
            sce_recruitment_data_table = pd.DataFrame(sum_up_data_1)
            if verbose:
                print(f"Data table is built")

            # PART 3: Get the mean amplitude of all transients involved for each SCE #
            if verbose:
                print(f"Computing mean transient amplitude of involved cells for each SCE")
            cell_activations_list = []
            for cell in range(n_cells):
                cell_activations = get_continous_time_periods(raster_dur[cell, :])
                cell_activations_list.append(cell_activations)
            amplitudes_list = []
            for sce in range(n_sce):
                amplitudes_by_sce = []
                for cell in range(n_cells):
                    cell_activations = cell_activations_list[cell]
                    if cell_transient_in_sce[cell, sce] != -1:
                        transient_id = cell_transient_in_sce[cell, sce]
                        onset = cell_activations[transient_id][0]
                        peak = cell_activations[transient_id][1]
                        amplitude = np.max(traces[cell, peak - 1: peak + 1]) - traces[cell, onset]
                        amplitudes_by_sce.append(amplitude)
                amplitudes_list.append(amplitudes_by_sce)
            mean_amplitude_by_sce = [np.nanmean(x) for x in amplitudes_list]

            # Build a pd.DataFrame to summarize the SCE mean transient amplitude (each row is a SCE)
            age_list_sce = [info_dict['age'] for k in range(n_sce)]
            weight_list_sce = [info_dict['weight'] for k in range(n_sce)]
            session_identifier_list_sce = [info_dict['identifier'] for k in range(n_sce)]
            animal_id_list_sce = [info_dict['subject_id'] for k in range(n_sce)]
            sum_up_data_2 = {'Age': age_list_sce, 'SubjectID': animal_id_list_sce, 'Weight': weight_list_sce,
                             'Session': session_identifier_list_sce, 'SCE#': np.arange(n_sce),
                             'MeanTransientAmplitude': mean_amplitude_by_sce}
            sce_transient_amplitude_data_table = pd.DataFrame(sum_up_data_2)
            if verbose:
                print(f"Data table is built")

            # Generate / append global pd.DataFrame tables #
            gobal_spike_ratio_data_table = gobal_spike_ratio_data_table.append(spike_ratio_data_table,
                                                                               ignore_index=True)
            gobal_sce_recruitment_data_table = gobal_sce_recruitment_data_table.append(sce_recruitment_data_table,
                                                                                       ignore_index=True)
            global_sce_transient_amplitude_data_table = global_sce_transient_amplitude_data_table.append(
                sce_transient_amplitude_data_table, ignore_index=True)

            self.update_progressbar(start_time, 100 / (n_sessions+1))

        if verbose:
            print(f"----------------------------------- GENERATE SUMMARY --------------------------------------")
            print(f"Generate simplest tables to keep one value per session or one value per animal")
        # In SCE spike ratio summary #
        # Generate a simplest in sce ratio table that keep one value per session #
        by_session_data_table_with_celltype = \
            gobal_spike_ratio_data_table.groupby(['SubjectID', 'Session', 'Celltype']) \
                .agg({'Age': 'mean', 'Cell#': 'size', 'Weight': 'mean', 'N_spikes': 'mean', 'N_spikes_in_SCEs': 'mean',
                      'In_SCE_spike_ratio': ['mean', 'std', 'min', 'median', 'max']}) \
                .rename(columns={'Cell#': 'N_Cells', 'N_spikes': 'Mean_N_spikes',
                                 'N_spikes_in_SCEs': 'Mean_N_spikes_in_SCE',
                                 'In_SCE_spike_ratio': 'In_SCE_spike_ratio_description'})
        by_session_data_table_without_celltype = \
            gobal_spike_ratio_data_table.groupby(['SubjectID', 'Session']) \
                .agg({'Age': 'mean', 'Cell#': 'size', 'Weight': 'mean', 'N_spikes': 'mean', 'N_spikes_in_SCEs': 'mean',
                      'In_SCE_spike_ratio': ['mean', 'std', 'min', 'median', 'max']}) \
                .rename(columns={'Cell#': 'N_Cells', 'N_spikes': 'Mean_N_spikes',
                                 'N_spikes_in_SCEs': 'Mean_N_spikes_in_SCE',
                                 'In_SCE_spike_ratio': 'In_SCE_spike_ratio_description'})

        # Generate a simplest in sce ratio table that keep one value per animal #
        by_animal_data_table_with_celltype = \
            gobal_spike_ratio_data_table.groupby(['SubjectID', 'Celltype']) \
                .agg({'Age': 'mean', 'Cell#': 'size', 'Weight': 'mean', 'N_spikes': 'mean', 'N_spikes_in_SCEs': 'mean',
                      'In_SCE_spike_ratio': ['mean', 'std', 'min', 'median', 'max']}) \
                .rename(columns={'Cell#': 'N_Cells', 'N_spikes': 'Mean_N_spikes',
                                 'N_spikes_in_SCEs': 'Mean_N_spikes_in_SCE',
                                 'In_SCE_spike_ratio': 'In_SCE_spike_ratio_description'})
        by_animal_data_table_without_celltype = \
            gobal_spike_ratio_data_table.groupby(['SubjectID']) \
                .agg({'Age': 'mean', 'Cell#': 'size', 'Weight': 'mean', 'N_spikes': 'mean', 'N_spikes_in_SCEs': 'mean',
                      'In_SCE_spike_ratio': ['mean', 'std', 'min', 'median', 'max']}) \
                .rename(columns={'Cell#': 'N_Cells', 'N_spikes': 'Mean_N_spikes',
                                 'N_spikes_in_SCEs': 'Mean_N_spikes_in_SCE',
                                 'In_SCE_spike_ratio': 'In_SCE_spike_ratio_description'})

        # SCE recruitment spike ratio summary #
        # Generate a simplest sce recruitment table that keep one value per session #
        by_session_recruitment_table_with_sce_epoch = \
            gobal_sce_recruitment_data_table.groupby(['SubjectID', 'Session', 'SCE_epoch']) \
                .agg({'mean', 'size'})

        by_session_recruitment_table_without_sce_epoch = \
            gobal_sce_recruitment_data_table.groupby(['SubjectID', 'Session']) \
                .agg({'mean', 'size'})

        # Generate a simplest sce recruitment table that keep one value per animal #
        by_animal_recruitment_table_with_sce_epoch = \
            gobal_sce_recruitment_data_table.groupby(['SubjectID', 'SCE_epoch']) \
                .agg({'mean', 'size'})

        by_animal_recruitment_table_without_celltype = \
            gobal_sce_recruitment_data_table.groupby(['SubjectID']) \
                .agg({'mean', 'size'})

        # Save results in table
        if save_table:
            if verbose:
                print(f"----------------------------------- SAVINGS --------------------------------------")
            # Set the paths for global tables #
            path_results = self.get_results_path()
            path_ratio_table_xls = os.path.join(f'{path_results}', f'inSCE_spikes_ratio_table.xlsx')
            path_ratio_table_csv = os.path.join(f'{path_results}', f'inSCE_spikes_ratio_table.csv')
            path_recruitment_table_xls = os.path.join(f'{path_results}', f'SCE_recruitment_table.xlsx')
            path_recruitment_table_csv = os.path.join(f'{path_results}', f'SCE_recruitment_table.csv')
            path_amplitude_table_xls = os.path.join(f'{path_results}', f'SCE_transients_amplitude_table.xlsx')
            path_amplitude_table_csv = os.path.join(f'{path_results}', f'SCE_transients_amplitude_table.csv')

            # Set the paths for spike in sce ratio summary tables #
            path_ratio_table_session_type_xls = os.path.join(f'{path_results}', f'inSCE_spikes_ratio_table_session_type.xlsx')
            path_ratio_table_session_xls = os.path.join(f'{path_results}', f'inSCE_spikes_ratio_table_session.xlsx')
            path_ratio_table_animal_type_xls = os.path.join(f'{path_results}', f'inSCE_spikes_ratio_table_animal_type.xlsx')
            path_ratio_table_animal_xls = os.path.join(f'{path_results}', f'inSCE_spikes_ratio_table_animal.xlsx')

            # Set the paths for sce recruitment summary tables #
            path_recruitment_table_session_epoch_xls = os.path.join(f'{path_results}',
                                                                    f'SCE_recruitment_table_session_epoch.xlsx')
            path_recruitment_table_session_xls = os.path.join(f'{path_results}', f'SCE_recruitment_table_session.xlsx')
            path_recruitment_table_animal_epoch_xls = os.path.join(f'{path_results}',
                                                                   f'SCE_recruitment_table_animal_epoch.xlsx')
            path_recruitment_table_animal_xls = os.path.join(f'{path_results}', f'SCE_recruitment_table_animal.xlsx')

            # Do the savings of global tables #
            gobal_spike_ratio_data_table.to_excel(path_ratio_table_xls)
            gobal_spike_ratio_data_table.to_csv(path_ratio_table_csv)
            gobal_sce_recruitment_data_table.to_excel(path_recruitment_table_xls)
            gobal_sce_recruitment_data_table.to_csv(path_recruitment_table_csv)
            global_sce_transient_amplitude_data_table.to_excel(path_amplitude_table_xls)
            global_sce_transient_amplitude_data_table.to_csv(path_amplitude_table_csv)

            # Do the savings of summary tables #
            by_session_data_table_with_celltype.to_excel(path_ratio_table_session_type_xls)
            by_session_data_table_without_celltype.to_excel(path_ratio_table_session_xls)
            by_animal_data_table_with_celltype.to_excel(path_ratio_table_animal_type_xls)
            by_animal_data_table_without_celltype.to_excel(path_ratio_table_animal_xls)

            # Do the savings of summary tables #
            by_session_recruitment_table_with_sce_epoch.to_excel(path_recruitment_table_session_epoch_xls)
            by_session_recruitment_table_without_sce_epoch.to_excel(path_recruitment_table_session_xls)
            by_animal_recruitment_table_with_sce_epoch.to_excel(path_recruitment_table_animal_epoch_xls)
            by_animal_recruitment_table_without_celltype.to_excel(path_recruitment_table_animal_xls)

            if verbose:
                print(f"Data save as excel and csv files")

        if verbose:
            print(f"-------------------------- WORK ON IN-SCE SPIKE RATIO -----------------------------")

        if verbose:
            print(f"Filter data table accordingly to the GUI requirements")
        # Filter general table on query from the GUI
        if cell_to_use == "all_cells":
            data_table = gobal_spike_ratio_data_table
        else:
            type_to_use = cell_to_use.capitalize()
            data_table = gobal_spike_ratio_data_table.query('Celltype == @type_to_use')

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

        if do_stats:
            if n_ages > 1:
                if verbose:
                    print(f"Do some statistics")
                    print(f"Compare the ratio: spikes in-SCE / total spikes for {cell_to_use} across age")
                distribution_by_age = [[] for k in range(n_ages)]
                if verbose:
                    print(f"N pups: {n_animals}, N sessions: {n_sessions}, N cells: {n_cells_stats}")
                for index in range(n_ages):
                    age = ages_list[index]
                    tmp_table = data_table[data_table.Age == age]
                    data = tmp_table.get("In_SCE_spike_ratio")
                    data_list = data.values.tolist()
                    distribution_by_age[index] = data_list
                multiple_comparison_one_factor_effect(distribution_by_age, pvalues=pvalue, verbose=verbose,
                                                      sessions_ids=ages_list)

        if verbose:
            print(f"Do the plots")

        # Do the plot according to GUI requirements
        if hue_ratio == "None":
            hue_ratio = None
            palette_ratio = None

        # ylabel = "Ratio: spikes in-SCE / total spikes " + "Population: " + cell_to_use
        ylabel = "spikes in-SCE / total spikes"

        filename = "In_SCE_spike_ratio_"

        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(width_fig, height_fig), dpi=dpi)
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)

        svm = sns.catplot(x=x_axis_name_ratio, y="In_SCE_spike_ratio", hue=hue_ratio, data=data_table, hue_order=None,
                          kind=kind_ratio, orient=None, color=fig_facecolor, palette=palette_ratio, ax=ax1)

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

        if verbose:
            print(f"--------------------------- WORK ON SCE RECRUITMENT ------------------------------")

        if do_stats:
            if n_ages > 1:
                if verbose:
                    print(f"Do some statistics")
                    print(f"Compare SCE recruitment among 'All Cells' across age")
                distribution_by_age = [[] for k in range(n_ages)]
                recruitement_data = gobal_sce_recruitment_data_table
                for index in range(n_ages):
                    age = ages_list[index]
                    tmp_table = recruitement_data[recruitement_data.Age == age]
                    data = tmp_table.get("AllCells_Recruitment")
                    data_list = data.values.tolist()
                    distribution_by_age[index] = data_list

                multiple_comparison_one_factor_effect(distribution_by_age, pvalues=pvalue, verbose=verbose,
                                                      sessions_ids=ages_list)

        if verbose:
            print(f"Do the plots")

        # Do the plot according to GUI requirements
        if hue_recruitment == "None":
            hue_recruitment = None
            palette_recruitment = None

        ylabel = "Proportion of cell recruited in SCE (% of 'All cells')"

        filename = "SCE_recruitment"

        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(width_fig, height_fig), dpi=dpi)
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)

        svm = sns.catplot(x=x_axis_name_recruitment, y="AllCells_Recruitment", hue=hue_recruitment,
                          data=gobal_sce_recruitment_data_table, hue_order=None, kind=kind_recruitment,
                          orient=None, color=fig_facecolor, palette=palette_recruitment, ax=ax1)

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

        if verbose:
            print(f"---------------------- WORK ON SCE TRANSIENTS' AMPLITUDES -------------------------")

        if verbose:
            print(f"Do the plots")

        # Do the plot according to GUI requirements
        if hue_amplitude == "None":
            hue_amplitude = None
            palette_amplitude = None

        ylabel = "Mean transient amplitude in SCE (df/f)"

        filename = "SCE_transient_amplitude_"

        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(width_fig, height_fig), dpi=dpi)
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)

        svm = sns.catplot(x=x_axis_name_amplitude, y="MeanTransientAmplitude", hue=hue_amplitude,
                          data=global_sce_transient_amplitude_data_table,
                          hue_order=None, kind=kind_amplitude, orient=None, color=fig_facecolor,
                          palette=palette_amplitude,
                          ax=ax1)

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

