from cicada.analysis.cicada_analysis import CicadaAnalysis
from cicada.utils.connectivity.connectivity_utils import build_pearson_adjacency_matrix
from cicada.utils.graphs.utils_graphs import build_graph_from_adjacency_matrix, plot_graph
from cicada.utils.graphs.graph_clustering import markov_clustering
from time import time
import numpy as np
from matplotlib.pylab import cm
from cicada.utils.display.colors import BREWER_COLORS
import os

class CicadaAssembliesGonzalezAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        CicadaAnalysis.__init__(self, name="Similarity Graph Clustering", family_id="Assemblies detection",
                                short_description="Gonzalez et al. 2019 Science",
                                config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaAssembliesGonzalezAnalysis(config_handler=self.config_handler)
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

        self.add_roi_response_series_arg_for_gui(short_description="Neural activity to use", long_description=None)

        key_names = [data.identifier for data in self._data_to_analyse]
        self.add_open_file_dialog_arg_for_gui(arg_name="adjacency_matrix_files",
                                              extensions="npy", mandatory=False,
                                              short_description="Saved adjacency matrix",
                                              long_description=None,
                                              key_names=key_names, family_widget=None)

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

        n_sessions = len(self._data_to_analyse)

        save_formats = kwargs.get("save_formats", "pdf")

        adjacency_matrix_files = kwargs.get("adjacency_matrix_files", None)
        if isinstance(adjacency_matrix_files, str):
            if len(self._data_to_analyse) > 1:
                # not matching the len of the data to analyse
                adjacency_matrix_files = None
            else:
                adjacency_matrix_files = {self._data_to_analyse[0].identifier: adjacency_matrix_files}

        for session_index, session_data in enumerate(self._data_to_analyse):
            session_identifier = session_data.identifier
            if verbose:
                print(f"-------------- {session_identifier} -------------- ")
            if isinstance(roi_response_series_dict, dict):
                roi_response_serie_info = roi_response_series_dict[session_identifier]
            else:
                roi_response_serie_info = roi_response_series_dict

            neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)

            neuronal_data_timestamps = session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_info)

            if adjacency_matrix_files is not None:
                adjacency_matrix = np.load(adjacency_matrix_files[session_identifier])
                print(f"adjacency_matrix.shape {adjacency_matrix.shape}")
            else:
                adjacency_matrix = build_pearson_adjacency_matrix(neuronal_data=neuronal_data,
                                                                  correlation_threshold=0.1,
                                                                  p_value_threshold=0.05,
                                                                  results_path=self.get_results_path(),
                                                                  data_id=session_identifier,
                                                                  verbose=int(verbose))
            graph = build_graph_from_adjacency_matrix(adjacency_matrix=adjacency_matrix, weight_on_edges=True,
                                                      directed_graph=True, symetric_matrix=False)
            plot_graph(graph=graph, filename=f"{session_identifier}_graph", iterations=2000,
                       node_color="red", edge_color="cornflowerblue",
                       with_labels=False, title=None, ax_to_use=None,
                       save_formats=save_formats, save_figure=True,
                       path_results=self.get_results_path(),
                       with_timestamp_in_file_name=False)
            # clusters is A list of tuples where each tuple represents a cluster and
            #               contains the indices of the nodes belonging to the cluster
            clusters = markov_clustering(graph, file_name=f'{session_identifier}_graph_clustered.pdf',
                                         results_path=self.get_results_path())
            # TODO: remove this temporary code
            # self.update_progressbar(time_started=self.analysis_start_time, increment_value=100 / n_sessions)
            # continue

            # print(f"Nb of clusters: {len(clusters)}")
            # for cluster_index, cluster in enumerate(clusters):
            #     print(f"Cluster {cluster_index}: {len(cluster)} cells")
            cluster_map = {node: cluster_index for cluster_index, cluster in enumerate(clusters) for node in cluster}
            n_cells_by_cluster_dict = {cluster_index: len(cluster) for cluster_index, cluster in enumerate(clusters)}
            node_colors = []
            n_clusters = 0
            # only coloring clusters with more than 2 cells
            for node in range(graph.number_of_nodes()):
                cluster_index = cluster_map[node]
                n_cells_in_cluster = n_cells_by_cluster_dict[cluster_index]
                if n_cells_in_cluster < 3:
                    node_colors.append("silver")
                else:
                    node_colors.append(BREWER_COLORS[n_clusters % len(BREWER_COLORS)])
                    n_clusters += 1
            print(f"n_clusters {n_clusters}")

            plot_graph(graph=graph, filename=f"{session_identifier}_graph_with_clusters",
                       node_color=node_colors, edge_color="silver",
                       node_size=20,
                       with_labels=False, title=None, ax_to_use=None,
                       save_formats=save_formats, save_figure=True,
                       path_results=self.get_results_path(),
                       with_timestamp_in_file_name=False)
            if verbose:
                print(" ")
            self.update_progressbar(time_started=self.analysis_start_time, increment_value=100 / n_sessions)

        print(f"Similarity Graph Clustering (Gonzalez) analysis run in {time() - self.analysis_start_time} sec")
