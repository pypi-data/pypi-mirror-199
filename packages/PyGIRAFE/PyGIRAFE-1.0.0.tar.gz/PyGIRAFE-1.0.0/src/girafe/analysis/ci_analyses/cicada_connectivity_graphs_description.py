from cicada.analysis.cicada_analysis import CicadaAnalysis
from cicada.utils.graphs.utils_graphs import build_connectivity_graphs
from cicada.utils.misc import get_yang_frames, from_timestamps_to_frame_epochs, get_continous_time_periods, \
    print_info_dict
from time import time
from datetime import datetime
import os
import numpy as np
import networkx as nx
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class CicadaConnectivityGraphsDescription(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        long_description = '<p align="center"><b>Do some statistics on connectivity graph</b></p><br>'
        long_description = long_description + 'Describe the connectivity graphs: return the density of the graph,' \
                                              ' return for each cell its number of predecessors and successors.<br><br>'
        long_description = long_description + 'Do some plots and save results in csv and xlxs formats'
        CicadaAnalysis.__init__(self, name="Connectivity graphs description", family_id="Connectivity",
                                short_description="Give basic stats on graphs",
                                long_description=long_description, config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaConnectivityGraphsDescription(config_handler=self.config_handler)
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

        self.add_int_values_arg_for_gui(arg_name="time_delay", min_value=100, max_value=1500,
                                        short_description="Time delay in ms to look for connected cells ",
                                        default_value=500, family_widget="figure_config_graph")

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
                                     family_widget="figure_config_graph")

        self.add_bool_option_for_gui(arg_name="save_table", true_by_default=True,
                                     short_description="Save results in tables",
                                     family_widget="figure_config_saving")

        self.add_bool_option_for_gui(arg_name="save_figure", true_by_default=True,
                                     short_description="Save figures",
                                     family_widget="figure_config_saving")

        representations = ["strip", "swarm", "violin", "box", "bar", "boxen"]
        self.add_choices_arg_for_gui(arg_name="representation_density", choices=representations,
                                     default_value="bar",
                                     short_description="Plot to use for 'Graph-density' figure",
                                     multiple_choices=False,
                                     family_widget="figure_density_config_representation")

        x_ax = ["Age", "SubjectID", "Session"]
        self.add_choices_arg_for_gui(arg_name="x_axis_density", choices=x_ax,
                                     default_value="Age", short_description="Variable to use for x axis groups",
                                     multiple_choices=False,
                                     family_widget="figure_density_config_representation")

        possible_hues = ["Age", "SubjectID", "Session", "None"]
        self.add_choices_arg_for_gui(arg_name="hue_density", choices=possible_hues,
                                     default_value="None",
                                     short_description="Variable to use for x axis sub-groups",
                                     multiple_choices=False,
                                     family_widget="figure_density_config_representation")

        palettes = ["muted", "deep", "pastel", "Blues"]
        self.add_choices_arg_for_gui(arg_name="palettes_density", choices=palettes,
                                     default_value="muted", short_description="Color palette for subgroups",
                                     long_description="In that case figure facecolor and figure edgecolor are useless",
                                     multiple_choices=False,
                                     family_widget="figure_density_config_representation")

        representations = ["strip", "swarm", "violin", "box", "bar", "boxen"]
        self.add_choices_arg_for_gui(arg_name="representation_connectivity", choices=representations,
                                     default_value="box",
                                     short_description="Plot to use for 'Connectivity' figure",
                                     multiple_choices=False,
                                     family_widget="figure_connectivity_config_representation")

        x_ax = ["Age", "SubjectID", "Session", "Celltype"]
        self.add_choices_arg_for_gui(arg_name="x_axis_connectivity", choices=x_ax,
                                     default_value="Age", short_description="Variable to use for x axis groups",
                                     multiple_choices=False,
                                     family_widget="figure_connectivity_config_representation")

        possible_hues = ["Age", "SubjectID", "Session", "Celltype", "None"]
        self.add_choices_arg_for_gui(arg_name="hue_connectivity", choices=possible_hues,
                                     default_value="None",
                                     short_description="Variable to use for x axis sub-groups",
                                     multiple_choices=False,
                                     family_widget="figure_connectivity_config_representation")

        palettes = ["muted", "deep", "pastel", "Blues"]
        self.add_choices_arg_for_gui(arg_name="palettes_connectivity", choices=palettes,
                                     default_value="muted", short_description="Color palette for subgroups",
                                     long_description="In that case figure facecolor and figure edgecolor are useless",
                                     multiple_choices=False,
                                     family_widget="figure_connectivity_config_representation")

        self.add_image_format_package_for_gui()

        self.add_color_arg_for_gui(arg_name="background_color", default_value=(0, 0, 0, 1.),
                                   short_description="background color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="fig_facecolor", default_value=(1, 1, 1, 1.),
                                   short_description="Figure face color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="axis_color", default_value=(1, 1, 1, 1.),
                                   short_description="Axes color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="label_color", default_value=(1, 1, 1, 1.),
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

        verbose = kwargs.get("verbose", True)

        time_delay = kwargs.get("time_delay")

        epoch_or_not = kwargs.get("epoch_or_not")

        epoch_group = kwargs.get("epochs_names")

        save_graphs = kwargs.get("save_graphs")

        force_path_to_graph = kwargs.get("force_path_to_graph")

        save_table = kwargs.get("save_table")

        x_axis_name_density = kwargs.get("x_axis_density")

        kind_density = kwargs.get("representation_density")

        hue_density = kwargs.get("hue_density")

        palette_density = kwargs.get("palettes_density")

        x_axis_name_connectivity = kwargs.get("x_axis_connectivity")

        kind_connectivity = kwargs.get("representation_connectivity")

        hue_connectivity = kwargs.get("hue_connectivity")

        palette_connectivity = kwargs.get("palettes_connectivity")

        fig_facecolor = kwargs.get("fig_facecolor")

        background_color = kwargs.get("background_color")

        labels_color = kwargs.get("label_color")

        axis_color = kwargs.get("axis_color")

        font_size = kwargs.get("axis_label_size", 20)

        fontweight = kwargs.get("fontweight")

        fontfamily = kwargs.get("font_type")

        # image package format
        save_formats = kwargs["save_formats"]
        if save_formats is None:
            save_formats = "pdf"

        save_figure = True

        dpi = kwargs.get("dpi", 100)

        width_fig = kwargs.get("width_fig")

        height_fig = kwargs.get("height_fig")

        with_timestamp_in_file_name = kwargs.get("with_timestamp_in_file_name", True)

        path_results = self.get_results_path()

        print("Connectivity graphs description: coming soon...")
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

        graph_density_table = pd.DataFrame()
        global_single_cell_info_table = pd.DataFrame()
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
            samp_r = session_data.get_ci_movie_sampling_rate(only_2_photons=True)

            # Get Neuronal Data
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

            # Check if graphs are already built
            group_name = []
            for epoch_group_name, epoch_info in epoch_group.items():
                if len(epoch_info) != 2:
                    continue
                group_name.append(epoch_group_name)

            if epoch_or_not == 'one_epoch':
                filename = session_identifier + "_connectivity_graphs_" + str(time_delay) + "ms_all_cells" + "_" + group_name[0]
            else:
                filename = session_identifier + "_connectivity_graphs_" + str(time_delay) + "ms_all_cells"
            path_to_graph_graphml = os.path.join(f'{path_to_graphs}', f'{filename}.graphml')

            files_check = [os.path.isfile(path_to_graph_graphml)]

            if all(files_check) is True:
                if verbose:
                    print(f"All graph file is already computed, just load it")
                connectivity_graph = nx.read_graphml(path=path_to_graph_graphml, node_type=int)
            else:
                if verbose:
                    print(f"Graphs files are not found")
                    print(f"Starting to build the connectivity graphs")

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
                                intervals_frames = from_timestamps_to_frame_epochs(
                                    time_stamps_array=epochs_timestamps,
                                    frames_timestamps=neuronal_data_timestamps,
                                    as_list=True)
                                epochs_frames_in_group.extend(intervals_frames)
                        frames_in_epoch.extend(epochs_frames_in_group)

                    # Use epoch frames as a mask to put every frame out of epoch at 0 #
                    out_of_epoch_frames = get_yang_frames(total_frames=n_frames, yin_frames=frames_in_epoch)[1]
                    raster[:, out_of_epoch_frames] = 0
                else:
                    pass

                connectivity_graph = build_connectivity_graphs(raster, sampling_rate=samp_r,
                                                               time_delay=time_delay,
                                                               save_graphs=save_graphs,
                                                               path_results=path_to_graphs,
                                                               filename=filename,
                                                               with_timestamp_in_file_name=False,
                                                               verbose=verbose)
                if verbose:
                    print(f"Connectivity graphs are built")

            if verbose:
                print(f"Get some statistics of the graph")

            # 1/ Get graph density and build table for density across ages (each row of the table is a session)
            graph_density = nx.density(connectivity_graph)
            graph_density = graph_density * 100
            sum_up_data = {'Age': info_dict['age'], 'Weight': info_dict['weight'], 'SubjectID': info_dict['subject_id'],
                           'Session': session_identifier, 'GraphDensity': [graph_density]}
            data_frame = pd.DataFrame(sum_up_data)
            graph_density_table = graph_density_table.append(data_frame, ignore_index=True)

            # 2/ Describe graph at single cell level
            n_successors_list = []
            out_connectivity_degree_list = []
            n_predecessors_list = []
            in_connectivity_degree_list = []
            n_neighbors_list = []
            all_connectivity_degree_list = []
            type_in_connected_cells_dict = {name: [[] for cell in range(n_cells)] for name in unique_types_list}
            connected_type_in_type_dict = {name: [[] for cell in range(n_cells)] for name in unique_types_list}
            cell_indices = []
            for cell in range(n_cells):
                # info 1: degree of connectivity of each cell
                successors_list = list(connectivity_graph.successors(cell))
                n_successors = len(successors_list)

                predecessors_list = list(connectivity_graph.predecessors(cell))
                n_predecessors = len(predecessors_list)

                all_neighbors_list = successors_list + predecessors_list
                n_neighbors = n_successors + n_predecessors

                n_neighbors_list.append(n_neighbors)
                n_successors_list.append(n_successors)
                n_predecessors_list.append(n_predecessors)

                percentage_all_connections = (n_neighbors / n_cells) * 100
                all_connectivity_degree_list.append(percentage_all_connections)

                percentage_out_connections = (n_successors / n_cells) * 100
                out_connectivity_degree_list.append(percentage_out_connections)

                percentage_in_connections = (n_predecessors / n_cells) * 100
                in_connectivity_degree_list.append(percentage_in_connections)

                cell_indices.append(cell)

                # Use cell-type information
                for celltype, info in type_in_connected_cells_dict.items():
                    type_name = celltype.lower()
                    type_indexes = cell_indices_by_cell_type.get(type_name)
                    if type_indexes is None:
                        continue
                    n_cell_this_type = len(type_indexes)
                    if n_neighbors > 0 and n_cell_this_type > 0:
                        n_connected_type = len(np.intersect1d(all_neighbors_list, type_indexes))
                        type_in_connected_cells = (n_connected_type / n_neighbors) * 100
                        connected_type_in_type = (n_connected_type / n_cell_this_type) * 100
                        # print(f"connected_type_in_type: {connected_type_in_type}")
                    else:
                        type_in_connected_cells = 'NA'
                        connected_type_in_type = 'NA'

                    data_type_in_connected_cells = type_in_connected_cells_dict.get(celltype)
                    data_type_in_connected_cells[cell] = type_in_connected_cells
                    dico1 = {celltype: data_type_in_connected_cells}
                    type_in_connected_cells_dict.update(dico1)

                    data_connected_type_in_type_dict = connected_type_in_type_dict.get(celltype)
                    data_connected_type_in_type_dict[cell] = connected_type_in_type
                    dico2 = {celltype: data_connected_type_in_type_dict}
                    connected_type_in_type_dict.update(dico2)

            # Build the table (in the table each row is a cell)
            age_list = [info_dict['age'] for k in range(n_cells)]
            weight_list = [info_dict['weight'] for k in range(n_cells)]
            session_identifier_list = [session_identifier for k in range(n_cells)]
            animal_id_list = [info_dict['subject_id'] for k in range(n_cells)]
            single_cell_info_dict = {'Age': age_list, 'Weight': weight_list, 'SubjectID': animal_id_list,
                                     'Session': session_identifier_list,
                                     'Cell': cell_indices,
                                     'Celltype': cell_type_list,
                                     'N_Predecessors': n_predecessors_list,
                                     'DegreeOfInConnectivity (%)': in_connectivity_degree_list,
                                     'N_Successors': n_successors_list,
                                     'DegreeOfOutConnectivity (%)': out_connectivity_degree_list,
                                     'N_Neighbors': n_neighbors_list,
                                     'DegreeOfConnectivity (%)': all_connectivity_degree_list}

            for index, celltype in enumerate(unique_types_list):
                name1 = celltype + '_in_connected_cells' + ' (%)'
                data1 = type_in_connected_cells_dict.get(celltype)
                single_cell_info_dict[name1] = data1

                name2 = 'connected_' + celltype + '_in_' + celltype + ' (%)'
                data2 = connected_type_in_type_dict.get(celltype)
                single_cell_info_dict[name2] = data2

            single_cell_info_table = pd.DataFrame(single_cell_info_dict)
            global_single_cell_info_table = global_single_cell_info_table.append(single_cell_info_table,
                                                                                 ignore_index=True)

            self.update_progressbar(start_time, 100 / n_sessions)

        # Save results in table
        if save_table:
            if verbose:
                print(f"----------------------------------- SAVINGS --------------------------------------")
            path_results = self.get_results_path()
            if epoch_or_not == 'one_epoch':
                path_table_xls = os.path.join(f'{path_results}',
                                              f'{str(time_delay)}ms_graphs_density_table_{group_name[0]}.xlsx')
                path_table_csv = os.path.join(f'{path_results}',
                                              f'{str(time_delay)}ms_graphs_density_table_{group_name[0]}.csv')
                path_cell_table_xls = os.path.join(f'{path_results}',
                                                   f'{str(time_delay)}ms_cell_connectivity_table_{group_name[0]}.xlsx')
                path_cell_table_csv = os.path.join(f'{path_results}',
                                                   f'{str(time_delay)}ms_cell_connectivity_table_{group_name[0]}.csv')
            else:
                path_table_xls = os.path.join(f'{path_results}',
                                              f'{str(time_delay)}ms_graphs_density_table.xlsx')
                path_table_csv = os.path.join(f'{path_results}',
                                              f'{str(time_delay)}ms_graphs_density_table.csv')
                path_cell_table_xls = os.path.join(f'{path_results}',
                                                   f'{str(time_delay)}ms_cell_connectivity_table.xlsx')
                path_cell_table_csv = os.path.join(f'{path_results}',
                                                   f'{str(time_delay)}ms_cell_connectivity_table.csv')
            if save_table:
                graph_density_table.to_excel(path_table_xls)
                graph_density_table.to_csv(path_table_csv)
                global_single_cell_info_table.to_excel(path_cell_table_xls)
                global_single_cell_info_table.to_csv(path_cell_table_csv)
                if verbose:
                    print(f"Data save as excel and csv files")

        # Do the plots
        if save_table:
            if verbose:
                print(f"------------------------------ DO SOME PLOTTING ---------------------------------")

        # Do the graph density plot according to GUI requirements
        if hue_density == "None":
            hue_density = None
            palette_density = None

        ylabel = "Graph density % of all possible connections (%)"

        filename = "graph_density_"

        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(width_fig, height_fig), dpi=dpi)

        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)

        svm = sns.catplot(x=x_axis_name_density, y="GraphDensity", hue=hue_density, data=graph_density_table,
                          hue_order=None, kind=kind_density, orient=None, color=fig_facecolor, palette=palette_density,
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

        # Do the degree of connectivity plot according to GUI requirements
        if hue_connectivity == "None":
            hue_connectivity = None
            palette_connectivity = None

        ylabel = "Degree of cell-connectivity (%)"

        filename = "connectivity_"

        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(width_fig, height_fig), dpi=dpi)
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)

        svm = sns.catplot(x=x_axis_name_connectivity, y="DegreeOfConnectivity (%)", hue=hue_connectivity,
                          data=global_single_cell_info_table, hue_order=None, kind=kind_connectivity,
                          orient=None, color=fig_facecolor, palette=palette_connectivity, ax=ax1)

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
            print(f"------------------------------- ANALYSIS DONE ----------------------------------")
