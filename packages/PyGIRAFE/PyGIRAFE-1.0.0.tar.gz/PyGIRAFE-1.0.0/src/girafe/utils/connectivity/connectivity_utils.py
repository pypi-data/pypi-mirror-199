import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import os
from datetime import datetime


def build_pearson_adjacency_matrix(neuronal_data, with_thresholds=True, correlation_threshold=0.1,
                                   p_value_threshold=0.05, verbose=0, data_id="", results_path=None):
    """
    Build the adjacency matrix of neuronal data
    Args:
        neuronal_data: 2d array of shape (n_cells x n_times)
        with_thresholds: use or not the following thresholds
        correlation_threshold: value between 0 and 1, correlation under the threshold will be put ot 0
        p_value_threshold: correlation with p > threshold will be put to 0
        verbose: (int) if > 0, some information will be printed
        data_id: describe the data, useful if verbose > 0 or results_path is not None
        results_path: if not None, (str) representing the path where to save the adjacency matrix, in numpy format

    Returns:

    """
    n_cells = neuronal_data.shape[0]

    adjacency_matrix = np.zeros((n_cells, n_cells))

    n_corr_kept = 0
    n_corr_total = 0
    if verbose > 0:
        print(f"Building pearson adjacency matrix for {data_id}")
    for first_cell in np.arange(n_cells):
        for second_cell in np.arange(first_cell, n_cells):
            # TODO: verify if the matrix should be symmetric, in that case no need calculate
            #  the correlation over all pairs
            if first_cell == second_cell:
                adjacency_matrix[first_cell, second_cell] = 1
                continue
            rho, p_value = scipy.stats.pearsonr(neuronal_data[first_cell], neuronal_data[second_cell])
            n_corr_total += 1
            if with_thresholds:
                if (p_value > p_value_threshold) or (rho <= correlation_threshold):
                    continue
                else:
                    adjacency_matrix[first_cell, second_cell] = rho
                    adjacency_matrix[second_cell, first_cell] = rho
            else:
                adjacency_matrix[first_cell, second_cell] = rho
                adjacency_matrix[second_cell, first_cell] = rho
            n_corr_kept += 1
    if with_thresholds:
        if verbose > 0:
            print(f"{n_corr_kept} correlation passed the threshold over a total of {n_corr_total}")
            print("")

    if results_path is not None:
        np.save(os.path.join(results_path, f"pearson_adjacency_matrix_{data_id}.npy"), adjacency_matrix)

    return adjacency_matrix


