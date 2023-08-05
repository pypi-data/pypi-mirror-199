import numpy as np
import networkx as nx
from girafe.utils.misc import get_continous_time_periods
from scipy import stats
import os
from datetime import datetime
# from fa2 import ForceAtlas2
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import math
import random


def build_connectivity_graphs(raster, sampling_rate, time_delay=500, save_graphs=False,
                              path_results=None, filename=None, with_timestamp_in_file_name=True, verbose=None):

    # Extract raster size #
    [n_cells, n_frames] = raster.shape

    # Convert time delay in frames #
    time_delay_s = time_delay / 1000
    frames_delay = int(np.round(time_delay_s * sampling_rate))
    if verbose:
        print(f"Delay in ms : {time_delay} ms")
        print(f"Sampling rate : {sampling_rate} frames/second")
        print(f"Delay in frames : {frames_delay} frames")

    # look neuron by neuron, at each spike and make a pair wise for each other neurons according to the spike
    # distribution around 500ms before and after. If the distribution is not uniform then we look where is the max
    # and we add it to n_out or n_in if before or after. If it is at the same time, then we don't add it.

    # building graph using Networkx package
    # DiGraph means directed graph
    connectivity_graph = nx.DiGraph()
    connectivity_graph.add_nodes_from(np.arange(n_cells))
    for neuron in np.arange(n_cells):
        neurons_to_consider = np.arange(n_cells)
        mask = np.ones(n_cells, dtype="bool")
        mask[neuron] = False
        neurons_to_consider = neurons_to_consider[mask]
        # look at onsets
        neuron_spikes, = np.where(raster[neuron, :])
        # is_early_born = (neuron == ms.early_born_cell)

        if len(neuron_spikes) == 0:
            continue

        spike_nums_to_use = raster

        distribution_array_2_d = np.zeros((n_cells, ((frames_delay * 2) + 1)), dtype="int16")

        event_index = frames_delay
        # looping on each spike of the main neuron
        # to build the distribution of each other neurons around the spikes of this one
        for n, event in enumerate(neuron_spikes):
            # only taking in consideration events that are not too close from bottom range or upper range
            min_limit = max(event - frames_delay, 0)
            max_limit = min((event + frames_delay), (n_frames - 1))
            mask = np.zeros((n_cells, ((frames_delay * 2) + 1)), dtype=bool)
            mask_start = 0
            if (event - frames_delay) < 0:
                mask_start = -1 * (event - frames_delay)
            mask_end = mask_start + (max_limit - min_limit) + 1
            # print(f"")
            mask[:, mask_start:mask_end] = spike_nums_to_use[:, min_limit:(max_limit + 1)] > 0
            distribution_array_2_d[mask] = distribution_array_2_d[mask] + 1

        # going neuron by neuron
        for neuron_to_consider in neurons_to_consider:
            distribution_array = distribution_array_2_d[neuron_to_consider, :]
            distribution_for_test = np.zeros(np.sum(distribution_array))
            frames_time = np.arange(-frames_delay, frames_delay + 1)
            i_n = 0
            for i_time, sum_spike in enumerate(distribution_array):
                if sum_spike > 0:
                    distribution_for_test[i_n:i_n + sum_spike] = frames_time[i_time]
                    i_n += sum_spike

            if len(distribution_for_test) >= 20:
                stat_n, p_value = stats.normaltest(distribution_for_test)
                ks, p_ks = stats.kstest(distribution_for_test, stats.randint.cdf,
                                        args=(np.min(distribution_for_test),
                                              np.max(distribution_for_test)))

                is_normal_distribution = p_value >= 0.05
                is_uniform_distribution = p_ks >= 0.05
                # if the distribution is normal or uniform, we skip it
                if is_normal_distribution or is_uniform_distribution:
                    continue
                else:
                    n_in_sum = np.sum(distribution_array[:event_index])
                    n_out_sum = np.sum(distribution_array[(event_index + 1):])
                    if n_in_sum > n_out_sum:
                        connectivity_graph.add_edge(neuron_to_consider, neuron)
                    if n_in_sum < n_out_sum:
                        connectivity_graph.add_edge(neuron, neuron_to_consider)
            else:
                continue

    if save_graphs is True and path_results is not None:
        time_str = ""
        if with_timestamp_in_file_name:
            time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")

        if not with_timestamp_in_file_name:

            nx.write_graphml(connectivity_graph, os.path.join(f'{path_results}', f'{filename}.graphml'))

            nx.write_gexf(connectivity_graph, os.path.join(f'{path_results}', f'{filename}.gexf'))

        else:

            nx.write_graphml(connectivity_graph, os.path.join(f'{path_results}', f'{filename}.graphml'))

            nx.write_gexf(connectivity_graph, os.path.join(f'{path_results}', f'{filename}.gexf'))

    # return graph_in, graph_out, connectivity_graph

    return connectivity_graph


