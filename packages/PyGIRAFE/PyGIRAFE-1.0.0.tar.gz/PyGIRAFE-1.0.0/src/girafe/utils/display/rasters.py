import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import patches
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
from matplotlib.transforms import Bbox
import seaborn as sns
from datetime import datetime
import matplotlib.cm as cm
import numpy as np
import math
import os
from girafe.utils.signal import gaussblur1D, norm01
from girafe.utils.misc import bin_raster
from girafe.utils.spike_trains import create_spike_train_neo_format
import neo
import quantities as pq
import elephant.conversion as elephant_conv


def plot_raster(spike_nums=None, title=None, file_name=None,
                frame_times=None,
                times_format="sec",
                bin_size_ms_for_spikes_sum=100,
                spike_train_format=False,
                y_ticks_labels=None,
                y_ticks_labels_size=None,
                y_ticks_labels_color="white",
                hide_raster_y_ticks_labels=True,
                x_ticks_labels_color="white",
                x_ticks_labels=None,
                x_ticks_labels_size=None,
                x_ticks=None,
                hide_x_ticks_labels=False,
                figure_background_color="black",
                without_ticks=True,
                save_raster=False,
                show_raster=False,
                plot_with_amplitude=False,
                activity_threshold=None,
                save_formats="png",
                span_area_coords=None,
                span_area_colors=None,
                span_area_only_on_raster=True,
                alpha_span_area=0.5,
                cells_to_highlight=None,
                cells_to_highlight_colors=None,
                color_peaks_activity=False,
                horizontal_lines=None,
                horizontal_lines_colors=None,
                horizontal_lines_sytle=None,
                horizontal_lines_linewidth=None,
                vertical_lines=None,
                vertical_lines_colors=None,
                vertical_lines_sytle=None,
                vertical_lines_linewidth=None,
                scatters_on_traces=None,
                scatters_on_traces_marker="*",
                scatters_on_traces_size=5,
                sliding_window_duration=1,
                show_sum_spikes_as_percentage=False,
                span_cells_to_highlight=None,
                span_cells_to_highlight_colors=None,
                spike_shape="|",
                spike_shape_size=10,
                raster_face_color='black',
                cell_spikes_color='white',
                activity_sum_plot_color="white",
                activity_sum_face_color="black",
                seq_times_to_color_dict=None,
                link_seq_categories=None,
                link_seq_color=None, min_len_links_seq=3,
                link_seq_line_width=1, link_seq_alpha=1,
                jitter_links_range=1,
                display_link_features=True,
                seq_colors=None, debug_mode=False,
                axes_list=None,
                SCE_times=None,
                raster_y_axis_label=None,
                raster_y_axis_label_size=None,
                axes_label_color='white',
                without_activity_sum=False,
                activity_sum_specified_y_lim=False,
                y_lim_sum_activity=None,
                show_activity_sum_label=False,
                spike_nums_for_activity_sum=None,
                spikes_sum_to_use=None,
                size_fig=None,
                cmap_name="jet", traces=None,
                display_traces=False,
                display_spike_nums=True,
                traces_lw=0.3,
                path_results=None,
                xkcd_mode=False,
                desaturate_color_according_to_normalized_amplitude=False,
                lines_to_display=None,
                lines_color="white",
                lines_width=1,
                lines_band=0,
                lines_band_color="white",
                use_brewer_colors_for_traces=False,
                dpi=100,
                with_timestamp_in_file_name=True,
                display_dashed_line_with_traces=False,
                show_y_scale=False,
                show_x_scale=False,
                y_scale_unit='AU',
                y_scale_length=1,
                x_scale_unit=None,
                x_scale_length=None,
                x_scale_label=None,
                ):
    """
    Plot or save a raster given a 2d array either binary representing onsets, peaks or rising time, or made of float
    to represents traces or encoding in onset/peaks/rising time a value.
    :param spike_nums: np.array of 2D, axis=1 (lines) represents the cells, the columns representing the spikes
    It could be binary, or containing the amplitude, if amplitudes values should be display put plot_with_amplitude
    to True
    :param frame_times: (1d np.array) if spike_train_format is False, used to represent the time for each frame representing
    in the 1d of spike_nums. If None, then the index in spike_names will be used to representing the x-axis
    :param times_format: (str) indicate the time format, could be "sec" or "ms"
    :param bin_size_ms_for_spikes_sum: (int) use if frame_times is not None and spikes sum is displayed. Size
    in ms of the bin to sum the spikes
    :param spike_train_format: if True, means the data is a list of np.array, and then spike_nums[i][j] is
    a timestamps value as float
    :param title: title to be plot
    :param file_name: name of the file if save_raster is True
    :param save_raster: if True, the plot will be save. To do so param should not be None and contain a variable
    path_results that will indicated where to save file_name
    :param show_raster: if True, the plot will be shown
    :param plot_with_amplitude: to display a color bar representing the content values.
    :param activity_threshold: Int representing a threshold that will be display as a red line on the sum of activity
    subplot.
    :param save_formats: string or list of string representing the formats in which saving the raster.
    Exemple: "pdf" or ["pdf", "png"]
    :param span_area_coords: List of list of tuples of two float representing coords (x, x) of span band with a color
    corresponding to the one in span_area_colors
    :param span_area_colors: list of colors, same len as span_area_coords
    :param span_area_only_on_raster: if True, means the span won't be on the sum of activity on the sub-plot as well
    :param cells_to_highlight: cells index to span (y-axis) with special spikes color, list of int
    :param cells_to_highlight_colors: cells colors to span, same len as cells_to_span, list of string
    :param color_peaks_activity: if True, will span to the color of cells_to_highlight_colors each time at which a cell
    among cells_to_highlight will spike on the activity peak diagram
    :param horizontal_lines: list of float, representing the y coord at which trace horizontal lines
    :param horizontal_lines_colors: if horizontal_lines is not None, will set the colors of each line,
    list of string or color code
    :param horizontal_lines_style: give the style of the lines, string
    :param vertical_lines: list of float, representing the x coord at which trace vertical lines
    :param vertical__lines_colors: if horizontal_lines is not None, will set the colors of each line,
    list of string or color code
    :param vertical__lines_style: give the style of the lines, string
    :param vertical_lines_linewidth: linewidth of vertical_lines
    :param raster_face_color: the background color of the raster
    :param cell_spikes_color: the color of the spikes of the raster
    :param spike_shape: shape of the spike, "|", "*", "o"
    :param spike_shape_size: use for shape != of "|"
    :param seq_times_to_color_dict: None or a dict with as the key a tuple of int representing the cell index,
    and as a value a list of set, each set composed of int representing the times value at which the cell spike should
    be colored. It will be colored if there is indeed a spike at that time otherwise, the default color will be used.
    :param seq_colors: A dict, with key a tuple represening the indices of the seq and as value of colors,
    a color, should have the same keys as seq_times_to_color_dict
    :param link_seq_color: if not None, give the color with which link the spikes from a sequence. If not None,
    seq_colors will be ignored. could be a dict with key same tuple as seq_times_to_color_dict or a string and then
    we use the same color for all seq
    :param min_len_links_seq: minimum len of a seq for the links to be drawn
    :param axes_list if not None, give a list of axes that will be used, and be filled, but no figure will be created
    or saved then. Doesn't work yet is show_amplitude is True
    :param SCE_times:  a list of tuple corresponding to the first and last index of each SCE,
    (last index being included in the SCE). Will display the position of the SCE and their number above the activity
    diagram. If None, the overall time will be displayed. Need to be adapted to the format spike_numw or
    spike_train. Equivalent to span_are_coords
    :param without_activity_sum: if True, don't plot the sum of activity diagram, valid only if axes_list is not None
    :param spike_nums_for_activity_sum: if different that the one given for the raster, should be the
    same second dimension
    :param spikes_sum_to_use: an array of 1D, that will be use to display the sum of activity,
    :param size_fig: tuple of int
    :param cmap_name: "jet" by default, used if with_amplitude for the colormap
    :param traces if not None and display_traces is True, will display traces instead of a raster
    :param display_traces, if True display traces
    :param display_spike_nums, if False, won't display a raster using spike_nums
    :param traces_lw, default 0.3,  linewidth of the traces
    :param path_results: indicate where to save the plot, replace the param.path_results if it exists
    :param desaturate_color_according_to_normalized_amplitude: if True, spike_nums should be filled with float between
    0 and 1, representing the amplitude of the spike. And if a color is given for a cell, then it will be desaturate
    according to this value
    :param lines_to_display, dict that takes for a key a tuple of int representing 2 cells, and as value a list of tuple of 2 float
    representing the 2 extremities of a line between those 2 cells. By defualt, no lines
    :param lines_color="white": colors of lines_to_display
    :param lines_width=1: width of lines_to_display
    :param lines_band=0: if > 0, display a band around the line with transparency
    :param lines_band_color="white"
    :param xkcd_mode (bool): Turn on xkcd sketch-style drawing mode
    :param with_timestamp_in_file_name: add a time_stamps in the file saved to identify when it's done
    :return:
    """

    # qualitative 12 colors : http://colorbrewer2.org/?type=qualitative&scheme=Paired&n=12
    # + 11 diverting
    brewer_colors = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f',
                     '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928', '#a50026', '#d73027',
                     '#f46d43', '#fdae61', '#fee090', '#ffffbf', '#e0f3f8', '#abd9e9',
                     '#74add1', '#4575b4', '#313695']
    brewer_colors = brewer_colors[::-1]

    if (spike_nums is None) and (traces is None):
        return

    if display_traces:
        if traces is None:
            return

    if spike_nums_for_activity_sum is None:
        if spike_nums is None:
            without_activity_sum = True
        else:
            spike_nums_for_activity_sum = spike_nums

    if plot_with_amplitude and spike_train_format:
        # not possible for now
        return

    if xkcd_mode:
        plt.xkcd()

    if spike_nums is None:
        n_cells = len(traces)
    else:
        n_cells = len(spike_nums)

    if axes_list is None:
        if size_fig is None:
            size_fig = (15, 8)
        if not plot_with_amplitude:
            if without_activity_sum:
                fig, ax1 = plt.subplots(nrows=1, ncols=1, sharex=False,
                                        figsize=size_fig, dpi=dpi)
            else:
                sharex = True  # False if (SCE_times is None) else True
                fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=sharex,
                                               gridspec_kw={'height_ratios': [10, 2]},
                                               figsize=size_fig, dpi=dpi)
            fig.set_tight_layout({'rect': [0, 0, 1, 0.95], 'pad': 2.0, 'h_pad': 1.5})
        else:
            fig = plt.figure(figsize=size_fig, dpi=dpi)
            fig.set_tight_layout({'rect': [0, 0, 1, 1], 'pad': 1, 'h_pad': 1})
            outer = gridspec.GridSpec(1, 2, width_ratios=[100, 1])  # , wspace=0.2, hspace=0.2)
        fig.patch.set_facecolor(figure_background_color)
    else:
        if without_activity_sum:
            ax1 = axes_list[0]
        else:
            ax1, ax2 = axes_list

    if plot_with_amplitude:
        inner = gridspec.GridSpecFromSubplotSpec(2, 1,
                                                 subplot_spec=outer[0], height_ratios=[10, 2])
        # inner.tight_layout(fig, pad=0.1)
        ax1 = fig.add_subplot(inner[0])  # plt.Subplot(fig, inner[0])
        min_value = np.min(spike_nums)
        max_value = np.max(spike_nums)
        step_color_value = 0.1
        colors = np.r_[np.arange(min_value, max_value, step_color_value)]
        mymap = plt.get_cmap("jet")
        # get the colors from the color map
        my_colors = mymap(colors)

        # colors = plt.cm.hsv(y / float(max(y)))
        scalar_map = plt.cm.ScalarMappable(cmap=cmap_name, norm=plt.Normalize(vmin=min_value, vmax=max_value))
        # # fake up the array of the scalar mappable. Urgh…
        scalar_map._A = []

    # -------- end plot with amplitude ---------

    ax1.set_facecolor(raster_face_color)

    min_time = 0
    max_time = 0

    max_n_color = n_cells
    if cells_to_highlight is not None:
        cells_to_highlight = np.array(cells_to_highlight)
    if display_traces:
        zorder_traces = 21 + len(traces)
        shift_up = np.median(np.amax(traces, axis=1))
        for cell, trace in enumerate(traces):
            if cells_to_highlight is not None:
                if cell in cells_to_highlight:
                    index = np.where(cells_to_highlight == cell)[0][0]
                    color = cells_to_highlight_colors[index]
            else:
                if use_brewer_colors_for_traces:
                    color = cm.rainbow(((cell % max_n_color) + 1) / (max_n_color + 1))
                else:
                    color = cell_spikes_color
            if cell == 0:
                ax1.plot(frame_times, trace, lw=traces_lw, color=color, zorder=zorder_traces)
            else:
                ax1.plot(frame_times, trace + cell * shift_up, lw=traces_lw, color=color, zorder=zorder_traces)
            if scatters_on_traces is not None:
                times_to_scatter = np.where(scatters_on_traces[cell, :])[0]
                ax1.scatter(times_to_scatter, trace[times_to_scatter] + cell,
                            color="white",
                            marker=scatters_on_traces_marker,
                            s=scatters_on_traces_size, zorder=zorder_traces - 1)
            zorder_traces -= 1
            line_beg_x = -1
            line_end_x = frame_times + 1
            if display_dashed_line_with_traces:
                ax1.hlines(cell, line_beg_x, line_end_x, lw=0.1, linestyles="dashed", color=color, zorder=5)
        if show_y_scale or show_x_scale:
            if x_ticks_labels_color is not None:
                scale_color = x_ticks_labels_color
            else:
                scale_color = 'white' if figure_background_color == (0.0, 0.0, 0.0, 1.0) else 'black'
            fontprops = fm.FontProperties(size=x_ticks_labels_size, family='monospace')
            # Y-axis scale
            if show_y_scale and (y_scale_length is not None) and (y_scale_unit is not None):
                y_scale_bar = AnchoredSizeBar(transform=ax1.transData,
                                              size=1, label=f'{y_scale_length} {y_scale_unit}', loc=1, label_top=False,
                                              pad=0.1,
                                              borderpad=0,
                                              sep=5,
                                              color=scale_color,
                                              frameon=False,
                                              size_vertical=y_scale_length,
                                              fontproperties=fontprops,
                                              bbox_to_anchor=(1., 1.),
                                              bbox_transform=ax1.transAxes
                                              )
                y_scale_bar.set(zorder=len(traces) + 22)
                ax1.add_artist(y_scale_bar)
            # X-axis scale
            if show_x_scale and (x_scale_length is not None) and (x_scale_unit is not None) and (x_scale_label is not None):
                x_scale_bar = AnchoredSizeBar(transform=ax1.transData,
                                              size=x_scale_length, label=f'{x_scale_label} {x_scale_unit}', loc=2,
                                              pad=0.1,
                                              label_top=True,
                                              borderpad=0,
                                              sep=5,
                                              color=scale_color,
                                              frameon=False,
                                              size_vertical=0.1,
                                              fontproperties=fontprops,
                                              bbox_to_anchor=(0., 1.),
                                              bbox_transform=ax1.transAxes
                                              )
                x_scale_bar.set(zorder=len(traces) + 22)
                ax1.add_artist(x_scale_bar)

    if (not spike_train_format) and (frame_times is not None):
        min_time = np.min(frame_times)
        max_time = np.max(frame_times)

    if display_spike_nums:
        for cell, spikes in enumerate(spike_nums):
            if spike_train_format:
                if cell == 0:
                    min_time = np.min(spikes)
                else:
                    min_time = int(np.min((min_time, np.min(spikes))))
                max_time = int(np.ceil(np.max((max_time, np.max(spikes)))))

            # print(f"Neuron {y}, total spikes {len(np.where(neuron)[0])}, "
            #       f"nb > 2: {len(np.where(neuron>2)[0])}, nb < 2: {len(np.where(neuron[neuron<2])[0])}")
            if display_traces:
                # same color as traces
                color_neuron = cm.rainbow(((cell % max_n_color) + 1) / (max_n_color + 1))
            else:
                color_neuron = cell_spikes_color
            if cells_to_highlight is not None:
                if cell in cells_to_highlight:
                    index = np.where(cells_to_highlight == cell)[0][0]
                    color_neuron = cells_to_highlight_colors[index]
            if spike_train_format:
                neuron_times = spikes
            else:
                neuron_times = np.where(spikes > 0)[0]
                if frame_times is not None:
                    neuron_times = frame_times[neuron_times]
            if spike_shape != "|":
                if plot_with_amplitude:
                    ax1.scatter(neuron_times, np.repeat(cell, len(neuron_times)),
                                color=scalar_map.to_rgba(spikes[spikes > 0]),
                                marker=spike_shape,
                                s=spike_shape_size, zorder=20)
                elif desaturate_color_according_to_normalized_amplitude:
                    n_spikes = len(neuron_times)
                    colors_list = [sns.desaturate(x, p) for x, p in
                                   zip([color_neuron] * n_spikes, spikes[neuron_times])]
                    ax1.scatter(neuron_times, np.repeat(cell, len(neuron_times)),
                                color=colors_list,
                                marker=spike_shape,
                                s=spike_shape_size, zorder=20)
                else:
                    if display_traces:
                        y_values = traces[cell, neuron_times] + cell
                    else:
                        y_values = np.repeat(cell, len(neuron_times))
                    ax1.scatter(neuron_times, y_values, color=color_neuron, marker=spike_shape,
                                s=spike_shape_size, zorder=20)
            else:
                if desaturate_color_according_to_normalized_amplitude:
                    n_spikes = len(neuron_times)
                    colors_list = [sns.desaturate(x, p) for x, p in
                                   zip([color_neuron] * n_spikes, spikes[neuron_times])]
                    ax1.vlines(neuron_times, cell - .5, cell + .5, color=colors_list,
                               linewidth=spike_shape_size, zorder=20)
                elif plot_with_amplitude:
                    ax1.vlines(neuron_times, cell - .5, cell + .5, color=scalar_map.to_rgba(spikes[spikes > 0]),
                               linewidth=spike_shape_size, zorder=20)
                else:
                    ax1.vlines(neuron_times, cell - .5, cell + .5, color=color_neuron, linewidth=spike_shape_size,
                               zorder=20)
        if show_y_scale or show_x_scale:
            if x_ticks_labels_color is not None:
                scale_color = x_ticks_labels_color
            else:
                scale_color = 'white' if figure_background_color == (0.0, 0.0, 0.0, 1.0) else 'black'
            fontprops = fm.FontProperties(size=x_ticks_labels_size, family='monospace')
            # X-axis scale
            if show_x_scale and (x_scale_length is not None) and (x_scale_unit is not None) and (
                    x_scale_label is not None):
                x_scale_bar = AnchoredSizeBar(transform=ax1.transData,
                                              size=x_scale_length, label=f'{x_scale_label} {x_scale_unit}', loc=3,
                                              label_top=True,
                                              pad=0.1,
                                              borderpad=0,
                                              sep=5,
                                              color=scale_color,
                                              frameon=False,
                                              size_vertical=0.1,
                                              fontproperties=fontprops,
                                              bbox_to_anchor=(0., 1.),
                                              bbox_transform=ax1.transAxes
                                              )
                ax1.add_artist(x_scale_bar)

    if lines_to_display is not None:
        """
        lines_to_display=None,
                       lines_color="white",
                       lines_width=1,
                       lines_band=0,
                       lines_band_color="white"
                       dict that takes for a key a tuple of int representing 2 cells, and as value a list of tuple of 2 float
    representing the 2 extremities of a line between those 2 cells. By defualt, no lines
        """
        for cells_tuple, spike_times_list in lines_to_display.items():
            for spike_times in spike_times_list:
                ax1.plot(list(spike_times), list(cells_tuple),
                         color=lines_color,
                         linewidth=lines_width, zorder=30, alpha=1)
                if lines_band > 0:
                    xy = np.zeros((4, 2))
                    xy[0, 0] = spike_times[0] - lines_band
                    xy[0, 1] = cells_tuple[0]
                    xy[1, 0] = spike_times[1] - lines_band
                    xy[1, 1] = cells_tuple[1]
                    xy[2, 0] = spike_times[1] + lines_band
                    xy[2, 1] = cells_tuple[1]
                    xy[3, 0] = spike_times[0] + lines_band
                    xy[3, 1] = cells_tuple[0]
                    band_patch = patches.Polygon(xy=xy,
                                                 fill=True,
                                                 # linewidth=line_width,
                                                 facecolor=lines_band_color,
                                                 # edgecolor=edge_color,
                                                 alpha=0.4,
                                                 zorder=10)  # lw=2
                    ax1.add_patch(band_patch)
                    # ax1.fill_between(list(spike_times), np.array(cells_tuple)-lines_band,
                    #                  np.array(cells_tuple)+lines_band, facecolor=lines_band_color, alpha=0.4,
                    #                  zorder=10)
    if seq_times_to_color_dict is not None:
        seq_count = 0
        links_labels = []
        links_labels_color = []
        links_labels_y_coord = []
        if jitter_links_range > 0:
            nb_jitters = 10
            indices_rand_x = np.linspace(-jitter_links_range, jitter_links_range, nb_jitters)
            np.random.shuffle(indices_rand_x)
        for seq_indices, seq_times_list in seq_times_to_color_dict.items():
            nb_seq_times = 0
            for times_list_index, times_list in enumerate(seq_times_list):
                x_coord_to_link = []
                y_coord_to_link = []
                for time_index, t in enumerate(times_list):
                    cell_index = seq_indices[time_index]
                    # in case of this seq of cell would be used in a zoom version of the raster
                    if cell_index >= n_cells:
                        continue
                    # first we make sure the cell does spike at the given time
                    if spike_train_format:
                        if t not in spike_nums[cell_index]:
                            continue
                    else:
                        pass
                        if spike_nums[cell_index, t] == 0:
                            cell_for_msg = cell_index
                            if y_ticks_labels is not None:
                                cell_for_msg = y_ticks_labels[cell_index]
                            print(f"Not there: seq {times_list_index} cell {cell_for_msg} - {cell_index}, "
                                  f"time {t}")
                            continue
                        # print(f"## There: seq {times_list_index} cell {cell_index}, time {t}")
                    if link_seq_color is not None:
                        x_coord_to_link.append(t)
                        y_coord_to_link.append(cell_index)
                    else:
                        # if so, we draw the spike
                        if spike_shape != "|":
                            ax1.scatter(t, cell_index, color=seq_colors[seq_indices],
                                        marker=spike_shape,
                                        s=spike_shape_size, zorder=20)
                        else:
                            ax1.vlines(t, cell_index - .5, cell_index + .5, color=seq_colors[seq_indices],
                                       linewidth=1, zorder=20)
                if (link_seq_color is not None) and (len(x_coord_to_link) >= min_len_links_seq):
                    if isinstance(link_seq_color, str):
                        color_to_use = link_seq_color
                    elif isinstance(link_seq_color, dict):
                        color_to_use = link_seq_color[seq_indices]
                    else:
                        color_to_use = link_seq_color[seq_count % len(link_seq_color)]
                    x_coord_to_link = np.array(x_coord_to_link)
                    if jitter_links_range > 0:
                        jitter_to_add = indices_rand_x[seq_count % nb_jitters]
                    else:
                        jitter_to_add = 0
                    ax1.plot(x_coord_to_link + jitter_to_add, y_coord_to_link,
                             color=color_to_use,
                             linewidth=link_seq_line_width, zorder=30, alpha=link_seq_alpha)
                    nb_seq_times += 1
            if nb_seq_times > 0:
                category = ""
                if link_seq_categories is not None:
                    category = "*" * link_seq_categories[seq_indices]
                links_labels.append(f"l{len(seq_indices)}, r{nb_seq_times} {category}")
                links_labels_color.append(color_to_use)
                links_labels_y_coord.append((seq_indices[0] + seq_indices[-1]) / 2)
            seq_count += 1

    if display_traces:
        ax1.set_ylim([- shift_up, n_cells * shift_up + max(traces[-1, :])])
    else:
        ax1.set_ylim(-0.5, n_cells)
    if y_ticks_labels is not None:
        if display_traces:
            ax1.set_yticks(np.arange(start=0, stop=n_cells*shift_up, step=shift_up))
        else:
            cell_index_step_size = int(50)
            ax1.set_yticks(np.arange(start=0, stop=n_cells, step=cell_index_step_size))
            y_ticks_labels = y_ticks_labels[0::cell_index_step_size]
        ax1.set_yticklabels(y_ticks_labels)
    if (x_ticks_labels is not None) and (x_ticks is not None):
        ax1.set_xticks(x_ticks)
        ax1.tick_params('x', length=2, width=0.5, which='both')
        ax1.set_xticklabels(x_ticks_labels, rotation=45)  # ha="right", va="center
    if x_ticks_labels_size is not None:
        ax1.xaxis.set_tick_params(labelsize=x_ticks_labels_size)
    if y_ticks_labels_size is not None:
        ax1.yaxis.set_tick_params(labelsize=y_ticks_labels_size)
    else:
        if n_cells < 50:
            y_ticks_labels_size = 5
        elif n_cells < 100:
            y_ticks_labels_size = 4
        elif n_cells < 200:
            y_ticks_labels_size = 3
        elif n_cells < 400:
            y_ticks_labels_size = 1
        else:
            y_ticks_labels_size = 0.1
        ax1.yaxis.set_tick_params(labelsize=y_ticks_labels_size)

    if hide_raster_y_ticks_labels:
        ax1.tick_params(labelleft=False)

    if without_ticks:
        if x_ticks is not None:
            ax1.tick_params(axis='y', which='both', length=0)
        else:
            ax1.tick_params(axis='both', which='both', length=0)

    if seq_times_to_color_dict is not None:
        if link_seq_color is not None:
            ax_right = ax1.twinx()
            ax_right.set_frame_on(False)
            ax_right.set_ylim(-1, n_cells)
            ax_right.set_yticks(links_labels_y_coord)
            # clusters labels
            ax_right.set_yticklabels(links_labels)
            ax_right.yaxis.set_ticks_position('none')
            if y_ticks_labels_size > 1:
                y_ticks_labels_size -= 1
            else:
                y_ticks_labels_size -= 0.5
            ax_right.yaxis.set_tick_params(labelsize=y_ticks_labels_size)
            # ax_right.yaxis.set_tick_params(labelsize=2)
            for index in np.arange(len(links_labels)):
                ax_right.get_yticklabels()[index].set_color(links_labels_color[index])

    if spike_train_format:
        n_times = int(math.ceil(max_time - min_time))
    else:
        if spike_nums is None:
            n_times = traces.shape[1]
        else:
            n_times = len(spike_nums[0, :])

    # draw span to highlight some periods
    if span_area_coords is not None and (len(span_area_coords) > 0) and (span_area_colors is not None) and \
            (len(span_area_coords) == len(span_area_colors)):
        # if len(span_area_coords) != len(span_area_colors):
        #     raise Exception("span_area_coords and span_area_colors are not the same size")
        for index, span_area_coord in enumerate(span_area_coords):
            for coord in span_area_coord:
                if span_area_colors is not None:
                    color = span_area_colors[index]
                else:
                    color = "lightgrey"
                ax1.axvspan(coord[0], coord[1], alpha=alpha_span_area, facecolor=color, zorder=1)

    if (span_cells_to_highlight is not None):
        for index, cell_to_span in enumerate(span_cells_to_highlight):
            ax1.axhspan(cell_to_span - 0.5, cell_to_span + 0.5, alpha=0.4,
                        facecolor=span_cells_to_highlight_colors[index])

    if horizontal_lines is not None:
        line_beg_x = 0
        line_end_x = 0
        if spike_train_format or (frame_times is not None):
            line_beg_x = min_time - 1
            line_end_x = max_time + 1
        else:
            line_beg_x = -1
            line_end_x = n_times + 1
        if horizontal_lines_linewidth is None:
            ax1.hlines(horizontal_lines, line_beg_x, line_end_x, color=horizontal_lines_colors, linewidth=2,
                       linestyles=horizontal_lines_sytle)
        else:
            ax1.hlines(horizontal_lines, line_beg_x, line_end_x, color=horizontal_lines_colors,
                       linewidth=horizontal_lines_linewidth,
                       linestyles=horizontal_lines_sytle)

    if vertical_lines is not None:
        line_beg_y = 0
        line_end_y = n_cells - 1
        ax1.vlines(vertical_lines, line_beg_y, line_end_y, color=vertical_lines_colors,
                   linewidth=vertical_lines_linewidth,
                   linestyles=vertical_lines_sytle)

    if spike_train_format or (frame_times is not None):
        ax1.set_xlim(min_time - 1, max_time + 1)
    else:
        ax1.set_xlim(-1, n_times + 1)
    # ax1.margins(x=0, tight=True)

    if not without_activity_sum or hide_x_ticks_labels:
        ax1.get_xaxis().set_visible(False)

    if title is not None:
        ax1.set_title(title)
    # Give x axis label for the spike raster plot
    # ax.xlabel('Frames')
    # Give y axis label for the spike raster plot
    if raster_y_axis_label is not None:
        ax1.set_ylabel(raster_y_axis_label)
    if raster_y_axis_label_size is not None:
        ax1.yaxis.label.set_size(raster_y_axis_label_size)
    ax1.xaxis.label.set_color(axes_label_color)
    ax1.yaxis.label.set_color(axes_label_color)

    # ax1.spines['left'].set_color(y_ticks_labels_color)
    # ax1.spines['bottom'].set_color(x_ticks_labels_color)
    # ax1.yaxis.label.set_color(y_ticks_labels_color)
    if isinstance(y_ticks_labels_color, list):
        for xtick, color in zip(ax1.get_yticklabels(), y_ticks_labels_color):
            xtick.set_color(color)
    else:
        ax1.tick_params(axis='y', colors=y_ticks_labels_color)
    ax1.tick_params(axis='x', colors=x_ticks_labels_color)

    # removing frame
    ax1.set_frame_on(False)

    if traces is not None and display_traces:
        ax1.set_ylim([- shift_up, n_cells * shift_up + max(traces[-1, :])])

    if (axes_list is not None) and without_activity_sum:
        return

    if not without_activity_sum:
        # ################################################################################################
        # ################################ Activity sum plot part ################################
        # ################################################################################################
        if (sliding_window_duration >= 1) and (spikes_sum_to_use is None):
            if frame_times is not None:
                # we use the neo format
                spike_trains = []
                # spike trains is a list of 1d np array with timestamps
                for spikes in spike_nums_for_activity_sum:
                    time_stamps = frame_times[np.where(spikes)[0]]
                    if times_format == "sec":
                        #then we transform it in ms
                        time_stamps = np.array([t * 1000 for t in time_stamps])
                    spike_trains.append(time_stamps)

                binsize = bin_size_ms_for_spikes_sum * pq.ms

                # first we create a spike_trains in the neo format, will put the timestamps in ms
                spike_trains, t_start, t_stop = create_spike_train_neo_format(spike_trains)
                n_cells = len(spike_trains)

                neo_spike_trains = []
                for cell in np.arange(n_cells):
                    spike_train = spike_trains[cell]
                    # print(f"n_spikes: {cells_label[cell]}: {len(spike_train)}")
                    neo_spike_train = neo.SpikeTrain(times=spike_train, units='ms',
                                                     t_start=t_start,
                                                     t_stop=t_stop)
                    neo_spike_trains.append(neo_spike_train)

                spike_trains_binned = elephant_conv.BinnedSpikeTrain(neo_spike_trains, binsize=binsize)
                spike_trains_binned = spike_trains_binned.to_bool_array().astype("int8")
                sum_spikes = np.sum(spike_trains_binned, axis=0)
            else:
                sum_spikes = np.zeros(n_times)
                if spike_train_format:
                    # TODO: use the same method as above when frame_times is not None
                    windows_sum = np.zeros((n_cells, n_times), dtype="int16")
                    # one cell can participate to max one spike by window
                    # if value is True, it means this cell has already been counted
                    cell_window_participation = np.zeros((n_cells, n_times), dtype="bool")
                    for cell, spikes_train in enumerate(spike_nums_for_activity_sum):
                        for spike_time in spikes_train:
                            # first determining to which windows to add the spike
                            spike_index = int(spike_time - min_time)
                            first_index_window = np.max((0, spike_index - sliding_window_duration))
                            if np.sum(cell_window_participation[cell, first_index_window:spike_index]) == 0:
                                windows_sum[cell, first_index_window:spike_index] += 1
                                cell_window_participation[cell, first_index_window:spike_index] = True
                            else:
                                for t in np.arange(first_index_window, spike_index):
                                    if cell_window_participation[cell, t] is False:
                                        windows_sum[cell, t] += 1
                                        cell_window_participation[cell, t] = True
                    sum_spikes = np.sum(windows_sum, axis=0)
                    if debug_mode:
                        print("sliding window over")
                    # for index, t in enumerate(np.arange(int(min_time), int((np.ceil(max_time) - sliding_window_duration)))):
                    #     # counting how many cell fire during that window
                    #     if (index % 1000) == 0:
                    #         print(f"index {index}")
                    #     sum_value = 0
                    #     t_min = t
                    #     t_max = t + sliding_window_duration
                    #     for spikes_train in spike_nums:
                    #         # give the indexes
                    #         # np.where(np.logical_and(spikes_train >= t, spikes_train < t_max))
                    #         spikes = spikes_train[np.logical_and(spikes_train >= t, spikes_train < t_max)]
                    #         nb_spikes = len(spikes)
                    #         if nb_spikes > 0:
                    #             sum_value += 1
                    #     sum_spikes[index] = sum_value
                    # sum_spikes[(n_times - sliding_window_duration):] = sum_value
                else:
                    for t in np.arange(0, (n_times - sliding_window_duration)):
                        # One spike by cell max in the sum process
                        sum_value = np.sum(spike_nums_for_activity_sum[:, t:(t + sliding_window_duration)], axis=1)
                        sum_spikes[t] = len(np.where(sum_value)[0])
                    sum_spikes[(n_times - sliding_window_duration):] = len(np.where(sum_value)[0])
        elif spikes_sum_to_use is None:
            if spike_train_format:
                pass
            else:
                # binary_spikes = np.zeros((n_cells, n_times), dtype="int8")
                # for spikes, spikes in enumerate(spike_nums_for_activity_sum):
                #     binary_spikes[spikes, spikes > 0] = 1
                # # if (param is not None) and (param.bin_size > 1):
                # #     sum_spikes = np.mean(np.split(np.sum(binary_spikes, axis=0), n_times // param.bin_size), axis=1)
                # #     sum_spikes = np.repeat(sum_spikes, param.bin_size)
                # # else:
                sum_spikes = np.sum(spike_nums_for_activity_sum, axis=0)
        else:
            sum_spikes = spikes_sum_to_use

        if spike_train_format or (frame_times is not None):
            x_value = np.linspace(min_time, max_time, len(sum_spikes))
        else:
            x_value = np.arange(n_times)

        if plot_with_amplitude:
            ax2 = fig.add_subplot(inner[1], sharex=ax1)

        ax2.set_facecolor(activity_sum_face_color)

        # sp = UnivariateSpline(x_value, sum_spikes, s=240)
        # ax2.fill_between(x_value, 0, smooth_curve(sum_spikes), facecolor="black") # smooth_curve(sum_spikes)
        if show_sum_spikes_as_percentage:
            if debug_mode:
                print("using percentages")
            sum_spikes = sum_spikes / n_cells
            sum_spikes *= 100
            if activity_threshold is not None:
                activity_threshold = activity_threshold / n_cells
                activity_threshold *= 100

        ax2.fill_between(x_value, 0, sum_spikes, facecolor=activity_sum_plot_color, zorder=10)

        if activity_threshold is not None:
            line_beg_x = 0
            line_end_x = 0
            if spike_train_format:
                line_beg_x = min_time - 1
                line_end_x = max_time + 1
            else:
                if frame_times is not None:
                    line_beg_x = min(frame_times)
                    line_end_x = max(frame_times)
                else:
                    line_beg_x = -1
                    line_end_x = len(spike_nums_for_activity_sum[0, :]) + 1
            if len(np.unique(activity_threshold)) == 1:
                ax2.hlines(activity_threshold, line_beg_x, line_end_x, color="red", linewidth=1, linestyles="dashed")
            else:
                ax2.plot(frame_times, activity_threshold, color="red", linewidth=1)

        # draw span to highlight some periods
        if (span_area_coords is not None) and (not span_area_only_on_raster):
            for index, span_area_coord in enumerate(span_area_coords):
                for coord in span_area_coord:
                    if span_area_colors is not None:
                        color = span_area_colors[index]
                    else:
                        color = "lightgrey"
                    ax2.axvspan(coord[0], coord[1], alpha=0.5, facecolor=color, zorder=1)

        # early born
        if (cells_to_highlight is not None) and color_peaks_activity:
            for index, cell_to_span in enumerate(cells_to_highlight):
                ax2.vlines(np.where(spike_nums_for_activity_sum[cell_to_span, :])[0], 0, np.max(sum_spikes),
                           color=cells_to_highlight_colors[index],
                           linewidth=2, linestyles="dashed", alpha=0.2)

        # ax2.yaxis.set_visible(False)
        ax2.set_frame_on(False)
        if hide_x_ticks_labels:
            ax2.get_xaxis().set_visible(False)
        else:
            ax2.get_xaxis().set_visible(True)

        if activity_sum_specified_y_lim is True and y_lim_sum_activity is not None:
            ax2.set_ylim(bottom=0, top=y_lim_sum_activity, emit=False, auto=False)
        else:
            ax2.set_ylim(bottom=0, top=np.max(sum_spikes) + 2, emit=False, auto=False)

        if spike_train_format or (frame_times is not None):
            ax2.set_xlim(min_time - 1, max_time + 1)
        else:
            if spike_nums_for_activity_sum is not None:
                ax2.set_xlim(-1, len(spike_nums_for_activity_sum[0, :]) + 1)
            else:
                ax2.set_xlim(-1, len(spikes_sum_to_use) + 1)

        if SCE_times is not None:
            ax_top = ax2.twiny()
            ax_top.set_frame_on(False)
            if spike_train_format:
                ax_top.set_xlim(min_time - 1, max_time + 1)
            else:
                if spike_nums_for_activity_sum is not None:
                    ax_top.set_xlim(-1, len(spike_nums_for_activity_sum[0, :]) + 1)
                else:
                    ax_top.set_xlim(-1, len(spikes_sum_to_use) + 1)
            xticks_pos = []
            for times_tuple in SCE_times:
                xticks_pos.append(times_tuple[0])
            ax_top.set_xticks(xticks_pos)
            ax_top.xaxis.set_ticks_position('none')
            ax_top.set_xticklabels(np.arange(len(SCE_times)))
            ax_top.tick_params(axis='x', colors=x_ticks_labels_color)
            plt.setp(ax_top.xaxis.get_majorticklabels(), rotation=90)
            if len(SCE_times) > 30:
                ax_top.xaxis.set_tick_params(labelsize=3)
            elif len(SCE_times) > 50:
                ax_top.xaxis.set_tick_params(labelsize=2)
            elif len(SCE_times) > 100:
                ax_top.xaxis.set_tick_params(labelsize=1)
            elif len(SCE_times) > 300:
                ax_top.xaxis.set_tick_params(labelsize=0.5)
            else:
                ax_top.xaxis.set_tick_params(labelsize=4)
        # print(f"max sum_spikes {np.max(sum_spikes)}, mean  {np.mean(sum_spikes)}, median {np.median(sum_spikes)}")

        if without_ticks:
            ax2.tick_params(axis='both', which='both', length=0)

        if isinstance(y_ticks_labels_color, list):
            for xtick, color in zip(ax2.get_yticklabels(), y_ticks_labels_color):
                xtick.set_color(color)
        else:
            ax2.tick_params(axis='y', colors=y_ticks_labels_color, labelsize=y_ticks_labels_size)
        ax2.tick_params(axis='x', colors=x_ticks_labels_color)

        if (x_ticks_labels is not None) and (x_ticks is not None):
            ax2.set_xticks(x_ticks)
            ax2.tick_params('x', length=2, width=0.5, which='both')
            ax2.set_xticklabels(x_ticks_labels, rotation=45)  # ha="right", va="center
        if x_ticks_labels_size is not None:
            ax2.xaxis.set_tick_params(labelsize=x_ticks_labels_size)
        ax2.xaxis.label.set_color(axes_label_color)
        ax2.yaxis.label.set_color(axes_label_color)

        if show_activity_sum_label:
            if show_sum_spikes_as_percentage:
                ax2.set_ylabel('Active (%)', fontsize=raster_y_axis_label_size, color=axes_label_color)
            else:
                ax2.set_ylabel(f'Active (\u03A3)', fontsize=raster_y_axis_label_size, color=axes_label_color)

    # color bar section
    if plot_with_amplitude:
        inner_2 = gridspec.GridSpecFromSubplotSpec(1, 1,
                                                   subplot_spec=outer[1])  # , wspace=0.1, hspace=0.1)
        ax3 = fig.add_subplot(inner_2[0])  # plt.Subplot(fig, inner_2[0])
        cb = fig.colorbar(scalar_map, cax=ax3)
        cb.ax.tick_params(axis='y', colors="white")
    if axes_list is None:
        if save_raster and (path_results is not None):
            # transforming a string in a list
            if isinstance(save_formats, str):
                save_formats = [save_formats]
            time_str = ""
            if with_timestamp_in_file_name:
                time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
            for save_format in save_formats:
                if not with_timestamp_in_file_name:
                    fig.savefig(os.path.join(f'{path_results}', f'{file_name}.{save_format}'),
                                format=f"{save_format}",
                                facecolor=fig.get_facecolor())
                else:
                    fig.savefig(os.path.join(f'{path_results}', f'{file_name}_{time_str}.{save_format}'),
                                format=f"{save_format}",
                                facecolor=fig.get_facecolor())
        # Display the spike raster plot
        if show_raster:
            plt.show()
        plt.close()