def get_time_correlation_data(spike_nums, events_times, time_around_events=5):
    """
       Will compute data that will be use in order to plot the time-correlation graph
       :return:
    """
    # ms_scale represents the space between each tick
    nb_neurons = len(spike_nums)
    n_times = len(spike_nums[0, :])
    # values for each cell
    time_lags_dict = dict()
    correlation_dict = dict()
    # for ploting
    time_lags_list = []
    correlation_list = []
    cells_list = []

    # first determining what is the maximum duration of an event, for array dimension purpose
    max_duration_event = 0
    for times in events_times:
        max_duration_event = np.max((max_duration_event, times[1]-times[0]))

    time_window = int(np.ceil((max_duration_event + (time_around_events * 2)) / 2))

    for neuron in np.arange(nb_neurons):
        # look at onsets
        neuron_spikes, = np.where(spike_nums[neuron, :])

        if len(neuron_spikes) == 0:
            continue

        spike_nums_to_use = spike_nums

        # time_window by 4
        distribution_array_2_d = np.zeros((nb_neurons, ((time_window * 4) + 1)),
                                          dtype="int16")

        mask = np.ones(nb_neurons, dtype="bool")
        mask[neuron] = False

        # event_index = time_window
        # looping on each spike of the main neuron
        for n, event_times in enumerate(events_times):
            # only taking in consideration events that are not too close from bottom range or upper range
            min_limit = max(0, (event_times[0] - time_around_events))
            max_limit = min(event_times[1]+1 + time_around_events, (n_times - 1))
            # min((peak_time + time_window), (n_times - 1))
            if np.sum(spike_nums[neuron, min_limit:max_limit]) == 0:
                continue
            # see to consider the case in which the cell spikes 2 times around a peak during the tim_window
            neuron_spike_time = np.where(spike_nums[neuron, min_limit:max_limit])[0][0]
            spikes_indices = np.where(spike_nums_to_use[:, min_limit:max_limit])
            conn_cells_indices = spikes_indices[0]
            spikes_indices = neuron_spike_time - spikes_indices[1]
            spikes_indices += time_window*2
            # print(f"spikes_indices {spikes_indices}")
            # copy_of_neuron_distrib = np.copy(distribution_array_2_d[neuron, :])
            distribution_array_2_d[conn_cells_indices, spikes_indices] += 1
            # distribution_array_2_d[neuron, :] = copy_of_neuron_distrib

        # sum of spikes at each times lag
        distribution_array = np.sum(distribution_array_2_d[mask, :], axis=0)
        # print(f"distribution_array {distribution_array}")
        total_spikes = np.sum(distribution_array)
        # adding the cell only if it has at least a spike around peak times
        if total_spikes > 0:
            correlation_value = np.max(distribution_array) / total_spikes
            # array_to_average = np.zeros(np.sum(distribution_array))
            # start = 0
            # for index, time_lag in enumerate(np.arange(-time_window * 2, time_window * 2 + 1)):
            #     n_spike_for_this_time_lag = distribution_array[index]
            #     array_to_average[start:(start+n_spike_for_this_time_lag)] = time_lag
            #     start += n_spike_for_this_time_lag
            # avg_time_lag = np.mean(array_to_average)
            # other way:
            time_lags_range = np.arange(-time_window * 2, time_window * 2 + 1)
            distribution_array = distribution_array * time_lags_range
            avg_time_lag = np.sum(distribution_array)/total_spikes
            time_lags_dict[neuron] = avg_time_lag
            correlation_dict[neuron] = correlation_value

    for cell, time_lag in time_lags_dict.items():
        time_lags_list.append(time_lag)
        correlation_list.append(correlation_dict[cell])
        cells_list.append(cell)

    return time_lags_list, correlation_list, time_lags_dict, correlation_dict, time_window, cells_list


