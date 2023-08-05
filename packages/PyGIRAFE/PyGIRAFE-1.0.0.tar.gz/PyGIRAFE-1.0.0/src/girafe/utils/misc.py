import numpy as np
import math


def split_string(string_to_split, separator=" "):
    """
    Call the split() function. Useful for cicada analyses to avoid issue when saved in yaml
    instead of using lambda and split()
    Args:
        string_to_split:
        separator:

    Returns:

    """
    return string_to_split.split(separator)

def find_nearest(array, value, is_sorted=True):
    """
    Return the index of the nearest content in array of value.
    from https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
    return -1 or len(array) if the value is out of range for sorted array
    Args:
        array:
        value:
        is_sorted:

    Returns:

    """
    if len(array) == 0:
        return -1

    if is_sorted:
        if value < array[0]:
            return -1
        elif value > array[-1]:
            return len(array)
        idx = np.searchsorted(array, value, side="left")
        if idx > 0 and (idx == len(array) or math.fabs(value - array[idx - 1]) < math.fabs(value - array[idx])):
            return idx - 1
        else:
            return idx
    else:
        array = np.asarray(array)
        idx = (np.abs(array - value)).idxmin()
        return idx


def validate_indices_in_string_format(str_indices):
    """
    Take a string representing a serie of indices (int) and make sure the format is correct,
    the string then could be used as an argument of extract_indices_from_string()
    There should be only '-' and numbers
    Ex: "1-3 5 10-20-30 6" is in a correct format
    "1 - 5 20.6 toto" is not correct
    Args:
        str_indices: (str)

    Returns: either False or a string indicating why is it False, if the format is correct return True

    """

    if not isinstance(str_indices, str):
        return "Not a string"

    str_indices = str_indices.strip()

    if len(str_indices) == 0:
        return "Empty string"

    # we check them one by one
    n_char = len(str_indices)
    str_indices_split = str_indices.split()
    for str_indice in str_indices_split:
        if str_indice.count("-") > 1:
            return "There shouldn't be more than one '-'"
        for index, character in enumerate(str_indice):
            if character == "-":
                # then we check around if it's a number
                if index > 0:
                    if not str_indice[index-1].isnumeric():
                        return "- should be surrounding by numbers"
                else:
                    return "- can't be the first character"
                if index < n_char -1:
                    if not str_indice[index + 1].isnumeric():
                        return "- should be surrounding by numbers"
                else:
                    return "- can't be the last character"
            elif not character.isnumeric():
                return f"{character} is not an authorised character"

    return True


def extract_indices_from_string(str_indices):
    """
    Take a string representing a serie of indices (int) and return a list of those integers
    There should be only '-' and numbers
    Ex: if str_indices is "1-3 25 6" it returns [1, 2, 3, 25, 6]
    If the format is incorrect, it returns an empty list
    Args:
        str_indices: (str)

    Returns:

    """
    validation = validate_indices_in_string_format(str_indices)
    if isinstance(validation, str) or not validation:
        return []

    indices_list = []

    n_char = len(str_indices)
    str_indices_split = str_indices.split()
    for str_indice in str_indices_split:
        if str_indice.count("-") > 0:
            interval_split = str_indice.split("-")
            indices_list.extend(range(int(interval_split[0]), int(interval_split[1])+1))
        else:
            indices_list.append(int(str_indice))

    return indices_list


def get_continous_time_periods(binary_array):
    """
    take a binary array and return a list of tuples representing the first and last position(included) of continuous
    positive period
    This code was copied from another project or from a forum, but i've lost the reference.
    :param binary_array:
    :return:
    """
    binary_array = np.copy(binary_array).astype("int8")
    # first we make sure it's binary
    if np.max(binary_array) > 1:
        binary_array[binary_array > 1] = 1
    if np.min(binary_array) < 0:
        binary_array[binary_array < 0] = 0
    n_times = len(binary_array)
    d_times = np.diff(binary_array)
    # show the +1 and -1 edges
    pos = np.where(d_times == 1)[0] + 1
    neg = np.where(d_times == -1)[0] + 1

    if (pos.size == 0) and (neg.size == 0):
        if len(np.nonzero(binary_array)[0]) > 0:
            return [(0, n_times-1)]
        else:
            return []
    elif pos.size == 0:
        # i.e., starts on an spike, then stops
        return [(0, neg[0])]
    elif neg.size == 0:
        # starts, then ends on a spike.
        return [(pos[0], n_times-1)]
    else:
        if pos[0] > neg[0]:
            # we start with a spike
            pos = np.insert(pos, 0, 0)
        if neg[-1] < pos[-1]:
            #  we end with aspike
            neg = np.append(neg, n_times - 1)
        # NOTE: by this time, length(pos)==length(neg), necessarily
        # h = np.matrix([pos, neg])
        h = np.zeros((2, len(pos)), dtype="int16")
        h[0] = pos
        h[1] = neg
        if np.any(h):
            result = []
            for i in np.arange(h.shape[1]):
                if h[1, i] == n_times-1:
                    result.append((h[0, i], h[1, i]))
                else:
                    result.append((h[0, i], h[1, i]-1))
            return result
    return []