def plot_with_imshow(raster, path_results=None, file_name=None, n_subplots=4, axes_list=None,
                     y_ticks_labels=None, y_ticks_labels_size=None,
                     speed_array=None,
                     fig=None, show_color_bar=False, hide_x_labels=True, without_ticks=True,
                     vmin=0.5, vmax=None, x_ticks_labels_color="white", y_ticks_labels_color="white",
                     values_to_plot=None, cmap="hot", show_fig=False, save_formats="pdf",
                     lines_to_display=None,
                     lines_color="white",
                     lines_width=1,
                     lines_band=0,
                     lines_band_color="white",
                     lines_band_alpha=0.5,
                     reverse_order=False,
                     x_ticks_labels_size=None,
                     background_color="black",
                     show_yaxis_title=False,
                     speeed_line_color="royalblue", ylabel_fontsize=5, axis_color="black", hide_cell_index=True,
                     hide_speed_values=False, y_label_suplot="Speed"):
    """

    :param raster: a 2-d array, 1d represents the cells, 2nd the times
    :param n_subplots: Divide the plot in n_subplots
    :param values_to_plot:
    :param cmap: colormap to use, by default "hot"
    :return:
    """
    n_cells, n_times = raster.shape

    if (speed_array is not None) and (speed_array.shape[0] != n_times):
        speed_array = None
    if axes_list is None:
        if speed_array is None:
            fig, axes = plt.subplots(nrows=n_subplots, ncols=1,
                                     gridspec_kw={'height_ratios': [1 / n_subplots] * n_subplots,
                                                  'width_ratios': [1]},
                                     figsize=(15, 6))
            fig.patch.set_facecolor(background_color)
        else:
            final_n_rows = 2 * n_subplots
            hr = [3 if (i % 2) == 0 else 1 for i in range(final_n_rows)]
            fig, axes = plt.subplots(nrows=final_n_rows, ncols=1, sharex=True,
                                     gridspec_kw={'height_ratios': hr,
                                                  'width_ratios': [1]},
                                     figsize=(15, 6))
            fig.patch.set_facecolor(background_color)
    else:
        axes = axes_list

    if (n_subplots == 1) and (axes_list is None):
        axes = [axes]
    if vmax is None:
        vmax = np.max(raster)

    if speed_array is None:
        # plot only the sequences
        for ax_index, ax in enumerate(axes):
            # Set common plot config
            ax.set_facecolor(background_color)
            ax.yaxis.label.set_color(y_ticks_labels_color)
            ax.xaxis.label.set_color(x_ticks_labels_color)
            ax.tick_params(axis='y', colors=y_ticks_labels_color)
            ax.tick_params(axis='x', colors=x_ticks_labels_color)

            ax.set_xticks(np.arange(0, (n_times // n_subplots), 100))
            ax.set_xticklabels(np.arange((n_times // n_subplots) * ax_index, (n_times // n_subplots) * (ax_index + 1), 100))
            ax.xaxis.set_tick_params(labelsize=x_ticks_labels_size)

            if y_ticks_labels_size is not None:
                ax.yaxis.set_tick_params(labelsize=y_ticks_labels_size)

            if without_ticks:
                ax.tick_params(axis='x', which='both', length=0)
                ax.tick_params(axis='y', which='both', length=0)

            im = ax.imshow(raster[:, (n_times // n_subplots) * ax_index:(n_times // n_subplots) * (ax_index + 1)],
                           cmap=plt.get_cmap(cmap), aspect='auto', vmin=vmin, vmax=vmax)

            if hide_x_labels:
                ax.tick_params(axis='x', colors=background_color)
            if hide_cell_index:
                ax.tick_params(axis='y', colors=background_color)

            if show_yaxis_title:
                ax.set_ylabel(f"{n_cells} Cells", fontsize=ylabel_fontsize)

            if without_ticks:
                ax.tick_params(axis='x', which='both', length=0)
                ax.tick_params(axis='y', which='both', length=0)

            if y_ticks_labels is not None:
                ax.set_yticks(np.arange(raster.shape[0]))
                ax.set_yticklabels(y_ticks_labels[:])

            if y_ticks_labels_size is not None:
                ax.yaxis.set_tick_params(labelsize=y_ticks_labels_size)

            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)

    else:
        for ax_index, ax in enumerate(axes):
            plot_ax_index = int(ax_index / 2)

            # Set common plot config
            ax.set_facecolor(background_color)
            ax.yaxis.label.set_color(y_ticks_labels_color)
            ax.xaxis.label.set_color(x_ticks_labels_color)
            ax.tick_params(axis='y', colors=y_ticks_labels_color)
            ax.tick_params(axis='x', colors=x_ticks_labels_color)

            ax.set_xticks(np.arange(0, (n_times // n_subplots), 100))
            ax.set_xticklabels(
                np.arange((n_times // n_subplots) * plot_ax_index, (n_times // n_subplots) * (plot_ax_index + 1), 100))
            ax.xaxis.set_tick_params(labelsize=x_ticks_labels_size)

            if y_ticks_labels_size is not None:
                ax.yaxis.set_tick_params(labelsize=y_ticks_labels_size)

            if without_ticks:
                ax.tick_params(axis='x', which='both', length=0)
                ax.tick_params(axis='y', which='both', length=0)

            # Found if axe index is even or odd: even means we plot the sequences, odd means we plot the speed
            if (ax_index % 2) == 0:
                im = ax.imshow(raster[:, (n_times // n_subplots) * plot_ax_index:(n_times // n_subplots) * (plot_ax_index + 1)],
                               cmap=plt.get_cmap(cmap), aspect='auto', vmin=vmin, vmax=vmax)
                if y_ticks_labels is not None:
                    ax.set_yticks(np.arange(raster.shape[0]))
                    ax.set_yticklabels(y_ticks_labels[:])
                if hide_x_labels:
                    ax.tick_params(axis='x', colors=background_color)
                if hide_cell_index:
                    ax.tick_params(axis='y', colors=background_color)
                if show_yaxis_title:
                    ax.set_ylabel(f"{n_cells} Cells", fontsize=ylabel_fontsize)
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.spines['bottom'].set_visible(False)
                ax.spines['left'].set_visible(False)
            else:
                ax.plot(np.arange(0, (n_times // n_subplots)), speed_array[(n_times // n_subplots) * plot_ax_index:
                                                                           (n_times // n_subplots) * (plot_ax_index + 1)],
                        color=speeed_line_color, lw=0.1, zorder=20)
                ax.set_ylim(bottom=0, top=(1.1 * np.max(speed_array)), emit=False)
                ax.spines['left'].set_color(axis_color)
                ax.spines['right'].set_color(background_color)
                ax.spines['bottom'].set_color(axis_color)
                ax.spines['top'].set_color(background_color)
                if show_yaxis_title:
                    ax.set_ylabel(f"{y_label_suplot}", fontsize=ylabel_fontsize)
                if hide_x_labels:
                    ax.tick_params(axis='x', colors=background_color)
                if hide_speed_values:
                    ax.tick_params(axis='y', colors=background_color)

        # ax.axis('off')
    # extent=[0, 10, 0, 1],
    # ax1.imshow(,  cmap=plt.get_cmap("hot")) # extent=[0, 1, 0, 1],
    # sns.heatmap(amplitude_spike_nums_ordered[:max_index_seq + 1, :],
    #             cbar=False, ax=ax1, cmap=plt.get_cmap("hot"), rasterized=True) #
    if show_color_bar and (fig is not None):
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cb = fig.colorbar(im, cax=cax, orientation='vertical')
        cb.ax.tick_params(axis='y', colors="white")

    if lines_to_display is not None and n_subplots == 1:
        """
        lines_to_display=None,
                       lines_color="white",
                       lines_width=1,
                       lines_band=0,
                       lines_band_color="white"
                       dict that takes for a key a tuple of int representing 2 cells, and as value a list of tuple of 2 float
    representing the 2 extremities of a line between those 2 cells. By defualt, no lines
        """
        ax = axes[0]
        for cells_tuple, spike_times_list in lines_to_display.items():
            for spike_times in spike_times_list:
                # ax.plot(list(spike_times), list(cells_tuple),
                #          color=lines_color,
                #          linewidth=lines_width, zorder=30, alpha=1)
                if lines_band > 0:
                    xy = np.zeros((4, 2))
                    xy[0, 0] = spike_times[0] - lines_band
                    xy[0, 1] = cells_tuple[0]
                    xy[1, 0] = spike_times[1] - lines_band
                    xy[1, 1] = cells_tuple[1]
                    xy[2, 0] = spike_times[1] + lines_band
                    xy[2, 1] = cells_tuple[1]
                    xy[3, 0] = spike_times[0] + lines_band
                    xy[3, 1] = cells_tuple[0]
                    band_patch = patches.Polygon(xy=xy,
                                                 fill=True,
                                                 # linewidth=line_width,
                                                 facecolor=lines_band_color,
                                                 # edgecolor=edge_color,
                                                 alpha=lines_band_alpha,
                                                 zorder=10)  # lw=2
                    ax.add_patch(band_patch)
    if reverse_order:
        for ax in axes:
            ax.set_ylim(ax.get_ylim()[::-1])

    if axes_list is None:
        if show_fig:
            plt.show()
        if (path_results is not None) and (file_name is not None):
            if isinstance(save_formats, str):
                save_formats = [save_formats]

            for save_format in save_formats:
                fig.savefig(f'{path_results}/{file_name}.{save_format}',
                            format=f"{save_format}",
                            facecolor=fig.get_facecolor())

        plt.close()


def plot_figure_with_map_and_raster_for_sequences(raster_dur, raw_traces, coord_obj, cells_in_seq,
                                                  span_area_coords, span_area_colors,
                                                  file_name, results_path, lines_to_display=None,
                                                  range_around_slope_in_frames=0,
                                                  without_sum_activity_traces=False,
                                                  frames_to_use=None, color_map_for_seq=cm.Reds,
                                                  speed_array=None, with_timestamp_in_file_name=True,
                                                  save_formats="pdf", dpi=500):
    """
    make a figure with cell map + 3 plots: fluorescence signal raw + blur and raster
    Args:
        raster_dur:
        raw_traces:
        coord_obj: Instance of CellsCoord in cicada.display.cells_map_utils
        cells_in_seq:
        span_area_coords:
        span_area_colors:
        file_name:
        results_path:
        lines_to_display:
        range_around_slope_in_frames:
        without_sum_activity_traces:
        frames_to_use:
        color_map_for_seq:
        speed_array:
        with_timestamp_in_file_name:
        save_formats:
        dpi:

    Returns:

    """
    # if ms.speed_by_frame is not None:
    #     speed_array = norm01(ms.speed_by_frame) - 1.5
    n_cells = raster_dur.shape[0]
    n_frames = raster_dur.shape[1]
    fig = plt.figure(figsize=(10, 11), dpi=dpi)  # constrained_layout=True,
    gs = fig.add_gridspec(12, 3)
    ax_empty = fig.add_subplot(gs[:3, 0])
    ax_map = fig.add_subplot(gs[:3, 1])
    ax_empty_2 = fig.add_subplot(gs[:3, 2])

    if without_sum_activity_traces:
        ax_raw_traces = fig.add_subplot(gs[3:7, :])
        ax_sum_raw_traces, ax_sum_all_raw_traces = (None, None)
    else:
        ax_raw_traces = fig.add_subplot(gs[3:5, :])
        ax_sum_raw_traces = fig.add_subplot(gs[5, :])
        ax_sum_all_raw_traces = fig.add_subplot(gs[6, :])

    ax_im_show = fig.add_subplot(gs[7:9, :])

    ax_raster = fig.add_subplot(gs[9:11, :])
    ax_empty_3 = fig.add_subplot(gs[11, :])
    background_color = "black"
    labels_color = "white"

    for ax in [ax_empty, ax_map, ax_empty_2, ax_raw_traces, ax_sum_raw_traces,
               ax_sum_all_raw_traces,
               ax_im_show, ax_raster, ax_empty_3]:
        if ax is None:
            continue
        ax.set_facecolor(background_color)
    fig.patch.set_facecolor(background_color)

    # first we display the cells map
    # color = (213 / 255, 38 / 255, 215 / 255, 1)  # #D526D7
    if color_map_for_seq is not None:
        cells_groups_colors = []
        cells_to_color = []
        for cell_index, cell in enumerate(cells_in_seq):
            cells_to_color.append([cell])
            color = color_map_for_seq(cell_index / (len(cells_in_seq)))
            # print(f"color {color}")
            cells_groups_colors.append(color)
    else:
        color = (67 / 255, 162 / 255, 202 / 255, 1)  # blue
        color = (33 / 255, 113 / 255, 181 / 255, 1)
        cells_groups_colors = [color]
        cells_to_color = [cells_in_seq]
    # check if at least a pair of cells intersect
    at_least_one_intersect = False
    for cell_index, cell_1 in enumerate(cells_in_seq[:-2]):
        for cell_2 in cells_in_seq[cell_index + 1:]:
            if cell_2 in coord_obj.intersect_cells[cell_1]:
                at_least_one_intersect = True
                break
        if at_least_one_intersect:
            break

    coord_obj.plot_cells_map(path_results=results_path,
                             ax_to_use=ax_map,
                             show_polygons=False,
                             fill_polygons=False,
                             connections_dict=None,
                             with_edge=True,
                             edge_line_width=0.2,
                             default_edge_color="#c6dbef",
                             cells_groups=cells_to_color,
                             cells_groups_colors=cells_groups_colors,
                             dont_fill_cells_not_in_groups=True,
                             with_cell_numbers=False,
                             cell_numbers_color="white",
                             text_size=2,
                             save_formats=save_formats)

    # one subplot for raw traces
    raw_traces_0_1 = np.copy(raw_traces)
    if frames_to_use is not None:
        raw_traces_0_1 = raw_traces_0_1[:, frames_to_use]
    for i in np.arange(len(raw_traces_0_1)):
        raw_traces_0_1[i] = (raw_traces_0_1[i] - np.mean(raw_traces_0_1[i]) / np.std(raw_traces_0_1[i]))
        raw_traces_0_1[i] = norm01(raw_traces_0_1[i])
        raw_traces_0_1[i] = norm01(raw_traces_0_1[i]) * 5

    plot_raster(spike_nums=raster_dur[cells_in_seq],
                path_results=results_path,
                display_spike_nums=False,
                axes_list=[ax_raw_traces],
                traces=raw_traces_0_1[cells_in_seq],
                display_traces=True,
                use_brewer_colors_for_traces=True,
                # cmap_name="Reds",
                spike_train_format=False,
                y_ticks_labels=cells_in_seq,
                y_ticks_labels_size=2,
                save_raster=False,
                show_raster=False,
                span_area_coords=span_area_coords,
                span_area_colors=span_area_colors,
                alpha_span_area=0.3,
                plot_with_amplitude=False,
                # raster_face_color="white",
                hide_x_ticks_labels=True,
                without_activity_sum=True,
                show_sum_spikes_as_percentage=True,
                span_area_only_on_raster=False,
                spike_shape='*',
                spike_shape_size=1,
                # lines_to_display=lines_to_display,
                # lines_color="white",
                # lines_width=0.35,
                # lines_band=range_around_slope_in_frames,
                # lines_band_color="white",
                save_formats="pdf")

    if not without_sum_activity_traces:
        # ploting sum of activity of the traces shown
        for traces_index, trace_to_use in enumerate([raw_traces_0_1[cells_in_seq], raw_traces_0_1]):
            sum_traces = np.sum(trace_to_use,
                                axis=0) \
                         / len(trace_to_use)
            sum_traces *= 100
            if traces_index == 0:
                ax_to_use = ax_sum_raw_traces
            else:
                ax_to_use = ax_sum_all_raw_traces
            ax_to_use.set_facecolor(background_color)
            ax_to_use.fill_between(np.arange(n_frames), 0, sum_traces, facecolor="#c6dbef", zorder=10)
            if span_area_coords is not None:
                for index, span_area_coord in enumerate(span_area_coords):
                    for coord in span_area_coord:
                        if span_area_colors is not None:
                            color = span_area_colors[index]
                        else:
                            color = "lightgrey"
                        ax_to_use.axvspan(coord[0], coord[1], alpha=0.6, facecolor=color, zorder=8)
            ax_to_use.set_xlim(0, n_frames - 1)
            ax_to_use.set_ylim(0, np.max(sum_traces))
            ax_to_use.get_xaxis().set_visible(False)
            # ax_to_use.get_xaxis().set_ticks([])
            ax_to_use.yaxis.label.set_color("white")
            # ax_to_use.xaxis.label.set_color("white")
            ax_to_use.tick_params(axis='y', colors="white")
            # ax_to_use.tick_params(axis='x', colors="white")
            ax_to_use.tick_params(axis='both', which='both', length=0)
            ax_to_use.yaxis.set_tick_params(labelsize=2)

    traces_for_imshow = np.copy(raw_traces[cells_in_seq])
    if frames_to_use is not None:
        traces_for_imshow = traces_for_imshow[:, frames_to_use]
    with_arnaud_normalization = True
    if with_arnaud_normalization:
        for i in np.arange(len(traces_for_imshow)):
            # traces_for_imshow[i] = traces_for_imshow[i] / np.median(traces_for_imshow[i])
            traces_for_imshow[i] = gaussblur1D(traces_for_imshow[i],
                                               traces_for_imshow.shape[1] / 2, 0)
            traces_for_imshow[i, :] = norm01(traces_for_imshow[i, :])
            traces_for_imshow[i, :] = traces_for_imshow[i, :] - np.median(traces_for_imshow[i, :])

    plot_with_imshow(raster=traces_for_imshow,
                     n_subplots=1, axes_list=[ax_im_show],
                     hide_x_labels=True,
                     y_ticks_labels_size=2,
                     y_ticks_labels=cells_in_seq,
                     fig=fig,
                     show_color_bar=False,
                     values_to_plot=None, cmap="hot",
                     without_ticks=True,
                     vmin=0, vmax=0.5,
                     reverse_order=True,
                     # lines_to_display=lines_to_display,
                     # lines_color="white",
                     # lines_width=0.2,
                     # lines_band=range_around_slope_in_frames,
                     # lines_band_color="white",
                     # lines_band_alpha=0.8,
                     speed_array=speed_array
                     )
    if frames_to_use is not None:
        x_ticks_labels = [x for x in frames_to_use if x % 100 == 0]
        x_ticks = [x for x in np.arange(0, 100 * len(x_ticks_labels), 100)]
    else:
        x_ticks_labels = [x for x in np.arange(n_frames) if x % 100 == 0]
        x_ticks = x_ticks_labels
    x_ticks_labels_size = 2

    cells_to_highlight = None
    cells_to_highlight_colors = None
    if color_map_for_seq is not None:
        cells_to_highlight_colors = []
        cells_to_highlight = []
        for cell_index, cell in enumerate(cells_in_seq):
            cells_to_highlight.append(cell_index)
            color = color_map_for_seq(cell_index / (len(cells_in_seq)))
            # print(f"color {color}")
            cells_to_highlight_colors.append(color)

    do_bin_raster = False
    bin_size = 12
    if do_bin_raster:
        raster_dur = bin_raster(raster=raster_dur, bin_size=bin_size, keep_same_dimension=True)

    plot_raster(spike_nums=raster_dur[cells_in_seq],
                path_results=results_path,
                x_ticks_labels=x_ticks_labels,
                x_ticks_labels_size=x_ticks_labels_size,
                x_ticks=x_ticks,
                size_fig=(10, 2),
                axes_list=[ax_raster],
                spike_train_format=False,
                y_ticks_labels=cells_in_seq,
                save_raster=False,
                show_raster=False,
                show_sum_spikes_as_percentage=True,
                without_activity_sum=True,
                plot_with_amplitude=False,
                span_area_coords=span_area_coords,
                span_area_colors=span_area_colors,
                cells_to_highlight=cells_to_highlight,
                cells_to_highlight_colors=cells_to_highlight_colors,
                alpha_span_area=0.5,
                # cells_to_highlight=cells_to_highlight,
                # cells_to_highlight_colors=cells_to_highlight_colors,
                # span_cells_to_highlight=span_cells_to_highlight,
                # span_cells_to_highlight_colors=span_cells_to_highlight_colors,
                span_area_only_on_raster=False,
                y_ticks_labels_size=1,
                spike_shape='o',
                spike_shape_size=0.1,
                cell_spikes_color="red",
                lines_to_display=lines_to_display,
                lines_color="white",
                lines_width=0.2,
                lines_band=range_around_slope_in_frames,
                lines_band_color="white",
                save_formats="pdf")
    # fig.tight_layout()
    fig.set_tight_layout({'rect': [0, 0, 1, 0.95], 'pad': 0.1, 'h_pad': 0})

    time_str = ""
    if with_timestamp_in_file_name:
        time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")

    if isinstance(save_formats, str):
        save_formats = [save_formats]
    for save_format in save_formats:
        fig.savefig(f'{results_path}/{file_name}'
                    f'_{time_str}.{save_format}',
                    format=f"{save_format}",
                    facecolor=fig.get_facecolor())

    plt.close()