def plot_time_correlation_graph(time_lags_list, correlation_list, time_lags_dict, correlation_dict,
                                n_cells, time_window,
                                data_id, path_results, plot_cell_numbers=False,
                                title_option="",
                                cells_groups=None, groups_colors=None, set_y_limit_to_max=True,
                                set_x_limit_to_max=True, xlabel=None, size_cells=100, size_cells_in_groups=240,
                                time_stamps_by_ms=0.01, ms_scale=200, save_formats="pdf",
                                show_percentiles=None, ax_to_use=None, color_to_use=None,
                                value_to_text_in_cell=None,
                                with_timestamp_in_file_name=False):
    # value_to_text_in_cell if not None, dict with key cell (int) and value a string to plot
    # ms_scale represents the space between each tick
    if ((cells_groups is not None) and (len(cells_groups) > 0)) or (color_to_use is None):
        default_cell_color = "grey"
    else:
        default_cell_color = color_to_use

    if ax_to_use is None:
        fig, ax = plt.subplots(nrows=1, ncols=1,
                               gridspec_kw={'height_ratios': [1]},
                               figsize=(20, 20))
        fig.patch.set_facecolor("black")
        ax.set_facecolor("black")
    else:
        ax = ax_to_use

    ax.scatter(time_lags_list, correlation_list, color=default_cell_color, marker="o",
               s=size_cells, zorder=1, alpha=0.5)

    if cells_groups is not None:
        for group_id, cells in enumerate(cells_groups):
            for cell in cells:
                if cell in time_lags_dict:
                    ax.scatter(time_lags_dict[cell], correlation_dict[cell], color=groups_colors[group_id],
                               marker="o",
                               s=size_cells_in_groups, zorder=10)
                # else:
                #     print(f"{data_id}: cell {cell} not in time-correlation graph")

    if plot_cell_numbers:
        for cell in np.arange(n_cells):
            if cell in time_lags_dict:
                text_str = str(cell)
                if value_to_text_in_cell is not None:
                    text_str = value_to_text_in_cell[cell]
                ax.text(x=time_lags_dict[cell], y=correlation_dict[cell], s=text_str,
                        ha='center', va="center", fontsize=3, fontweight='bold')

    xticks_pos = []
    # display a tick every 200 ms, time being in seconds
    times_for_s_scale = ms_scale * 0.001
    time_window_s = (time_window / time_stamps_by_ms) * 0.001
    xticklabels = []
    labels_in_s = np.arange(-time_window_s * 2, time_window_s * 2 + 1, times_for_s_scale)
    pos_range = np.arange(-time_window * 2, time_window * 2 + 1, ms_scale * time_stamps_by_ms)
    # print(f"max_value {max_value}")
    if set_x_limit_to_max:
        min_range_index = 0
        max_range_index = len(pos_range) - 1
    else:
        max_value = np.max((np.abs(np.min(time_lags_list)), np.abs(np.max(time_lags_list))))
        min_range_index = np.searchsorted(pos_range, -max_value, side='left') - 1
        max_range_index = np.searchsorted(pos_range, max_value, side='right')
    # print(f"min_range_index {min_range_index}, max_range_index {max_range_index}, pos_range {pos_range}")
    labels_in_s = labels_in_s[min_range_index:max_range_index + 5:5]
    for index_pos, pos in enumerate(pos_range[min_range_index:max_range_index + 5:5]):
        xticks_pos.append(pos)
        xticklabels.append(np.round(labels_in_s[index_pos], 1))
    if len(labels_in_s) > 20:
        ax.xaxis.set_tick_params(labelsize=2)
    else:
        ax.xaxis.set_tick_params(labelsize=5)

    # print(f"xticks_pos {xticks_pos}")
    # print(f"xticklabels {xticklabels}")
    ax.set_xticks(xticks_pos)
    ax.set_xticklabels(xticklabels)
    ax.tick_params(axis='y', colors="white")
    ax.tick_params(axis='x', colors="white")
    if set_x_limit_to_max:
        ax.set_xlim(-time_window * 2, (time_window * 2) + 1)
    else:
        ax.set_xlim(pos_range[min_range_index], pos_range[max_range_index])

    if show_percentiles is not None:
        for perc_value in show_percentiles:
            correlation_threshold = np.percentile(correlation_list, perc_value)
            if set_x_limit_to_max:
                start_x = -time_window * 2
                end_x = (time_window * 2) + 1
            else:
                start_x = pos_range[min_range_index]
                end_x = pos_range[max_range_index]
            ax.hlines(correlation_threshold, start_x, end_x, color="white", linewidth=1, linestyles="dashed")

    if set_y_limit_to_max:
        ax.set_ylim(0, 1.1)

    if xlabel is None:
        ax.set_xlabel("Time lag (s)")
    else:
        ax.set_xlabel(xlabel)
    ax.set_ylabel("Correlation")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")

    legend_elements = [Patch(facecolor=default_cell_color,
                             edgecolor="white",
                             label=f"{data_id} {title_option}")]
    ax.legend(handles=legend_elements)

    # plt.title(f"Time-correlation graph {data_id} {title_option}")

    #  :param plot_option: if 0: plot n_out and n_int, if 1 only n_out, if 2 only n_in, if 3: only n_out with dotted to
    # show the commun n_in and n_out, if 4: only n_in with dotted to show the commun n_in and n_out,
    if ax_to_use is None:
        if isinstance(save_formats, str):
            save_formats = [save_formats]
        time_str = ""
        if with_timestamp_in_file_name:
            time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
        for save_format in save_formats:
            if not with_timestamp_in_file_name:
                fig.savefig(os.path.join(f'{path_results}', f'{data_id}.{save_format}'),
                            format=f"{save_format}",
                            facecolor=fig.get_facecolor())
            else:
                fig.savefig(os.path.join(f'{path_results}', f'{data_id}{time_str}.{save_format}'),
                            format=f"{save_format}",
                            facecolor=fig.get_facecolor())
        plt.close()