def give_unique_id_to_each_transient_of_raster_dur(raster_dur):
    """
    we create a spike_nums_dur but not binary, for a given cell each transient will have an id (int)
    unique from other transients of this cell
    :param raster_dur: 2-D binary array (should not be uint, but int)
    :return:
    """

    #
    spike_nums_dur_numbers = np.ones(raster_dur.shape, dtype="int16")
    # -1 means no transient
    spike_nums_dur_numbers *= -1
    for cell in np.arange(raster_dur.shape[0]):
        # first we want to identify each transient
        periods = get_continous_time_periods(raster_dur[cell])
        for period_index, period in enumerate(periods):
            spike_nums_dur_numbers[cell, period[0]:period[1] + 1] = period_index
    return spike_nums_dur_numbers


def get_tree_dict_as_a_list(tree_dict):
    """
    Take a dict that contains as value only other dicts or list of simple types value sor a simple type value
    and return a list of list of all keys with last data at the end
    Args:
        tree_dict:

    Returns:

    """
    tree_as_list = []
    for key, sub_tree in tree_dict.items():
        # branch_list = [key]
        # tree_as_list.append(branch_list)
        if isinstance(sub_tree, dict):
            branches = get_tree_dict_as_a_list(tree_dict=sub_tree)
            tree_as_list.extend([[key] + branch for branch in branches])
        elif isinstance(sub_tree, list):
            # means we reached a leaves
            for leaf in sub_tree:
                tree_as_list.append([key, leaf])
        else:
            # means we reached a leaf
            leaf = sub_tree
            tree_as_list.append([key, leaf])
    return tree_as_list


def from_timestamps_array_to_list(time_stamps_array, frames_timestamps):
    """

    Args:
        time_stamps_array: 2d array (2, n_points)
        frames_timestamps: 1d array of float of length n_frames, containing the timestamps of the frames,
        used to keep only the epochs in this range

    Returns: a list of tuples of 2 float, or a 2d of (2, n_frames) dimensions

    """
    first_frame_ts = frames_timestamps[0]
    last_frame_ts = frames_timestamps[-1]

    intervals_list = []

    for index_ts in range(time_stamps_array.shape[1]):
        first_ts = time_stamps_array[0, index_ts]
        last_ts = time_stamps_array[1, index_ts]

        # keeping only the one in range of the frame timestamps
        if (first_ts < first_frame_ts) or (last_ts < first_frame_ts):
            continue

        if last_ts > last_frame_ts:
            continue

        intervals_list.append((first_ts, last_ts))

    return intervals_list


def from_timestamps_to_frame_epochs(time_stamps_array, frames_timestamps, as_list):
    """

    Args:
        time_stamps_array: 2d array (2, n_points)
        frames_timestamps: 1d array of float of length n_frames, containing the timestamps of the frames
        as_list: if True, return a list of tuples of 2 int, or a 2d of (2, n_frames) dimensions

    Returns:

    """
    first_frame_ts = frames_timestamps[0]
    last_frame_ts = frames_timestamps[-1]

    intervals_list = []

    for index_ts in range(time_stamps_array.shape[1]):
        first_ts = time_stamps_array[0, index_ts]
        last_ts = time_stamps_array[1, index_ts]

        # keeping only the one in range of the frame timestamps
        if (first_ts < first_frame_ts) or (last_ts < first_frame_ts):
            continue

        if last_ts > last_frame_ts:
            continue

        first_frame = find_nearest(frames_timestamps, value=first_ts)
        last_frame = find_nearest(frames_timestamps, value=last_ts)
        intervals_list.append((first_frame, last_frame))

    if as_list:
        return intervals_list

    result = np.zeros((2, len(intervals_list)), dtype="int64")
    for interval_index in range(len(intervals_list)):
        result[0, interval_index] = intervals_list[interval_index][0]
        result[1, interval_index] = intervals_list[interval_index][1]

    return result