def plot_graph(graph, with_fa2=False, randomized_positions=False, filename=None, iterations=2000,
               node_color=None, edge_color=None, background_color=None, cmap=None, node_size=10,
               with_labels=False, title=None, ax_to_use=None, using_my_weight=False,
               save_formats=None, save_figure=False, path_results=None, with_timestamp_in_file_name=False):
    """

    :param graph:
    :param with_fa2:
    :param randomized_positions:
    :param filename:
    :param iterations:
    :param node_color:
    :param edge_color:
    :param background_color:
    :param cmap:
    :param node_size:
    :param with_labels:
    :param title:
    :param ax_to_use:
    :param using_my_weight: if True, edges must have a property "my_weight" that contains a value, the bigger it is,
    the stronger the link between the nodes
    :param save_formats:
    :param save_figure:
    :param path_results:
    :param with_timestamp_in_file_name:
    :return:
    """
    # if with_fa2:
    #     forceatlas2 = ForceAtlas2(
    #         # Behavior alternatives
    #         outboundAttractionDistribution=False,  # Dissuade hubs
    #         linLogMode=False,  # NOT IMPLEMENTED
    #         adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
    #         edgeWeightInfluence=1.0,
    #
    #         # Performance
    #         jitterTolerance=1.0,  # Tolerance
    #         barnesHutOptimize=True,
    #         barnesHutTheta=1.2,
    #         multiThreaded=False,  # NOT IMPLEMENTED
    #
    #         # Tuning
    #         scalingRatio=3.0,
    #         strongGravityMode=False,
    #         gravity=1.0,
    #
    #         # Log
    #         verbose=True)
    #
    #     positions = forceatlas2.forceatlas2_networkx_layout(graph, pos=None, iterations=iterations)
    if randomized_positions:
        # from: https://github.com/guyallard/markov_clustering
        # number of nodes to use
        numnodes = graph.number_of_nodes()

        # generate random positions as a dictionary where the key is the node id and the value
        # is a tuple containing 2D coordinates
        # TODO: need to get all nodes name
        positions = {i: (random.random() * 2 - 1, random.random() * 2 - 1) for i in range(numnodes)}
    elif using_my_weight:
        positions = nx.spring_layout(graph, weight='myweight')
    else:
        positions = None

    if ax_to_use is None:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
        fig.tight_layout()
        ax.set_facecolor(background_color)
    else:
        ax = ax_to_use
    if node_color is None:
        node_color = "cornflowerblue"
    if edge_color is None:
        edge_color = "cornflowerblue"
    nx.draw_networkx(graph, pos=positions, node_size=node_size, edge_color=edge_color,
                     cmap=cmap, font_color=edge_color,  font_size=5,
                     node_color=node_color, arrowsize=4, width=0.4, alpha=0.5,
                     with_labels=with_labels, arrows=True,
                     ax=ax)
    if ax_to_use is not None:
        legend_elements = []
        legend_elements.append(Patch(facecolor="cornflowerblue",
                                     edgecolor='white', label=f'{title}'))
        ax.legend(handles=legend_elements)

    if (title is not None) and (ax_to_use is None):
        plt.title(title)

    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    if ax_to_use is None:
        # padding between ticks label and  label axis
        # ax1.tick_params(axis='both', which='major', pad=15)
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


