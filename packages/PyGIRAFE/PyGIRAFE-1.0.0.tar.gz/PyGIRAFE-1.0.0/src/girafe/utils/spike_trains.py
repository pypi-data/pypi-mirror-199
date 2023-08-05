import numpy as np

def create_spike_train_neo_format(spike_trains):
    """
    Take a spike train in sec and prepare it to be transform in neo format.
    Args:
        spike_trains: list of list or list of np.array, representing for each cell the timestamps in sec of its spikes

    Returns: a new spike_trains in ms and the first and last timestamp (chronologically) of the spike_train.

    """

    new_spike_trains = []
    t_start = None
    t_stop = None
    for cell in np.arange(len(spike_trains)):
        spike_train = spike_trains[cell]
        new_spike_trains.append(spike_train)
        if len(spike_train) == 0:
            continue
        if t_start is None:
            t_start = spike_train[0]
        else:
            t_start = min(t_start, spike_train[0])
        if t_stop is None:
            t_stop = spike_train[-1]
        else:
            t_stop = max(t_stop, spike_train[-1])

    return new_spike_trains, t_start, t_stop
