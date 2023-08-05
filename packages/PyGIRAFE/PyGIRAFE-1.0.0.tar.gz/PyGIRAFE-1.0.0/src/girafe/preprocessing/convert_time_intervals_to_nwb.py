from cicada.preprocessing.convert_to_nwb import ConvertToNWB
from cicada.preprocessing.utils import get_continous_time_periods
from pynwb.behavior import BehavioralEpochs
import hdf5storage
import numpy as np
import yaml


class ConvertTimeIntervalsToNWB(ConvertToNWB):
    def __init__(self, nwb_file):
        ConvertToNWB.__init__(self, nwb_file)

    def convert(self, **kwargs):
        """Convert the data and add it to the nwb_file

        Args:
            **kwargs: arbitrary arguments
        """
        super().convert(**kwargs)

        # if "name" not in kwargs:
        #     raise Exception(f"'name' argument should be pass to convert "
        #                     f"function in class {self.__class__.__name__}")

        name = kwargs.get("name", None)

        # if "description" not in kwargs:
        #     raise Exception(f"'description' argument should be pass to convert "
        #                     f"function in class {self.__class__.__name__}")

        description = kwargs.get("description", "")

        # bool that indicated if the time intervals already takes into consideration the calcium imaging recording
        # pauses. If not, then they will be added so it matches the recording
        ci_recording_pause_included = False
        if "ci_recording_pause_included" in kwargs:
            if kwargs["ci_recording_pause_included"] is True:
                ci_recording_pause_included = True

        # indicate if intervals are from behavior then we will create data from BehavioralEpochs
        is_behavioral_data = False
        if "behavior" in kwargs:
            if kwargs["behavior"] is True:
                is_behavioral_data = True

        time_in_frames = False
        if "time_in_frames" in kwargs:
            if kwargs["time_in_frames"] is True:
                time_in_frames = True

        if "intervals_data" not in kwargs:
            raise Exception(f"'intervals_data' argument should be pass to convert "
                            f"function in class {self.__class__.__name__}")

        intervals_data = kwargs["intervals_data"]
        intervals_list = []
        # take as key the name of the interval and as value a list of intervals such as intervals_list
        # intervals_list or intervals_dict should not be empty
        # intervals_dict is filled form npz files produced by cicada
        intervals_dict = dict()
        # if True, means we add those intervals to the invalid times recorded in the nwb_file
        as_invalid_times = False
        if intervals_data is not None:
            if isinstance(intervals_data, str):
                # then we check if it's not a file_name
                if intervals_data.endswith(".yaml") or intervals_data.endswith(".yml"):
                    with open(intervals_data, 'r') as stream:
                        intervals_yaml_data = yaml.safe_load(stream)
                        intervals_list = []
                        if "as_invalid_times" in intervals_yaml_data:
                            if intervals_yaml_data['as_invalid_times']:
                                as_invalid_times = True
                        if "frame_intervals" not in intervals_yaml_data:
                            print(f"'frame_intervals' not found in the file {intervals_data}, {name} intervals not created")
                            return
                        frame_intervals = intervals_yaml_data["frame_intervals"]
                        start_times_sorted = list(frame_intervals.keys())
                        start_times_sorted.sort()
                        # frame_intervals dict : key represent the frame of the start of the interval,
                        # and value the stop frame
                        for start_time in start_times_sorted:
                            intervals_list.append((start_time, frame_intervals[start_time]))
                        print(f"start_times_sorted {start_times_sorted}")
                        print(f"as_invalid_times {intervals_list}")
                        intervals_dict[name] = intervals_list
                if intervals_data.endswith(".npz"): # and "cicada" in intervals_data:
                    # it means the data was produced using cicada
                    cicada_intervals_dict = np.load(intervals_data)
                    for interval_name, intervals_array in cicada_intervals_dict.items():
                        # intervals_arrayarray of shape (2, n_intervals)
                        intervals_list = []
                        for interval_index in range(intervals_array.shape[1]):
                            intervals_list.append((intervals_array[0, interval_index],
                                                   intervals_array[1, interval_index]))
                        # TODO: possibility of keeping or not interval_name for which no intervals exist
                        # print(f"{time_in_frames} interval_name {interval_name} {intervals_list}")
                        if len(intervals_list) > 0:
                            intervals_dict[interval_name] = intervals_list
                        # intervals_dict[interval_name] = intervals_list
                if intervals_data.endswith(".mat"): # and "cicada" in intervals_data:
                    # it means the data was produced using cicada
                    cicada_intervals_dict = hdf5storage.loadmat(intervals_data)

                    interval_names = kwargs.get("interval_names", None)
                    if interval_names is None:
                        interval_names = list(cicada_intervals_dict.keys())
                    else:
                        if isinstance(interval_names, str):
                            interval_names = [interval_names]
                        if not isinstance(interval_names, list):
                            raise Exception(f"interval_names should be a list and not: {interval_names}")

                    for interval_name in interval_names:
                        if interval_name not in cicada_intervals_dict:
                            continue
                        intervals_array = cicada_intervals_dict[interval_name]
                        if not isinstance(intervals_array, np.ndarray):
                            continue
                        # intervals_arrayarray of shape (2, n_intervals)
                        intervals_list = []
                        for interval_index in range(intervals_array.shape[1]):
                            intervals_list.append((intervals_array[0, interval_index],
                                                   intervals_array[1, interval_index]))
                        # TODO: possibility of keeping or not interval_name for which no intervals exist
                        # print(f"{time_in_frames} interval_name {interval_name} {intervals_list}")
                        if len(intervals_list) > 0:
                            intervals_dict[interval_name] = intervals_list
                        # intervals_dict[interval_name] = intervals_list
            else:
                # intervals_data so far is 1D array of boolean
                # intervals_list is a sequence of pair of integer representing the first and last frame (included)
                # part of the interval
                intervals_list = get_continous_time_periods(intervals_data.astype("int8"))
                intervals_dict[name] = intervals_list
        else:
            print(f"{self.nwb_file.identifier} In ConvertTimeIntervalsToNWB {name} -> {description} -> intervals_data is None")
            return
        # TODO: see to put option so intervals are not only array of boolean representing the frames
        #  at which action happens

        # pause_intervals = None
        # if 'ci_recording_on_pause' in self.nwb_file.intervals:
        #     pause_intervals = self.nwb_file.intervals['ci_recording_on_pause']

        ci_frames_time_series = None
        try:
            ci_frames_time_series = self.nwb_file.get_acquisition("ci_frames")
            # print(f"ci_frames_series {ci_frames_time_series}")
        except KeyError:
            print(f"No ci_frames_time_series found in the nwb file") #, we cannot create the time intervals {name}
            # return

        # we need the sampling rate to add the intervals
        # sometimes it is not needed is intervals are not in frames
        try:
            image_series = self.nwb_file.acquisition["motion_corrected_ci_movie"]
            sampling_rate = image_series.rate
        except KeyError:
            print(f"No motion_corrected_ci_movie in acquisition")
            sampling_rate = None

        timestamps = None
        if (not ci_recording_pause_included) and (ci_frames_time_series is not None):
            # BEFORE: ci_frames_time_series is a 1d array of boolean, with True if the index correponds to the acquisition of
            # a frame during CI recording. Same length as timestamps, which contains all timestamps of the recording
            # based on the abf sampling_rate
            # NEW: ci_frames_time_series is a 1d array of integers containing the abf frame corresponding to each ci
            # frame. timestamps contains the time in sec from the beginning of the abf recording of each ci frame
            frames_indices = ci_frames_time_series.data  # np.where(ci_frames_time_series.data)[0]
            timestamps = ci_frames_time_series.timestamps

        if is_behavioral_data:
            if 'behavior' in self.nwb_file.processing:
                behavior_nwb_module = self.nwb_file.processing['behavior']
            else:
                behavior_nwb_module = self.nwb_file.create_processing_module(name="behavior",
                                                                             description="behavioral data")
            try:
                behavior_epochs = behavior_nwb_module.get(name='BehavioralEpochs')
            except KeyError:
                behavior_epochs = BehavioralEpochs(name='BehavioralEpochs')
                behavior_nwb_module.add_data_interface(behavior_epochs)

            for name, intervals_list in intervals_dict.items():
                print(f"In ConvertTimeIntervalsToNWB {name} -> n intervals {len(intervals_list)}")
                print(f"Intervals added as 'IntervalSeries' in 'behavior' module in 'BehavioralEpochs'")
                time_stamps_to_store = []
                data_to_store = []
                for interval in intervals_list:
                    if not time_in_frames:
                        start_time = interval[0]
                        stop_time = interval[1]
                    else:
                        if timestamps is not None:
                            start_time = timestamps[interval[0]]  # timestamps[frames_indices[interval[0]]]
                            stop_time = timestamps[interval[1]]  # timestamps[frames_indices[interval[1]]]
                        else:
                            # time in seconds
                            start_time = interval[0] * (1 / sampling_rate)
                            stop_time = interval[1] * (1 / sampling_rate)
                    time_stamps_to_store.extend([start_time, stop_time])
                    data_to_store.extend([1, -1])
                # data: >0 if interval started, <0 if interval ended.
                # timestamps: Timestamps for samples stored in data
                behavior_epochs.create_interval_series(name=name, data=data_to_store, timestamps=time_stamps_to_store,
                                                       comments='no comments',
                                                       description=description,
                                                       control=None, control_description=None)

        else:

            columns_pause = list()
            columns_pause.append({"name": "start_time", "description": "Start time of epoch, in seconds"})
            columns_pause.append({"name": "stop_time", "description": "Stop time of epoch, in seconds"})
            columns_pause.append({"name": "start_original_frame",
                                  "description": "Frame at which the epoch starts (included), using frames from the"
                                                 "original concatenated movie"})
            columns_pause.append({"name": "stop_original_frame",
                                  "description": "Frame at which the epoch stops (included), using frames from the "
                                                 "original concatenated movie"})

            for name, intervals_list in intervals_dict.items():
                if not as_invalid_times:
                    time_intervals = self.nwb_file.create_time_intervals(name=name, description=description,
                                                                         columns=columns_pause)
                print(f"In ConvertTimeIntervalsToNWB {name} -> n intervals {len(intervals_list)}")
                print(f"Intervals added as 'DataFrame' in 'nwb_data.intervals'")
                for interval in intervals_list:
                    if timestamps is not None:
                        start_time = timestamps[interval[0]] # timestamps[frames_indices[interval[0]]]
                        stop_time = timestamps[interval[1]] # timestamps[frames_indices[interval[1]]]
                    else:
                        # time in seconds
                        start_time = interval[0] * (1 / sampling_rate)
                        stop_time = interval[1] * (1 / sampling_rate)

                    data_dict = {}
                    data_dict["start_time"] = start_time
                    data_dict["stop_time"] = stop_time
                    data_dict["start_original_frame"] = interval[0]
                    data_dict["stop_original_frame"] = interval[1]
                    # print(f"{self.nwb_file.identifier}: data_dict {data_dict}")

                    if as_invalid_times:
                        # we add those intervals during which the CI recording is on pause as invalid_time
                        # so those time intervals will be removed from analysis'
                        self.nwb_file.add_invalid_time_interval(
                            start_time=start_time,
                            stop_time=stop_time)
                    else:
                        time_intervals.add_row(data_dict)
