from cicada.preprocessing.convert_to_nwb import ConvertToNWB
from pynwb.base import TimeSeries

class ConvertCiFramesTsToNWB(ConvertToNWB):

    def __init__(self, nwb_file):
        super().__init__(nwb_file)

    def convert(self, **kwargs):
        # ci_frames_indices: 1d array not really useful, could be np.arange(n_frames)
        # timestamps_in_sec: 1d array, each index corresponds to a ci frame, each value is the timestamps of the frame
        ci_frames_time_series = TimeSeries(
            name="ci_frames",
            data=ci_frames_indices,  # ci_frames_bool,
            timestamps=timestamps_in_sec,  # self.timestamps_in_sec
            unit='s')
        # record the data as an acquisition
        # to recover the data do: nwb_file.get_acquisition(name=name_channel)
        self.nwb_file.add_acquisition(ci_frames_time_series)
