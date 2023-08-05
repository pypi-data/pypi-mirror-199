from cicada.preprocessing.convert_to_nwb import ConvertToNWB
from pynwb.base import TimeSeries
from pynwb.behavior import BehavioralTimeSeries
import numpy as np


class ConvertSignalToNWB(ConvertToNWB):
    def __init__(self, nwb_file):
        ConvertToNWB.__init__(self, nwb_file)

    def convert(self, **kwargs):
        """Convert the data and add it to the nwb_file

        Args:
            **kwargs: arbitrary arguments
        """
        super().convert(**kwargs)

        # identify the signal, should be a string
        data_id = kwargs.get("data_id", None)
        # identify the data (for ex: "all_cells", "INs" etc...)
        if data_id is None:
            # not mandatory
            print(f"No data_id in class {self.__class__.__name__}")
            return

        signal_data = kwargs.get("signal_data", None)
        # 1d array
        if signal_data is None:
            # not mandatory
            print(f"No signal_data in class {self.__class__.__name__}")
            return

        timestamps = kwargs.get("timestamps", None)
        # 1d array, same length as signal_data
        if timestamps is None:
            # not mandatory
            print(f"No timestamps in class {self.__class__.__name__}")
            return

        unity = kwargs.get("unity", None)
        if unity is None:
            print(f"No unity in {self.__class__.__name__}")

        nwb_module = kwargs.get('nwb_module')

        if 'behavior' in self.nwb_file.processing:
            behavior_nwb_module = self.nwb_file.processing['behavior']
        else:
            behavior_nwb_module = self.nwb_file.create_processing_module(name="behavior",
                                                                         description="behavioral data")
        try:
            behavior_timeseries = behavior_nwb_module.get(name='BehavioralTimeSeries')
        except KeyError:
            behavior_timeseries = BehavioralTimeSeries(name='BehavioralTimeSeries')
            behavior_nwb_module.add_data_interface(behavior_timeseries)

        if 'ophys' in self.nwb_file.processing:
            ophys_mod = self.nwb_file.processing['ophys']
        else:
            ophys_mod = self.nwb_file.create_processing_module('ophys', 'contains optical physiology processed data')

        if len(signal_data.shape) == 2:
            if signal_data.shape[1] > 1:
                print(f"Signal {data_id} has more than one dimension, its shape is {signal_data.shape}")
                return
            signal_data = np.ndarray.flatten(signal_data)
        if len(timestamps.shape) == 2:
            if timestamps.shape[1] > 1:
                print(f"Timestamps of signal {data_id} has more than one dimension, its shape is {timestamps.shape}")
                return
            timestamps = np.ndarray.flatten(timestamps)
        if len(timestamps) != len(signal_data):
            print(f"Signal {data_id} has a different length of its timestamps, {len(signal_data)} vs {len(timestamps)}")
            return

        # TODO: See to do self.nwb_file.add_acquisition(time_series)
        if nwb_module == 'behavior':
            behavior_timeseries.create_timeseries(name=data_id, data=np.transpose(signal_data), unit=unity,
                                                  timestamps=timestamps, description=data_id)
            print(f"Creating time series: {data_id} of length {len(signal_data)} "
                  f"in 'behavior' module as 'BehavioralTimeSeries'")
        if nwb_module == 'ophys':
            signal_time_series = TimeSeries(name=data_id, data=np.transpose(signal_data), unit=unity,
                                            timestamps=timestamps,
                                            description=data_id)
            ophys_mod.add_data_interface(signal_time_series)
            print(f"Creating time series: {data_id} of length {len(signal_data)} "
                  f"in 'ophys' module as 'TimeSeries'")



