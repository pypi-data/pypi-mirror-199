from cicada.analysis.cicada_analysis import CicadaAnalysis
from time import time
import numpy as np
from cicada.utils.graphs.utils_graphs import build_connectivity_graphs
from cicada.utils.graphs.utils_graphs import plot_graph
from cicada.utils.graphs.utils_graphs import plot_connectivity_graphs
from cicada.utils.misc import validate_indices_in_string_format, extract_indices_from_string, print_info_dict
from cicada.utils.misc import get_yang_frames, from_timestamps_to_frame_epochs, get_continous_time_periods
import os
import networkx as nx
import matplotlib.colors


class CicadaConnectivityGraph(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        long_description = '<p align="center"><b>Build and display connectivity graph</b></p><br>'
        long_description = long_description + 'Build and save a directed graph showing cell connectivity ' \
                                              '(as defined in Bonifazi 2009).<br><br>'
        long_description = long_description + 'Nodes of the graph can be colored according to the cell-type.<br><br>'
        long_description = long_description + 'For each session the graph is saved in graphml and gexf formats'
        CicadaAnalysis.__init__(self, name="Connectivity graph", family_id="Connectivity",
                                short_description="Build connectivity graph (for connectivity see Bonifazi, 2009)",
                                long_description=long_description,
                                config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaConnectivityGraph(config_handler=self.config_handler)
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

        self.add_bool_option_for_gui(arg_name="color_by_cell_type", true_by_default=True,
                                     short_description="Color each node of the graph based on cell-type",
                                     family_widget="figure_config_celltypes")

        all_cell_types = []
        for data_to_analyse in self._data_to_analyse:
            all_cell_types.extend(data_to_analyse.get_all_cell_types())

        all_cell_types = list(set(all_cell_types))

        self.add_choices_for_groups_for_gui(arg_name="cells_groups", choices=all_cell_types,
                                            with_color=True,
                                            mandatory=False,
                                            short_description="Groups of cells to color",
                                            long_description="Select cells's groups you want to color in the raster",
                                            family_widget="cell_type",
                                            add_custom_group_field=True,
                                            custom_group_validation_fct=validate_indices_in_string_format,
                                            custom_group_processor_fct=None)

        self.add_bool_option_for_gui(arg_name="sort_raster_by_cell_type", true_by_default=False,
                                     short_description="Sort raster cells' groups ",
                                     family_widget="cell_type")

        self.add_int_values_arg_for_gui(arg_name="time_delay", min_value=100, max_value=1500,
                                        short_description="Time delay in ms to look for connected cells ",
                                        default_value=500, family_widget="figure_config_delay")

        possibilities = ['full_recording', 'one_epoch']
        self.add_choices_arg_for_gui(arg_name="epoch_or_not", choices=possibilities,
                                     default_value="full_recording",
                                     short_description="Compute the connectivity over the full recording or "
                                                       "on a specific epoch",
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
                                            short_description="Behaviors to group: compute connectivity on ONE epoch",
                                            long_description="Here you need to specify which individual behaviors "
                                                             "belong to the epoch ('group')",
                                            family_widget="epochs")

        self.add_bool_option_for_gui(arg_name="save_graphs", true_by_default=True,
                                     short_description="Save graph",
                                     family_widget="figure_config_data")

        self.add_bool_option_for_gui(arg_name="plot_them_all", true_by_default=False,
                                     short_description="Do a figure with all graphs",
                                     family_widget="figure_config_data")

        self.add_bool_option_for_gui(arg_name="do_plot_graphs", true_by_default=True,
                                     short_description="Plot the graphs",
                                     family_widget="figure_config_data")

        self.add_image_format_package_for_gui()

        self.add_color_arg_for_gui(arg_name="background_color", default_value=(0, 0, 0, 1.),
                                   short_description="background color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="fig_facecolor", default_value=(1, 1, 1, 1.),
                                   short_description="Figure face color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="fig_edgecolor", default_value=(1, 1, 1, 1.),
                                   short_description="Figure edge color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="axis_color", default_value=(1, 1, 1, 1.),
                                   short_description="Axes color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="axes_label_color", default_value=(1, 1, 1, 1.),
                                   short_description="Axes label color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="ticks_labels_color", default_value=(1, 1, 1, 1.),
                                   short_description="Axes ticks labels color",
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

        self.add_field_text_option_for_gui(arg_name="force_path_to_graph", default_value="",
                                           short_description="Specify a path to load and/or save all the graph files",
                                           long_description=None, family_widget="figure_config_savings")

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

        start_time = time()

        roi_response_series_dict = kwargs["roi_response_series"]

        cell_to_use = kwargs.get("cell_to_use")

        color_by_cell_type = kwargs.get("color_by_cell_type")

        cells_groups_dict = kwargs.get("cells_groups")

        verbose = kwargs.get("verbose", True)

        time_delay = kwargs.get("time_delay")

        epoch_or_not = kwargs.get("epoch_or_not")

        epoch_group = kwargs.get("epochs_names")

        save_graphs = kwargs.get("save_graphs")

        force_path_to_graph = kwargs.get("force_path_to_graph")

        do_plot_graphs = kwargs.get("do_plot_graphs")

        plot_them_all = kwargs.get("plot_them_all")

        fig_facecolor = kwargs.get("fig_facecolor")
        figure_facecolor = matplotlib.colors.to_hex(fig_facecolor, keep_alpha=False)

        fig_edgecolor = kwargs.get("fig_edgecolor")
        figure_edgecolor = matplotlib.colors.to_hex(fig_edgecolor, keep_alpha=False)

        background_color = kwargs.get("background_color")

        # image package format
        save_formats = kwargs["save_formats"]
        if save_formats is None:
            save_formats = "pdf"

        save_figure = True

        dpi = kwargs.get("dpi", 100)

        width_fig = kwargs.get("width_fig")

        height_fig = kwargs.get("height_fig")

        with_timestamps_in_file_name = kwargs.get("with_timestamp_in_file_name", True)

        path_results = self.get_results_path()

        print("Connectivity graphs: coming soon...")
        n_sessions = len(self._data_to_analyse)

        if verbose:
            print(f"{n_sessions} sessions to analyse")

        # Create saving folder for graphs if necessary
        if bool(force_path_to_graph) is False or force_path_to_graph.isspace() is True:
            if verbose:
                print(f"No specified folder to save the graph, look in {os.path.dirname(path_results)}")
            tmp_path = os.path.dirname(path_results)
            folder_to_save_graphs = "Connectivity_graphs"
            path_to_graphs = os.path.join(f'{tmp_path}', f'{folder_to_save_graphs}')
            if os.path.isdir(path_to_graphs) is False:
                os.mkdir(path_to_graphs)
                if verbose:
                    print(f"No directory found to save the graphs, create directory at : {path_to_graphs}")
            else:
                if verbose:
                    print(f"Folder to save graph already here, save the graphs in : {path_to_graphs}")
        else:
            path_to_graphs = force_path_to_graph
            if verbose:
                print(f"All graphs will be loaded and save in: {path_to_graphs}")

        session_id_list = []
        fig_facecolor_list = [[] for session in range(n_sessions)]
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
            neuronal_data_timestamps = session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_info)
            duration_s = neuronal_data_timestamps[len(neuronal_data_timestamps)-1] - neuronal_data_timestamps[0]
            duration_m = duration_s / 60
            if verbose:
                print(f"Acquisition last for : {duration_s} seconds // {duration_m} minutes ")

            neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)
            raster_dur = neuronal_data
            [n_cells, n_frames] = raster_dur.shape

            # Build raster from raster_dur #
            raster = np.zeros((n_cells, n_frames), dtype="int8")
            for cell in range(n_cells):
                tmp_tple = get_continous_time_periods(raster_dur[cell, :])
                for tple in range(len(tmp_tple)):
                    onset = tmp_tple[tple][0]
                    raster[cell, onset] = 1

            samp_r = session_data.get_ci_movie_sampling_rate(only_2_photons=True)

            if verbose:
                print(f"N cells: {n_cells}, N frames: {n_frames}")
                print(f"Sampling rate: {samp_r} frames/second")

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

            # Check Data with respect to the specific analysis
            type_required = cell_to_use.capitalize()
            if type_required != "All_cells":
                if type_required not in cell_type_list:
                    if verbose:
                        print(f"No {type_required} identified in this session. Cannot do the graph for this session")
                    continue
            session_id_list.append(session_identifier)

            # Filter raster to keep the cell to use
            if cell_to_use == "all_cells":
                raster_to_use = raster
            else:
                index_to_keep = cell_indices_by_cell_type.get(cell_to_use)
                raster_to_use = raster[index_to_keep, :]

            # Filter the raster to keep only the spikes in a given epoch #
            if epoch_or_not == 'one_epoch':
                # Get the rest frames of this session if 'rest' is not already defined as a behavior
                data_behaviors_list = session_data.get_behavioral_epochs_names()
                behaviors_list = [name.lower() for name in data_behaviors_list]
                if 'rest' not in behaviors_list:
                    active_frames = []
                    for behavior in behaviors_list:
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
                    intervals_rest_frames = get_continous_time_periods(deducted_rest_frames)

                # Get the frames included in the defined epoch
                frames_in_epoch = []
                group_name = []
                for epoch_group_name, epoch_info in epoch_group.items():
                    if len(epoch_info) != 2:
                        continue
                    group_name.append(epoch_group_name)

                    epochs_names_in_group = epoch_info[0]
                    if verbose:
                        print(f"Restricting connectivity analysis to {epoch_group_name}, "
                              f"that includes: {epochs_names_in_group}")

                    # Loop on all the epochs included in the main epoch
                    epochs_frames_in_group = []
                    for epoch_name in epochs_names_in_group:
                        if epoch_name == 'rest' and 'rest' not in behaviors_list:
                            epochs_frames_in_group.extend(intervals_rest_frames)
                            if verbose:
                                print(f"'rest' is not an already defined behavior, it will be deducted by the "
                                      f"ensemble of all frames in none of all defined behaviors")
                        else:
                            # looking in behaviors
                            epochs_timestamps = session_data.get_behavioral_epochs_times(epoch_name=epoch_name)
                            if epochs_timestamps is None:
                                # means this session doesn't have this epoch name
                                continue
                            # now we want to get the intervals time_stamps and convert them in frames
                            intervals_frames = from_timestamps_to_frame_epochs(time_stamps_array=epochs_timestamps,
                                                                               frames_timestamps=neuronal_data_timestamps,
                                                                               as_list=True)
                            epochs_frames_in_group.extend(intervals_frames)
                    frames_in_epoch.extend(epochs_frames_in_group)

                # Use epoch frames as a mask to put every frame out of epoch at 0 #
                out_of_epoch_frames = get_yang_frames(total_frames=n_frames, yin_frames=frames_in_epoch)[1]
                raster_to_use[:, out_of_epoch_frames] = 0
            else:
                pass

            # Deal with nodes color
            if len(unique_types_list) >= 2 and color_by_cell_type and cell_to_use == "all_cells":
                figure_facecolor = [[] for neuron in range(n_cells)]
                colors = ['#b50d0d', '#435fec', '#e9473f', '#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99',
                          '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928']
                color_to_use = 0
                for key, info in cell_indices_by_cell_type.items():
                    indexes = cell_indices_by_cell_type.get(key)
                    tmp_n_cell = len(indexes)
                    for cell in range(tmp_n_cell):
                        tmp_index = indexes[cell]
                        figure_facecolor[tmp_index] = colors[color_to_use]
                    color_to_use = color_to_use + 1
            elif (cells_groups_dict is not None) and (len(cells_groups_dict) > 0):
                figure_facecolor = [figure_facecolor for neuron in range(n_cells)]
                cell_indices_by_cell_type = session_data.get_cell_indices_by_cell_type(roi_serie_keys=
                                                                                       roi_response_serie_info)
                cells_added = []
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
                        if len(cell_indices) == 0:
                            continue
                        for cell in cell_indices:
                            figure_facecolor[cell] = cells_group_color
                        cells_added.extend(list(cell_indices))
                # cells_left = np.setdiff1d(np.arange(len(neuronal_data)), cells_added)

            # else:
            #     figure_facecolor = figure_facecolor
            fig_facecolor_list[session_index] = figure_facecolor

            # Check if graphs are already built
            if epoch_or_not == 'one_epoch':
                filename = session_identifier + "_connectivity_graphs_" + str(time_delay) + "ms_" + cell_to_use + "_" + group_name[0]
            else:
                filename = session_identifier + "_connectivity_graphs_" + str(time_delay) + "ms_" + cell_to_use
            path_to_graph_graphml = os.path.join(f'{path_to_graphs}', f'{filename}.graphml')

            files_check = [os.path.isfile(path_to_graph_graphml)]

            if all(files_check) is True:
                if verbose:
                    print(f"Graph file is already computed, just load it")
                connectivity_graph = nx.read_graphml(path=path_to_graph_graphml, node_type=int)
            else:
                if verbose:
                    print(f"Graph file is not found")
                    print(f"Starting to build the connectivity graphs")
                connectivity_graph = build_connectivity_graphs(raster=raster_to_use, sampling_rate=samp_r,
                                                               time_delay=time_delay,
                                                               save_graphs=save_graphs,
                                                               path_results=path_to_graphs,
                                                               filename=filename,
                                                               with_timestamp_in_file_name=False,
                                                               verbose=verbose)
                if verbose:
                    print(f"Connectivity graph is built")

            if do_plot_graphs:
                if verbose:
                    print(f"Plot Connectivity graph")
                if epoch_or_not == 'one_epoch':
                    graph_title = session_identifier + " " + type_required + " " + group_name[0]
                else:
                    graph_title = session_identifier + " " + type_required
                plot_graph(connectivity_graph,  with_fa2=False, randomized_positions=True,
                           filename=filename,
                           iterations=2000,
                           node_color=figure_facecolor, edge_color=figure_edgecolor, background_color=background_color,
                           with_labels=False, title=graph_title,
                           ax_to_use=None,
                           save_formats=save_formats, save_figure=save_figure,
                           path_results=self.get_results_path(),
                           with_timestamp_in_file_name=with_timestamps_in_file_name)

            self.update_progressbar(start_time, 100 / n_sessions)

        if plot_them_all:
            if verbose:
                print(f"Plotting figure with all graphs")
            plot_connectivity_graphs(session_id_list, graph_files_path=path_to_graphs,
                                     background_color=background_color,
                                     node_color=fig_facecolor_list, edge_color=figure_edgecolor,
                                     size_fig=(width_fig, height_fig),
                                     save_formats=save_formats, save_figure=save_figure,
                                     path_results=self.get_results_path(),
                                     with_timestamp_in_file_name=with_timestamps_in_file_name, celltype=cell_to_use,
                                     time_delay=time_delay)

        print(f"Analysis done")
