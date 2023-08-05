# use CDLIB package
# or pip install markov_clustering[drawing]
import networkx as nx
import markov_clustering as mc
# from cdlib import algorithms, viz
import os

import matplotlib.pyplot as plt
from cdlib import NodeClustering
from cdlib.utils import convert_graph_formats
from community import induced_graph

# see https://github.com/guyallard/markov_clustering

def markov_clustering(graph, file_name, results_path, with_best_modularity=True):
    """

    Args:
        graph: networkx graph instance
        with_best_modularity: bool, if True, run several inflation values to find the best cluster define by its
        modularity score

    Returns: A list of tuples where each tuple represents a cluster and
              contains the indices of the nodes belonging to the cluster

    """
    use_cdlib_version = False
    if use_cdlib_version:
        coms = algorithms.markov_clustering(graph, max_loop=100)  # 1000
        pos = nx.spring_layout(graph)
        print(f"plotting cdlib version")
        plot_network_clusters(graph, coms, pos, file_name=file_name, results_path=results_path)  # viz.
        # TODO: get the clusters from coms
        return None
        # result_dict = coms.to_node_community_map()
    else:
        # then get the adjacency matrix (in sparse form)
        matrix = nx.to_scipy_sparse_matrix(graph)

        if with_best_modularity:
            max_modularity = 0
            clusters = None
            # perform clustering using different inflation values from 1.5 and 2.5
            # for each clustering run, calculate the modularity
            for inflation in [i / 10 for i in range(15, 26)]:
                result = mc.run_mcl(matrix, inflation=inflation)
                tmp_clusters = mc.get_clusters(result)
                modularity = mc.modularity(matrix=result, clusters=tmp_clusters)
                if modularity > max_modularity:
                    max_modularity = modularity
                    clusters = tmp_clusters
                # print("inflation:", inflation, "modularity:", modularity)
        else:
            result = mc.run_mcl(matrix, inflation=2)  # run MCL with default parameters
            clusters = mc.get_clusters(result)  # get clusters

        return clusters


__all__ = ["plot_network_clusters", "plot_community_graph"]

COLOR = ['r', 'b', 'g', 'c', 'm', 'y', 'k',
         '0.8', '0.2', '0.6', '0.4', '0.7', '0.3', '0.9', '0.1', '0.5']


def plot_network_clusters(graph, partition, position, file_name, results_path, figsize=(8, 8), node_size=50,
                          plot_overlaps=False,
                          plot_labels=False):
    """
    Plot a graph with node color coding for communities.

    :param graph: NetworkX/igraph graph
    :param partition: NodeClustering object
    :param position: A dictionary with nodes as keys and positions as values. Example: networkx.fruchterman_reingold_layout(G)
    :param figsize: the figure size; it is a pair of float, default (8, 8)
    :param node_size: int, default 200
    :param plot_overlaps: bool, default False. Flag to control if multiple algorithms memberships are plotted.
    :param plot_labels: bool, default False. Flag to control if node labels are plotted.

    Example:

    >>> from cdlib import algorithms, viz
    >>> import networkx as nx
    >>> g = nx.karate_club_graph()
    >>> coms = algorithms.louvain(g)
    >>> pos = nx.spring_layout(g)
    >>> viz.plot_network_clusters(g, coms, pos)
    """
    partition = partition.communities
    graph = convert_graph_formats(graph, nx.Graph)

    n_communities = min(len(partition), len(COLOR))
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    fig.tight_layout()
    plt.axis('off')

    nx.draw_networkx_nodes(graph, position, node_size=node_size, node_color='gray', ax=ax)
    # fig.set_edgecolor('k')
    nx.draw_networkx_edges(graph, position, alpha=.5, ax=ax, edge_color="k")
    print(f'n_communities {n_communities}')
    print(f"partition {partition}")
    for i in range(n_communities):
        if len(partition[i]) > 0:
            if plot_overlaps:
                size = (n_communities - i) * node_size
            else:
                size = node_size
            nx.draw_networkx_nodes(graph, position, node_size=size,
                                   nodelist=partition[i], node_color=COLOR[i], ax=ax)
    if plot_labels:
        nx.draw_networkx_labels(graph, position, ax=ax, labels={node: str(node) for node in graph.nodes()})

    fig.savefig(os.path.join(f'{results_path}', f'{file_name}.pdf'),
                format=f"pdf")