def plot_connectivity_graphs(session_id_list, graph_files_path=None, background_color=None,
                             node_color=None, edge_color=None,
                             size_fig=None,
                             save_formats=None, save_figure=False, path_results=None,
                             with_timestamp_in_file_name=False, celltype=None, time_delay=None):
    # qualitative 12 colors : http://colorbrewer2.org/?type=qualitative&scheme=Paired&n=12
    # + 11 diverting
    colors = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f',
              '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928', '#a50026', '#d73027',
              '#f46d43', '#fdae61', '#fee090', '#ffffbf', '#e0f3f8', '#abd9e9',
              '#74add1', '#4575b4', '#313695']

    # we plot one graph for each session
    n_sessions = len(session_id_list)
    max_n_lines = 10
    n_lines = n_sessions if n_sessions <= max_n_lines else max_n_lines
    n_col = math.ceil(n_sessions / n_lines)
    # for histogram all events
    fig, axes = plt.subplots(nrows=n_lines, ncols=n_col,
                             gridspec_kw={'width_ratios': [1] * n_col,
                                          'height_ratios': [1] * n_lines},
                             figsize=size_fig)
    fig.set_tight_layout({'rect': [0, 0, 1, 0.95], 'pad': 1.5, 'h_pad': 1.5})
    fig.patch.set_facecolor(background_color)

    if n_sessions == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    node_color_list = node_color
    for ax_index, ax in enumerate(axes):
        ax.set_facecolor(background_color)
        axes[ax_index].set_facecolor(background_color)
        session_identifier = session_id_list[ax_index]
        filename = session_identifier + "_connectivity_graphs_" + str(time_delay) + "ms_" + celltype
        node_color = node_color_list[ax_index]

        path_to_graph_graphml = os.path.join(f'{graph_files_path}', f'{filename}.graphml')
        connectivity_graph = nx.read_graphml(path=path_to_graph_graphml, node_type=int)
        name = "connectivity_graphs_" + celltype

        plot_graph(graph=connectivity_graph, with_fa2=False, randomized_positions=True, filename=name, iterations=2000,
                   node_color=node_color, edge_color=edge_color, background_color=background_color,
                   cmap=None, node_size=10,
                   with_labels=False, title=session_identifier, ax_to_use=ax,
                   save_formats=save_formats, save_figure=save_figure, path_results=path_results,
                   with_timestamp_in_file_name=with_timestamp_in_file_name)

    if save_figure and (path_results is not None):
        # transforming a string in a list
        if isinstance(save_formats, str):
            save_formats = [save_formats]
        time_str = ""
        if with_timestamp_in_file_name:
            time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
        for save_format in save_formats:
            if not with_timestamp_in_file_name:
                fig.savefig(os.path.join(f'{path_results}', f'{name}.{save_format}'),
                            format=f"{save_format}")
            else:
                fig.savefig(os.path.join(f'{path_results}', f'{name}_{time_str}.{save_format}'),
                            format=f"{save_format}")
    plt.close()


def build_graph_from_adjacency_matrix(adjacency_matrix, weight_on_edges=True,
                                      directed_graph=True, symetric_matrix=False):
    """
    Build a graph from the value in adjacency_matrix, put an edge for every value
    Args:
        adjacency_matrix: 2d array (n_cellsxn_cells)
        weight_on_edges:
        directed_graph:
        symetric_matrix: if True then the matrix is symetric and we don't need to use

    Returns:

    """

    adjacency_matrix = np.copy(adjacency_matrix)
    # removing auto-correlation between cells
    np.fill_diagonal(adjacency_matrix, 0)
    n_cells = adjacency_matrix.shape[0]
    if directed_graph:
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()
    graph.add_nodes_from(np.arange(n_cells))

    for cell in np.arange(n_cells - 1):
        conected_cells = np.where(adjacency_matrix[cell] > 0)[0]
        if weight_on_edges:
            # with weight
            edges = [(cell, c_cell, adjacency_matrix[cell, c_cell]) for c_cell in conected_cells]
            graph.add_weighted_edges_from(edges)
        else:
            edges = [(cell, c_cell) for c_cell in conected_cells]
            graph.add_edges_from(edges)

    if (not symetric_matrix) and directed_graph:
        # exploring the other side of the matrix
        for cell in np.arange(n_cells - 1):
            conected_cells = np.where(adjacency_matrix[:, cell] > 0)[0]
            if weight_on_edges:
                # with weight
                edges = [(cell, c_cell, adjacency_matrix[c_cell, cell]) for c_cell in conected_cells]
                graph.add_weighted_edges_from(edges)
            else:
                edges = [(cell, c_cell) for c_cell in conected_cells]
                graph.add_edges_from(edges)
    return graph


