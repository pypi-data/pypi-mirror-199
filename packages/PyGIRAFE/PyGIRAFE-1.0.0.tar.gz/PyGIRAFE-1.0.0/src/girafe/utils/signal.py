import numpy as np

def norm01(data):
    """
    Normalize value between 0 and 1
    Args:
        data: 1d array

    Returns:

    """
    data = np.asarray(data, dtype="float")
    min_value = np.min(data)
    max_value = np.max(data)

    difference = max_value - min_value

    data -= min_value

    if difference > 0:
        data = data / difference

    return data


def gaussblur1D(data, dw, dim):
    """
    Apply a gaussian blur on 1d data
    Args:
        data:
        dw:
        dim:

    Returns:

    """
    n_times = data.shape[dim]

    if n_times % 2 == 0:
        kt = np.arange((-n_times / 2) + 0.5, (n_times / 2) - 0.5 + 1)
    else:
        kt = np.arange(-(n_times - 1) / 2, ((n_times - 1) / 2 + 1))

    if dim == 0:
        fil = np.exp(-np.square(kt) / dw ** 2) * np.ones(data.shape[0])
    elif dim == 1:
        fil = np.ones(data.shape[1]) * np.exp(-np.square(kt) / dw ** 2)
    elif dim == 2:
        fil = np.zeros((data.shape[0], data.shape[1], data.shape[2]))
        for i in np.arange(n_times):
            fil[:, :, i] = np.ones((data.shape[0], data.shape[1])) * np.exp(-np.square(kt[i]) / dw ** 2)

    tfA = np.fft.fftshift(np.fft.fft(data, axis=dim))
    b = np.real(np.fft.ifft(np.fft.ifftshift(tfA * fil), axis=dim))

    return b


def gauss_blur(data, dw):
    """
    2D gaussian filter in Fourier domainon 2 first dimensions
    :param data:
    :param dw:
    :return:
    """

    n_x, n_y = data.shape

    if n_x % 2 == 0:
        kx = np.arange((-n_x / 2) + 0.5, (n_x / 2) - 0.5 + 1)
    else:
        kx = np.arange(-(n_x - 1) / 2, ((n_x - 1) / 2 + 1))

    if n_y % 2 == 0:
        ky = np.arange((-n_y / 2) + 0.5, (n_y / 2) - 0.5 + 1)
    else:
        ky = np.arange(-(n_y - 1) / 2, ((n_y - 1) / 2 + 1))

    k_x, k_y = np.meshgrid(kx, ky)

    kr_ho = np.sqrt(np.square(k_x) + np.square(k_y))
    fil = np.exp(-np.square(kr_ho) / dw ** 2)
    # b = np.zeros(n_x, n_y)
    # tfa = np.zeros(n_x, n_y)

    tfA = np.fft.fftshift(np.fft.fft2(data))
    b = np.real(np.fft.ifft2(np.fft.ifftshift(tfA * fil)))

    return b
