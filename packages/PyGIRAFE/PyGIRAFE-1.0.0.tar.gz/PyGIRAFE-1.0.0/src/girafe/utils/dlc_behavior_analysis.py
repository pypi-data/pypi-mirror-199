import os
import h5py
import numpy as np
import pandas as pd
import yaml
from sklearn.decomposition import PCA
import scipy.signal
import scipy.signal as signal
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.manifold import TSNE
import seaborn as sns
from pynwb import NWBHDF5IO
from bisect import bisect_right
import hdf5storage
import math
from girafe.utils.misc import find_nearest
from datetime import datetime
import pandas as pd

# qualitative 12 colors : http://colorbrewer2.org/?type=qualitative&scheme=Paired&n=12
# + 11 diverting
BREWER_COLORS = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f',
                 '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928', '#a50026', '#d73027',
                 '#f46d43', '#fdae61', '#fee090', '#ffffbf', '#e0f3f8', '#abd9e9',
                 '#74add1', '#4575b4', '#313695']


def plot_hist_distribution(distribution_data, description, param=None, values_to_scatter=None,
                           xticks_labelsize=10, yticks_labelsize=10, x_label_font_size=15, y_label_font_size=15,
                           labels=None, scatter_shapes=None, colors=None, tight_x_range=False,
                           twice_more_bins=False, background_color="black", labels_color="white",
                           xlabel="", ylabel=None, path_results=None, save_formats="pdf",
                           v_line=None, x_range=None,
                           ax_to_use=None, color_to_use=None):
    """
    Plot a distribution in the form of an histogram, with option for adding some scatter values
    :param distribution_data:
    :param description:
    :param param:
    :param values_to_scatter:
    :param labels:
    :param scatter_shapes:
    :param colors:
    :param tight_x_range:
    :param twice_more_bins:
    :param xlabel:
    :param ylabel:
    :param save_formats:
    :return:
    """
    distribution = np.array(distribution_data)
    if color_to_use is None:
        hist_color = "blue"
    else:
        hist_color = color_to_use
    edge_color = "white"
    if x_range is not None:
        min_range = x_range[0]
        max_range = x_range[1]
    elif tight_x_range:
        max_range = np.max(distribution)
        min_range = np.min(distribution)
    else:
        max_range = 100
        min_range = 0
    weights = (np.ones_like(distribution) / (len(distribution))) * 100
    if ax_to_use is None:
        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(12, 12))
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)
    else:
        ax1 = ax_to_use
    bins = int(np.sqrt(len(distribution)))
    if twice_more_bins:
        bins *= 2
    hist_plt, edges_plt, patches_plt = ax1.hist(distribution, bins=bins, range=(min_range, max_range),
                                                facecolor=hist_color,
                                                edgecolor=edge_color,
                                                weights=weights, log=False, label=description)
    if values_to_scatter is not None:
        scatter_bins = np.ones(len(values_to_scatter), dtype="int16")
        scatter_bins *= -1

        for i, edge in enumerate(edges_plt):
            # print(f"i {i}, edge {edge}")
            if i >= len(hist_plt):
                # means that scatter left are on the edge of the last bin
                scatter_bins[scatter_bins == -1] = i - 1
                break

            if len(values_to_scatter[values_to_scatter <= edge]) > 0:
                if (i + 1) < len(edges_plt):
                    bool_list = values_to_scatter < edge  # edges_plt[i + 1]
                    for i_bool, bool_value in enumerate(bool_list):
                        if bool_value:
                            if scatter_bins[i_bool] == -1:
                                new_i = max(0, i - 1)
                                scatter_bins[i_bool] = new_i
                else:
                    bool_list = values_to_scatter < edge
                    for i_bool, bool_value in enumerate(bool_list):
                        if bool_value:
                            if scatter_bins[i_bool] == -1:
                                scatter_bins[i_bool] = i

        decay = np.linspace(1.1, 1.15, len(values_to_scatter))
        for i, value_to_scatter in enumerate(values_to_scatter):
            if i < len(labels):
                ax1.scatter(x=value_to_scatter, y=hist_plt[scatter_bins[i]] * decay[i], marker=scatter_shapes[i],
                            color=colors[i], s=60, zorder=20, label=labels[i])
            else:
                ax1.scatter(x=value_to_scatter, y=hist_plt[scatter_bins[i]] * decay[i], marker=scatter_shapes[i],
                            color=colors[i], s=60, zorder=20)
    y_min, y_max = ax1.get_ylim()
    if v_line is not None:
        ax1.vlines(v_line, y_min, y_max,
                   color="white", linewidth=2,
                   linestyles="dashed", zorder=5)

    ax1.legend()

    if tight_x_range:
        ax1.set_xlim(min_range, max_range)
    else:
        ax1.set_xlim(0, 100)
        xticks = np.arange(0, 110, 10)

        ax1.set_xticks(xticks)
        # sce clusters labels
        ax1.set_xticklabels(xticks)
    ax1.yaxis.set_tick_params(labelsize=xticks_labelsize)
    ax1.xaxis.set_tick_params(labelsize=yticks_labelsize)
    ax1.tick_params(axis='y', colors=labels_color)
    ax1.tick_params(axis='x', colors=labels_color)
    # TO remove the ticks but not the labels
    # ax1.xaxis.set_ticks_position('none')

    if ylabel is None:
        ax1.set_ylabel("Distribution (%)", fontsize=30, labelpad=20)
    else:
        ax1.set_ylabel(ylabel, fontsize=y_label_font_size, labelpad=20)
    ax1.set_xlabel(xlabel, fontsize=x_label_font_size, labelpad=20)

    ax1.xaxis.label.set_color(labels_color)
    ax1.yaxis.label.set_color(labels_color)

    # padding between ticks label and  label axis
    # ax1.tick_params(axis='both', which='major', pad=15)

    if ax_to_use is None:
        fig.tight_layout()
        if isinstance(save_formats, str):
            save_formats = [save_formats]
        if path_results is None:
            path_results = param.path_results
        time_str = ""
        if param is not None:
            time_str = param.time_str
        for save_format in save_formats:
            fig.savefig(f'{path_results}/{description}'
                        f'_{time_str}.{save_format}',
                        format=f"{save_format}",
                        facecolor=fig.get_facecolor())

        plt.close()