def welsh_powell(graph):
    """
    Implementation of the Welsh-Powell algorithm
    From: https://repl.it/repls/SpatialIgnorantList
    Args:
        graph: NetworkX graph instance

    Returns:

    """
    # sorting the nodes based on it's valency
    node_list = sorted(graph.nodes(), key=lambda x: graph.degree(x))
    # dictionary to store the colors assigned to each node
    col_val = {}
    # assign the first color to the first node
    col_val[node_list[0]] = 0
    # Assign colors to remaining N-1 nodes
    for node in node_list[1:]:
        available = [True] * len(graph.nodes())  # boolean list[i] contains false if the node color 'i' is not available

        # iterates through all the adjacent nodes and marks it's color as unavailable, if it's color has been set already
        for adj_node in graph.neighbors(node):
            if adj_node in col_val.keys():
                col = col_val[adj_node]
                available[col] = False
        clr = 0
        for clr in range(len(available)):
            if available[clr] == True:
                break
        col_val[node] = clr
    return col_val


def detect_hub_cells(graphs_to_analyse, cell_connectivity_threshold=5,
                     top_connected_cells=20, verbose=True):
    """
    :param graphs_to_analyse: a dictionary key is the graph ID, data is the graph
    :param cell_connectivity_threshold: minimal degree of connectivity of the hub in a graph
    :param top_connected_cells: hub cell is in the 'top_connected_cells' % most connected cells across graphs
    :param verbose:
    :return:
    """

    hubs_dict = dict()
    cells_connectivity = []
    bc_values = []
    for key, data in graphs_to_analyse.items():
        graph = graphs_to_analyse.get(key)
        n_cells = graph.number_of_nodes()
        for cell in np.arange(n_cells):
            cells_connectivity.append(len(graph[cell]))
        bc_dict = nx.betweenness_centrality(graph)
        bc_values.extend(list(bc_dict.values()))

    # determining hubs for each ms
    for key, data in graphs_to_analyse.items():
        if verbose:
            print(f"--------- Look for hub cells in graph from: {key} -----------")
        graph = graphs_to_analyse.get(key)
        n_cells = graph.number_of_nodes()

        # first selecting cells connected to more than x% cells
        # we dot it among this particular mouse
        cells_connectivity_perc_threshold = cell_connectivity_threshold
        # step 1
        cells_selected_s1 = []
        local_cells_connectivity = []
        for cell in np.arange(n_cells):
            local_cells_connectivity.append(len(graph[cell]))
            if ((len(graph[cell]) / n_cells) * 100) >= cells_connectivity_perc_threshold:
                cells_selected_s1.append(cell)
        if len(cells_selected_s1) == 0:
            if verbose:
                print(f"Failed at step 1: no cell connected to more than {cells_connectivity_perc_threshold}% of the cells")
            continue

        # step 2
        cells_selected_s2 = []
        connec_treshold = np.percentile(cells_connectivity, (100 - top_connected_cells))
        for cell in cells_selected_s1:
            if local_cells_connectivity[cell] >= connec_treshold:
                cells_selected_s2.append(cell)
        if len(cells_selected_s2) == 0:
            if verbose:
                print(f"Failed at step 2: no cell in the top {top_connected_cells}% of highly connected cells")
            continue

        # step 3
        cells_selected_s3 = []
        local_bc_dict = nx.betweenness_centrality(graph)
        bc_perc_threshold = np.percentile(bc_values, 80)
        for cell in cells_selected_s2:
            if local_bc_dict[cell] >= bc_perc_threshold:
                cells_selected_s3.append(cell)
        if len(cells_selected_s3) == 0:
            if verbose:
                print(f"Failed at step 3: no cell has high betweenness centrality")
            continue

        if verbose:
            print(f"HUB cells (n={len(cells_selected_s3)}): {cells_selected_s3}")

        hubs_dict[key] = cells_selected_s3

    return hubs_dict

