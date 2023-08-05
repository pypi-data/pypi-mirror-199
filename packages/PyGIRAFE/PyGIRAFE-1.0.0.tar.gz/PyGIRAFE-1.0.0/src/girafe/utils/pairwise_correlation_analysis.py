import numpy as np
from girafe.utils.connectivity.connectivity_utils import build_pearson_adjacency_matrix
import scipy.spatial.distance as sci_sp_dist
import matplotlib.pyplot as plt
import seaborn as sns
import math
import os
from datetime import datetime


def get_pairwise_hamming_similarity(neuronal_data):
    """
    Distribution of pair-wise Hamming distance of all cells
    :param neuronal_data: Must be binary matrix n_cells x n_frames (activity of the cell is 1, otherwise 0)
    :return:
    """
    n_cells = neuronal_data.shape[0]
    similarity_matrix = np.zeros((n_cells, n_cells), dtype=float)
    for cell_1 in range(n_cells):
        for cell_2 in np.arange(cell_1, n_cells):
            hamm_dist = sci_sp_dist.hamming(neuronal_data[cell_1], neuronal_data[cell_2])
            similarity = 1 - hamm_dist
            similarity_matrix[cell_1, cell_2] = similarity
            similarity_matrix[cell_2, cell_1] = similarity
    return similarity_matrix


def get_pairwise_jaccard_similarity(neuronal_data):
    n_cells = neuronal_data.shape[0]
    similarity_matrix = np.zeros((n_cells, n_cells), dtype=float)
    for cell_1 in range(n_cells):
        for cell_2 in np.arange(cell_1, n_cells):
            jaccard_dist = sci_sp_dist.jaccard(neuronal_data[cell_1], neuronal_data[cell_2])
            similarity = 1 - jaccard_dist
            similarity_matrix[cell_1, cell_2] = similarity
            similarity_matrix[cell_2, cell_1] = similarity
    return similarity_matrix


def compute_similarity_matrix(neuronal_data=None, method=None, verbose=False):
    if verbose:
        print(f"Starting to compute similarity matrix")

    similarity_metric = method

    if verbose:
        print(f"Use {similarity_metric} as metric to compute similarity matrix")

    if similarity_metric == "Pearson":
        similarity_matrix = build_pearson_adjacency_matrix(neuronal_data=neuronal_data, with_thresholds=False,
                                                           verbose=0)

    if similarity_metric == "Hamming":
        similarity_matrix = get_pairwise_hamming_similarity(neuronal_data=neuronal_data)

    if similarity_metric == "Jacquard":
        similarity_matrix = get_pairwise_jaccard_similarity(neuronal_data=neuronal_data)

    if verbose:
        print(f"Similarity matrix is computed")

    return similarity_matrix


def plot_similarity_matrix(data, filename=None, background_color=None, size_fig=None, save_figure=True, path_results=None,
                           save_formats="", with_timestamp_in_file_name=False):
    """
    :param data: either the similarity matrix or a dict key is the name data is the associated similarity matrix
    :param filename:
    :param background_color:
    :param size_fig:
    :param save_figure:
    :param path_results:
    :param save_formats:
    :param with_timestamp_in_file_name:
    :return:
    """
    if isinstance(data, dict):
        key_list = []
        for key, info in data.items():
            key_list.append(key)

        # we plot one graph for each epoch
        n_plots = len(key_list)
        if n_plots > 6:
            max_n_cols = 5
        else:
            max_n_cols = 3

        n_cols = n_plots if n_plots <= max_n_cols else max_n_cols
        n_lines = math.ceil(n_plots / n_cols)
        print(f"n_lines {n_lines}, n_cols {n_cols}")
        fig, axes = plt.subplots(nrows=n_lines, ncols=n_cols,
                                 gridspec_kw={'width_ratios': [1] * n_cols, 'height_ratios': [1] * n_lines},
                                 figsize=size_fig)
        fig.set_tight_layout({'rect': [0, 0, 1, 0.95], 'pad': 1.5, 'h_pad': 1.5})
        fig.patch.set_facecolor(background_color)

        for index, ax in enumerate(axes.flatten()):
            if index >= n_plots:
                continue
            name = key_list[index]
            data_to_plot = data.get(name)
            sns.heatmap(data_to_plot, vmin=0, vmax=1, ax=ax, annot=False, xticklabels=50, yticklabels=50)
            ax.set_title(name, fontsize=8)
    else:
        n_lines = 1
        n_col = 1
        fig, ax = plt.subplots(nrows=n_lines, ncols=n_col,
                               gridspec_kw={'width_ratios': [1] * n_col, 'height_ratios': [1] * n_lines},
                               figsize=size_fig)
        fig.set_tight_layout({'rect': [0, 0, 1, 0.95], 'pad': 1.5, 'h_pad': 1.5})
        fig.patch.set_facecolor(background_color)
        sns.heatmap(data, vmin=0, vmax=1, ax=ax, annot=False, xticklabels=50, yticklabels=50)
        plt.title(label='Full recording Similarity matrix', fontdict=None, loc='center', pad=None)

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
                            format=f"{save_format}")
            else:
                fig.savefig(os.path.join(f'{path_results}', f'{filename}_{time_str}.{save_format}'),
                            format=f"{save_format}")
    plt.close()
