from sortedcontainers import SortedDict
import numpy as np
import matplotlib.pyplot as plt
import math
import os


def get_psth_values(data, epochs, ref_in_epoch, range_value, fcts_to_apply):
    """

    Args:
        data: 2d array (n_cells * n_frames) could be int or float, the value will be summed then normalize by the number
        of cells
        epochs: list of list of two int, representing the first and last_frame of each epoch. If an epoch is composed
        of only one frame, then the two int are the same.
        ref_in_epoch: str, either "start", "end", "middle", indicate what part of the epoch will be the "stimulus"
        time in the PSTH
        range_value: int, how many steps (frames) to collect before and after the "stimulus"
        fcts_to_apply: a list of functions that will be apply at each time point over the sums of the activity in each epoch
        in order to return one value.

    Returns: a list of the same length as fct_to_apply, containing a list of float of size '(range_value*2)+1'

    """
    if len(data.shape) != 2:
        print(f"get_psth_values(): data should have 2 dimensions, it has {len(data.shape)}")
        return

    n_frames = data.shape[1]
    n_cells = len(data)

    # --------------------------- SELECTING EVENT FRAMES ---------------------------

    epoch_frames = []
    # collecting the epoch frames around which center the PSTH depending on the option choosen
    for epoch in epochs:
        if ref_in_epoch == "end":
            epoch_frames.append(epoch[-1])
        elif ref_in_epoch == "middle":
            mean_frame = int((epoch[-1] + epoch[0]) // 2)
            epoch_frames.append(mean_frame)
        else:
            # first frame of the epoch
            epoch_frames.append(epoch[0])
    # print(f"epochs {epochs}")
    # print(f"epoch_frames {epoch_frames}")
    # ------------ SUM OF ACTIVITY FOR EACH FRAME AROUND EVENTs -----------------

    # key is an int representing the distance in frame from the "stimulus",
    # the stimulus key being the zero. The max elements in the dict is
    # ((range_value * 2) + 1)
    sum_activity_by_frame_dict = SortedDict()

    for epoch_index, epoch_frame in enumerate(epoch_frames):
        beg_frame = np.max((0, epoch_frame - range_value))
        end_frame = np.min((n_frames, epoch_frame + range_value + 1))

        # before the event
        sum_activity_before = np.sum(data[:, beg_frame:epoch_frame], axis=0)
        frames_before = np.arange(-(epoch_frame - beg_frame), 0)

        for i, frame in enumerate(frames_before):
            if frame not in sum_activity_by_frame_dict:
                sum_activity_by_frame_dict[frame] = []
            if len(sum_activity_before) > i:
                sum_activity_by_frame_dict[frame].append(sum_activity_before[i])

        # after the event
        sum_activity_after = np.sum(data[:, epoch_frame:end_frame], axis=0)
        frames_after = np.arange(0, end_frame - epoch_frame)
        for i, frame in enumerate(frames_after):
            if frame not in sum_activity_by_frame_dict:
                sum_activity_by_frame_dict[frame] = []
            if len(sum_activity_after) > i:
                sum_activity_by_frame_dict[frame].append(sum_activity_after[i])

    frames_indices = np.arange(-1 * range_value, range_value + 1)
    psth_values = list()
    for fct_index in range(len(fcts_to_apply)):
        psth_values.append([])

    for frame in frames_indices:
        for fct_index, fct_to_apply in enumerate(fcts_to_apply):
            if frame not in sum_activity_by_frame_dict:
                psth_values[fct_index].append(0)
            else:
                sum_activity = sum_activity_by_frame_dict[frame]
                sum_activity = (fct_to_apply(sum_activity) / n_cells)
                psth_values[fct_index].append(sum_activity)
    return frames_indices, psth_values


def plot_several_psth(results_path, data_psth, colors_plot,
                      file_name, label_legends=None, x_label=None, y_label=None,
                      color_ticks="white",
                      axes_label_color="white",
                      axes_border_color="white",
                      color_v_line="white", line_width=2,
                      line_mode=True, background_color="black",
                      threshold_line_y_values=None,
                      with_same_y_scale=True,
                      figsize=(30, 20),
                      ticks_labels_size=5,
                      axis_label_size=30,
                      legend_police_size=10,
                      axis_label_pad=20,
                      ticks_length=6,
                      ticks_width=2,
                      top_border_visible=False,
                      right_border_visible=False,
                      bottom_border_visible=False,
                      left_border_visible=False,
                      save_formats="pdf",
                      summary_plot=True):
    """

    Args:
        results_path: (string) path of dir where to save the results
        data_psth: list of length the number of plot. Each list contains 2 list or 1d array, the first one being
        time_x_values and second one y_values. time_x_values 1d array containing the time from -n to +n corresponding to y_values
        y_values list of 1d array, from 1 to 3 1d array of the same length as time_x_values.
        First one represents the mean or median values, if 2 elements then the second represents the std, if
        3 elements then the 2nd and 3rd elements represents the 25th and 75th percentile
        colors_plot: list of colors, same length as data_psth
        label_legends: None or list of string same length as data_psth
        threshold_line_y_values: list same lengh of data_psth, containing float representing threshold horizontal
        lines to display
        file_name:
        x_label:
        y_label:
        color_ticks:
        with_same_y_scale: (bool) if True, then the plots should have the limits in the y-axis
        ticks_labels_size: (int) size of the ticks label
        axes_label_color:
        color_v_line:
        line_width:
        line_mode:
        background_color:
        figsize:
        save_formats:
        summary_plot:

    Returns:

    """

    n_psth = len(data_psth)

    # print(f"n_psth {n_psth} {results_path} {file_name}")

    if line_mode and summary_plot:
        n_plots = n_psth + 1
    else:
        n_plots = n_psth

    if n_plots > 6:
        max_n_lines = 5
    else:
        max_n_lines = 2
    n_lines = n_plots if n_plots <= max_n_lines else max_n_lines
    n_col = math.ceil(n_plots / n_lines)

    fig, axes = plt.subplots(nrows=n_lines, ncols=n_col,
                             gridspec_kw={'width_ratios': [1] * n_col, 'height_ratios': [1] * n_lines},
                             figsize=figsize)
    fig.set_tight_layout({'rect': [0, 0, 1, 0.95], 'pad': 1.5, 'h_pad': 1.5})
    fig.patch.set_facecolor(background_color)

    axes = axes.flatten()

    y_lim_values = None
    if with_same_y_scale:
        y_lim_values = [0, 0]
        for ax_index in range(len(axes)):
            if ax_index >= n_psth:
                continue
            # y_values is a list of 1d array
            time_x_values, psth_values = data_psth[ax_index]
            psth_values_to_use = psth_values[0]
            # then we take the 75th percentile
            if len(psth_values) == 3:
                psth_values_to_use = psth_values[2]
            max_value = np.max(psth_values_to_use)
            if (max_value + 1) > y_lim_values[1]:
                y_lim_values[1] = max_value + 1

    for ax_index, ax in enumerate(axes):
        ax.set_facecolor(background_color)
        if ax_index >= n_psth:
            continue
        time_x_values, psth_values = data_psth[ax_index]
        color_plot = colors_plot[ax_index]
        if label_legends is None:
            label_legend = None
        else:
            label_legend = label_legends[ax_index]

        if threshold_line_y_values is not None:
            threshold_line_y_value = threshold_line_y_values[ax_index]
        else:
            threshold_line_y_value = None
        # ms = ms_to_analyse[ax_index]
        plot_one_psth(results_path=results_path, time_x_values=time_x_values,
                      psth_values=psth_values, color_plot=color_plot, x_label=x_label,
                      y_label=y_label,
                      color_ticks=color_ticks,
                      y_lim_values=y_lim_values,
                      axes_label_color=axes_label_color,
                      color_v_line=color_v_line, label_legend=label_legend, line_width=line_width,
                      line_mode=line_mode, background_color=background_color, ax_to_use=ax,
                      figsize=(15, 10),
                      ticks_labels_size=ticks_labels_size,
                      axis_label_size=axis_label_size,
                      axis_label_pad=axis_label_pad,
                      legend_police_size=legend_police_size,
                      ticks_length=ticks_length,
                      ticks_width=ticks_width,
                      top_border_visible=top_border_visible,
                      right_border_visible=right_border_visible,
                      bottom_border_visible=bottom_border_visible,
                      left_border_visible=left_border_visible,
                      axes_border_color=axes_border_color,
                      file_name=None,
                      save_formats="pdf",
                      put_mean_line_on_plt=summary_plot,
                      threshold_line_y_value=threshold_line_y_value)
    if isinstance(save_formats, str):
        save_formats = [save_formats]
    for save_format in save_formats:
        fig.savefig(f'{results_path}/{file_name}.{save_format}',
                    format=f"{save_format}",
                    facecolor=fig.get_facecolor())
    plt.close()


def plot_one_psth(results_path, time_x_values, psth_values, color_plot, x_label=None, y_label=None,
                  color_ticks="white",
                  axes_label_color="white",
                  axes_border_color="white",
                  color_v_line="white", label_legend=None, line_width=2,
                  line_mode=True, background_color="black", ax_to_use=None,
                  figsize=(15, 10),
                  ticks_labels_size=5,
                  axis_label_size=30,
                  axis_label_pad=20,
                  legend_police_size=10,
                  ticks_length=6,
                  ticks_width=2,
                  top_border_visible=False,
                  right_border_visible=False,
                  bottom_border_visible=False,
                  left_border_visible=False,
                  y_lim_values=None,
                  file_name=None,
                  save_formats="pdf",
                  put_mean_line_on_plt=False,
                  threshold_line_y_value=None):
    """

    Args:
        results_path: (string) path of dir where to save the results
        time_x_values: 1d array containing the time from -n to +n corresponding to y_values
        psth_values: list of 1d array, from 1 to 3 1d array of the same length as time_x_values.
        First one represents the mean or median values, if 2 elements then the second represents the std, if
        3 elements then the 2nd and 3rd elements represents the 25th and 75th percentile
        color_plot: color of the plot
        x_label:
        y_label:
        color_ticks:
        axes_label_color:
        y_lim_values: (tuple of float), None or 2 values used to set the y_lim
        color_v_line: color of the line representing the "stim"
        label_legend: None if no label, otherwise the label legend
        line_width:
        line_mode: (bool) if False, bar mode is activated
        background_color:
        ax_to_use: None if we plot a unique figure, file_name should not be None then, otherwise the ax
        in which to plot.
        figsize: tuple of int (width, height)
        ticks_labels_size: (int) size of the ticks label
        axis_label_size: (int) size of the axes label size
        axis_label_pad: (int) padding betwwen the axes and their label
        file_name:
        save_formats: string or list of string, like "pdf", "png"
        put_mean_line_on_plt: if True, means we use a trick to plot on the last "grid" so we collect
        all the plots in one place.
        threshold_line_y_value: float, if not None, an horizontal line is displayed representing for example a
        threshold value

    Returns:

    """
    max_value = 0
    if ax_to_use is None:
        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=figsize)
        fig.patch.set_facecolor(background_color)

        ax1.set_facecolor(background_color)
    else:
        ax1 = ax_to_use

    if line_mode:
        ax1.plot(time_x_values,
                 psth_values[0], color=color_plot, lw=line_width, label=label_legend)
        if threshold_line_y_value is not None:
            ax1.hlines(threshold_line_y_value, np.min(time_x_values), np.max(time_x_values),
                       lw=1, linestyles="dashed", color="white", zorder=10)
        if put_mean_line_on_plt:
            plt.plot(time_x_values,
                     psth_values[0], color=color_plot, lw=2)
        max_value = np.max((max_value, np.max(psth_values[0])))
        if len(psth_values) == 2:
            ax1.fill_between(time_x_values, psth_values[0] - psth_values[1],
                             psth_values[0] + psth_values[1],
                             alpha=0.5, facecolor=color_plot)
            max_value = np.max((max_value, np.max(psth_values[0] + psth_values[1])))
        elif len(psth_values) == 3:
            ax1.fill_between(time_x_values, psth_values[1], psth_values[2],
                             alpha=0.5, facecolor=color_plot)
            max_value = np.max((max_value, np.max(psth_values[2])))
    else:
        hist_color = color_plot
        edge_color = color_plot
        ax1.bar(time_x_values,
                psth_values[0], color=hist_color, edgecolor=edge_color,
                label=label_legend)
        if threshold_line_y_value is not None:
            ax1.hlines(threshold_line_y_value, np.min(time_x_values), np.max(time_x_values),
                       lw=1, linestyles="dashed", color="white", zorder=10)
        max_value = np.max((max_value, np.max(psth_values[0])))

    ax1.vlines(0, 0,
               max_value, color=color_v_line, linewidth=2,
               linestyles="dashed")
    if put_mean_line_on_plt:
        plt.vlines(0, 0,
                   max_value, color=color_v_line, linewidth=2,
                   linestyles="dashed")

    ax1.tick_params(axis='y', colors=color_ticks, labelsize=ticks_labels_size, length=ticks_length, width=ticks_width)
    ax1.tick_params(axis='x', colors=color_ticks, labelsize=ticks_labels_size, length=ticks_length, width=ticks_width)

    if label_legend is not None:
        ax1.legend(prop={'size': legend_police_size})

    if y_label is not None:
        ax1.set_ylabel(y_label, fontsize=axis_label_size, labelpad=axis_label_pad)
    if x_label is not None:
        ax1.set_xlabel(x_label, fontsize=axis_label_size, labelpad=axis_label_pad)
    if y_lim_values is not None:
        ax1.set_ylim(y_lim_values[0], y_lim_values[1])
    else:
        ax1.set_ylim(0, max_value + 1)

    ax1.xaxis.label.set_color(axes_label_color)
    ax1.yaxis.label.set_color(axes_label_color)

    ax1.xaxis.set_tick_params(rotation=45)

    ax1.spines['top'].set_visible(top_border_visible)
    ax1.spines['right'].set_visible(right_border_visible)
    ax1.spines['bottom'].set_visible(bottom_border_visible)
    ax1.spines['left'].set_visible(left_border_visible)

    ax1.spines['bottom'].set_color(axes_border_color)
    ax1.spines['top'].set_color(axes_border_color)
    ax1.spines['right'].set_color(axes_border_color)
    ax1.spines['left'].set_color(axes_border_color)

    # xticks = np.arange(0, len(data_dict))
    # ax1.set_xticks(time_x_values)
    # # sce clusters labels
    # ax1.set_xticklabels(labels)

    if ax_to_use is None and (file_name is not None):
        if isinstance(save_formats, str):
            save_formats = [save_formats]
        for save_format in save_formats:
            fig.savefig(f'{results_path}/{file_name}.{save_format}',
                        format=f"{save_format}",
                        facecolor=fig.get_facecolor())
    if ax_to_use is None:
        plt.close()