class DlcAnalysis:

    def __init__(self, data_path, results_path, identifier, pos_left_file_name, skeketon_left_file_name,
                 pos_right_file_name, skeleton_right_file_name, cicada_file, nwb_file):
        self.data_path = data_path
        self.results_path = results_path
        self.pos_left_file_name = pos_left_file_name
        self.skeketon_left_file_name = skeketon_left_file_name
        self.pos_right_file_name = pos_right_file_name
        self.skeleton_right_file_name = skeleton_right_file_name
        self.cicada_file = cicada_file
        self.nwb_file = nwb_file
        self.n_frames = 0
        self.identifier = identifier
        self.likelihood_threshold = 0.1

        self.time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")

        self.bodyparts_triplets = {'forelimb_left': ['forepaw_left', 'foreleg_joint_left', 'foreleg_body_jonction_left'],
                              'forelimb_right': ['forepaw_right', 'foreleg_joint_right', 'foreleg_body_jonction_right'],
                              "hindlimb_left": ['hindlepaw_left', 'hindleleg_joint_left',
                                                'hindleleg_body_jonction_left'],
                              "hindlimb_right": ['hindlepaw_right', 'hindleleg_joint_right',
                                                 'hindleleg_body_jonction_right'],
                              "tail": ['tail_prox', 'tail_mid', 'tail_dist']}

        self.skeletons_duos = {'forelimb_left': ['forepaw_foreleg_joint_left',
                                            'foreleg_joint_foreleg_body_jonction_left'],
                          'forelimb_right': ['forepaw_foreleg_joint_right',
                                             'foreleg_joint_foreleg_body_jonction_right'],
                          "hindlimb_left": ['hindlepaw_hindleleg_joint_left',
                                            'hindleleg_joint_hindleleg_body_jonction_left'],
                          "hindlimb_right": ['hindlepaw_hindleleg_joint_right',
                                             'hindleleg_joint_hindleleg_body_jonction_right'],
                          "tail": ['tail_prox_tail_mid', 'tail_mid_tail_dist']}

        # take as key the index of the body_part and return its name
        self.body_parts_name_dict = dict()
        # take the name of a bodypart and return it's index, in body_parts_pos_to_concatenate
        self.bodyparts_indices = dict()
        # matches indices in self.bodyparts_indices
        # shape is (n_body_parts, 2 (x, y), n_frames)
        # values could be equal to np.nan
        self.limbs_body_parts_pos_array = None

        # skeleton array shape: # n_bodyparts, (length, orientation, likelihood), n_frames

        self.n_frames_left, self.bodyparts_left, self.body_parts_pos_array_left, \
        self.skeleton_parts_left, self.skeleton_parts_pos_array_left, self.left_cam_id = \
            get_data_from_dlc_h5_files(data_path, pos_file_name=self.pos_left_file_name,
                                       skeketon_file_name=self.skeketon_left_file_name,
                                       replace_by_nan=False,
                                       likelihood_threshold=self.likelihood_threshold)

        #
        self.n_frames_right, self.bodyparts_right, self.body_parts_pos_array_right, self.skeleton_parts_right, \
        self.skeleton_parts_pos_array_right, self.right_cam_id = \
            get_data_from_dlc_h5_files(data_path, pos_file_name=self.pos_right_file_name,
                                       skeketon_file_name=self.skeleton_right_file_name,
                                       replace_by_nan=False,
                                       likelihood_threshold=self.likelihood_threshold)
        print(f"self.n_frames_right {self.n_frames_right}")
        print(f"self.bodyparts_right {self.bodyparts_right}, ")

        self.behavior_by_frame_left, self.behavior_left_time_stamps, self.gt_behavior_left = encode_frames_from_cicada(
            cicada_file=self.cicada_file,
            nwb_file=self.nwb_file,
            cam_id=self.left_cam_id, n_frames=self.n_frames_left,
            side_to_exclude="right",
            no_behavior_str="still")

        self.behavior_by_frame_right, self.behavior_right_time_stamps, self.gt_behavior_right = \
            encode_frames_from_cicada(
                cicada_file=self.cicada_file,
                nwb_file=self.nwb_file,
                cam_id=self.right_cam_id, n_frames=self.n_frames_right,
                side_to_exclude="left",
                no_behavior_str="still")

        self.gt_behavior = np.load(self.cicada_file)

        # array (n_body_parts, n_frames), binary, if 1 there is mvt, if 0 no mvt
        self.binary_mvt_matrix = None

        self.speed_matrix = None
        self.distance_matrix = None
        # number of pixels of distance between a bodypart over 2 frames
        self.distance_threshold = 4
        # key is a tuple of 2 string representing 2 body parts, and value is an int representing the index of the
        # joint bodyparts in orientation_matrix and length_matrix,
        self.joint_name_to_indices_dict = dict()
        self.indices_to_joint_name_dict = dict()
        self.orientation_matrix = None
        self.length_matrix = None
        self.orientation_diff_matrix = None
        self.length_diff_matrix = None

        self.fusion_both_side_timestamps()
        self.evaluate_speed()
        self.fusion_skeleton_data()
        # using skeleton and pos values, we decide which part of the body is moving and during which frames
        self.build_binary_mvt_matrix()
        self.save_values_in_excel()
        self.classify_behavior()

    def fusion_both_side_timestamps(self):
        # first frame will be the furthest timestamps
        if self.behavior_left_time_stamps[0] > self.behavior_right_time_stamps[0]:
            first_time_stamp = self.behavior_left_time_stamps[0]
        else:
            first_time_stamp = self.behavior_right_time_stamps[0]

        if self.behavior_left_time_stamps[-1] < self.behavior_right_time_stamps[-1]:
            last_time_stamp = self.behavior_left_time_stamps[-1]
        else:
            last_time_stamp = self.behavior_right_time_stamps[-1]

        # now we cut time_stamps and frames, so both side are synchronized
        # first left side
        if self.behavior_left_time_stamps[0] != first_time_stamp:
            frame_index = find_nearest(self.behavior_left_time_stamps, first_time_stamp)
            self.behavior_left_time_stamps = self.behavior_left_time_stamps[frame_index:]
            self.body_parts_pos_array_left = self.body_parts_pos_array_left[:, :, frame_index:]
            self.skeleton_parts_pos_array_left = self.skeleton_parts_pos_array_left[:, :, frame_index:]

        if self.behavior_left_time_stamps[-1] != last_time_stamp:
            frame_index = find_nearest(self.behavior_left_time_stamps, last_time_stamp)
            self.behavior_left_time_stamps = self.behavior_left_time_stamps[:frame_index + 1]
            self.body_parts_pos_array_left = self.body_parts_pos_array_left[:, :, :frame_index + 1]
            self.skeleton_parts_pos_array_left = self.skeleton_parts_pos_array_left[:, :, :frame_index + 1]

        if self.behavior_right_time_stamps[0] != first_time_stamp:
            frame_index = find_nearest(self.behavior_right_time_stamps, first_time_stamp)
            self.behavior_right_time_stamps = self.behavior_right_time_stamps[frame_index:]
            self.body_parts_pos_array_right = self.body_parts_pos_array_right[:, :, frame_index:]
            self.skeleton_parts_pos_array_right = self.skeleton_parts_pos_array_right[:, :, frame_index:]

        if self.behavior_right_time_stamps[-1] != last_time_stamp:
            frame_index = find_nearest(self.behavior_right_time_stamps, last_time_stamp)
            self.behavior_right_time_stamps = self.behavior_right_time_stamps[:frame_index + 1]
            self.body_parts_pos_array_right = self.body_parts_pos_array_right[:, :, :frame_index + 1]
            self.skeleton_parts_pos_array_right = self.skeleton_parts_pos_array_right[:, :, :frame_index + 1]

        self.n_frames = len(self.behavior_left_time_stamps)
        # print(f"len(behavior_left_time_stamps) {len(self.behavior_left_time_stamps)}, "
        #       f"len(behavior_right_time_stamps) {len(self.behavior_right_time_stamps)}")

        print(f"self.body_parts_pos_array_right.shape {self.body_parts_pos_array_right.shape}, "
              f"self.body_parts_pos_array_left.shape {self.body_parts_pos_array_left.shape}")

        # we want to fusion get the same time referenciel for both side and we want to get the speed
        # of each part over the time, first measuring the euclidian distance
        # for the tail, we want to keep only one version, using Nan on each side to get an idea of the distance between
        # 2 points

    def fusion_skeleton_data(self):
        """
        Take skeleton data from both movie and put data in length_matrix and distance_matrix, filling in the same
        time joint_name_to_indices_dict
        Returns:

        """
        index_so_far = 0

        n_parts = (len(self.skeleton_parts_pos_array_right) - 2) * 2 + 2

        self.length_matrix = np.empty((n_parts, self.n_frames))
        self.length_matrix[:] = np.nan
        self.orientation_matrix = np.empty((n_parts, self.n_frames))
        self.orientation_matrix[:] = np.nan

        self.length_diff_matrix = np.zeros((n_parts, self.n_frames))
        self.orientation_diff_matrix = np.zeros((n_parts, self.n_frames))

        for side in ["left", "right"]:
            if side == "right":
                parts_name, skeleton_array = self.skeleton_parts_right, self.skeleton_parts_pos_array_right
            else:
                parts_name, skeleton_array = self.skeleton_parts_left, self.skeleton_parts_pos_array_left

            for part_index, part_name in enumerate(parts_name):
                if "tail" in part_name:
                    continue
                # part name consist of both bodyparts joined by a "_"
                # we hide the side at the end such as "_left" or "_right"
                new_part_name = part_name + f"_{side}"
                positive_lk_frames = np.where(skeleton_array[part_index, 2, :] >= self.likelihood_threshold)[0]
                negative_lk_frames = np.where(skeleton_array[part_index, 2, :] < self.likelihood_threshold)[0]
                # skeleton_array array shape: # n_bodyparts, (length, orientation, likelihood), n_frames
                # first taking the diff, whatever the likelihood
                self.length_diff_matrix[index_so_far, 1:] = np.abs(np.diff(skeleton_array[part_index, 0, :]))
                self.orientation_diff_matrix[index_so_far, 1:] = np.abs(np.diff(skeleton_array[part_index, 1, :]))
                # then putting 0 value where the likelihood is under the threshold and the value after
                for index_lk in negative_lk_frames:
                    self.length_diff_matrix[index_so_far, index_lk] = 0
                    self.orientation_diff_matrix[index_so_far, index_lk] = 0
                    if index_lk < (self.n_frames - 1):
                        self.length_diff_matrix[index_so_far, index_lk + 1] = 0
                        self.orientation_diff_matrix[index_so_far, index_lk + 1] = 0

                self.length_matrix[index_so_far, positive_lk_frames] = skeleton_array[part_index, 0,
                                                                                      positive_lk_frames]
                self.orientation_matrix[index_so_far, positive_lk_frames] = skeleton_array[part_index, 1,
                                                                                           positive_lk_frames]
                self.joint_name_to_indices_dict[new_part_name] = index_so_far
                self.indices_to_joint_name_dict[index_so_far] = new_part_name
                index_so_far += 1

        skeleton_array_dict = dict()
        skeleton_array_dict["left"] = self.skeleton_parts_pos_array_left
        skeleton_array_dict["right"] = self.skeleton_parts_pos_array_right
        parts_name_indices_dict = {"right": dict(), "left": dict()}
        for index, part_name in enumerate(self.skeleton_parts_right):
            parts_name_indices_dict["right"][part_name] = index
        for index, part_name in enumerate(self.skeleton_parts_left):
            parts_name_indices_dict["left"][part_name] = index

        sides = ["left", "right"]
        # now we want to join skeleton of the tail from both side
        for tail_part in ["tail_prox_tail_mid", "tail_mid_tail_dist"]:
            frame = 0
            while frame < self.n_frames:
                if frame == 0:
                    frame += 1
                    continue
                for side_index, side in enumerate(sides):
                    part_index = parts_name_indices_dict[side][tail_part]
                    skeleton_array = skeleton_array_dict[side]
                    # both need to be over likelihood
                    if (skeleton_array[part_index, 2, frame - 1] < self.likelihood_threshold) or \
                            (skeleton_array[part_index, 2, frame] < self.likelihood_threshold):
                        continue
                    self.length_diff_matrix[index_so_far, frame] = abs(skeleton_array[part_index, 0, frame] -
                                                                   skeleton_array[part_index, 0, frame - 1])
                    self.orientation_diff_matrix[index_so_far, frame] = abs(skeleton_array[part_index, 1, frame] -
                                                                        skeleton_array[part_index, 1, frame - 1])
                    # reversing it so we continue on the same side
                    if side_index == 1:
                        sides = sides[::-1]
                    break
                frame += 1
            self.joint_name_to_indices_dict[tail_part] = index_so_far
            self.indices_to_joint_name_dict[index_so_far] = tail_part
            index_so_far += 1

    def evaluate_speed(self):
        # first we want to measure the euclidean distance for each part from x_y values
        # first for the limbs
        index_body_part = 0
        body_parts_pos_to_concatenate = []
        for left_index, left_body_part in enumerate(self.bodyparts_left):
            if "tail" in left_body_part:
                continue
            body_parts_pos_to_concatenate.append(self.body_parts_pos_array_left[left_index])
            self.body_parts_name_dict[index_body_part] = left_body_part + "_left"
            self.bodyparts_indices[left_body_part + "_left"] = index_body_part
            index_body_part += 1

        for right_index, right_body_part in enumerate(self.bodyparts_right):
            if "tail" in right_body_part:
                continue
            body_parts_pos_to_concatenate.append(self.body_parts_pos_array_right[right_index])
            self.body_parts_name_dict[index_body_part] = right_body_part + "_right"
            self.bodyparts_indices[right_body_part + "_right"] = index_body_part
            index_body_part += 1

        body_parts_pos_array = np.zeros((len(body_parts_pos_to_concatenate),
                                         body_parts_pos_to_concatenate[0].shape[0],
                                         body_parts_pos_to_concatenate[0].shape[1]))
        for index, pos_array in enumerate(body_parts_pos_to_concatenate):
            body_parts_pos_array[index] = pos_array

        self.limbs_body_parts_pos_array = body_parts_pos_array
        # that's for the limbs, take in consideration the NaN values

        no_nan_replacement = True
        distance_matrix = euclidean_distance_for_bodyparts(body_parts_pos_array,
                                                           no_nan_replacement=no_nan_replacement)
        # now we apply a diff at the distance matrix to get speed estimation

        # version with no NAN
        if not no_nan_replacement:
            speed_matrix = np.abs(np.diff(distance_matrix, axis=1))
            # + 3 for the tail
            tmp_matrix = np.zeros((speed_matrix.shape[0] + 3, speed_matrix.shape[1] + 1))
            tmp_matrix[:speed_matrix.shape[0], 1:] = speed_matrix
            speed_matrix = tmp_matrix
        else:
            # version with Nan
            speed_matrix = np.zeros((distance_matrix.shape[0] + 3, distance_matrix.shape[1]))
            for body_part_index in np.arange(distance_matrix.shape[0]):
                for frame in np.arange(self.n_frames):
                    if frame == 0:
                        continue
                    # speed is positive only if both distances are not NaN
                    if (distance_matrix[body_part_index, frame - 1] == np.nan) or \
                            (distance_matrix[body_part_index, frame] == np.nan):
                        continue

                    speed_matrix[body_part_index, frame] = abs(distance_matrix[body_part_index, frame] -
                                                               distance_matrix[body_part_index, frame - 1])

        # now we want to add the tail, to do so we will fusion both side information
        # we add directly to speed
        tail_speed = self.get_tail_speed()

        self.body_parts_name_dict[index_body_part] = "tail_prox"
        self.bodyparts_indices["tail_prox"] = index_body_part
        self.body_parts_name_dict[index_body_part + 1] = "tail_mid"
        self.bodyparts_indices["tail_mid"] = index_body_part + 1
        self.body_parts_name_dict[index_body_part + 2] = "tail_dist"
        self.bodyparts_indices["tail_dist"] = index_body_part + 2
        speed_matrix[index_body_part:index_body_part + 3] = tail_speed

        # now we keep only the frame in which a certain movement is found
        speed_threshold = 10

        self.speed_matrix = speed_matrix

        no_nan_replacement = False
        distance_matrix = euclidean_distance_for_bodyparts(body_parts_pos_array,
                                                           no_nan_replacement=no_nan_replacement)
        self.distance_matrix = np.zeros((distance_matrix.shape[0] + 3, distance_matrix.shape[1]))
        self.distance_matrix[:distance_matrix.shape[0]] = distance_matrix

        tail_distances = self.get_tail_distances()
        self.distance_matrix[distance_matrix.shape[0]:] = tail_distances

        # before thresholding speed, we plot the histograms
        self.plot_speed()

    def plot_speed(self):
        for bodypart_family, bodyparts in self.bodyparts_triplets.items():
            fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                    figsize=(16, 8))

            for bodypart in bodyparts:
                bodypart_index = self.bodyparts_indices[bodypart]
                speed_values = self.speed_matrix[bodypart_index]
                plot_hist_distribution(distribution_data=speed_values,
                                       description=f"hist_{bodypart}",
                                       path_results=self.results_path,
                                       tight_x_range=True,
                                       twice_more_bins=True,
                                       xlabel=f"Speed",
                                       save_formats="png")
                ax1.plot(speed_values, c=BREWER_COLORS[bodypart_index % len(BREWER_COLORS)], linewidth=1.5,
                         label=bodypart)

            plt.legend()
            # chartBox = ax1.get_position()
            # ax1.set_position([chartBox.x0, chartBox.y0, chartBox.width * 0.6, chartBox.height])
            # ax1.legend(loc='upper center', bbox_to_anchor=(1.45, 0.8), shadow=True, ncol=1)
            plt.xlabel("frames", fontweight="bold", fontsize=12, labelpad=10)
            # ax1.set_xlim(-500, 500)
            ax1.set_yscale("log")
            plt.ylabel("Speed", fontweight="bold", fontsize=12, labelpad=10)

            fig.savefig(f'{self.results_path}/speed_plots_{bodypart_family}_{self.time_str}.pdf',
                        format="pdf")
            plt.close()

    def build_binary_mvt_matrix(self):

        # we remove speed above a certain threshold
        # above we consider it as artefact
        max_speed_threshold = 80
        print("")
        print(f"### max speed threshold {max_speed_threshold}")
        print("")
        self.speed_matrix[self.speed_matrix >= max_speed_threshold] = 0

        # using diff_distance_matrix allows to use the speed of the movement as threshold
        # self.binary_mvt_matrix = np.zeros((self.speed_matrix.shape[0], self.speed_matrix.shape[1]))
        # self.binary_mvt_matrix[np.where(self.speed_matrix > speed_threshold)] = 1

        max_distance_threshold = 50
        print("")
        print(f"### max distance threshold {max_distance_threshold}")
        print("")
        self.distance_matrix[self.distance_matrix >= max_distance_threshold] = 0

        self.binary_mvt_matrix = np.zeros((self.distance_matrix.shape[0], self.distance_matrix.shape[1]))
        self.binary_mvt_matrix[np.where(self.distance_matrix > self.distance_threshold)] = 1

    def save_values_in_excel(self):

        # also recording it in an excel file
        writer = pd.ExcelWriter(f'{self.results_path}/speed_values_{self.time_str}.xlsx')
        results_df = pd.DataFrame()
        results_df.insert(loc=0, column="time_stamps",
                          value=np.round(self.behavior_left_time_stamps, 2),
                          allow_duplicates=False)

        i = 1
        for bodypart_family, bodyparts in self.bodyparts_triplets.items():
            for bodypart_duo in self.skeletons_duos[bodypart_family]:
                skeleton_index = self.joint_name_to_indices_dict[bodypart_duo]
                orientation_values = np.round(self.orientation_diff_matrix[skeleton_index], 2)
                results_df.insert(loc=i, column=bodypart_duo + "_orientation",
                                  value=orientation_values,
                                  allow_duplicates=False)
                i += 1
                length_values = np.round(self.length_diff_matrix[skeleton_index], 2)
                results_df.insert(loc=i, column=bodypart_duo + "_length",
                                  value=length_values,
                                  allow_duplicates=False)
                i += 1
            for bodypart in bodyparts:
                bodypart_index = self.bodyparts_indices[bodypart]
                speed_values = np.round(self.speed_matrix[bodypart_index], 2)
                results_df.insert(loc=i, column=bodypart + "_speed",
                                  value=speed_values,
                                  allow_duplicates=False)
                i += 1
                distance_values = np.round(self.distance_matrix[bodypart_index], 2)
                results_df.insert(loc=i, column=bodypart + "_dist",
                                  value=distance_values,
                                  allow_duplicates=False)
                i += 1
        results_df.to_excel(writer, 'summary', index=False)
        writer.save()

    def get_tail_distances(self):
        """
                Fusion both side of tail and compute the distance if it's 3 parts
                Returns:

        """
        tail_names = ["tail_prox", "tail_mid", "tail_dist"]
        tail_indices = {"left": dict(), "right": dict()}
        sides = ["left", "right"]
        global_pos_dict = {"left": self.body_parts_pos_array_left, "right": self.body_parts_pos_array_right}
        tail_pos_dict = {"left": dict(), "right": dict()}
        bodyparts_dict = {"left": self.bodyparts_left, "right": self.bodyparts_right}

        body_parts_pos_to_concatenate = []
        tail_part_index = 0

        for side in sides:
            for body_part_index, body_part in enumerate(bodyparts_dict[side]):
                if body_part in tail_names:
                    tail_pos_dict[side][body_part] = global_pos_dict[side][body_part_index]
                    body_parts_pos_to_concatenate.append(global_pos_dict[side][body_part_index])
                    tail_indices[side][body_part] = tail_part_index
                    tail_part_index += 1

        body_parts_pos_array = np.zeros((len(body_parts_pos_to_concatenate),
                                         body_parts_pos_to_concatenate[0].shape[0],
                                         body_parts_pos_to_concatenate[0].shape[1]))
        for index, pos_array in enumerate(body_parts_pos_to_concatenate):
            body_parts_pos_array[index] = pos_array

        # that's for the limbs, take in consideration the NaN values
        distance_matrix = euclidean_distance_for_bodyparts(body_parts_pos_array, no_nan_replacement=True)

        tail_distances = np.zeros((len(tail_names), self.n_frames))

        last_side_used = sides[0]

        for final_index, tail_name in enumerate(tail_names):
            for frame_index in np.arange(self.n_frames):
                # then we start by either of the side and look if two values in a row are not nan and we use
                # it to measure the distance
                # when changing side, we put it to zero
                for side_index, side in enumerate(sides):
                    tail_index = tail_indices[side][tail_name]
                    distance = distance_matrix[tail_index, frame_index]

                    if distance == np.nan:
                        last_side_used = side
                        continue
                    if last_side_used == side:
                        tail_distances[final_index, frame_index] = distance
                    else:
                        tail_distances[final_index, frame_index] = 0
                    last_side_used = side
                    if side_index == 1:
                        sides = sides[::-1]
                    break

        return tail_distances

    def get_tail_speed(self):
        """
        Fusion both side of tail and compute the speed if it's 3 parts
        Returns:

        """
        tail_names = ["tail_prox", "tail_mid", "tail_dist"]
        tail_indices = {"left": dict(), "right": dict()}
        sides = ["left", "right"]
        global_pos_dict = {"left": self.body_parts_pos_array_left, "right": self.body_parts_pos_array_right}
        tail_pos_dict = {"left": dict(), "right": dict()}
        bodyparts_dict = {"left": self.bodyparts_left, "right": self.bodyparts_right}

        body_parts_pos_to_concatenate = []
        tail_part_index = 0

        for side in sides:
            for body_part_index, body_part in enumerate(bodyparts_dict[side]):
                if body_part in tail_names:
                    tail_pos_dict[side][body_part] = global_pos_dict[side][body_part_index]
                    body_parts_pos_to_concatenate.append(global_pos_dict[side][body_part_index])
                    tail_indices[side][body_part] = tail_part_index
                    tail_part_index += 1

        body_parts_pos_array = np.zeros((len(body_parts_pos_to_concatenate),
                                         body_parts_pos_to_concatenate[0].shape[0],
                                         body_parts_pos_to_concatenate[0].shape[1]))
        for index, pos_array in enumerate(body_parts_pos_to_concatenate):
            body_parts_pos_array[index] = pos_array

        # that's for the limbs, take in consideration the NaN values
        distance_matrix = euclidean_distance_for_bodyparts(body_parts_pos_array, no_nan_replacement=True)

        tail_speed = np.zeros((len(tail_names), self.n_frames))

        for final_index, tail_name in enumerate(tail_names):
            for frame_index in np.arange(self.n_frames):
                if frame_index == 0:
                    tail_speed[final_index, frame_index] = 0
                    continue
                # then we start by either of the side and look if two values in a row are not nan and we use
                # it to measure the speed
                speed_measured = False
                for side_index, side in enumerate(sides):
                    tail_index = tail_indices[side][tail_name]
                    distance_before = distance_matrix[tail_index, frame_index - 1]
                    distance_now = distance_matrix[tail_index, frame_index]
                    if (distance_before == np.nan) or (distance_now == np.nan):
                        continue
                    speed_measured = True
                    tail_speed[final_index, frame_index] = abs(distance_now - distance_before)
                    if side_index == 1:
                        sides = sides[::-1]
                    break
                if speed_measured:
                    continue
                tail_speed[final_index, frame_index] = 0

        return tail_speed

    def classify_behavior(self):

        # variables to adjust
        # still_vs_mvt[np.where(np.sum(mvt_matrix, axis=0) >= 2)] = 1
        # gap_to_fill = 3
        # (n_moving_bodyparts >= len(bodyparts_triplets) - 2)

        # ### Just any kind of mvt for more than 1 frame of duration ###
        # mvt is 1
        # still_vs_mvt = np.zeros(self.n_frames, dtype="int16")

        # ### now we want to distinguish the different type of mvt and to make it stronger to outlier
        # we will keep a mvt only if 2 of 3 parts of each component of the body are in mvt

        # TODO: fusion information about tail
        bodyparts_triplets = {'forelimb_left': ['forepaw_left', 'foreleg_joint_left', 'foreleg_body_jonction_left'],
                              'forelimb_right': ['forepaw_right', 'foreleg_joint_right', 'foreleg_body_jonction_right'],
                              "hindlimb_left": ['hindlepaw_left', 'hindleleg_joint_left',
                                                'hindleleg_body_jonction_left'],
                              "hindlimb_right": ['hindlepaw_right', 'hindleleg_joint_right',
                                                 'hindleleg_body_jonction_right'],
                              "tail": ['tail_prox', 'tail_mid', 'tail_dist']}
        # key being the bodypart
        still_vs_mvt_dict = dict()
        # first key key to put in npz and value a list of periods
        periods_by_type_of_mvt = dict()
        periods_by_type_of_mvt["complex_mvt"] = np.zeros(self.n_frames, dtype="int8")
        periods_by_type_of_mvt["startle"] = np.zeros(self.n_frames, dtype="int8")

        for key_triplets, triplet in bodyparts_triplets.items():
            periods_by_type_of_mvt[f"twitch_{key_triplets}"] = np.zeros(self.n_frames, dtype="int8")
            periods_by_type_of_mvt[f"mvt_{key_triplets}"] = np.zeros(self.n_frames, dtype="int8")

            body_indices = np.array([self.bodyparts_indices[bodypart] for bodypart in triplet])

            mvt_matrix = self.binary_mvt_matrix[body_indices]
            still_vs_mvt = np.zeros(self.n_frames, dtype="int16")

            # 1 represents mvt, we want at least 2 out of the 3 body part in the triplet to be active to consider it mvt
            # n_bodyparts_triplets = len(bodyparts_triplets)
            # depending on the bodypart, we decide if the limb is moving
            if key_triplets == "tail":
                min_tail_diff_orientation = 0.1
                # if tail, at least 2 part should be moving
                still_vs_mvt[np.where(np.sum(mvt_matrix, axis=0) >= 2)] = 1

                tail_mvt_periods = get_continous_time_periods(still_vs_mvt)

                for tail_mvt_period in tail_mvt_periods:
                    # if duration if more than 2 frames length, then we look at the distance between position every
                    # 2 frames, if it doesn't move much, then we remove it
                    first_frame = tail_mvt_period[0]
                    last_frame = tail_mvt_period[1]
                    duration_period = last_frame - first_frame + 1

                    joint_index = self.joint_name_to_indices_dict[f"tail_mid_tail_dist"]
                    max_mid_dist_tail = np.max(self.orientation_diff_matrix[joint_index, first_frame:last_frame + 1])
                    joint_index = self.joint_name_to_indices_dict[f"tail_prox_tail_mid"]
                    max_prox_mid_tail = np.max(self.orientation_diff_matrix[joint_index, first_frame:last_frame + 1])
                    if (max_mid_dist_tail < min_tail_diff_orientation) and \
                            (max_prox_mid_tail < min_tail_diff_orientation):
                        # we remove it
                        # self.behavior_left_time_stamps
                        print(
                            f"/// {key_triplets} {first_frame} -> {last_frame} removed due to small orientation")
                        still_vs_mvt[first_frame:last_frame + 1] = 0

            else:
                # now either the paw could move by itself, but the angle with the joint should change
                paw_index = 0
                paw_bodypart_name = None
                for i, bodypart in enumerate(triplet):
                    if "paw" in bodypart:
                        paw_index = i
                        paw_bodypart_name = bodypart
                        break
                # TODO: add angle of joint to check
                # for now we consider that if the paw is not moving, the limb is not moving neither
                still_vs_mvt[np.where(mvt_matrix[paw_index, :])] = 1
                # then we want to remove the case when it's moving because the dlc go forth and back without real mvt
                paw_mvt_periods = get_continous_time_periods(still_vs_mvt)

                body_part_index = self.bodyparts_indices[paw_bodypart_name]
                # matches indices in self.bodyparts_indices
                # shape is (n_body_parts, 2 (x, y), n_frames)
                # values could be equal to np.nan
                # self.limbs_body_parts_pos_array
                min_distance = 2
                min_orientation = 6
                for paw_mvt_period in paw_mvt_periods:
                    # if duration if more than 2 frames length, then we look at the distance between position every
                    # 2 frames, if it doesn't move much, then we remove it
                    first_frame = paw_mvt_period[0]
                    last_frame = paw_mvt_period[1]
                    duration_period = last_frame - first_frame + 1

                    paw_period_removed = False
                    if duration_period > 2:
                        distance_every_two = []
                        for index_frame in np.arange(first_frame, last_frame, 1):
                            if index_frame + 2 > last_frame:
                                break
                            x_1 = self.limbs_body_parts_pos_array[body_part_index, 0, index_frame]
                            y_1 = self.limbs_body_parts_pos_array[body_part_index, 1, index_frame]

                            x_2 = self.limbs_body_parts_pos_array[body_part_index, 0, index_frame+2]
                            y_2 = self.limbs_body_parts_pos_array[body_part_index, 1, index_frame+2]

                            if (x_1 == np.nan) or (x_2 == np.nan):
                                continue
                            else:
                                distance = math.sqrt(((x_1 - x_2) ** 2) + ((y_1 - y_2) ** 2))
                                distance_every_two.append(distance)
                        distance_every_two = np.array(distance_every_two)
                        # print(f"{duration_period}: distance_every_two {distance_every_two}")
                        if len(distance_every_two) > 1:
                            if len(np.where(distance_every_two <= min_distance)[0]) >= ((duration_period // 2)*0.6):
                                print(f"/// {paw_bodypart_name} {first_frame} -> {last_frame} removed due to back and forth")
                                # then we remove the mvt period
                                still_vs_mvt[first_frame:last_frame+1] = 0
                                paw_period_removed = True
                    # if not removed, now we want to make sure that the orientation of the paw with join is at least
                    # once more than 5, otherwise it means it didn't really move and we remove the mvt
                    if not paw_period_removed:
                        """
                                self.orientation_diff_matrix[index_so_far, positive_lk_frames]
                                self.joint_name_to_indices_dict[new_part_name] = index_so_far
                                self.indices_to_joint_name_dict[index_so_far] = new_part_name
                        """
                        if "left" in paw_bodypart_name:
                            side = "left"
                        else:
                            side = "right"
                        if "fore" in paw_bodypart_name:
                            name_part = "fore"
                        else:
                            name_part = "hindle"

                        joint_index = self.joint_name_to_indices_dict[f"{name_part}paw_{name_part}leg_joint_{side}"]
                        if np.max(self.orientation_diff_matrix[joint_index, first_frame:last_frame+1]) < min_orientation:
                            # we remove it
                            # self.behavior_left_time_stamps
                            print(
                                f"/// {paw_bodypart_name} {first_frame} -> {last_frame} removed due to small orientation")
                            still_vs_mvt[first_frame:last_frame + 1] = 0

                # TODO: See to use angle as well
                # either the joint and bodyjunction should move
                # joint_and_body_jct_indices = [0, 1, 2]
                # joint_and_body_jct_indices.remove(paw_index)
                # joint_and_body_jct_indices = np.array(joint_and_body_jct_indices)
                # still_vs_mvt[np.where(np.sum(mvt_matrix[joint_and_body_jct_indices], axis=0) == 2)] = 1

            invert_still_vs_mvt = 1 - still_vs_mvt
            still_periods = get_continous_time_periods(invert_still_vs_mvt)
            gap_to_fill = 3
            # feeling the gap of 2 frames without mvt
            for still_period in still_periods:
                if (still_period[1] - still_period[0] + 1) <= gap_to_fill:
                    still_vs_mvt[still_period[0]:still_period[1] + 1] = 1
            # TODO: See to remove mvt of less than 2 frames here
            still_vs_mvt_dict[key_triplets] = still_vs_mvt
            # print(f"{key_bodypart} np.sum(still_vs_mvt) {np.sum(still_vs_mvt)}")

        # now we want to identify startle and complex_mvt
        # we create dictionnaries that contains each part with tuple representing start and end of movement.
        # we will remove those that have been identified as part of a startle or complex_mvt
        # key is the bodyaprt, then dict with id for the period, and tuple of int representing the period
        periods_id_by_bodypart_dict = dict()
        # periods_array_with_id
        # key is bodypart, value is an array of n_frames with value of each the id of the period, starting from 1
        periods_array_with_id_dict = dict()
        # list with an unique id all periods (bodypart family, first_frame, last_frame)
        all_periods = set()

        # ranking period according to their duration, behavior is recording at 20 Hz
        # 1000 ms / 50 ms
        twitch_duration_threshold = 20
        # startle_threshold = 24

        for key_bodypart, still_vs_mvt in still_vs_mvt_dict.items():
            periods = get_continous_time_periods(still_vs_mvt)
            periods_id_by_bodypart_dict[key_bodypart] = dict()
            periods_array_with_id = np.zeros(self.n_frames, dtype="int16")
            for period_index, period in enumerate(periods):
                periods_array_with_id[period[0]:period[1] + 1] = period_index + 1
                periods_id_by_bodypart_dict[key_bodypart][period_index + 1] = period
                all_periods.add((key_bodypart, period[0], period[1]))
                # print(f"all_periods.add {(key_bodypart, period[0], period[1])}")
            periods_array_with_id_dict[key_bodypart] = periods_array_with_id

        # print(f"periods_array_with_id_dict {periods_array_with_id_dict}")

        # now we want to explore all periods in periods_id_by_bodypart_dict to check which ones should be associated
        # to startle or complex mvt
        while len(all_periods) > 0:
            # get period id and remove it from the set in the same time
            period_id = all_periods.pop()
            key_bodypart = period_id[0]
            first_frame = period_id[1]
            last_frame = period_id[2]
            mvt_duration = last_frame - first_frame + 1
            # we want at least 2 frames (100 ms) to consider it as mvt
            if mvt_duration < 2:
                continue
            # we get the names of other bodyparts to explore
            bodyparts_names = list(bodyparts_triplets.keys())
            bodyparts_names.remove(key_bodypart)
            # KeyError: ('hindlimb', 22245, 22300)
            # key is id (bodypart, first_frame, last_frame) and value is the duration
            other_mvts_dict = dict()
            # complex_mvt or startle are defined as if all or all - 2 bodypart are active in the same time
            for bodypart_to_explore in bodyparts_names:
                periods_array_with_id = periods_array_with_id_dict[bodypart_to_explore]
                # we look if a concomittent mvt happened
                if np.sum(periods_array_with_id[first_frame:last_frame + 1]) > 0:
                    # another mvt happened in the same time
                    period_ids = list(np.unique(periods_array_with_id[first_frame:last_frame + 1]))
                    if 0 in period_ids:
                        period_ids.remove(0)
                    if len(period_ids) > 1:
                        # we keep the one with the most frames
                        max_n_frames = 0
                        period_id = None
                        for i in period_ids:
                            frames_count = len(np.where(periods_array_with_id[first_frame:last_frame + 1] == i)[0])
                            if frames_count > max_n_frames:
                                period_id = i
                                max_n_frames = frames_count
                    else:
                        period_id = period_ids[0]
                    period = periods_id_by_bodypart_dict[bodypart_to_explore][period_id]
                    other_mvts_dict[(bodypart_to_explore, period[0], period[1])] = period[1] - period[0] + 1
            # now let's count how many other part are moving in the same time
            n_moving_bodyparts = len(other_mvts_dict)
            if (n_moving_bodyparts >= len(bodyparts_triplets) - 3) or (
                    n_moving_bodyparts > 0 and np.max(list(other_mvts_dict.values())) > 40):
                # then we are in the category startle or complex_mvt
                # if one of the other mvt part has a long mvt, then we rank it complex_mvt
                # complex mvt here is defined as more than 2 sec
                # we take the first frame of all mvts, and the last last_frame of all
                first_first_frame = first_frame
                last_last_frame = last_frame
                for key_other_mvt in other_mvts_dict.keys():
                    if key_other_mvt[1] < first_first_frame:
                        first_first_frame = key_other_mvt[1]
                    if key_other_mvt[2] > last_last_frame:
                        last_last_frame = key_other_mvt[2]
                    # we remove other mvt from the set meanwhile
                    if key_other_mvt in all_periods:
                        all_periods.remove(key_other_mvt)

                if np.max(list(other_mvts_dict.values())) > twitch_duration_threshold:
                    # using array, we can extend previous complet_mvt period
                    periods_by_type_of_mvt["complex_mvt"][first_first_frame:last_last_frame + 1] = 1
                else:
                    periods_by_type_of_mvt["startle"][first_first_frame:last_last_frame + 1] = 1
            else:
                # we are in the category twitch or mvt of one body part
                if mvt_duration <= twitch_duration_threshold:
                    # we classify it as a twitch
                    periods_by_type_of_mvt[f"twitch_{key_bodypart}"][first_frame:last_frame + 1] = 1
                else:
                    # else a mvt
                    periods_by_type_of_mvt[f"mvt_{key_bodypart}"][first_frame:last_frame + 1] = 1

        # we're gonna a loop until no more changes are done
        modif_done = True
        # str just use for display purpose
        modif_reason = ""
        n_loops_of_modif = 0
        while modif_done:
            modif_done = False
            n_loops_of_modif += 1
            print(f"n_loops_of_modif {n_loops_of_modif} {modif_reason}")
            modif_reason = ""
            # now we want to fusion periods of complex_mvt that would be close and also merge them with close by other mvt
            complex_mvt_periods = get_continous_time_periods(periods_by_type_of_mvt["complex_mvt"])
            # gap between two complex mvt to fill, 20 frames == 1.5sec
            max_gap_by_complex_mvt = 30
            for complex_mvt_period_index, complex_mvt_period in enumerate(complex_mvt_periods[:-1]):
                last_frame = complex_mvt_period[1]
                next_frame = complex_mvt_periods[complex_mvt_period_index + 1][0]
                if next_frame - last_frame <= max_gap_by_complex_mvt:
                    # we fill the gap
                    periods_by_type_of_mvt["complex_mvt"][last_frame + 1:next_frame] = 1
                    modif_done = True
                    modif_reason = modif_reason + " max_gap_by_complex_mvt"
                    # Removing other mvt happening during the GAP
                    first_frame_index = complex_mvt_period[0]
                    last_frame_index = complex_mvt_periods[complex_mvt_period_index][1]
                    # a simple way, we remove all positive frame from first to last_frame_index in other mvt
                    for mvt_key, mvt_array in periods_by_type_of_mvt.items():
                        if mvt_key == "complex_mvt":
                            continue
                        # TODO: See to make sure we don't cut some periods when doing so
                        #  to do so, we would need to encode each period with an index, to make sure it did diseappear
                        mvt_array[first_frame_index:last_frame_index + 1] = 0

            # now we want to fusion startles and very close twitches from startles together
            max_gap_startle = 15  # 750 msec

            startle_mvt_periods = get_continous_time_periods(periods_by_type_of_mvt["startle"])
            # first we check if startles didn't become complex_mvt
            for startle_mvt_period_index, startle_mvt_period in enumerate(startle_mvt_periods):
                if startle_mvt_period[1] - startle_mvt_period[0] + 1 > twitch_duration_threshold:
                    modif_done = True
                    modif_reason = modif_reason + " startle_extended"
                    periods_by_type_of_mvt["complex_mvt"][startle_mvt_period[0]:startle_mvt_period[1] + 1] = 1
                    periods_by_type_of_mvt["startle"][startle_mvt_period[0]:startle_mvt_period[1] + 1] = 0

            startle_mvt_periods = get_continous_time_periods(periods_by_type_of_mvt["startle"])
            for startle_mvt_period_index, startle_mvt_period in enumerate(startle_mvt_periods[:-1]):
                last_frame = startle_mvt_period[1]
                next_frame = startle_mvt_periods[startle_mvt_period_index + 1][0]
                if next_frame - last_frame <= max_gap_startle:
                    modif_done = True
                    modif_reason = modif_reason + " max_gap_startle"
                    first_frame_index = startle_mvt_period[0]
                    last_frame_index = startle_mvt_periods[startle_mvt_period_index][1]
                    duration_new_startle = last_frame_index - first_frame_index + 1
                    # then either it becomes a complex_mvt or become a longer startle
                    if duration_new_startle > twitch_duration_threshold:
                        periods_by_type_of_mvt["complex_mvt"][first_frame_index:last_frame_index + 1] = 1
                        # We remove it from startle
                        periods_by_type_of_mvt["startle"][first_frame_index:last_frame_index + 1] = 0
                    else:
                        periods_by_type_of_mvt["startle"][last_frame + 1:next_frame] = 1
                        # a simple way, we remove all positive frame from first to last_frame_index in other mvt
                        for mvt_key, mvt_array in periods_by_type_of_mvt.items():
                            if mvt_key == "startle":
                                continue
                            # TODO: See to make sure we don't cut some periods when doing so
                            #  to do so, we would need to encode each period with an index, to make sure it did diseappear
                            mvt_array[first_frame_index:last_frame_index + 1] = 0
            for mvt_key, mvt_array in periods_by_type_of_mvt.items():
                if mvt_key in ["complex_mvt"]:  # , "startle"
                    continue
                is_mvt_startle = False
                if mvt_key == "startle":
                    is_mvt_startle = True
                gap_for_fusion = {"startle": 10, "complex_mvt": 20}  # 500 msec & 1 sec
                mvt_periods = get_continous_time_periods(mvt_array)
                # then we look at all periods in mvt_complex and startle to see if we can fusion
                for mvt_period in mvt_periods:
                    first_frame_mvt = mvt_period[0]
                    last_frame_mvt = mvt_period[1]
                    gap_value = min(first_frame_mvt, gap_for_fusion["complex_mvt"])
                    if gap_value > 0:
                        if np.sum(periods_by_type_of_mvt["complex_mvt"]
                                  [first_frame_mvt - gap_for_fusion["complex_mvt"]:first_frame_mvt]) > 0:
                            # then we change it to complex_mvt
                            periods_by_type_of_mvt["complex_mvt"][first_frame_mvt:last_frame_mvt + 1] = 1
                            mvt_array[first_frame_mvt:last_frame_mvt + 1] = 0
                            modif_done = True
                            modif_reason = modif_reason + " gap fusion complex mvt"
                            continue
                    # if a startle was detected just before a complex_mvt, we should consider it
                    # as part of the complex_mvt and not as a startle
                    if is_mvt_startle:
                        # we use the fusion gap of startle here still
                        gap_value = min(self.n_frames - last_frame_mvt, gap_for_fusion["startle"])
                        if gap_value > 0:
                            if np.sum(periods_by_type_of_mvt["complex_mvt"]
                                      [last_frame_mvt:last_frame_mvt + gap_for_fusion["startle"]]) > 0:
                                # then we change it to startle
                                periods_by_type_of_mvt["complex_mvt"][first_frame_mvt:last_frame_mvt + 1] = 1
                                mvt_array[first_frame_mvt:last_frame_mvt + 1] = 0
                                modif_done = True
                                modif_reason = modif_reason + " gap fusion startle before complex mvt"
                                continue
                    if not is_mvt_startle:
                        # for startle mvt, we only look to fusion them with complex mvt
                        # for startle we look before and after
                        gap_value = min(first_frame_mvt, gap_for_fusion["startle"])
                        if gap_value > 0:
                            if np.sum(periods_by_type_of_mvt["startle"]
                                      [first_frame_mvt - gap_for_fusion["startle"]:first_frame_mvt]) > 0:
                                # then we change it to startle
                                periods_by_type_of_mvt["startle"][first_frame_mvt:last_frame_mvt + 1] = 1
                                mvt_array[first_frame_mvt:last_frame_mvt + 1] = 0
                                modif_done = True
                                modif_reason = modif_reason + " gap fusion startle before"
                                continue
                        # gap_value = min(self.n_frames - last_frame_mvt, gap_for_fusion["startle"])
                        # if gap_value > 0:
                        #     if np.sum(periods_by_type_of_mvt["startle"]
                        #               [last_frame_mvt:last_frame_mvt + gap_for_fusion["startle"]]) > 0:
                        #         # then we change it to startle
                        #         periods_by_type_of_mvt["startle"][first_frame_mvt:last_frame_mvt + 1] = 1
                        #         mvt_array[first_frame_mvt:last_frame_mvt + 1] = 0
                        #         modif_done = True
                        #         modif_reason = modif_reason + " gap fusion startle after"
                        #         continue
        print(f"n_loops_of_modif final:  {n_loops_of_modif}")

        for action_str in ["cicada", "evaluate"]:
            # will be saved in the npz
            # each key is the tag, and value is a 2d array (2x n_intervals) with start and finish in sec on lines,
            # each column is an interval
            behaviors_encoding_dict = dict()
            for key_behavior, binary_array in periods_by_type_of_mvt.items():
                if action_str == "evaluate":
                    key_to_use = key_behavior
                else:
                    key_to_use = "auto_" + key_behavior
                periods = get_continous_time_periods(binary_array)
                if "left" in key_behavior:
                    behaviors_encoding_dict[key_to_use] = \
                        encode_period_with_timestamps(periods=periods,
                                                      timestamps=self.behavior_left_time_stamps)
                else:
                    behaviors_encoding_dict[key_to_use] = \
                        encode_period_with_timestamps(periods=periods,
                                                      timestamps=self.behavior_right_time_stamps)
            if self.gt_behavior is not None and (action_str == "evaluate"):
                evaluate_behavior_predictions(ground_truth_labels=self.gt_behavior,
                                              other_labels=behaviors_encoding_dict,
                                              n_frames=self.n_frames,
                                              behavior_timestamps=self.behavior_right_time_stamps)

            np.savez(os.path.join(self.results_path, f"test_{self.identifier}_{action_str}.npz"),
                     **behaviors_encoding_dict)


def get_continous_time_periods(binary_array):
    """
    take a binary array and return a list of tuples representing the first and last position(included) of continuous
    positive period
    This code was copied from another project or from a forum, but i've lost the reference.
    :param binary_array:
    :return:
    """
    binary_array = np.copy(binary_array).astype("int8")
    n_times = len(binary_array)
    d_times = np.diff(binary_array)
    # show the +1 and -1 edges
    pos = np.where(d_times == 1)[0] + 1
    neg = np.where(d_times == -1)[0] + 1

    if (pos.size == 0) and (neg.size == 0):
        if len(np.nonzero(binary_array)[0]) > 0:
            return [(0, n_times - 1)]
        else:
            return []
    elif pos.size == 0:
        # i.e., starts on an spike, then stops
        return [(0, neg[0])]
    elif neg.size == 0:
        # starts, then ends on a spike.
        return [(pos[0], n_times - 1)]
    else:
        if pos[0] > neg[0]:
            # we start with a spike
            pos = np.insert(pos, 0, 0)
        if neg[-1] < pos[-1]:
            #  we end with aspike
            neg = np.append(neg, n_times - 1)
        # NOTE: by this time, length(pos)==length(neg), necessarily
        # h = np.matrix([pos, neg])
        h = np.zeros((2, len(pos)), dtype="int32")
        h[0] = pos
        h[1] = neg
        if np.any(h):
            result = []
            for i in np.arange(h.shape[1]):
                if h[1, i] == n_times - 1:
                    result.append((h[0, i], h[1, i]))
                else:
                    result.append((h[0, i], h[1, i] - 1))
            return result
    return []


def get_behaviors_movie_time_stamps(nwb_file, cam_id):
    """

    Args:
        nwb_file:
        cam_id: '22983298' or '23109588'

    Returns:

    """
    io = NWBHDF5IO(nwb_file, 'r')
    nwb_data = io.read()

    for name, acquisition_data in nwb_data.acquisition.items():
        if name.startswith(f"cam_{cam_id}"):
            return np.array(acquisition_data.timestamps)

    return None


def match_frame_to_timestamp(frame_timestamps, timestamp):
    """
    Find which frame match the given timestamp
    Args:
        frame_timestamps:
        timestamp:

    Returns:

    """
    index = find_nearest(frame_timestamps, timestamp)
    # index = bisect_right(frame_timestamps, timestamp) - 1
    return index


def encode_frames_from_cicada(cicada_file, nwb_file, cam_id, n_frames, side_to_exclude=None, no_behavior_str="still"):
    """
    Return a list of len n_frames with str representing each frame behavior
    Args:
        cicada_file:
        n_frames:
        side_to_exclude: not apply for npz content, all of it is return as the third argument

    Returns:

    """
    npz_content = np.load(cicada_file)

    tags = []
    tags_index = dict()
    n_tags = 0
    for tag_name, value in npz_content.items():
        if side_to_exclude in tag_name:
            continue
        if value.shape[1] > 0:
            tags.append(tag_name)
            tags_index[tag_name] = n_tags
            n_tags += 1

    print(f"encode_frames_from_cicada() {cam_id} tags {tags}")

    interval_id = 0
    intervals_array = np.zeros((len(tags), n_frames), dtype="int16")
    interval_info_dict = dict()
    behavior_time_stamps = get_behaviors_movie_time_stamps(nwb_file=nwb_file, cam_id=cam_id)
    if len(behavior_time_stamps) != n_frames:
        print(f"len(behavior_time_stamps) != n_frames, {len(behavior_time_stamps)} != {n_frames}")
        if len(behavior_time_stamps) > n_frames:
            # removing the last frames
            behavior_time_stamps = behavior_time_stamps[:n_frames - len(behavior_time_stamps)]
        else:
            raise Exception("Wrong number of frames")
    # print(f"behavior_time_stamps {behavior_time_stamps}")
    for tag_name, value in npz_content.items():
        if side_to_exclude in tag_name:
            continue

        for i in range(value.shape[1]):
            # print(f"value[0, i] {value[0, i]}, {value[1, i]+1}")
            # TODO: Transform the seconds value in the frame number of the given cam
            first_frame = match_frame_to_timestamp(behavior_time_stamps, value[0, i])
            last_frame = match_frame_to_timestamp(behavior_time_stamps, value[1, i])
            intervals_array[tags_index[tag_name], first_frame:last_frame] = interval_id
            # duration in sec
            interval_info_dict[interval_id] = value[1, i] - value[0, i] + 1
            interval_id += 1

    tags_by_frame = []
    for frame_index in range(n_frames):
        tags_indices = np.where(intervals_array[:, frame_index] > 0)[0]
        if len(tags_indices) == 0:
            tags_by_frame.append(no_behavior_str)
        elif len(tags_indices) == 1:
            tags_by_frame.append(tags[tags_indices[0]])
        else:
            # then we select the shorter one
            for i, tag_index in enumerate(tags_indices):
                if i == 0:
                    shorter_tag = tags[tag_index]
                    interval_id = intervals_array[tag_index, frame_index]
                    shorter_duration = interval_info_dict[interval_id]
                else:
                    interval_id = intervals_array[tag_index, frame_index]
                    duration = interval_info_dict[interval_id]
                    if duration < shorter_duration:
                        shorter_duration = duration
                        shorter_tag = tags[tag_index]
            tags_by_frame.append(shorter_tag)
    return tags_by_frame, behavior_time_stamps, npz_content


def apply_tsne(data, behavior_by_frame=None):
    # sns.set(rc={'figure.figsize': (11.7, 8.27)})
    # if behavior_by_frame is not None:
    #     palette = sns.color_palette("hls", len(np.unique(behavior_by_frame)))
    # else:
    #     palette = sns.color_palette("hls", 10)

    tsne = TSNE(verbose=1, n_components=2, perplexity=50, n_iter=500)
    data_embedded = tsne.fit_transform(data)
    # print(f"apply_tsne() data_embedded.shape {data_embedded.shape}")
    plot_t_sne_results(x_data=data_embedded[:, 0], y_data=data_embedded[:, 1], z_data=None,
                       behavior_by_frame=behavior_by_frame)
    # sns.scatterplot(data_embedded[:, 0], data_embedded[:, 1], hue=behavior_by_frame,
    #                 legend='full', palette=palette)
    #
    # plt.show()


def load_t_sne_from_b_soid(b_soid_file, n_frames, behavior_by_frame=None):
    data = hdf5storage.loadmat(b_soid_file)
    print(f"data {data['tsne_feats'].shape}")
    # shape is (n_frames//2, 3)
    tsne_feats = data['tsne_feats']
    # first we double the number of frames
    new_tsne_feats = np.zeros((n_frames, tsne_feats.shape[1]))
    for frame in np.arange(tsne_feats.shape[0]):
        new_tsne_feats[frame * 2] = tsne_feats[frame]
        new_tsne_feats[(frame * 2) + 1] = tsne_feats[frame]

    with_z_data = True
    if with_z_data:
        plot_t_sne_results(new_tsne_feats[:, 0], new_tsne_feats[:, 1], z_data=new_tsne_feats[:, 2],
                           behavior_by_frame=behavior_by_frame)
    else:
        plot_t_sne_results(new_tsne_feats[:, 0], new_tsne_feats[:, 1], z_data=None, behavior_by_frame=behavior_by_frame)


def plot_t_sne_results(x_data, y_data, z_data=None, behavior_by_frame=None):
    if z_data is not None:
        fig = plt.figure()
        ax = Axes3D(fig)

        unique_behavior = np.unique(behavior_by_frame)
        behavior_to_color = dict()
        for index_b, behavior in enumerate(unique_behavior):
            behavior_to_color[behavior] = BREWER_COLORS[index_b % len(BREWER_COLORS)]
        colors = [behavior_to_color[b] for b in behavior_by_frame]
        ax.scatter(x_data, y_data, z_data, c=colors)
        plt.show()
        return

    sns.set(rc={'figure.figsize': (11.7, 8.27)})
    if behavior_by_frame is not None:
        palette = sns.color_palette("hls", len(np.unique(behavior_by_frame)))
    else:
        palette = sns.color_palette("hls", 10)

    sns.scatterplot(x_data, y_data, hue=behavior_by_frame,
                    legend='full', palette=palette)

    plt.show()


def get_data_from_dlc_h5_files(data_path, pos_file_name, skeketon_file_name=None, replace_by_nan=False, verbose=1,
                               likelihood_threshold=0.1):
    if '22983298' in pos_file_name:
        cam_id = '22983298'
    else:
        cam_id = '23109588'

    pos_h5_file = h5py.File(os.path.join(data_path, pos_file_name), 'r')
    if skeketon_file_name is not None:
        skeketon_h5_file = h5py.File(os.path.join(data_path, skeketon_file_name), 'r')

    config_yaml = os.path.join(data_path, "config.yaml")
    with open(config_yaml, 'r') as stream:
        config_data = yaml.load(stream, Loader=yaml.FullLoader)
    bodyparts = config_data['bodyparts']
    bodyparts_indices = dict()
    n_bodyparts = len(bodyparts)
    # print(f"bodyparts {bodyparts}")

    # list of list of 2 part linked
    skeleton_pairs_list = config_data['skeleton']
    # same named as used in the csv
    skeleton_parts = [s1 + "_" + s2 for s1, s2 in skeleton_pairs_list]
    # print(f"skeleton_parts {skeleton_parts}")
    n_skeleton_parts = len(skeleton_parts)

    pos_h5_data = pos_h5_file['df_with_missing']['table']
    if skeketon_file_name is not None:
        skeleton_h5_data = skeketon_h5_file['df_with_missing']['table']

    n_frames = len(pos_h5_data)

    # x, y, likelihood
    pos_data_array = np.zeros((n_frames, len(bodyparts) * 3))
    for frame in np.arange(n_frames):
        pos_data_array[frame] = np.array(pos_h5_data[frame][1])

    if skeketon_file_name is not None:
        # length, orientation, likelihood
        skeleton_h5_data_array = np.zeros((n_frames, n_skeleton_parts * 3))
        for frame in np.arange(n_frames):
            skeleton_h5_data_array[frame] = np.array(skeleton_h5_data[frame][1])

    bodyparts_pos_dict = dict()
    body_parts_pos_array = np.zeros((n_bodyparts, 3, n_frames))
    # n_bodyparts, (length, orientation, likelihood), n_frames
    skeleton_parts_pos_array = np.zeros((n_skeleton_parts, 3, n_frames))
    for body_index, bodypart in enumerate(bodyparts):
        bodyparts_indices[bodypart] = body_index
        # # likelihood
        print(f"{bodypart} mean likelihood {np.mean(pos_data_array[:, (body_index * 3) + 2])}")
        for frame in np.arange(n_frames):
            body_parts_pos_array[body_index, 0, frame] = pos_data_array[frame, body_index * 3]
            body_parts_pos_array[body_index, 1, frame] = pos_data_array[frame, (body_index * 3) + 1]
            body_parts_pos_array[body_index, 2, frame] = pos_data_array[frame, (body_index * 3) + 2]

        bodyparts_pos_dict[bodypart] = body_parts_pos_array[body_index]
    if skeketon_file_name is not None:
        for skeleton_index, skeleton_part in enumerate(skeleton_parts):
            # skeleton_parts_indices[skeleton_part] = skeleton_index

            for frame in np.arange(n_frames):
                skeleton_parts_pos_array[skeleton_index, 0, frame] = skeleton_h5_data_array[frame, skeleton_index * 3]
                skeleton_parts_pos_array[skeleton_index, 1, frame] = skeleton_h5_data_array[
                    frame, (skeleton_index * 3) + 1]
                skeleton_parts_pos_array[skeleton_index, 2, frame] = skeleton_h5_data_array[
                    frame, (skeleton_index * 3) + 2]

    # pcutoff
    # if 1 no thresholding
    if likelihood_threshold < 1:
        if skeketon_file_name is not None:
            to_filter = ["bodyparts", "sketleton_parts"]
        else:
            to_filter = ["bodyparts"]
        for parts_to_filter in to_filter:
            # filling with nan for now
            if verbose:
                print(f"### n labels wrong (p_cutoff < {likelihood_threshold})")
                print(f"# For {parts_to_filter}")
            if parts_to_filter == "bodyparts":
                print('in parts_to_filter == "bodyparts"')
                n_parts = n_bodyparts
                parts_pos_array = body_parts_pos_array
                labels = bodyparts
            else:
                n_parts = n_skeleton_parts
                parts_pos_array = skeleton_parts_pos_array
                labels = skeleton_parts
            for part_index in np.arange(n_parts):
                indices = np.where(parts_pos_array[part_index, 2, :] < likelihood_threshold)[0]
                if verbose:
                    print(f"{labels[part_index]}: {len(indices)}")
                # TODO: See to do like in B-SOID, replacing it by the position with the highest likelihood
                #  over a temporal window
                # replacing x, y by NaN
                if replace_by_nan:
                    parts_pos_array[part_index, 0, indices] = np.nan
                    parts_pos_array[part_index, 1, indices] = np.nan
                else:
                    # we want to put the previous value or the mean between previous and next if known
                    for frame_index in indices:
                        if frame_index == 0:
                            # looking for next frame_index know
                            if frame_index + 1 in indices:
                                next_index = frame_index + 1
                                while next_index in indices:
                                    next_index += 1
                                if next_index < parts_pos_array.shape[2]:
                                    parts_pos_array[part_index, 0, frame_index] = parts_pos_array[
                                        part_index, 0, next_index]
                                    parts_pos_array[part_index, 1, frame_index] = parts_pos_array[
                                        part_index, 1, next_index]
                            else:
                                parts_pos_array[part_index, 0, frame_index] = parts_pos_array[
                                    part_index, 0, frame_index + 1]
                                parts_pos_array[part_index, 1, frame_index] = parts_pos_array[
                                    part_index, 1, frame_index + 1]
                        else:
                            x_values = parts_pos_array[part_index, 0]
                            y_values = parts_pos_array[part_index, 1]
                            if (frame_index + 1) in indices or frame_index == (n_frames - 1):
                                # we take previous value
                                parts_pos_array[part_index, 0, frame_index] = x_values[frame_index - 1]
                                parts_pos_array[part_index, 1, frame_index] = y_values[frame_index - 1]
                            else:
                                # we take the mean
                                parts_pos_array[part_index, 0, frame_index] = (x_values[frame_index - 1] +
                                                                               x_values[frame_index + 1]) / 2
                                parts_pos_array[part_index, 1, frame_index] = (y_values[frame_index - 1] +
                                                                               y_values[frame_index + 1]) / 2
        print("")
    pos_h5_file.close()
    if skeketon_file_name is not None:
        skeketon_h5_file.close()
    else:
        skeleton_parts, skeleton_parts_pos_array = (None, None)
    return n_frames, bodyparts, body_parts_pos_array, skeleton_parts, skeleton_parts_pos_array, cam_id


def euclidean_distance_for_bodyparts(body_parts_pos_array, no_nan_replacement=False):
    # we put in each frame index the distance from the last frame
    distance_matrix = np.zeros((len(body_parts_pos_array), body_parts_pos_array.shape[2]))

    for bodypart_index in np.arange(body_parts_pos_array.shape[0]):
        for frame_index in np.arange(body_parts_pos_array.shape[2]):
            if frame_index == 0:
                distance_matrix[bodypart_index, frame_index] = 0
                continue

            x_1 = body_parts_pos_array[bodypart_index, 0, frame_index - 1]
            y_1 = body_parts_pos_array[bodypart_index, 1, frame_index - 1]
            x_2 = body_parts_pos_array[bodypart_index, 0, frame_index]
            y_2 = body_parts_pos_array[bodypart_index, 1, frame_index]
            # if one of both positions are Nan, then we put 0 as distance.
            if (x_1 == np.nan) or (x_2 == np.nan):
                if no_nan_replacement:
                    distance_matrix[bodypart_index, frame_index] = np.nan
                else:
                    distance_matrix[bodypart_index, frame_index] = 0
            else:
                distance = math.sqrt(((x_1 - x_2) ** 2) + ((y_1 - y_2) ** 2))
                distance_matrix[bodypart_index, frame_index] = distance

    return distance_matrix


def encode_period_with_timestamps(periods, timestamps):
    """
    Return an array that will contain the periods, used to save npz for CICADA
    Args:
        periods:
        timestamps:

    Returns:

    """
    mvt_encoding = np.zeros((2, len(periods)))
    for index, mvt_period in enumerate(periods):
        # Removing mvt period that last only 1 frame
        if mvt_period[1] - mvt_period[0] < 2:
            continue
        mvt_encoding[0, index] = timestamps[mvt_period[0]]
        mvt_encoding[1, index] = timestamps[mvt_period[1]]

    return mvt_encoding


def get_binary_vector_from_2d_behavior_array(behavior_2d_array, n_frames):
    result = np.zeros(n_frames, dtype="int16")
    # print(f"behavior_2d_array {behavior_2d_array}")
    for interval_index in range(behavior_2d_array.shape[1]):
        result[behavior_2d_array[0, interval_index]: behavior_2d_array[1, interval_index] + 1] = 1
    return result


def transform_second_behavior_matrix_to_frame(behavior_periods, behavior_timestamps,
                                              last_time_stamp_to_consider=None):
    """

    Args:
        behavior_periods: (2xn_periods) array
        behavior_timestamps: give the timestamps (in sec) for each frame
        last_time_stamp_to_consider: (float) if not None, any period of activity that start after this
        timestamp will not be taken into consideration
    Returns:

    """
    n_periods = behavior_periods.shape[1]
    if last_time_stamp_to_consider is not None:
        # we count how many periods to consider
        n_periods = 0
        for index in range(behavior_periods.shape[1]):
            first_time_stamp = behavior_periods[0, index]
            if first_time_stamp <= last_time_stamp_to_consider:
                n_periods += 1

    behavior_in_frames = np.zeros((2, n_periods), dtype="int16")
    real_index = 0
    for index in range(behavior_periods.shape[1]):
        if last_time_stamp_to_consider is not None:
            first_time_stamp = behavior_periods[0, index]
            if first_time_stamp > last_time_stamp_to_consider:
                # periods being ordered
                break
        first_frame = match_frame_to_timestamp(behavior_timestamps, behavior_periods[0, index])
        last_frame = match_frame_to_timestamp(behavior_timestamps, behavior_periods[1, index])
        behavior_in_frames[0, index] = first_frame
        behavior_in_frames[1, index] = last_frame
    return behavior_in_frames


def evaluate_behavior_predictions(ground_truth_labels, other_labels, n_frames, behavior_timestamps):
    """

    Args:
        ground_truth_labels: dict with key behavior and value 2d array (2*frames)
        other_labels: dict with key behavior and value 2d array (2*frames)

    Returns:

    """

    # first we determine until which timestamps the the ground truth has been labeled
    last_time_stamp_to_consider = 0
    for key_behavior in other_labels.keys():
        if key_behavior not in ground_truth_labels:
            continue
        bahavior_periods = ground_truth_labels[key_behavior]
        for index in range(bahavior_periods.shape[1]):
            first_time_stamp = bahavior_periods[0, index]
            last_time_stamp = bahavior_periods[1, index]
            if last_time_stamp > last_time_stamp_to_consider:
                last_time_stamp_to_consider = last_time_stamp

    for key_behavior, other_behavior_activity_array in other_labels.items():
        if key_behavior not in ground_truth_labels:
            print(f"{key_behavior} not defined in ground truth")
            continue

        print(f"## METRICS for {key_behavior}")
        other_behavior_activity_array = transform_second_behavior_matrix_to_frame(behavior_periods=
                                                                                  other_behavior_activity_array,
                                                                                  behavior_timestamps=
                                                                                  behavior_timestamps,
                                                                                  last_time_stamp_to_consider=
                                                                                  last_time_stamp_to_consider)

        other_binary_activity = get_binary_vector_from_2d_behavior_array(other_behavior_activity_array, n_frames)

        gt_behavior_activity_array = ground_truth_labels[key_behavior]
        gt_behavior_activity_array = transform_second_behavior_matrix_to_frame(behavior_periods=
                                                                               gt_behavior_activity_array,
                                                                               behavior_timestamps=behavior_timestamps)
        gt_binary_activity = get_binary_vector_from_2d_behavior_array(gt_behavior_activity_array, n_frames)

        # now we count tp, fp
        tp = 0
        fp = 0
        # tn should not exists
        tn = 0
        fn = 0
        for active_period_index in range(gt_behavior_activity_array.shape[1]):
            first_frame = gt_behavior_activity_array[0, active_period_index]
            last_frame = gt_behavior_activity_array[1, active_period_index]
            if np.sum(other_binary_activity[first_frame:last_frame + 1]) > 0:
                tp += 1
            else:
                fn += 1

        for period_index in range(other_behavior_activity_array.shape[1]):
            first_frame = other_behavior_activity_array[0, period_index]
            last_frame = other_behavior_activity_array[1, period_index]
            if np.sum(gt_binary_activity[first_frame:last_frame + 1]) == 0:
                fp += 1

        print(f"tp {tp}, fp {fp}, fn {fn}")
        print(f"Over {gt_behavior_activity_array.shape[1]} active periods, {tp} were identified and {fn} were missed")
        print(f"{fn} were wrongly assigned as present")

        if (tp + fn) > 0:
            sensitivity = tp / (tp + fn)
        else:
            sensitivity = 1

        if (tp + fp) > 0:
            ppv = tp / (tp + fp)
        else:
            ppv = 1

        print(f"SENSITIVITY: {np.round(sensitivity * 100, 2)}%, PPV: {np.round(ppv * 100, 2)}%")

        print(f"")


def basic_solution(n_frames, bodyparts, body_parts_pos_array, skeleton_parts, skeleton_parts_pos_array,
                   results_path, behavior_time_stamps, gt_behavior=None
                   ):
    """

    Args:
        n_frames:
        bodyparts:
        body_parts_pos_array: array of 3 dim with body_part_index, (x, y, lk), frame
        skeleton_parts:
        skeleton_parts_pos_array:
        behavior_by_frame:
        results_path:

    Returns:

    """
    # TODO: Integrate both movie parts

    behaviors = ['still', 'twitch_foreleg', 'twitch_hindleleg', "complex_mvt"]

    # will be saved in the npz
    # each key is the tag, and value is a 2d array (2x n_intervals) with start and finish in sec on lines,
    # each column is an interval
    behaviors_encoding_dict = dict()

    n_behaviors = len(behaviors)

    bodyparts_indices = dict()
    for body_index, bodypart in enumerate(bodyparts):
        bodyparts_indices[bodypart] = body_index

    # for each behavior, 1 at a frame index means the behavior is happening at this frame
    # behavior_matrix = np.zeros((n_behaviors, n_frames), dtype="int16")

    # first we want to measure the euclidean distance for each part from x_y values
    distance_matrix = euclidean_distance_for_bodyparts(body_parts_pos_array)

    # now we apply a diff at the distance matrix
    diff_distance_matrix = np.abs(np.diff(distance_matrix, axis=1))
    tmp_matrix = np.zeros((diff_distance_matrix.shape[0], diff_distance_matrix.shape[1] + 1))
    tmp_matrix[:, 1:] = diff_distance_matrix
    diff_distance_matrix = tmp_matrix
    # print(f"diff_distance_matrix {diff_distance_matrix}")
    # print(f"np.mean(diff_distance_matrix) {np.mean(diff_distance_matrix)}")

    # now we keep only the frame in which a certain movement is found
    mvt_threshold = 5

    # using diff_distance_matrix allows to use the speed of the movement as threshold
    binary_mvt_matrix = np.zeros((distance_matrix.shape[0], distance_matrix.shape[1]))
    binary_mvt_matrix[np.where(diff_distance_matrix > mvt_threshold)] = 1
    # print(np.sum(binary_mvt_matrix))

    # ### Just any kind of mvt for more than 1 frame of duration ###
    # mvt is 1
    still_vs_mvt = np.zeros(n_frames, dtype="int16")

    # at least 2 part moving
    still_vs_mvt[np.where(np.sum(binary_mvt_matrix, axis=0) > 1)] = 1
    mvt_periods = get_continous_time_periods(still_vs_mvt)

    # behaviors_encoding_dict["mvt"] = encode_period_with_timestamps(periods=mvt_periods, timestamps=behavior_time_stamps)

    # ### now we want to distinguish the diffrent type of mvt and to make it stronger to outlier
    # we will keep a mvt only if 2 of 3 parts of each component of the body are in mvt

    # TODO: in the future add left and right limbs, and fusion information about tail
    bodyparts_triplets = {'forelimb': ['forepaw', 'foreleg_joint', 'foreleg_body_jonction'],
                          "hindlimb": ['hindlepaw', 'hindleleg_joint', 'hindleleg_body_jonction'],
                          "tail": ['tail_prox', 'tail_mid', 'tail_dist']}
    # key being the bodypart
    still_vs_mvt_dict = dict()
    # first key key to put in npz and value a list of periods
    periods_by_type_of_mvt = dict()
    periods_by_type_of_mvt["complex_mvt"] = np.zeros(n_frames, dtype="int8")
    periods_by_type_of_mvt["startle"] = np.zeros(n_frames, dtype="int8")

    for key_bodypart, triplet in bodyparts_triplets.items():
        npz_key_bodypart = key_bodypart
        if npz_key_bodypart != "tail":
            npz_key_bodypart = npz_key_bodypart + "_left"

        periods_by_type_of_mvt[f"twitch_{npz_key_bodypart}"] = np.zeros(n_frames, dtype="int8")
        periods_by_type_of_mvt[f"mvt_{npz_key_bodypart}"] = np.zeros(n_frames, dtype="int8")
        # periods_by_type_of_mvt[f"twith_{key_bodypart}"] = []

        body_indices = np.array([bodyparts_indices[bodypart] for bodypart in triplet])
        mvt_matrix = binary_mvt_matrix[body_indices]
        still_vs_mvt = np.zeros(n_frames, dtype="int16")

        # 1 represents mvt, we want at least 2 out of the 3 body part in the triplet to be active to consider it mvt
        still_vs_mvt[np.where(np.sum(mvt_matrix, axis=0) > 1)] = 1
        invert_still_vs_mvt = 1 - still_vs_mvt
        still_periods = get_continous_time_periods(invert_still_vs_mvt)
        gap_to_fill = 1
        # feeling the gap of 1 frame without mvt
        for still_period in still_periods:
            if (still_period[1] - still_period[0] + 1) <= gap_to_fill:
                still_vs_mvt[still_period[0]:still_period[1] + 1] = 1

        still_vs_mvt_dict[key_bodypart] = still_vs_mvt

    # now we want to identify startle and complex_mvt
    # we create dictionnaries that contains each part with tuple representing start and end of movement.
    # we will remove those that have been identified as part of a startle or complex_mvt
    # key is the bodyaprt, then dict with id for the period, and tuple of int representing the period
    periods_id_by_bodypart_dict = dict()
    # periods_array_with_id
    # key is bodypart, value is an array of n_frames with value of each the id of the period, starting from 1
    periods_array_with_id_dict = dict()
    # list with an unique id all periods (bodypart family, first_frame, last_frame)
    all_periods = set()

    # ranking period according to their duration, behavior is recording at 20 Hz
    # 1000 ms / 50 ms
    twitch_duration_threshold = 20
    # startle_threshold = 24

    for key_bodypart, still_vs_mvt in still_vs_mvt_dict.items():
        periods = get_continous_time_periods(still_vs_mvt)
        periods_id_by_bodypart_dict[key_bodypart] = dict()
        periods_array_with_id = np.zeros(n_frames, dtype="int16")
        for period_index, period in enumerate(periods):
            periods_array_with_id[period[0]:period[1] + 1] = period_index + 1
            periods_id_by_bodypart_dict[key_bodypart][period_index + 1] = period
            all_periods.add((key_bodypart, period[0], period[1]))
            # print(f"all_periods.add {(key_bodypart, period[0], period[1])}")
        periods_array_with_id_dict[key_bodypart] = periods_array_with_id

    # now we want to explore all periods in periods_id_by_bodypart_dict to check which ones should be associated
    # to startle or complex mvt
    while len(all_periods) > 0:
        # get period id and remove it from the set in the same time
        period_id = all_periods.pop()
        key_bodypart = period_id[0]
        first_frame = period_id[1]
        last_frame = period_id[2]
        mvt_duration = last_frame - first_frame + 1
        # we want at least 3 frames (150 ms) to consider it as mvt
        if mvt_duration <= 3:
            continue
        npz_key_bodypart = key_bodypart
        if npz_key_bodypart != "tail":
            npz_key_bodypart = npz_key_bodypart + "_left"
        # we get the names of other bodyparts to explore
        bodyparts_names = list(bodyparts_triplets.keys())
        bodyparts_names.remove(key_bodypart)
        # KeyError: ('hindlimb', 22245, 22300)
        # key is id (bodypart, first_frame, last_frame) and value is the duration
        other_mvts_dict = dict()
        # complex_mvt or startle are defined as if all or all - 1 bodypart are active in the same time
        for bodypart_to_explore in bodyparts_names:
            periods_array_with_id = periods_array_with_id_dict[bodypart_to_explore]
            # we look if a concomittent mvt happened
            if np.sum(periods_array_with_id[first_frame:last_frame + 1]) > 0:
                # another mvt happened in the same time
                period_ids = list(np.unique(periods_array_with_id[first_frame:last_frame + 1]))
                if 0 in period_ids:
                    period_ids.remove(0)
                if len(period_ids) > 1:
                    # we keep the one with the most frames
                    max_n_frames = 0
                    period_id = None
                    for i in period_ids:
                        frames_count = len(np.where(periods_array_with_id[first_frame:last_frame + 1] == i)[0])
                        if frames_count > max_n_frames:
                            period_id = i
                            max_n_frames = frames_count
                else:
                    period_id = period_ids[0]
                period = periods_id_by_bodypart_dict[bodypart_to_explore][period_id]
                other_mvts_dict[(bodypart_to_explore, period[0], period[1])] = period[1] - period[0] + 1
        # now let's count how many other part are moving in the same time
        n_moving_bodyparts = len(other_mvts_dict)
        if (n_moving_bodyparts >= len(bodyparts_triplets) - 1) or (
                n_moving_bodyparts > 0 and np.max(list(other_mvts_dict.values())) > 40):
            # then we are in the category startle or complex_mvt
            # if one of the other mvt part has a long mvt, then we rank it complex_mvt
            # complex mvt here is defined as more than 2 sec
            # we take the first frame of all mvts, and the last last_frame of all
            first_first_frame = first_frame
            last_last_frame = last_frame
            for key_other_mvt in other_mvts_dict.keys():
                if key_other_mvt[1] < first_first_frame:
                    first_first_frame = key_other_mvt[1]
                if key_other_mvt[2] > last_last_frame:
                    last_last_frame = key_other_mvt[2]
                # we remove other mvt from the set meanwhile
                if key_other_mvt in all_periods:
                    all_periods.remove(key_other_mvt)

            if np.max(list(other_mvts_dict.values())) > twitch_duration_threshold:
                # using array, we can extend previous complet_mvt period
                periods_by_type_of_mvt["complex_mvt"][first_first_frame:last_last_frame + 1] = 1
            else:
                periods_by_type_of_mvt["startle"][first_first_frame:last_last_frame + 1] = 1
        else:
            # we are in the category twitch or mvt of one body part
            if mvt_duration <= twitch_duration_threshold:
                # we classify it as a twitch
                periods_by_type_of_mvt[f"twitch_{npz_key_bodypart}"][first_frame:last_frame + 1] = 1
            else:
                # else a mvt
                periods_by_type_of_mvt[f"mvt_{npz_key_bodypart}"][first_frame:last_frame + 1] = 1
    # TODO: See how to fusion other mvt with complex_mvt after that

    for key_behavior, binary_array in periods_by_type_of_mvt.items():
        periods = get_continous_time_periods(binary_array)
        behaviors_encoding_dict[key_behavior] = encode_period_with_timestamps(periods=periods,
                                                                              timestamps=behavior_time_stamps)
    if gt_behavior is not None:
        evaluate_behavior_predictions(ground_truth_labels=gt_behavior, other_labels=behaviors_encoding_dict,
                                      n_frames=n_frames, behavior_timestamps=behavior_time_stamps)

    np.savez(os.path.join(results_path, "test.npz"), **behaviors_encoding_dict)

    return distance_matrix


def dlc_behavior_analysis():
    session_to_analyse = "p6"  # "p5" p7

    if session_to_analyse == "p7":
        root_path = "/media/julien/Not_today/hne_not_today/data/behavior_movies/dlc_predictions/p7_200103_200110_200110_a000_2020_02"
        data_path = os.path.join(root_path, "data")

        pos_left_file_name = "behavior_p7_20_01_10_cam_23109588_cam2_a000_fps_20DLC_resnet50_test_valentinFeb17shuffle1_440000.h5"
        skeketon_left_file_name = "behavior_p7_20_01_10_cam_23109588_cam2_a000_fps_20DLC_resnet50_test_valentinFeb17shuffle1_440000_skeleton.h5"

        pos_right_file_name = "behavior_p7_20_01_10_cam_22983298_cam1_a000_fps_20DLC_resnet50_test_valentinFeb17shuffle1_440000.h5"
        skeleton_right_file_name = "behavior_p7_20_01_10_cam_22983298_cam1_a000_fps_20DLC_resnet50_test_valentinFeb17shuffle1_440000_skeleton.h5"

        cicada_file = os.path.join(data_path, "p7_200103_200110_200110_a000_2020_02_behavior_manual_labeling_RD.npz")
        nwb_file = os.path.join(data_path, "p7_200103_200110_200110_a000_2020_02_17.14-05-47.nwb")

    elif session_to_analyse == "p5":

        root_path = "/media/julien/Not_today/hne_not_today/data/behavior_movies/dlc_predictions/p5_19_12_10_0"
        # root_path = "/Users/pappyhammer/Documents/academique/these_inmed/robin_michel_data/data/behavior_movies/dlc_predictions/p5_19_12_10_0"

        data_path = os.path.join(root_path, "data")

        pos_left_file_name = "behavior_p5_19_12_10_0_cam_23109588_cam2_a001_fps_20DLC_resnet50_test_valentinFeb17shuffle1_155000.h5"
        skeketon_left_file_name = "behavior_p5_19_12_10_0_cam_23109588_cam2_a001_fps_20DLC_resnet50_test_valentinFeb17shuffle1_155000_skeleton.h5"

        pos_right_file_name = "behavior_p5_19_12_10_0_cam_22983298_cam1_a001_fps_20DLC_resnet50_test_valentinFeb17shuffle1_220000.h5"
        skeleton_right_file_name = "behavior_p5_19_12_10_0_cam_22983298_cam1_a001_fps_20DLC_resnet50_test_valentinFeb17shuffle1_220000_skeleton.h5"

        cicada_file = os.path.join(data_path, "p5_behavior_mannual_labbelling_final_version.npz")
        nwb_file = os.path.join(data_path, "p5_191205_191210_0_191210_a001_2020_02_17.14-06-07.nwb")
    elif session_to_analyse == "p6":

        root_path = "/media/julien/Not_today/hne_not_today/data/behavior_movies/dlc_predictions/p6_19_09_27_1_a000"
        # root_path = "/Users/pappyhammer/Documents/academique/these_inmed/robin_michel_data/data/behavior_movies/dlc_predictions/p5_19_12_10_0"

        data_path = os.path.join(root_path, "data")

        pos_left_file_name = "behavior_p6_19_09_27_1_cam_23109588_cam2_a000_fps_20DLC_resnet50_test_valentinFeb17shuffle1_440000.h5"
        skeketon_left_file_name = "behavior_p6_19_09_27_1_cam_23109588_cam2_a000_fps_20DLC_resnet50_test_valentinFeb17shuffle1_440000_skeleton.h5"

        pos_right_file_name = "behavior_p6_19_09_27_1_cam_22983298_cam1_a000_fps_20DLC_resnet50_test_valentinFeb17shuffle1_440000.h5"
        skeleton_right_file_name = "behavior_p6_19_09_27_1_cam_22983298_cam1_a000_fps_20DLC_resnet50_test_valentinFeb17shuffle1_440000_skeleton.h5"

        cicada_file = os.path.join(data_path, "model_tags_behavior.npz")
        nwb_file = os.path.join(data_path, "p6_190921_190927_1_190927_a000_2020_03_07.17-08-49.nwb")
    else:
        raise Exception("Session unknown")

    results_path = os.path.join(root_path, "results")

    dlc_analysis = DlcAnalysis(data_path, results_path, session_to_analyse, pos_left_file_name, skeketon_left_file_name,
                               pos_right_file_name, skeleton_right_file_name, cicada_file, nwb_file)

    raise Exception("TEST")

    using_h5 = True

    if using_h5:
        try_basic_solution = False

        pos_left_file_name = "behavior_p5_19_12_10_0_cam_23109588_cam2_a001_fps_20DLC_resnet50_test_valentinFeb17shuffle1_155000.h5"
        skeketon_left_file_name = "behavior_p5_19_12_10_0_cam_23109588_cam2_a001_fps_20DLC_resnet50_test_valentinFeb17shuffle1_155000_skeleton.h5"

        pos_right_file_name = "behavior_p5_19_12_10_0_cam_22983298_cam1_a001_fps_20DLC_resnet50_test_valentinFeb17shuffle1_220000.h5"
        skeketon_right_file_name = "behavior_p5_19_12_10_0_cam_22983298_cam1_a001_fps_20DLC_resnet50_test_valentinFeb17shuffle1_220000_skeleton.h5"

        n_frames, bodyparts, body_parts_pos_array, skeleton_parts, skeleton_parts_pos_array, left_cam_id = \
            get_data_from_dlc_h5_files(data_path, pos_file_name=pos_left_file_name,
                                       skeketon_file_name=skeketon_left_file_name,
                                       replace_by_nan=False)
        print(f"n_frames {n_frames}")
        #
        n_frames_right, bodyparts_right, body_parts_pos_array_right, skeleton_parts_right, \
        skeleton_parts_pos_array_right, right_cam_id = \
            get_data_from_dlc_h5_files(data_path, pos_file_name=pos_right_file_name,
                                       skeketon_file_name=skeketon_right_file_name,
                                       replace_by_nan=False)

        n_skeleton_parts = len(skeleton_parts_pos_array)
        n_bodyparts = len(body_parts_pos_array)

        behavior_by_frame_left = None
        use_cicada_file = True
        if use_cicada_file:
            behavior_by_frame_left, behavior_left_time_stamps, gt_behavior_left = encode_frames_from_cicada(
                cicada_file=cicada_file,
                nwb_file=nwb_file,
                cam_id=left_cam_id, n_frames=n_frames,
                side_to_exclude="right",
                no_behavior_str="still")

            behavior_by_frame_right, behavior_right_time_stamps, gt_behavior_right = encode_frames_from_cicada(
                cicada_file=cicada_file,
                nwb_file=nwb_file,
                cam_id=right_cam_id, n_frames=n_frames_right,
                side_to_exclude="left",
                no_behavior_str="still")
            # print(f'behavior_by_frame_left {behavior_by_frame_left}')

        if try_basic_solution:
            bas_dlco(data_path=data_path, dlc_pos_file_left=pos_left_file_name, dlc_pos_file_right=pos_right_file_name,
                     behavior_left_time_stamps=behavior_left_time_stamps,
                     behavior_right_time_stamps=behavior_right_time_stamps)
            raise Exception("BAS test")
            distance_matrix = basic_solution(n_frames, bodyparts, body_parts_pos_array, skeleton_parts,
                                             skeleton_parts_pos_array,
                                             results_path, behavior_left_time_stamps, gt_behavior=gt_behavior_left)
            # data_to_cluster = np.zeros((n_frames, (n_bodyparts + n_skeleton_parts * 1)))
            # data_to_cluster[:, :n_bodyparts] = distance_matrix.transpose()
            # data_to_cluster[:, n_bodyparts:n_bodyparts + n_skeleton_parts] = skeleton_parts_pos_array[:, 0, :].transpose()
            # # data_to_cluster[:, n_bodyparts * 2:(n_bodyparts * 2 + n_skeleton_parts)] = \
            # #     skeleton_parts_pos_array[:, 0, :].transpose()
            # # data_to_cluster[:, (n_bodyparts * 2 + n_skeleton_parts):(n_bodyparts * 2 + n_skeleton_parts * 2)] = \
            # #     skeleton_parts_pos_array[:, 1, :].transpose()
            # apply_tsne(data=data_to_cluster, behavior_by_frame_left=behavior_by_frame_left)
            raise Exception("BASIC SOLUTION")

        try_wavelet = False
        if try_wavelet:
            n_components = 10
            data_to_cluster = np.zeros((n_frames, (n_bodyparts * n_components + n_skeleton_parts * 2 * n_components)))
            # data_to_cluster = np.zeros((n_frames, (n_bodyparts * 2 * n_components)))
            index_data_to_cluster = 0
            part_categories = ["bodyparts", "skeleton_parts"]
            # part_categories = ["bodyparts"]
            for part_categorie in part_categories:
                # Filling with nan for now
                print(f"# Wavelet {part_categorie}")
                # TODO: Replace bodypart by the distance between each
                if part_categorie == "bodyparts":
                    n_parts = n_bodyparts
                    # parts_pos_array = body_parts_pos_array
                    parts_pos_array = euclidean_distance_for_bodyparts(body_parts_pos_array)
                    labels = bodyparts
                else:
                    n_parts = n_skeleton_parts
                    parts_pos_array = skeleton_parts_pos_array
                    labels = skeleton_parts
                for part_index in np.arange(n_parts):
                    # data_index represents the index of x, y or orientation, length in the matrix
                    for data_index in [0, 1]:
                        if data_index == 1 and len(parts_pos_array.shape) == 2:
                            continue
                        if len(parts_pos_array.shape) == 2:
                            values = parts_pos_array[part_index, :]
                        else:
                            values = parts_pos_array[part_index, data_index, :]
                        # widths = np.arange(0.3, 5)
                        fs = 20
                        freq = np.linspace(0.1, fs / 2, 375)
                        w = 20.
                        widths = w * fs / (2 * freq * np.pi)
                        # signal.ricker
                        cwtm = np.abs(scipy.signal.cwt(data=values, wavelet=scipy.signal.ricker, widths=widths))
                        # cwtm = np.abs(scipy.signal.cwt(data=values, wavelet=scipy.signal.morlet2, widths=widths))
                        # print(f"cwtm.shape {cwtm.shape}")
                        t = np.arange(n_frames)
                        plot_it = False
                        if plot_it:
                            plt.pcolormesh(t, freq, cwtm, cmap='viridis')
                            plt.title(labels[part_index])
                            plt.show()

                        pca = PCA(n_components=n_components)
                        pca.fit(cwtm)
                        # print(f"pca.explained_variance_ratio_ {pca.explained_variance_ratio_}")
                        # print(f"components_ {pca.components_.shape}")
                        data_to_cluster[:,
                        index_data_to_cluster * n_components:(index_data_to_cluster + 1) * n_components] = \
                            pca.components_.transpose()
                        index_data_to_cluster += 1
                print(f"data_to_cluster.shape {data_to_cluster.shape}")
                pca = PCA(n_components=30)
                pca.fit(data_to_cluster.transpose())
                data_to_cluster = pca.components_.transpose()
                print(f"data_to_cluster.shape 2nd {data_to_cluster.shape}")
                apply_tsne(data=data_to_cluster, behavior_by_frame=behavior_by_frame_left)
                raise Exception("End Wavelet")
        # apply_tsne(data=skeleton_parts_pos_array[:, 0:2, :])
        # print(f"body_parts_pos_array[:, 1, :] {body_parts_pos_array[:, 1, :].shape}")
        distance_version = True
        if distance_version:
            parts_pos_array = euclidean_distance_for_bodyparts(body_parts_pos_array)
            data_to_cluster = np.zeros((n_frames, (n_bodyparts * 1 + n_skeleton_parts * 2)))
            data_to_cluster[:, :n_bodyparts] = parts_pos_array.transpose()
            # data_to_cluster[:, n_bodyparts:n_bodyparts * 2] = body_parts_pos_array[:, 1, :].transpose()
            data_to_cluster[:, n_bodyparts:(n_bodyparts + n_skeleton_parts)] = \
                skeleton_parts_pos_array[:, 0, :].transpose()
            data_to_cluster[:, (n_bodyparts + n_skeleton_parts):(n_bodyparts + n_skeleton_parts * 2)] = \
                skeleton_parts_pos_array[:, 1, :].transpose()
            print(f"data_to_cluster.shape {data_to_cluster.shape}")
        else:
            data_to_cluster = np.zeros((n_frames, (n_bodyparts * 2 + n_skeleton_parts * 2)))
            data_to_cluster[:, :n_bodyparts] = body_parts_pos_array[:, 0, :].transpose()
            data_to_cluster[:, n_bodyparts:n_bodyparts * 2] = body_parts_pos_array[:, 1, :].transpose()
            data_to_cluster[:, n_bodyparts * 2:(n_bodyparts * 2 + n_skeleton_parts)] = \
                skeleton_parts_pos_array[:, 0, :].transpose()
            data_to_cluster[:, (n_bodyparts * 2 + n_skeleton_parts):(n_bodyparts * 2 + n_skeleton_parts * 2)] = \
                skeleton_parts_pos_array[:, 1, :].transpose()
            print(f"data_to_cluster.shape {data_to_cluster.shape}")

        b_soid_file = os.path.join(data_path, "TSNE.mat")
        use_b_soid = False
        if use_b_soid:
            load_t_sne_from_b_soid(b_soid_file, n_frames=n_frames, behavior_by_frame=behavior_by_frame_left)
        else:
            apply_tsne(data=data_to_cluster, behavior_by_frame=behavior_by_frame_left)

        raise Exception("H5 OVER")

    pos_file_name = "behavior_p5_19_12_10_0_cam_23109588_cam2_a001_fps_20DLC_resnet50_test_valentinFeb17shuffle1_155000.csv"
    skeketon_file_name = "behavior_p5_19_12_10_0_cam_23109588_cam2_a001_fps_20DLC_resnet50_test_valentinFeb17shuffle1_155000_skeleton.csv"

    pos_df = pd.read_csv(os.path.join(data_path, pos_file_name), low_memory=False)
    skeleton_df = pd.read_csv(os.path.join(data_path, skeketon_file_name), low_memory=False)

    # Preview the first 5 lines of the loaded data
    print(f"pos_df.head() {pos_df.head()}")
    print(f"skeleton_df.head() {skeleton_df.head()}")


if __name__ == "__main__":
    dlc_behavior_analysis()