def get_stability_among_cell_assemblies(assemblies_1, assemblies_2, divide_by_total_of_both=True):
    """

    Args:
        assemblies_1: list of list of int reprensenting the index of a cell
        assemblies_2:
        divide_by_total_of_both: if True, we divide the number of cell in common by the total amount
        of different cells represented by the two assemblies that has been compared, otherwise we divide it
        just by the number of cell in assembly_1

    Returns: list of the same size as assembly_1, of integers representing the percentage of cells in each
    assembly that are part of a same assembly in assemblies_2

    """

    perc_list = list()
    for ass_1 in assemblies_1:
        if len(ass_1) == 0:
            continue
        max_perc = 0
        for ass_2 in assemblies_2:
            # easiest way would be to use set() and intersection, but as 2 channels could have the same name
            # we want to have 2 instances different, even so we won't know for sure if that's the same
            n_in_common = len(list(set(ass_1).intersection(ass_2)))
            all_cells = []
            all_cells.extend(ass_1)
            all_cells.extend(ass_2)
            n_different_channels = len(set(all_cells))
            #
            if divide_by_total_of_both:
                perc = (n_in_common / n_different_channels) * 100
            else:
                perc = (n_in_common / len(ass_1)) * 100
            max_perc = max(max_perc, perc)
        perc_list.append(max_perc)

    return perc_list


def bin_raster(raster, bin_size, keep_same_dimension=True):
    """
     Bin a raster over the frames, keeping the same number of frames (filling by 1 all frames bined) or
     reducing the number of frames
    :param raster: éd array
    :param bin_size:
    :param keep_same_dimension:
    :return:
    """
    # first we check if n_frames is divisible by bin_size
    n_frames = raster.shape[1]
    if (keep_same_dimension is False) and (n_frames % bin_size != 0):
        print(f"bin_size {bin_size} is not compatible with {n_frames} frames")
        return
    if keep_same_dimension:
        bin_raster = np.zeros(raster.shape, dtype="int8")
        for beg_index in np.arange(0, raster.shape[1], bin_size):
            end_index = min(raster.shape[1], beg_index + bin_size)
            for cell in np.arange(raster.shape[0]):
                if np.sum(raster[cell, beg_index:end_index]) > 0:
                    bin_raster[cell, beg_index:end_index] = 1
        return bin_raster

    bin_raster = np.zeros((raster.shape[0], raster.shape[1] // bin_size), dtype="int8")
    for cell in np.arange(raster.shape[0]):
        cell_raster = np.sum(np.reshape(raster[cell], (raster.shape[1] // bin_size, bin_size)), axis=1)
        bin_raster[cell] = cell_raster
    return bin_raster


def get_yang_frames(total_frames=12500, yin_frames=None):
    """
    :param total_frames: total number of frames
    :param yin_frames: a list of tuples with start and end of yin frame periods
    :return: bool_yang_frames: True if Yang, False if Yin
    """
    # Boolean variable yang frames to output
    bool_yang_frames = np.ones((total_frames, ), dtype=bool)

    # Count active periods in yin frames
    n_active_periods = len(yin_frames)

    # Loop on this period to turn them to false in yang frames
    for active_period in range(n_active_periods):
        start_period = yin_frames[active_period][0]
        end_period = yin_frames[active_period][1]
        frame_to_not_take = np.arange(start_period, end_period + 1)
        bool_yang_frames[frame_to_not_take] = False

    yang_frames_list = np.where(bool_yang_frames)[0]

    return bool_yang_frames, yang_frames_list


def fill_gaps_in_continuous_periods(boolean_serie, max_gap_size):
    """

    :param boolean_serie:
    :param max_gap_size:
    :return:
    """
    filled_boolean_serie = boolean_serie
    continuous_periods = get_continous_time_periods(boolean_serie)
    n_epochs = len(continuous_periods)
    if n_epochs == 0:
        print(f"No continuous time periods found, return unchanged serie")
        return boolean_serie

    for epoch in np.arange(1, n_epochs):
        epoch_start = continuous_periods[epoch][0]
        previous_epoch_stop = continuous_periods[epoch - 1][1]
        gap_size = epoch_start - previous_epoch_stop
        if gap_size <= max_gap_size:
            filled_boolean_serie[previous_epoch_stop: epoch_start] = True

    return filled_boolean_serie


def print_info_dict(my_dict):
    for key, data in my_dict.items():
        print(f"- {key}: {data}")
