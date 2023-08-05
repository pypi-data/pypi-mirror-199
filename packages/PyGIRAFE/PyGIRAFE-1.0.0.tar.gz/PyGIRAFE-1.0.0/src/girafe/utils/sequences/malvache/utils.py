import numpy as np
from sklearn.decomposition import PCA


def xcov(a, b, lags):
    """
    Cross-covariance or autocovariance, returned as a vector or matrix.

    If x is an M × N matrix, then xcov(x) returns a (2M – 1) × N2 matrix
    with the autocovariances and cross-covariances of the columns of x.
    If you specify a maximum lag maxlag, then the output c has size (2 × maxlag – 1) × N2.
    :param a: 1st matrix
    :param b: 2nd matrix
    :param lags:
    :return:
    """

    # the cross-covariance is the cross-correlation function of two sequences with their means removed
    a = a - np.mean(a)
    b = b - np.mean(b)
    # with full mode, test all the lags
    xy_cov = np.correlate(a, b, mode="full")
    center_index = len(xy_cov) // 2
    if lags <= 0:
        return xy_cov[center_index]
    else:
        return xy_cov[center_index-lags:center_index+lags+1]


def covnorm(a, b, lags):
    """
    Compute the normalized cross-covariance
    :param a:
    :param b:
    :param lags:
    :return:
    """
    n = len(a)
    x_cov_result = xcov(a, b, lags)
    # print(f"x_cov_result {x_cov_result}")
    c = x_cov_result / np.std(a) / np.std(b) / n
    return c


def centralize_data(data):
    """
    TODO: comment
    """
    n_cells, n_times = data.shape
    # centralize data
    # average value for each cell
    cells_mean = np.mean(data, axis=1)
    data_centralized = (data - cells_mean.reshape((n_cells, 1)))
    # average instensity at each time frame - average over all pixels
    times_mean = np.mean(data_centralized, axis=0)
    data_centralized = (data_centralized - times_mean.reshape((1, n_times)))
    data = data_centralized

    return data_centralized


def step1_pca(data, n_pc_max):
    n_cells, n_times = data.shape
    if n_times < n_cells:
        # then we would need to do spatial covariance on temporal matrix
        raise Exception("n_times < n_cells")

    data = centralize_data(data)

    data_mt = (np.dot(data[:, :-1].transpose(), data[:, 1:]) + np.dot(data[:, 1:].transpose(), data[:, :-1])) \
              / n_times / 2

    # print(f"data_mt {data_mt.shape}")
    # eigenvectors and eigenvalues
    pca = PCA(n_components=n_pc_max)  #
    pca_result = pca.fit_transform(data_mt)
    pc_time_course = pca.components_

    return data, pc_time_course


def normalize_array_0_255(img_array):
    minv = np.amin(img_array)
    # minv = 0
    maxv = np.amax(img_array)
    if maxv - minv == 0:
        img_array = img_array.astype(np.uint8)
    else:
        img_array = (255 * (img_array - minv) / (maxv - minv)).astype(np.uint8)
    return img_array

