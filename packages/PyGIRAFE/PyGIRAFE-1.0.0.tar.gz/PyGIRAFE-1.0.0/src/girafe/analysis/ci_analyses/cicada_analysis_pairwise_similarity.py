from cicada.analysis.cicada_analysis import CicadaAnalysis
from cicada.utils.misc import get_continous_time_periods, get_yang_frames, from_timestamps_to_frame_epochs, \
    print_info_dict
from cicada.utils.pairwise_correlation_analysis import compute_similarity_matrix, plot_similarity_matrix
from cicada.utils.display.cells_map_utils import CellsCoord, compute_distance_from_center
import numpy as np
import pandas as pd
import seaborn as sns
from time import time
from datetime import datetime
import matplotlib.pyplot as plt
import os
import h5py


class CicadaAnalysisPairwiseSimilarity(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        CicadaAnalysis.__init__(self, name="Pairwise similarity", family_id="Descriptive statistics",
                                short_description="Evaluate and show pairwise similarity",
                                config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaAnalysisPairwiseSimilarity(config_handler=self.config_handler)
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

        self.add_roi_response_series_arg_for_gui(short_description="Neuronal activity to use", long_description=None,
                                                 family_widget="figure_config_data_to_use")

        self.add_segmentation_arg_for_gui()

        data_avalaible = ["Traces", "Rasterdur", "Raster"]
        self.add_choices_arg_for_gui(arg_name="data_to_correlate", choices=data_avalaible,
                                     default_value="Rasterdur",
                                     short_description="Data to use to compute pairwise similarity measures",
                                     multiple_choices=False,
                                     family_widget="figure_config_data_to_use")

        # TODO: implement something with connectivity (to see the cell that have similar connectivity)
        similarity_metrics = ["Pearson", "Hamming", "Jacquard"]
        self.add_choices_arg_for_gui(arg_name="similarity_metric", choices=similarity_metrics,
                                     default_value="Pearson",
                                     short_description="Metric to use to build the pairwise similarity matrix",
                                     multiple_choices=False,
                                     family_widget="figure_config_metric_to_use")

        possibilities = ['full_recording', 'one_by_epoch']
        self.add_choices_arg_for_gui(arg_name="epochs_to_use", choices=possibilities,
                                     default_value="full_recording",
                                     short_description="Compute one similarity matrix over the full "
                                                       "recording or one by epoch",
                                     multiple_choices=False,
                                     family_widget="epochs")

        all_epochs = []
        for data_to_analyse in self._data_to_analyse:
            all_epochs.extend(data_to_analyse.get_behavioral_epochs_names())
        all_epochs = list(np.unique(all_epochs))
        self.add_choices_for_groups_for_gui(arg_name="epochs_names", choices=all_epochs,
                                            with_color=True,
                                            mandatory=False,
                                            short_description="Behaviors to group: build one similarity matrix per epoch",
                                            long_description="Here you need to specify which individual behaviors "
                                                             "belong to the same group",
                                            family_widget="epochs")

        self.add_bool_option_for_gui(arg_name="specify_twitches_duration", true_by_default=False,
                                     short_description="Arbitrary set twitch duration",
                                     family_widget="epochs")

        self.add_int_values_arg_for_gui(arg_name="twitches_duration", min_value=100, max_value=1500,
                                        short_description="Duration after twitch to define 'twitch-related' activity (ms)",
                                        default_value=1000, family_widget="epochs")

        self.add_bool_option_for_gui(arg_name="save_table", true_by_default=True,
                                     short_description="Save similarity values in tables",
                                     family_widget="saving")

        self.add_bool_option_for_gui(arg_name="do_plots", true_by_default=True,
                                     short_description="Do some plots",
                                     family_widget="saving")

        representations = ["strip", "swarm", "violin", "box", "bar", "boxen"]
        self.add_choices_arg_for_gui(arg_name="representation", choices=representations,
                                     default_value="violin", short_description="Kind of plot to use",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        x_ax = ["Age", "SubjectID", "Session", "PairType"]
        self.add_choices_arg_for_gui(arg_name="x_axis", choices=x_ax,
                                     default_value="Age", short_description="Variable to use for x axis groups",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        possible_hues = ["Age", "SubjectID", "Session", "PairType", "None"]
        self.add_choices_arg_for_gui(arg_name="hue", choices=possible_hues,
                                     default_value="None",
                                     short_description="Variable to use for x axis sub-groups",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        palettes = ["muted", "deep", "pastel", "Blues"]
        self.add_choices_arg_for_gui(arg_name="palettes", choices=palettes,
                                     default_value="muted", short_description="Color palette for x-axis subgroups",
                                     long_description="In that case figure facecolor and figure edgecolor are useless",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        self.add_color_arg_for_gui(arg_name="fig_facecolor", default_value=(1, 1, 1, 1.),
                                   short_description="Figure face color",
                                   long_description="Useless if a 'hue' is specified, in such a case use 'palette'",
                                   family_widget="figure_config_color")

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

        self.add_bool_option_for_gui(arg_name="compute_cell_dist", true_by_default=True,
                                     short_description="Correlate with distance between cells",
                                     family_widget="segmentation")

        self.add_field_float_option_for_gui(arg_name="pixel_size", default_value="2.0", mandatory=False,
                                            short_description="Pixel size",
                                            long_description=None, family_widget="segmentation")

        plot_styles = ['Scatter plot', 'Bar plot']
        self.add_choices_arg_for_gui(arg_name="correlation_plot_style", choices=plot_styles,
                                     default_value="Scatter lot",
                                     short_description="Style of correlation plot",
                                     long_description="We will automatically switch to averaged bar plot "
                                                      "if there is too many points (ie too many pair of cells)",
                                     multiple_choices=False,
                                     family_widget="figure2_config")

        self.add_int_values_arg_for_gui(arg_name="binsize", min_value=1, max_value=50,
                                        short_description="Bin size to average similarity per bin",
                                        default_value=30, family_widget="figure2_config")

        self.add_color_arg_for_gui(arg_name="fig_edgecolor", default_value=(1, 1, 1, 1.),
                                   short_description="Figure edge color",
                                   long_description="Use only in distance vs correlation scatter plot",
                                   family_widget="figure2_config_color")

        self.add_color_arg_for_gui(arg_name="fig_facecolor2", default_value=(1, 1, 1, 1.),
                                   short_description="Figure facecolor",
                                   long_description="Use only in distance vs correlation scatter plot",
                                   family_widget="figure2_config_color")

        self.add_image_format_package_for_gui()

        self.add_color_arg_for_gui(arg_name="background_color", default_value=(0, 0, 0, 1.),
                                   short_description="background color",
                                   long_description=None, family_widget="general_color")

        self.add_color_arg_for_gui(arg_name="axis_color", default_value=(1, 1, 1, 1.),
                                   short_description="Axes color",
                                   long_description=None, family_widget="general_color")

        self.add_color_arg_for_gui(arg_name="labels_color", default_value=(1, 1, 1, 1.),
                                   short_description="Label color",
                                   long_description=None, family_widget="general_color")

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

        segmentation_dict = kwargs['segmentation']

        compute_cell_dist = kwargs.get("compute_cell_dist")

        pixel_size = kwargs.get("pixel_size")

        data_to_correlate = kwargs.get("data_to_correlate")

        similarity_metric = kwargs.get("similarity_metric")

        epochs_to_use = kwargs.get("epochs_to_use")

        epoch_groups = kwargs.get("epochs_names")

        specify_twitches_duration = kwargs.get("specify_twitches_duration")

        path_results = self.get_results_path()

        save_table = kwargs.get("save_table")

        do_plots = kwargs.get("do_plots")

        x_axis_name = kwargs.get("x_axis")

        hue = kwargs.get("hue")

        kind = kwargs.get("representation")

        palette = kwargs.get("palettes")

        background_color = kwargs.get("background_color")

        fig_facecolor = kwargs.get("fig_facecolor")

        correlation_plot_style = kwargs.get("correlation_plot_style")

        binsize = kwargs.get("binsize")

        fig_edgecolor = kwargs.get("fig_edgecolor")

        fig_facecolor2 = kwargs.get("fig_facecolor2")

        axis_color = kwargs.get("axis_color")

        labels_color = kwargs.get("labels_color")

        font_size = kwargs.get("font_size")

        fontweight = kwargs.get("fontweight")

        fontfamily = kwargs.get("font_type")

        # image package format
        save_formats = kwargs["save_formats"]
        if save_formats is None:
            save_formats = "pdf"

        save_figure = kwargs.get("save_figure", True)

        dpi = kwargs.get("dpi", 100)

        width_fig = kwargs.get("width_fig")

        height_fig = kwargs.get("height_fig")

        with_timestamp_in_file_name = kwargs.get("with_timestamp_in_file_name", True)

        start_time = time()

        print("Description of pairwise similarity: coming soon...")

        n_sessions = len(self._data_to_analyse)
        n_sessions_to_use = n_sessions
        if verbose:
            print(f"{n_sessions} sessions to analyse")

        similarity_general_table = pd.DataFrame()
        correlation_general_table = pd.DataFrame()
        distance_only_general_table = pd.DataFrame()
        similarity_general_table_dict = dict()
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
            n_cells_start, n_frames_start = neuronal_data.shape
            if verbose:
                print(f"Starting with: N cells = {n_cells_start}, N frames = {n_frames_start}")

            # See what is the selected data :
            if data_to_correlate == "Traces":
                traces = neuronal_data
                active_cells = np.where(traces.any(axis=1))[0]
                no_active_cells = n_cells_start - len(active_cells)
                traces = traces[active_cells, :]
                for trace_index, trace in enumerate(traces):
                    traces[trace_index] = (trace - np.nanmedian(trace)) / np.nanmedian(trace)
                data = traces
                if verbose:
                    print(f"Remove {no_active_cells} cells whit flat zero signal")
                    print(f"Still : {data.shape[0]} active cells in analysis")
            else:
                raster_dur = neuronal_data
                [n_cells, n_frames] = raster_dur.shape
                raster = np.zeros((n_cells, n_frames))
                for cell in range(n_cells):
                    tmp_tple = get_continous_time_periods(raster_dur[cell, :])
                    for tple in range(len(tmp_tple)):
                        onset = tmp_tple[tple][0]
                        raster[cell, onset] = 1
                # Get cells that spikes at least once
                sum_spikes = np.sum(raster, axis=1)
                active_cells = np.where(sum_spikes >= 1)[0]
                no_active_cells = n_cells - len(active_cells)

                if data_to_correlate == "Rasterdur":
                    data = raster_dur
                    data = data[active_cells, :]
                    if verbose:
                        print(f"Remove {no_active_cells} cells without spikes in the recording")
                        print(f"Still : {data.shape[0]} active cells in analysis")
                if data_to_correlate == "Raster":
                    data = raster
                    data = data[active_cells, :]
                    if verbose:
                        print(f"Remove {no_active_cells} cells without spikes in the recording")
                        print(f"Still : {data.shape[0]} cells in the analysis")
            active_cells = list(active_cells)

            # Get Cell-type Data and build cell-type list
            cell_indices_by_cell_type = session_data.get_cell_indices_by_cell_type(roi_serie_keys=
                                                                                   roi_response_serie_info)
            tmp_cell_type_list = []
            for cell in range(n_cells_start):
                tmp_cell_type_list.append("Unclassified")

            for key, info in cell_indices_by_cell_type.items():
                cell_type = key.capitalize()
                indexes = cell_indices_by_cell_type.get(key)
                tmp_n_cell = len(indexes)
                for cell in range(tmp_n_cell):
                    tmp_ind = indexes[cell]
                    tmp_cell_type_list[tmp_ind] = cell_type
            cell_type_list = [tmp_cell_type_list[i] for i in active_cells]

            unique_types = np.unique(cell_type_list)
            unique_types_list = unique_types.tolist()

            # Get CI movie sampling rate
            ci_sampling_rate = session_data.get_ci_movie_sampling_rate(only_2_photons=True)
            if ci_sampling_rate is None:
                ci_sampling_rate = session_data.get_rrs_sampling_rate(keys=roi_response_serie_info)

            # Get the frames to include in the analysis if use epochs
            if epochs_to_use == 'one_by_epoch':
                if verbose:
                    print(f"Build group of frames for each defined epoch")
                # Filter data based on the epochs: get the frames included in each epoch
                data_for_epoch = dict()
                active_frames = []
                group_names = []
                if specify_twitches_duration:
                    twitches_duration = kwargs.get("twitches_duration")
                    twitches_duration = twitches_duration / 1000
                    frames_delay = int(np.round(twitches_duration * ci_sampling_rate))
                for epoch_group_name, epoch_info in epoch_groups.items():
                    if len(epoch_info) != 2:
                        continue
                    group_names.append(epoch_group_name)

                    # Check whether this main epoch is the one of twitches
                    name_to_check = epoch_group_name.lower()
                    twitches_group = False
                    if name_to_check.find('twi') != -1:
                        twitches_group = True

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
                    active_frames.extend(epochs_frames_in_group)

                    n_periods = len(epochs_frames_in_group)
                    frames_to_take = []
                    for event in range(n_periods):
                        start = epochs_frames_in_group[event][0]
                        if twitches_group is True and specify_twitches_duration is True:
                            end = epochs_frames_in_group[event][0] + frames_delay
                        else:
                            end = epochs_frames_in_group[event][1]
                        frames_to_take.extend(np.arange(start, end + 1))

                    data_epoch = data[:, frames_to_take]
                    sum_spikes_epoch = np.sum(data_epoch, axis=1)
                    epoch_active_cells = np.where(sum_spikes_epoch)[0]
                    epoch_no_active_cells = np.where(sum_spikes_epoch == 0)[0]
                    data_to_take = data[:, frames_to_take]
                    data_to_take = data_to_take[epoch_active_cells, :]
                    if epochs_to_use != "full_recording":
                        if verbose:
                            print(f"Remove {len(epoch_no_active_cells)} cells with no spikes in '{epoch_group_name}' epoch")
                            print(f"Still : {data_to_take.shape[0]} active cells in analysis")
                    data_for_epoch[epoch_group_name] = data_to_take

                group_names.append('rest')
                rest_frames = get_yang_frames(total_frames=n_frames_start, yin_frames=active_frames)[1]
                rest_data = data[:, rest_frames]
                sum_spikes_rest = np.sum(rest_data, axis=1)
                rest_active_cells = np.where(sum_spikes_rest)[0]
                rest_no_active_cells = np.where(sum_spikes_rest == 0)[0]
                rest_data = rest_data[rest_active_cells, :]
                if epochs_to_use != "full_recording":
                    if verbose:
                        print(f"Remove {len(rest_no_active_cells)} cells with no spikes in 'rest' epoch")
                        print(f"Still : {rest_data.shape[0]} active cells in analysis")
                data_for_epoch['rest'] = rest_data

            # Check compatibility between data to use and similarity metric
            if data_to_correlate in ["Traces"] and similarity_metric in ["Hamming", "Jacquard"]:
                if verbose:
                    print(f"Data from: {data_to_use} is not compatible with similarity from {similarity_metric}")
                    print(f"Use Pearson correlation as default metric")
                similarity_metric = "Pearson"

            # Compute similarity matrix: Use full recording or compute one for each specified epoch
            if epochs_to_use == 'full_recording':
                if verbose:
                    print(f" ")
                    print(f"Using full recording")
                data_to_use = data
                similarity_matrix = compute_similarity_matrix(neuronal_data=data_to_use, method=similarity_metric,
                                                              verbose=verbose)
                print(f" ")
                print(f"Put the results in a table")
                # Get the distribution of similarities
                cell_1_id = []
                cell_2_id = []
                n_used_cells = data_to_use.shape[0]
                n_pairs = int((n_used_cells * (n_used_cells - 1)) / 2)

                type_cell_1 = []
                type_cell_2 = []
                type_in_pair = [[] for k in range(n_pairs)]
                similarity_score = []
                pair = 0
                for cell_1 in range(n_used_cells):
                    for cell_2 in np.arange(cell_1 + 1, n_used_cells):
                        cell_1_id.append(cell_1)
                        cell_1_type = cell_type_list[cell_1]
                        type_cell_1.append(cell_1_type)
                        cell_2_id.append(cell_2)
                        cell_2_type = cell_type_list[cell_2]
                        type_cell_2.append(cell_2_type)
                        if cell_1_type == cell_2_type:
                            type_in_pair[pair] = cell_1_type + '_' + cell_2_type
                        else:
                            ind_1 = unique_types_list.index(cell_1_type)
                            ind_2 = unique_types_list.index(cell_2_type)
                            indices_pair = [ind_1, ind_2]
                            indices_pair = np.sort(indices_pair)
                            indices_pair = indices_pair.tolist()
                            index_type1 = indices_pair[0]
                            index_type2 = indices_pair[1]
                            name_1 = unique_types_list[index_type1]
                            name_2 = unique_types_list[index_type2]
                            type_in_pair[pair] = name_1 + '_' + name_2
                        similarity_score.append(similarity_matrix[cell_1, cell_2])
                        pair = pair + 1

                # Put it in a table
                age_list = [info_dict['age'] for k in range(n_pairs)]
                weight_list = [info_dict['weight'] for k in range(n_pairs)]
                session_identifier_list = [info_dict['identifier'] for k in range(n_pairs)]
                animal_id_list = [info_dict['subject_id'] for k in range(n_pairs)]
                sum_up_data = {'Age': age_list, 'Weight': weight_list, 'SubjectID': animal_id_list,
                               'Session': session_identifier_list, 'Cell_1#': cell_1_id, 'Cell_1Type': type_cell_1,
                               'Cell_2#': cell_2_id, 'Cell_2Type': type_cell_2, 'PairType': type_in_pair,
                               'SimilarityScore': similarity_score}
                similarity_score_table = pd.DataFrame(sum_up_data)

                # Append data table
                similarity_general_table = similarity_general_table.append(similarity_score_table, ignore_index=True)

            else:
                if verbose:
                    print(f" ")
                    print(f"Using Epochs")
                similarity_matrix_dict = dict()
                for index, name in enumerate(group_names):
                    if verbose:
                        print(f"Working on epoch: {name}")
                    data_to_use = data_for_epoch.get(name)
                    similarity_matrix = compute_similarity_matrix(neuronal_data=data_to_use, method=similarity_metric,
                                                                  verbose=verbose)
                    similarity_matrix_dict[name] = similarity_matrix

                    print(f" ")
                    print(f"Put the results for {name} epoch in a table")
                    # Get the distribution of similarities
                    cell_1_id = []
                    cell_2_id = []
                    n_used_cells = data_to_use.shape[0]
                    n_pairs = int((n_used_cells * (n_used_cells - 1)) / 2)

                    type_cell_1 = []
                    type_cell_2 = []
                    type_in_pair = [[] for k in range(n_pairs)]
                    similarity_score = []
                    pair = 0
                    for cell_1 in range(n_used_cells):
                        for cell_2 in np.arange(cell_1 + 1, n_used_cells):
                            cell_1_id.append(cell_1)
                            cell_1_type = cell_type_list[cell_1]
                            type_cell_1.append(cell_1_type)
                            cell_2_id.append(cell_2)
                            cell_2_type = cell_type_list[cell_2]
                            type_cell_2.append(cell_2_type)
                            if cell_1_type == cell_2_type:
                                type_in_pair[pair] = cell_1_type + '_' + cell_2_type
                            else:
                                ind_1 = unique_types_list.index(cell_1_type)
                                ind_2 = unique_types_list.index(cell_2_type)
                                indices_pair = [ind_1, ind_2]
                                indices_pair = np.sort(indices_pair)
                                indices_pair = indices_pair.tolist()
                                index_type1 = indices_pair[0]
                                index_type2 = indices_pair[1]
                                name_1 = unique_types_list[index_type1]
                                name_2 = unique_types_list[index_type2]
                                type_in_pair[pair] = name_1 + '_' + name_2
                            similarity_score.append(similarity_matrix[cell_1, cell_2])
                            pair = pair + 1

                    # Put it in a table
                    age_list = [info_dict['age'] for k in range(n_pairs)]
                    weight_list = [info_dict['weight'] for k in range(n_pairs)]
                    session_identifier_list = [info_dict['identifier'] for k in range(n_pairs)]
                    animal_id_list = [info_dict['subject_id'] for k in range(n_pairs)]
                    sum_up_data = {'Age': age_list, 'Weight': weight_list, 'SubjectID': animal_id_list,
                                   'Session': session_identifier_list, 'Cell_1#': cell_1_id, 'Cell_1Type': type_cell_1,
                                   'Cell_2#': cell_2_id, 'Cell_2Type': type_cell_2, 'PairType': type_in_pair,
                                   'SimilarityScore': similarity_score}
                    similarity_score_table = pd.DataFrame(sum_up_data)

                    # Append data table
                    if session_index == 0 and index == 0:
                        similarity_general_table_dict = {group: pd.DataFrame() for group in group_names}
                    else:
                        pass
                    similarity_general_table_dict[name] = similarity_general_table_dict[name].append(
                        similarity_score_table, ignore_index=True)

            # Plot similarity matrix
            if epochs_to_use == 'full_recording':
                if verbose:
                    print(f" ")
                    print(f"Plot the correlation matrix")
                plot_similarity_matrix(data=similarity_matrix,
                                       filename=data_to_correlate + "_similarity_matrix_" + session_identifier,
                                       background_color=background_color,
                                       size_fig=(width_fig, height_fig),
                                       save_figure=save_figure, path_results=path_results, save_formats=save_formats,
                                       with_timestamp_in_file_name=with_timestamp_in_file_name)
            else:
                if verbose:
                    print(f" ")
                    print(f"Plot the correlation matrices")
                plot_similarity_matrix(data=similarity_matrix_dict,
                                       filename=data_to_correlate + "_similarity_matrix_" + session_identifier,
                                       background_color=background_color,
                                       size_fig=(width_fig, height_fig),
                                       save_figure=save_figure, path_results=path_results, save_formats=save_formats,
                                       with_timestamp_in_file_name=with_timestamp_in_file_name)

            # Look for distance between cells of each pair #
            if compute_cell_dist:
                if verbose:
                    print(f" ")
                    print(f"Correlate pairwise similarity between cells with distance between cells")
                if isinstance(segmentation_dict, dict):
                    segmentation_info = segmentation_dict[session_identifier]
                else:
                    segmentation_info = segmentation_dict

                if verbose:
                    print(f"First get the pixels masks")
                pixel_mask = session_data.get_pixel_mask(segmentation_info=segmentation_info)
                tmp_pixel_mask_list = [pixel_mask[cell] for cell in range(len(pixel_mask))]

                pixel_mask_list = [tmp_pixel_mask_list[i] for i in active_cells]

                cells_coord = CellsCoord(pixel_masks=pixel_mask_list, nb_lines=None, nb_col=None,
                                         from_matlab=False, invert_xy_coord=False)
                cell_center_coord = cells_coord.center_coord

                # Try to get CI movie dimensions from the 'TwoPhotonSeries'
                if verbose:
                    print(f"Then get the size of the field of view")
                is_ci_movie = session_data.contains_ci_movie(consider_only_2_photons=True)
                if is_ci_movie:
                    n_lines, n_cols = session_data.get_ci_movie_dimension(only_2_photons=True)
                    if (n_lines is not None) and (n_cols is not None):
                        print(f"Dimension of calcium imaging movie (n_lines x n_cols) is {n_lines}x{n_cols} pixels")
                else:
                    n_lines = None
                    n_cols = None
                    print(f"No dimension of calcium imaging movie found yet, try from 'PlanSegmentation'")
                # If it does not return n_lines and n_cols try to get them from 'image mask' in PlanSegmentation
                if (n_lines is None) and (n_cols is None):
                    n_lines, n_cols = session_data.get_ci_dimension_from_img_mask(segmentation_info=segmentation_info)
                    if (n_lines is not None) and (n_cols is not None):
                        print(f"Dimension of calcium imaging movie (n_lines x n_cols) is {n_lines}x{n_cols} pixels")
                    else:
                        print(f"Image size was not found from the 'TwoPhotonSeries' or from 'image_mask'")

                if verbose:
                    print(f"Compute distance for each pair of cell")
                cell_dist_matrix = compute_distance_from_center(cell_center_coord)
                cell_dist_matrix_um = cell_dist_matrix * pixel_size

                distances = cell_dist_matrix_um[np.triu_indices(len(active_cells), k=1)]
                corr = similarity_matrix[np.triu_indices(len(active_cells), k=1)]

                # Do the plot
                if verbose:
                    print(f"Plot cell-distances vs cell pairwise-similarity for {session_identifier} ")

                filename = f"Pairwise-similarity_{similarity_metric}_on_{data_to_correlate}_{session_identifier}_"

                fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                        gridspec_kw={'height_ratios': [1]},
                                        figsize=(width_fig, height_fig), dpi=dpi)
                ax1.set_facecolor(background_color)
                fig.patch.set_facecolor(background_color)

                # Check number of cells before Scatter plot
                if n_cells_start > 200 and correlation_plot_style == "Scatter plot":
                    correlation_plot_style = "Bar plot"
                    if verbose:
                        print(f"Do Bar plot instead of Scatter plot")

                if correlation_plot_style == "Scatter plot":
                    if verbose:
                        print(f"Use Scatter plot")
                    ax1.scatter(x=distances, y=corr, facecolors=fig_facecolor2, edgecolors=fig_edgecolor)

                    ax1.set_ylabel(f"Pairwise-similarity ({similarity_metric} on {data_to_correlate})",
                                   fontsize=font_size, labelpad=20, fontweight=fontweight,
                                   fontfamily=fontfamily)

                if correlation_plot_style == "Bar plot":
                    if verbose:
                        print(f"Use Bar plot")
                    # Make a distribution of mean similarity per distance bin:
                    order_to_sort = np.argsort(distances)
                    ordered_distances = np.sort(distances)
                    ordered_corr = corr[order_to_sort]

                    # Find the bin for each value:
                    if (n_lines is not None) and (n_cols is not None):
                        lines_size = n_lines * pixel_size
                        cols_size = n_cols * pixel_size
                        max_dist = np.sqrt(lines_size ** 2 + cols_size ** 2)
                    else:
                        max_dist = 1.1 * ordered_distances[-1]
                    binning = np.arange(start=0, stop=max_dist, step=binsize)
                    bin_ids = np.digitize(ordered_distances, bins=binning, right=True)
                    unique_bins = np.unique(bin_ids)

                    # Get the average and std of the pairwise similarity in each bin
                    mean_corr_per_bin = np.zeros(len(binning))
                    std_corr_per_bin = np.zeros(len(binning))
                    for bin_id in unique_bins:
                        corr_to_take = ordered_corr[np.where(bin_ids == bin_id)[0]]
                        mean_corr_per_bin[bin_id] = np.nanmean(corr_to_take)
                        std_corr_per_bin[bin_id] = np.nanstd(corr_to_take)

                    # Get ready for plot
                    bar_locs = binning[unique_bins]
                    bar_heigth = mean_corr_per_bin[unique_bins]
                    bar_error = std_corr_per_bin[unique_bins]
                    bar_width = binsize

                    ax1.bar(x=bar_locs, height=bar_heigth, yerr=bar_error, width=bar_width, bottom=0, align='edge',
                            color=fig_facecolor2, edgecolor=fig_edgecolor, ecolor=fig_edgecolor)

                    ax1.set_ylabel(f"Mean Pairwise-similarity ({similarity_metric} on {data_to_correlate})",
                                   fontsize=font_size, labelpad=20, fontweight=fontweight,
                                   fontfamily=fontfamily)

                # Common settings for Scatter plot and Bar plot
                ax1.yaxis.label.set_color(labels_color)
                ax1.set_xlabel(f"Distance (µm)",
                               fontsize=font_size, labelpad=20, fontweight=fontweight,
                               fontfamily=fontfamily)
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

                # Put it in a results table
                if epochs_to_use == 'full_recording':
                    # Get similarity table and append a column for distances
                    corelation_similarity_score_table = similarity_score_table
                    corelation_similarity_score_table['Distance (µm)'] = distances
                    # Append data table at each imaging session
                    correlation_general_table = correlation_general_table.append(corelation_similarity_score_table,
                                                                                 ignore_index=True)
                else:
                    # Get the similarity table from the last epoch analyzed
                    distance_only_table = similarity_score_table
                    # Drop  similarity values (they are from the last epoch we don't care and want distance only here)
                    distance_only_table = distance_only_table.drop('SimilarityScore')
                    distance_only_table['Distance (µm)'] = distances
                    # Append data table at each imaging session
                    distance_only_general_table = distance_only_general_table.append(distance_only_table,
                                                                                     ignore_index=True)

            self.update_progressbar(start_time, 100 / n_sessions)

        # Save results in table
        path_results = self.get_results_path()
        if save_table:
            n_rows = len(similarity_general_table.index)
            if epochs_to_use == 'full_recording':
                if verbose:
                    print(f" ")
                    print(f"----------------------------------- SAVINGS --------------------------------------")
                if compute_cell_dist:
                    table_name = f'{data_to_correlate}_pairwise_similarity_table_with_distances'
                    # Build a summary table:
                    table_to_sumarize = correlation_general_table.drop(
                        columns=['Cell_1#', 'Cell_1Type', 'Cell_2#', 'Cell_2Type'], axis=1)
                    table_sum = table_to_sumarize.groupby(['SubjectID', 'Session', 'PairType']).agg({'size', 'mean', 'median'})
                    # First do '.csv':
                    distance_table_path_csv = os.path.join(f'{path_results}', f'{table_name}.csv')
                    correlation_general_table.to_csv(distance_table_path_csv)
                    # Second do h5 file:
                    distance_table_path_h5 = os.path.join(f'{path_results}', f'{table_name}.h5')
                    similarity_general_table.to_hdf(distance_table_path_h5, "/data")
                    # Third do '.xlsx' only if relatively small table
                    if n_rows < 1000000:
                        distance_table_path = os.path.join(f'{path_results}', f'{table_name}.xlsx')
                        correlation_general_table.to_excel(distance_table_path)
                    # Save summary in xlsx format:
                    summary_distance_table_path_xlsx = os.path.join(f'{path_results}', f'{table_name}_summary.xlsx')
                    table_sum.to_excel(summary_distance_table_path_xlsx)

                else:
                    table_name = f'{data_to_correlate}_pairwise_similarity_table'
                    # Build a summary table:
                    table_to_sumarize = similarity_general_table.drop(
                        columns=['Cell_1#', 'Cell_1Type', 'Cell_2#', 'Cell_2Type'], axis=1)
                    table_sum = table_to_sumarize.groupby(['SubjectID', 'Session', 'PairType']).agg({'size', 'mean', 'median'})
                    # First do '.csv':
                    path_table_csv = os.path.join(f'{path_results}', f'{table_name}.csv')
                    similarity_general_table.to_csv(path_table_csv)
                    # Second do h5 file:
                    path_table_h5 = os.path.join(f'{path_results}', f'{table_name}.h5')
                    similarity_general_table.to_hdf(path_table_h5, "/data")
                    # Third do '.xlsx' only if relatively small table
                    if n_rows < 1000000:
                        path_table_xlsx = os.path.join(f'{path_results}', f'{table_name}.xlsx')
                        similarity_general_table.to_excel(path_table_xlsx)
                    # Save summary in xlsx format:
                    summary_distance_table_path_xlsx = os.path.join(f'{path_results}', f'{table_name}_summary.xlsx')
                    table_sum.to_excel(summary_distance_table_path_xlsx)
                if verbose:
                    print(f"Result tables are saved")
            else:
                if verbose:
                    print(f" ")
                    print(f"----------------------------------- SAVINGS --------------------------------------")
                # Fist save the distances between cells in each pair if it was computed
                if compute_cell_dist:
                    table_name = f'Cell_distance_table'
                    # Build a summary table:
                    table_to_sumarize = distance_only_general_table.drop(
                        columns=['Cell_1#', 'Cell_1Type', 'Cell_2#', 'Cell_2Type'], axis=1)
                    table_sum_distance = table_to_sumarize.groupby(['SubjectID', 'Session', 'PairType']).agg({'size', 'mean', 'median'})
                    # First do '.csv':
                    path_table_csv = os.path.join(f'{path_results}', f'{table_name}.csv')
                    distance_only_general_table.to_csv(path_table_csv)
                    # Second do h5 file:
                    path_table_h5 = os.path.join(f'{path_results}', f'{table_name}.h5')
                    distance_only_general_table.to_hdf(path_table_h5, "/data")
                    # Third do '.xlsx' only if relatively small table
                    if n_rows < 1000000:
                        path_table_xlsx = os.path.join(f'{path_results}', f'{table_name}.xlsx')
                        distance_only_general_table.to_excel(path_table_xlsx)
                    # Save summary in xlsx format:
                    summary_distance_table_path_xlsx = os.path.join(f'{path_results}', f'{table_name}_summary.xlsx')
                    table_sum_distance.to_excel(summary_distance_table_path_xlsx)

                # Second save the similarity epoch by epoch
                for key, data in similarity_general_table_dict.items():
                    table = similarity_general_table_dict.get(key)
                    n_rows_table = len(table.index)
                    table_name = f'{data_to_correlate}_{key}_pairwise_similarity_table'
                    # Build a summary table:
                    table_to_sumarize = table.drop(
                        columns=['Cell_1#', 'Cell_1Type', 'Cell_2#', 'Cell_2Type'], axis=1)
                    table_sum = table_to_sumarize.groupby(['SubjectID', 'Session', 'PairType']).agg({'size', 'mean', 'median'})
                    # First do '.csv':
                    path_table_csv = os.path.join(f'{path_results}', f'{table_name}.csv')
                    table.to_csv(path_table_csv)
                    # Second do h5 file:
                    path_table_h5 = os.path.join(f'{path_results}', f'{table_name}.h5')
                    table.to_hdf(path_table_h5, "/data")
                    # Third do '.xlsx' only if relatively small table
                    if n_rows_table < 1000000:
                        path_table_xlsx = os.path.join(f'{path_results}', f'{table_name}.xlsx')
                        table.to_excel(path_table_xlsx)
                    # Save summary in xlsx format:
                    summary_distance_table_path_xlsx = os.path.join(f'{path_results}', f'{table_name}_summary.xlsx')
                    table_sum.to_excel(summary_distance_table_path_xlsx)
                    if verbose:
                        print(f"Epoch: {key}. Result tables are saved")

        # Do some plots (from the tables)
        if do_plots:
            if verbose:
                print(f" ")
                print(f"----------------------------------- DO PLOTS --------------------------------------")

        # Do the plot according to GUI requirements
        if epochs_to_use == 'full_recording':
            if hue == "None":
                hue = None
                palette = None

            if similarity_metric == "Pearson":
                suffixe = "correlation"
            else:
                suffixe = "index"

            ylabel = "Pairwise Similarity " + similarity_metric + " " + suffixe

            filename = data_to_correlate + f"_{similarity_metric}_similarity_distribution_"

            fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                    gridspec_kw={'height_ratios': [1]},
                                    figsize=(width_fig, height_fig), dpi=dpi)
            ax1.set_facecolor(background_color)
            fig.patch.set_facecolor(background_color)

            svm = sns.catplot(x=x_axis_name, y="SimilarityScore", hue=hue, data=similarity_general_table,
                              hue_order=None, kind=kind, orient=None, color=fig_facecolor, palette=palette, ax=ax1)

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
        else:
            for key, data in similarity_general_table_dict.items():
                table = similarity_general_table_dict.get(key)
                if hue == "None":
                    hue = None
                    palette = None

                if similarity_metric == "Pearson":
                    suffixe = "correlation"
                else:
                    suffixe = "index"

                ylabel = "Pairwise Similarity " + similarity_metric + " " + suffixe + " during " + key

                filename = data_to_correlate + "_" + key + "_similarity_distribution_" + similarity_metric + "_method"

                fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                        gridspec_kw={'height_ratios': [1]},
                                        figsize=(width_fig, height_fig), dpi=dpi)
                ax1.set_facecolor(background_color)
                fig.patch.set_facecolor(background_color)

                svm = sns.catplot(x=x_axis_name, y="SimilarityScore", hue=hue, data=table,
                                  hue_order=None, kind=kind, orient=None, color=fig_facecolor, palette=palette, ax=ax1)

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

        print(f" ")
        print(f"DONE")
