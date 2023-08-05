import numpy as np
from scipy import signal, stats


def get_sce_threshold(rasterdur, n_surrogates=100, percentile=95, verbose=False):
    [n_cells, n_frames] = rasterdur.shape
    if verbose:
        print(f"Starting to obtain the {n_surrogates} rolled rasters")
    rnd_rasters = np.zeros((n_cells, n_frames, n_surrogates))
    for surrogate in range(n_surrogates):
        for cell in range(n_cells):
            rnd_rasters[cell, :, surrogate] = np.roll(rasterdur[cell, :], np.random.randint(1, n_frames))

    rnd_sum_cells = np.sum(rnd_rasters, axis=0)

    n_values = n_frames * n_surrogates

    rnd_sum_cells_vector = np.reshape(rnd_sum_cells, (n_values,))

    cell_threshold = np.percentile(rnd_sum_cells_vector, percentile)

    if verbose:
        print(f"Threshold obtain for SCE detection with {percentile} percentile: {cell_threshold} cells, "
              f"representing {np.round((cell_threshold / n_cells) * 100, decimals=1)} % of the detected cells")

    return rnd_rasters, cell_threshold


def detect_sce_on_traces(raw_traces, speed=None, use_speed=False, speed_threshold=None, sce_n_cells_threshold=5,
                         sce_min_distance=4, n_synchronous_frames=2, use_median_norm=True, use_bleaching_correction=False,
                         use_savitzky_golay_filt=True):

    traces = np.copy(raw_traces)
    if speed is None:
        use_speed = False

    if use_speed is True:
        if speed_threshold is None:
            speed_threshold = 1  # define below which instantaneous speed (cm/s) we consider mice in rest period
        else:
            pass
        print(f"{len(np.where(speed <= speed_threshold)[0])} frames with speed below speed threshold "
              f"({speed_threshold} cm/s)")

    if use_speed is False:
        if speed_threshold is not None:
            print(f"Speed threshold is useless if speed is not used")
        else:
            pass

    if use_median_norm is True:
        median_normalization(traces)

    if use_bleaching_correction is True:
        bleaching_correction(traces)

    if use_savitzky_golay_filt is True:
        savitzky_golay_filt(traces)

    print(f"Traces normalization done with n traces: {len(traces)}")

    # Detect small transients
    n_cells, n_frames = traces.shape
    window_size = 40  # size in frames of the sliding window to detect transients
    activity_tmp_all_cells = [[] for i in range(n_cells)]

    if use_speed is True:
        print(f"Starting detection of small transients using speed threshold")
        for i in range(n_cells):
            if i == np.round(n_cells/4):
                print("Done for 25% of the cells")
            if i == np.round(n_cells/2):
                print("Done for 50% of the cells")
            if i == np.round(3 * n_cells / 4):
                print("Done for 75% of the cells")
            activity_tmp = np.zeros(n_frames)
            trace_tmp = traces[i, :]
            burst_threshold = np.median(trace_tmp) + stats.iqr(trace_tmp) / 2
            for k in range(window_size + 1, n_frames - window_size):
                if speed[k] < speed_threshold:
                    window_tmp = np.arange(k - window_size, k + window_size)
                    median_tmp = np.median(trace_tmp[window_tmp])
                    if np.sum(activity_tmp[k - 10:k - 1]) == 0 and median_tmp < burst_threshold:
                        activity_tmp[k] = (trace_tmp[k] - median_tmp) > (3 * stats.iqr(trace_tmp[window_tmp]))
            activity_tmp_all_cells[i] = np.where(activity_tmp)[0]

    if use_speed is False:
        print(f"Starting detection without speed threshold")
        for i in range(n_cells):
            if i == np.round(n_cells / 4):
                print("Done for 25% of the cells")
            if i == np.round(n_cells / 2):
                print("Done for 50% of the cells")
            if i == np.round(3 * n_cells / 4):
                print("Done for 75% of the cells")
            activity_tmp = np.zeros(n_frames)
            trace_tmp = traces[i, :]
            burst_threshold = np.median(trace_tmp) + stats.iqr(trace_tmp) / 2
            for k in np.arange(window_size + 1, n_frames - window_size, 5):
                window_tmp = np.arange(k - window_size, k + window_size)
                median_tmp = np.median(trace_tmp[window_tmp])
                if np.sum(activity_tmp[k - 10:k - 1]) == 0 and median_tmp < burst_threshold:
                    activity_tmp[k] = (trace_tmp[k] - median_tmp) > (3 * stats.iqr(trace_tmp[window_tmp]))
            activity_tmp_all_cells[i] = np.where(activity_tmp)[0]
            # print(f" cell #{i} has {len(activity_tmp_all_cells[i])} small activation")

    print(f"Small transients detection is done")

    raster = np.zeros((n_cells, n_frames))
    for i in range(n_cells):
        raster[i, activity_tmp_all_cells[i]] = 1

    print(f"Raster is obtained")

    # sum activity over n consecutive frames
    sum_activity = np.zeros(n_frames - n_synchronous_frames)
    print(f"Sum activity over {n_synchronous_frames} consecutive CI frames")
    for i in range(n_frames - n_synchronous_frames):
        sum_activity[i] = np.sum(np.amax(raster[:, np.arange(i, i + n_synchronous_frames)], axis=1))

    print(f"Sum activity is obtained with max is {np.max(sum_activity)}")

    # select synchronous calcium events
    sce_loc = signal.find_peaks(sum_activity, height=sce_n_cells_threshold, distance=sce_min_distance)[0]
    n_sce = len(sce_loc)

    print(f"SCE are detected with {n_sce} SCEs ")

    # create cells vs sce matrix
    sce_cells_matrix = np.zeros((n_cells, n_sce))
    for i in range(n_sce):
        sce_cells_matrix[:, i] = np.amax(raster[:, np.arange(np.max((sce_loc[i]-1, 0)),
                                                             np.min((sce_loc[i]+2, n_frames)))], axis=1)

    return sce_cells_matrix, sce_loc, raster


def median_normalization(traces):
    n_cells, n_frames = traces.shape
    for i in range(n_cells):
        traces[i, :] = traces[i, :] / np.median(traces[i, :])
    return traces


def bleaching_correction(traces):
    n_cells, n_frames = traces.shape
    for k in range(n_cells):
        p0 = np.polyfit(np.arange(n_frames), traces[k, :], 3)
        traces[k, :] = traces[k, :] / np.polyval(p0, np.arange(n_frames))
    return traces


def savitzky_golay_filt(traces):
    traces = signal.savgol_filter(traces, 5, 3, axis=1)
    return traces

