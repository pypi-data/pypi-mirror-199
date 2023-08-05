from cicada.preprocessing.convert_to_nwb import ConvertToNWB
import numpy as np
import yaml
import pyabf
import math
import scipy.signal as sci_signal
import matplotlib.pyplot as plt
from pynwb.base import TimeSeries
from pynwb.behavior import Position, BehavioralTimeSeries
from cicada.preprocessing.utils import get_continous_time_periods, merging_time_periods, class_name_to_module_name

class ConvertAbfToNWB(ConvertToNWB):
    """Class to convert ABF data to NWB """
    def __init__(self, nwb_file):
        super().__init__(nwb_file)
        self.abf = None
        self.first_frame_index = 0
        # array of integers representing the index at which the frame has been acquired
        # the indices is used in sweepY
        self.ci_frames_indices = None
        self.frames_data = None
        self.timestamps_in_sec = None
        self.timestamps_in_ms = None
        # if ABF sampling rate is 10 kHz:
        self.nframes_in_10khz_abf = None
        self.n_imaging_blocks = None
        # for behavior
        self.timestamps_behavior_in_sec = None
        self.timestamps_behavior_in_ms = None
        # means if there are more than one movie, we consider it as one movie (concatenation of the segments)
        # without any breaks in the movie
        self.fusion_movie_segments = False
        self.sampling_rate_calcium_imaging = None
        # contains the frames indices (matching self.ci_frames_indices) after which there is a gap (for ex when
        # 2 movies are concatenated)
        self.gap_indices = np.zeros(0, dtype="int16")

        self.behavior_channels = None
        self.behavior_name_to_channel = None
        self.timestamps_speed_in_sec = None

    def convert(self, **kwargs):
        """
        The goal of this function is to extract from an Axon Binary Format (ABF) file its content
        and make it accessible through the NWB file.
        The content can be: LFP signal, piezzo signal, speed of the animal on the treadmill. All, None or a few
        of these informations could be available.
        One information always present is the timestamps, at the abf sampling_rate, of the frames acquired
        by the microscope to create the calcium imaging movie. Such movie could be the concatenation of a few
        movies, such is the case if the movie need to be saved every x frames for memory issue for ex.
        If the movie is the concatenation of many, then there is an option to choose to extract the information as
        if 2 frames concatenate are contiguous in times (such as then LFP signal or piezzo would be match movie),
        or to add interval_times indicating at which time the recording is on pause and at which time it's starting
        again. The time interval containing this information is named "ci_recording_on_pause" and you can get it
        doing:
        if 'ci_recording_on_pause' in nwb_file.intervals:
        pause_intervals = nwb_file.intervals['ci_recording_on_pause']

        Args:
            **kwargs (dict) : kwargs is a dictionary, potentials keys and values types are:
            abf_yaml_file_name: mandatory parameter. The value is a string representing the path
            and file_name of the yaml file associated to this abf file. In the abf:
            frames_channel: mandatory parameter. The value is an int representing the channel
            of the abf in which is the frames timestamps data.
            abf_file_name: mandatory parameter. The value is a string representing the path
            and file_name of the abf file.

        """
        super().convert(**kwargs)

        if "abf_yaml_file_name" not in kwargs:
            raise Exception(f"'abf_yaml_file' argument should be pass to convert "
                            f"function in class {self.__class__.__name__}")

        if "abf_file_name" not in kwargs:
            raise Exception(f"'abf_file_name' argument should be pass to convert "
                            f"function in class {self.__class__.__name__}")

        if "fusion_movie_segments" in kwargs:
            self.fusion_movie_segments = bool(kwargs["fusion_movie_segments"])

        # yaml_file that will contains the information to read the abf file
        abf_yaml_file_name = kwargs["abf_yaml_file_name"]
        if abf_yaml_file_name is None:
            return
        with open(abf_yaml_file_name, 'r') as stream:
            abf_yaml_data = yaml.safe_load(stream)

        if "frames_channel" in abf_yaml_data:
            frames_channel = int(abf_yaml_data["frames_channel"])
        else:
            frames_channel = -1
            print(f"No 'frames_channel' provided in the yaml file "
                            f"{abf_yaml_file_name}")
            # raise Exception(f"No 'frames_channel' provided in the yaml file "
            #                 f"{abf_yaml_file_name}")

        if "nframes_in_10khz_abf" in abf_yaml_data:
            self.nframes_in_10khz_abf = int(abf_yaml_data["nframes_in_10khz_abf"])
        if "n_imaging_blocks" in abf_yaml_data:
            self.n_imaging_blocks = int(abf_yaml_data["n_imaging_blocks"])

        # key is an int representing a channel index, value is a list of 1 or 2 elements, first element is a string
        # caraterazing the channel name and the second element (optionnal) is the new sampling_rate in which saving
        # the data. If not present, the original sampling_rate will be kept
        channels_to_save_dict = dict()
        # channel with the LFP data
        lfp_channel = abf_yaml_data.get("lfp_channel")
        if lfp_channel is not None:
            channels_to_save_dict[lfp_channel] = ["lfp"]
            # give the sampling rate to use for downsampling the lfp and record
            # it in the nwb file. If no argument, then the original sampling_rate will be kept
            lfp_downsampling_hz = abf_yaml_data.get("lfp_downsampling_hz")
            if lfp_downsampling_hz is not None:
                channels_to_save_dict[lfp_channel].append(lfp_downsampling_hz)
            else:
                lfp_downsampling_hz = '50'
                channels_to_save_dict[lfp_channel].append(lfp_downsampling_hz)
            print(f"LFP channel are by default down-sampled {lfp_downsampling_hz} times")

        # channel with the run data
        run_channel = abf_yaml_data.get("run_channel")
        if run_channel is not None:
            channels_to_save_dict[run_channel] = ["run"]

        # channel with the direction data (complement of speed)
        direction_channel = abf_yaml_data.get("direction_channel")
        if direction_channel is not None:
            channels_to_save_dict[direction_channel] = ['direction']
        belt_length = abf_yaml_data.get("belt_length")

        # channel with the piezzo data (could be more than one channel
        piezo_channels = abf_yaml_data.get("piezo_channels", None)

        if piezo_channels is not None:
            if isinstance(piezo_channels, int):
                # converting int in list
                piezo_channels = [piezo_channels]
            for piezo_channel in piezo_channels:
                channels_to_save_dict[piezo_channel] = ["piezo_" + str(piezo_channel)]
                piezzo_downsampling_hz = abf_yaml_data.get("piezo_downsampling_hz")
                if piezzo_downsampling_hz is not None:
                    channels_to_save_dict[piezo_channel].append(piezzo_downsampling_hz)
                else:
                    piezzo_downsampling_hz = '1000'
                    channels_to_save_dict[piezo_channel].append(piezzo_downsampling_hz)
                print(f"Piezzo channel are by default down-sampled {piezzo_downsampling_hz} times")

        # map the name to the channel
        self.behavior_name_to_channel = dict()
        self.behavior_channels = []
        behavior_names = abf_yaml_data.get("behavior_adc_names", None)
        if behavior_names is not None:
            # if True then we build the tiff with recording pauses to synchronize it with behavior frames
            self.fusion_movie_segments = False
            if isinstance(behavior_names, int):
                # converting int in list
                behavior_names = [behavior_names]
            # converting it to str
            behavior_names = [str(beh) for beh in behavior_names]
            for behavior_name in behavior_names:
                print(f"behavior_name {behavior_name}")
        else:
            behavior_names = []

        # if given, indicated an offset to be taken in consideration between the data acquisition
        # and the frames
        offset = abf_yaml_data.get("offset", None)

        abf_file_name = kwargs["abf_file_name"]
        """
        dir(abf):
        abf ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', 
        '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', 
        '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', 
        '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_adcSection', '_cacheStimulusFiles', 
        '_dacSection', '_dataGain', '_dataOffset', '_dtype', '_epochPerDacSection', '_epochSection', 
        '_fileSize', '_headerV2', '_ide_helper', '_loadAndScaleData', '_makeAdditionalVariables', 
        '_nDataFormat', '_preLoadData', '_protocolSection', '_readHeadersV1', '_readHeadersV2', 
        '_sectionMap', '_stringsIndexed', '_stringsSection', '_sweepBaselinePoints', '_tagSection', 
        'abfDateTime', 'abfDateTimeString', 'abfFileComment', 'abfFilePath', 'abfID', 'abfVersion', 
        'abfVersionString', 'adcNames', 'adcUnits', 'channelCount', 'channelList', 'creatorVersion', 
        'creatorVersionString', 'dacNames', 'dacUnits', 'data', 'dataByteStart', 'dataLengthMin', 
        'dataLengthSec', 'dataPointByteSize', 'dataPointCount', 'dataPointsPerMs', 'dataRate', 
        'dataSecPerPoint', 'fileGUID', 'headerHTML', 'headerLaunch', 'headerMarkdown', 'headerText', 
        'holdingCommand', 'launchInClampFit', 'protocol', 'protocolPath', 'saveABF1', 'setSweep', 
        'stimulusByChannel', 'stimulusFileFolder', 'sweepC', 'sweepChannel', 'sweepCount', 'sweepD', 
        'sweepEpochs', 'sweepIntervalSec', 'sweepLabelC', 'sweepLabelX', 'sweepLabelY', 'sweepLengthSec', 
        'sweepList', 'sweepNumber', 'sweepPointCount', 'sweepUnitsC', 'sweepUnitsX', 'sweepUnitsY', 
        'sweepX', 'sweepY', 'tagComments', 'tagSweeps', 'tagTimesMin', 'tagTimesSec']
        """
        try:
            self.abf = pyabf.ABF(abf_file_name)
        except (FileNotFoundError, OSError, TypeError) as e:
            print(f"Abf file not found: {abf_file_name}")
            return
        # displaying the header with all abf informations
        print(f"ABF, self.abf.adcNames {self.abf.adcNames}")
        # mapping behavior names to channels
        if len(behavior_names) > 0:
            # replacing a particular channel 'IN 5' by '22983298'
            for behavior_name in behavior_names:
                if behavior_name in self.abf.adcNames or \
                        (behavior_name == '22983298' and (('IN 5' in self.abf.adcNames) or
                                                          ('IN 13' in self.abf.adcNames))):
                    if behavior_name not in self.abf.adcNames:
                        if 'IN 5' in self.abf.adcNames:
                            index = self.abf.adcNames.index('IN 5')
                        else:
                            index = self.abf.adcNames.index('IN 13')
                        channel = self.abf.channelList[index]
                        channels_to_save_dict[channel] = [f'cam_{behavior_name}']
                        self.behavior_channels.append(channel)
                        self.behavior_name_to_channel[behavior_name] = behavior_name
                    else:
                        index = self.abf.adcNames.index(behavior_name)
                        channel = self.abf.channelList[index]
                        channels_to_save_dict[channel] = [f'cam_{behavior_name}']
                        self.behavior_channels.append(channel)
                        self.behavior_name_to_channel[behavior_name] = behavior_name
            # print(f"self.behavior_channels {self.behavior_channels}")
        # print(f"self.abf {self.abf.headerText}")
        # raise Exception("NOT TODAY")

        #   ------------- CI FRAMEs -----------------
        # print(f"abf number of channels: {self.abf.channelCount}")
        # raise Exception("TOTO")
        if frames_channel == -1:
            # this case should happen only for REM data control, without calcium imagery
            self.determine_behavior_movie_frames_indices()
            return

        self.abf.setSweep(sweepNumber=0, channel=frames_channel)

        timestamps_in_sec = self.abf.sweepX
        # print(f"ci frames: timestamps_in_sec len {len(timestamps_in_sec)} {timestamps_in_sec}")
        # timestamps_in_sec = np.arange(len(self.abf.sweepY)) * (1 / self.abf.dataRate)
        # to avoid issue with float approximation, we compute ourself the timestamps and in ms
        timestamps_in_ms = np.arange(len(self.abf.sweepY)) * (1 / self.abf.dataRate) * 1000
        self.frames_data = self.abf.sweepY
        # first frame corresponding at the first frame recorded in the calcium imaging movie
        self.first_frame_index = np.where(self.frames_data < 0.01)[0][0]
        self.frames_data = self.frames_data[self.first_frame_index:]
        self.timestamps_in_sec = timestamps_in_sec[self.first_frame_index:]
        self.timestamps_in_ms = timestamps_in_ms[self.first_frame_index:]
        # to avoid issue with float approximation, we compute ourselves the timestamps
        # to avoid issue with float approximation, we compute ourselves the timestamps
        # print(f"self.abf.dataSecPerPoint {self.abf.dataSecPerPoint}")
        # print(f"self.timestamps_in_ms[:10] {self.timestamps_in_ms[:10]}")

        # determining ci_frames_indices
        self.determine_ci_frames_indices()

        #   ------------- BEHAVIOR MOVIE -----------------
        # checking how many frames in behaviour movie, if presents
        self.determine_behavior_movie_frames_indices()

        # For Speed as signal
        self.timestamps_speed_in_sec = timestamps_in_sec

        print(f"abf number of channels: {self.abf.channelCount}")
        print(f"channels_to_save_dict {channels_to_save_dict}")

        for current_channel in np.arange(1, self.abf.channelCount):
            # name of the channel in abf
            # print(f"Name channel {current_channel}: {self.abf.adcNames[current_channel]}")

            # to get labels
            # print(f"self.abf.sweepLabelY {self.abf.sweepLabelY}")
            # print(f"self.abf.sweepLabelX {self.abf.sweepLabelX}")

            if current_channel not in channels_to_save_dict:
                continue

            if channels_to_save_dict[current_channel][0] == "run":
                print(f"Process ABF speed channel: speed")
                self.process_run_data(run_channel=run_channel)
                if direction_channel is not None and belt_length is not None:
                    print(f"Process ABF speed channel: position")
                    self.process_position_data(run_channel=run_channel, direction_channel=direction_channel,
                                               belt_length=belt_length)
                continue
            # so far this code only analyse run and lfp channel
            if (channels_to_save_dict[current_channel][0] != "lfp") and \
                    (not channels_to_save_dict[current_channel][0].startswith("piezo")):
                continue
            self.abf.setSweep(sweepNumber=0, channel=current_channel)
            # abf_current_channel_data == mvt_data from the previous version
            abf_current_channel_data = self.abf.sweepY
            if offset is not None:
                abf_current_channel_data = abf_current_channel_data + offset
            abf_current_channel_data = abf_current_channel_data[self.first_frame_index:]

            # for LFP we used in the past down_sampling at 1000 Hz and for piezo 50 Hz
            if len(channels_to_save_dict[current_channel]) > 1:
                down_sampling_hz = int(channels_to_save_dict[current_channel][1])
            else:
                down_sampling_hz = self.abf.dataRate

            sampling_step = int(self.abf.dataRate / down_sampling_hz)

            if (not self.fusion_movie_segments) or (len(self.gap_indices) == 0):
                last_index = min(len(abf_current_channel_data) - 1, self.ci_frames_indices[-1])
                abf_data_to_save = abf_current_channel_data[:last_index:sampling_step]
                abf_data_to_save = np.concatenate((abf_data_to_save, np.array([abf_current_channel_data[last_index]])))
                timestamps_to_save = self.timestamps_in_ms[:last_index:sampling_step]
                timestamps_to_save = np.concatenate((timestamps_to_save,
                                                     np.array([self.timestamps_in_ms[last_index]])))
            else:
                abf_data_to_save = np.zeros(0)
                timestamps_to_save = np.zeros(0)
                # +1 to get the first frame of the segment
                segments_indices = [0] + list(self.gap_indices + 1)
                # print(f"segments_indices {segments_indices}")
                for index_segt, segt_first_frame in enumerate(segments_indices):
                    if index_segt == len(segments_indices) - 1:
                        last_abf_frame = self.ci_frames_indices[-1]
                    else:
                        last_abf_frame = self.ci_frames_indices[segments_indices[index_segt + 1] - 1]
                    if last_abf_frame == len(abf_current_channel_data):
                        last_abf_frame -= 1
                    # sampling_step is produced according to a down_sampling_hz that changes
                    # according to the channel (lfp, piezzo etc...)
                    new_data = abf_current_channel_data[np.arange(self.ci_frames_indices[segt_first_frame],
                                                                  last_abf_frame, sampling_step)]
                    new_timestamps = self.timestamps_in_ms[self.ci_frames_indices[segt_first_frame]:last_abf_frame:
                                                           sampling_step]
                    # by adding the last_abf_frame we change the interval of time between the two last elements
                    # but this allow to keep the data well aligned
                    abf_data_to_save = np.concatenate((abf_data_to_save, new_data,
                                                       np.array([abf_current_channel_data[last_abf_frame]])))
                    timestamps_to_save = np.concatenate((timestamps_to_save, new_timestamps,
                                                       np.array([self.timestamps_in_ms[last_abf_frame]])))

            if (lfp_channel is not None) and (lfp_channel == current_channel):
                name_channel = "lfp"
                continue
                # TODO: We don't save the lfp in the NWB so far: do it if we get nice lfp and create an ecphys module
            else:
                name_channel = "piezo_" + str(np.where(piezo_channels == current_channel)[0][0])

            # given the conversion factor to get the timestamps in sec
            # we record them in ms to have a better precision
            # record the data as an acquisition
            # to recover the data do: nwb_file.get_acquisition(name=name_channel)
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
            piezzo_starting_time = timestamps_to_save[0] / 1000
            behavior_timeseries.create_timeseries(name=name_channel, data=np.transpose(abf_data_to_save),
                                                  starting_time=piezzo_starting_time, rate=float(sampling_step),
                                                  unit='mV')

    def determine_behavior_movie_frames_indices(self):
        if len(self.behavior_channels) == 0:
            return

        # threshold_value = 0.5
        threshold_value = 0.25

        for behavior_channel in self.behavior_channels:
            # name of the channel in abf
            adc_name = self.abf.adcNames[behavior_channel]
            if (adc_name == 'IN 5') or (adc_name == 'IN 13'):
                # changing the name as it represents one of the behavior cam
                adc_name = '22983298'
            print(f"Adc name channel {behavior_channel}: {adc_name}")
            self.abf.setSweep(sweepNumber=0, channel=behavior_channel)
            frames_data_behavior = self.abf.sweepY

            acquisition_start = np.where(frames_data_behavior < 0.1)[0][0]
            print(f"acquisition_start {acquisition_start}")
            # then we want the first frame index
            # first_frame_index = np.where(frames_data_behavior[acquisition_start + 1:] > 0.5)[0][0]
            # first_frame_index += acquisition_start
            # print(f"acquisition_start {acquisition_start}, first_frame_index {first_frame_index}")

            # plt.plot(frames_data_behavior[acquisition_start-100:acquisition_start+100000])
            # plt.show()
            # raise Exception("TOTO")

            timestamps_behavior_in_sec = self.abf.sweepX
            # print(f"timestamps_behavior_in_sec len {len(timestamps_behavior_in_sec)}  {timestamps_behavior_in_sec}")
            # to avoid issue with float approximation, we compute ourselves the timestamps and in ms
            timestamps_behavior_in_ms = np.arange(len(self.abf.sweepX)) * (1 / self.abf.dataRate) * 1000
            timestamps_behavior_in_sec = timestamps_behavior_in_sec[acquisition_start+1:]
            # timestamps_behavior_in_sec[:-acquisition_start]
            timestamps_behavior_in_ms = timestamps_behavior_in_ms[acquisition_start+1:]

            # keeping the frames after the first acquisition
            frames_data_behavior = frames_data_behavior[acquisition_start + 1:]

            binary_frames_data = np.zeros(len(frames_data_behavior), dtype="int8")

            binary_frames_data[frames_data_behavior >= threshold_value] = 1
            binary_frames_data[frames_data_behavior < threshold_value] = 0

            # similar to self.ci_frames_indices but behavior movies
            behavior_movie_frames_indices = np.where(np.diff(binary_frames_data) == 1)[0] + 1
            # removing the last 2 frames
            behavior_movie_frames_indices = behavior_movie_frames_indices[:-2]
            print(f"n frames for channel {behavior_channel}: {len(behavior_movie_frames_indices)}")
            # print(f"behavior_movie_frames_indices {behavior_movie_frames_indices}")

            # given the conversion factor to get the timestamps in sec
            # we record them in ms to have a better precision

            # print(f"timestamps_behavior_in_sec[behavior_movie_frames_indices] "
            #       f"{timestamps_behavior_in_sec[behavior_movie_frames_indices]}")
            bhv_frames_time_series = TimeSeries(
                name=f"cam_{adc_name}",
                data=np.transpose(behavior_movie_frames_indices), # behavior_frames_bool,
                timestamps=np.array(timestamps_behavior_in_sec[behavior_movie_frames_indices]), # timestamps_behavior_in_sec,
                # conversion=0.001,
                unit='s')
            # record the data as an acquisition
            # to recover the data do: nwb_file.get_acquisition(name=name_channel)
            self.nwb_file.add_acquisition(bhv_frames_time_series)

    def determine_ci_frames_indices(self):
        """
        Using the frames data channel, estimate the timestamps of each frame of the calcium imaging movie.
        If there are breaks between each recording (the movie being a concatenation of different movies), then
        there is an option to either skip those non registered frames that will be skept in all other data (lfp, piezzo,
        ...) or to determine how many frames to add in the movie and where so it matches the other data recording in
        the abf file

        """
        threshold_value = 0.02
        print(f"ABF acquisition rate: {self.abf.dataRate} Hz")
        if self.abf.dataRate < 50000:
            print(f"Deal with ABF at lower rate than 50 kHz")
            # Check if some frames are missing or not: if not we do as usual, if yes we linespace the number of frames
            # Find CI frames:
            binary_frames_data = np.zeros(len(self.frames_data), dtype="int8")
            binary_frames_data[self.frames_data >= threshold_value] = 1
            binary_frames_data[self.frames_data < threshold_value] = 0

            binary_frames_data_periods = get_continous_time_periods(binary_frames_data)
            gaps_size = np.zeros(len(binary_frames_data_periods), dtype=int)

            for gap in range(len(binary_frames_data_periods)):
                gaps_size[gap] = binary_frames_data_periods[gap][1] - binary_frames_data_periods[gap][0]

            observed_long_gap_location = list(np.where(gaps_size > 5 * self.abf.dataRate)[0])
            expected_long_gap_location = [int((self.nframes_in_10khz_abf / self.n_imaging_blocks) * block) - 1
                                          for block in np.arange(1, self.n_imaging_blocks + 1)]

            if observed_long_gap_location == expected_long_gap_location:
                print(f"All CI frames are still detected in the ABF: use exact CI frame timestamps from ABF")
                # Do as is self.abf.rate == 50 kHz
                self.ci_frames_indices = np.where(np.diff(binary_frames_data) == 1)[0] + 1
                # then we want to determine the size of the breaks between each movie segment if there are some
                diff_active_frames = np.diff(self.ci_frames_indices)
                # calculating the gap threshold above which we estimate the movie recording has been on hold
                median_bw_two_frames = np.median(diff_active_frames)
                frames_gap_threshold = median_bw_two_frames + 5 * np.std(diff_active_frames)  # 5 is usually good
                self.gap_indices = np.where(diff_active_frames > frames_gap_threshold)[0]
                print(f"N Gaps in CI movie: {len(self.gap_indices)}")
                # first we calculate the sampling rate of the movie
                if len(self.gap_indices) == 0:
                    self.sampling_rate_calcium_imaging = 1 / (((self.timestamps_in_ms[self.ci_frames_indices[-1]] -
                                                                self.timestamps_in_ms[
                                                                    self.ci_frames_indices[0]]) / 1000) / len(
                        self.ci_frames_indices))
                else:
                    # contains the sampling rate of each movie recorded
                    movies_sampling_rate = []
                    for i, gap_index in enumerate(self.gap_indices):
                        first_frame_segment = 0 if i == 0 else self.gap_indices[i - 1] + 1
                        # estimating the sampling rate of the movie
                        segment_time_in_ms = self.timestamps_in_ms[self.ci_frames_indices[gap_index]] - \
                                             self.timestamps_in_ms[self.ci_frames_indices[first_frame_segment]]
                        movies_sampling_rate.append(
                            1 / ((segment_time_in_ms / 1000) / (gap_index - first_frame_segment + 1)))

                    # estimating the sampling rate of the movie on the last segment
                    segment_time_in_ms = self.timestamps_in_ms[self.ci_frames_indices[-1]] - \
                                         self.timestamps_in_ms[self.ci_frames_indices[self.gap_indices[-1] + 1]]
                    movies_sampling_rate.append(
                        1 / ((segment_time_in_ms / 1000) / (len(self.ci_frames_indices) - (self.gap_indices[-1] + 1))))
                    self.sampling_rate_calcium_imaging = np.mean(movies_sampling_rate)
                print(f"Movie sampling rate {self.sampling_rate_calcium_imaging} Hz")

                ci_frames_time_series = TimeSeries(
                    name="ci_frames",
                    data=np.transpose(self.ci_frames_indices),  # ci_frames_bool,
                    timestamps=np.array(self.timestamps_in_sec[self.ci_frames_indices]),  # self.timestamps_in_sec
                    # conversion=0.001,
                    unit='s')
                # record the data as an acquisition
                # to recover the data do: nwb_file.get_acquisition(name=name_channel)
                self.nwb_file.add_acquisition(ci_frames_time_series)

                if (not self.fusion_movie_segments) and (len(self.gap_indices) > 0):
                    # pause_time_intervals = TimeIntervals
                    columns_pause = []
                    columns_pause.append({"name": "start_time", "description": "Start time of epoch, in seconds"})
                    columns_pause.append({"name": "stop_time", "description": "Stop time of epoch, in seconds"})
                    columns_pause.append({"name": "start_original_frame",
                                          "description": "Frame after which the pause starts, using frames from the"
                                                         "original concatenated movie"})
                    columns_pause.append({"name": "stop_original_frame",
                                          "description": "Frame at which the pause ends, using frames from the "
                                                         "original concatenated movie"})
                    pause_time_intervals = self.nwb_file.create_time_intervals(name="ci_recording_on_pause",
                                                                               description='Intervals that correspond to '
                                                                                           'the time of last frame recorded '
                                                                                           'before the pause, and stop_time '
                                                                                           'is the time of the first frame '
                                                                                           'recorded after the pause, during calcium imaging'
                                                                                           'recording.',
                                                                               columns=columns_pause)
                    for i, gap_index in enumerate(self.gap_indices):
                        # we save as a TimeInterval the interval during which the calcium imaging movie recording
                        # is on pause. First value is the time of last frame recorded before the pause, and stop_time
                        # is the time of the first frame recorded after the pause
                        # issue with add_epoch, it does work but after saving, when loading the nwb_file, there is no
                        # epoch. Solution using add_time_intervals inspired by this issue
                        # https://github.com/NeurodataWithoutBorders/pynwb/issues/958
                        data_dict = {}
                        data_dict["start_time"] = self.timestamps_in_sec[self.ci_frames_indices[gap_index]]
                        data_dict["stop_time"] = self.timestamps_in_sec[self.ci_frames_indices[gap_index + 1]]
                        data_dict["start_original_frame"] = gap_index
                        data_dict["stop_original_frame"] = gap_index + 1
                        pause_time_intervals.add_row(data_dict)

                        # we add those intervals during which the CI recording is on pause as invalid_time
                        # so those time intervals will be removed from analysis'
                        self.nwb_file.add_invalid_time_interval(
                            start_time=self.timestamps_in_sec[self.ci_frames_indices[gap_index]],
                            stop_time=self.timestamps_in_sec[self.ci_frames_indices[gap_index + 1]])
            else:
                print(f"Some CI frames are missing in the ABF: use line space instead of exact CI frames timestamps")
                if self.n_imaging_blocks == 1:
                    print(f"Only one imaging block")
                    missing_frames = [expected_long_gap_location[0] - observed_long_gap_location[0]]
                    print(f"N missing frames in imaging block: {missing_frames}")

                    stop_block = binary_frames_data_periods[observed_long_gap_location[0]][0]

                    print(f"One imaging block: from t=0 s to t={np.round(stop_block / self.abf.dataRate, decimals=2)} s")

                    active_frames = np.linspace(start=0, stop=stop_block, num=self.nframes_in_10khz_abf).astype(int)

                    mean_diff_active_frames = np.mean(np.diff(active_frames)) / self.abf.dataRate
                    if mean_diff_active_frames < 0.09:
                        raise Exception("mean_diff_active_frames < 0.09")
                    self.ci_frames_indices = active_frames
                    self.sampling_rate_calcium_imaging = 1 / (((self.timestamps_in_ms[self.ci_frames_indices[-1]] - \
                                                           self.timestamps_in_ms[self.ci_frames_indices[0]]) / 1000) / len(
                        self.ci_frames_indices))
                    print(f"ABF to NWB: sampling rate calcium imaging {self.sampling_rate_calcium_imaging}")

                    # given the conversion factor to get the timestamps in sec
                    # we record them in ms to have a better precision

                    ci_frames_time_series = TimeSeries(
                        name="ci_frames",
                        data=np.transpose(self.ci_frames_indices),  # ci_frames_bool,
                        timestamps=np.array(self.timestamps_in_sec[self.ci_frames_indices]),  # self.timestamps_in_sec
                        # conversion=0.001,
                        unit='s')
                    # record the data as an acquisition
                    # to recover the data do: nwb_file.get_acquisition(name=name_channel)
                    self.nwb_file.add_acquisition(ci_frames_time_series)
                else:
                    if self.n_imaging_blocks != len(observed_long_gap_location):
                        print(f"{self.n_imaging_blocks} imaging blocks given by abf yaml "
                              f"and {len(observed_long_gap_location)} blocks found in abf, "
                              f"do not account for gaps in CI movie and just linspace the total number of CI frames")
                        mask_frames_data = np.ones(len(self.frames_data), dtype="bool")
                        # we need to detect the frames manually, but first removing data between movies
                        selection = np.where(self.frames_data >= threshold_value)[0]
                        mask_selection = np.zeros(len(selection), dtype="bool")
                        pos = np.diff(selection)
                        # looking for continuous data between movies
                        to_keep_for_removing = np.where(pos == 1)[0] + 1
                        mask_selection[to_keep_for_removing] = True
                        selection = selection[mask_selection]
                        # we remove the "selection" from the frames data
                        mask_frames_data[selection] = False
                        frames_data = self.frames_data[mask_frames_data]

                        active_frames = np.linspace(start=0, stop=len(frames_data),
                                                    num=self.nframes_in_10khz_abf).astype(int)

                        mean_diff_active_frames = np.mean(np.diff(active_frames)) / self.abf.dataRate
                        if mean_diff_active_frames < 0.09:
                            raise Exception("mean_diff_active_frames < 0.09")
                        self.ci_frames_indices = active_frames
                        self.sampling_rate_calcium_imaging = 1 / (((self.timestamps_in_ms[self.ci_frames_indices[-1]] - \
                                                                    self.timestamps_in_ms[
                                                                        self.ci_frames_indices[0]]) / 1000) / len(
                            self.ci_frames_indices))
                        print(f"ABF to NWB: sampling rate calcium imaging {self.sampling_rate_calcium_imaging}")

                        # given the conversion factor to get the timestamps in sec
                        # we record them in ms to have a better precision

                        ci_frames_time_series = TimeSeries(
                            name="ci_frames",
                            data=np.transpose(self.ci_frames_indices),  # ci_frames_bool,
                            timestamps=np.array(self.timestamps_in_sec[self.ci_frames_indices]),
                            # self.timestamps_in_sec
                            # conversion=0.001,
                            unit='s')
                        # record the data as an acquisition
                        # to recover the data do: nwb_file.get_acquisition(name=name_channel)
                        self.nwb_file.add_acquisition(ci_frames_time_series)
                    else:
                        print(f"{self.n_imaging_blocks} imaging blocks given by abf yaml "
                              f"and {len(observed_long_gap_location)} blocks found in abf, "
                              f"linespace {int(self.nframes_in_10khz_abf / self.n_imaging_blocks)} frames per block ")

                        missed_frames = [expected_long_gap_location[i] - observed_long_gap_location[i]
                                         for i in range(self.n_imaging_blocks)]

                        missing_frames = [missed_frames[0], list(np.diff(missed_frames))]
                        print(f"N missing frames per imaging block: {missing_frames}")

                        active_frames = []
                        nframes_per_block = int(self.nframes_in_10khz_abf / self.n_imaging_blocks)

                        for imaging_block in range(self.n_imaging_blocks):
                            if imaging_block == 0:
                                stop_block = binary_frames_data_periods[observed_long_gap_location[imaging_block]][0]
                                print(f"Imaging block {imaging_block}: from t=0 s to "
                                      f"t={np.round(stop_block / self.abf.dataRate, decimals=2)} s")
                                active_frames = list(np.linspace(start=0, stop=stop_block, num=nframes_per_block).astype(int))
                            else:
                                start_block = binary_frames_data_periods[observed_long_gap_location[imaging_block-1]][1]
                                stop_block = binary_frames_data_periods[observed_long_gap_location[imaging_block]][0]
                                print(f"Imaging block {imaging_block}: "
                                      f"from t={np.round(start_block / self.abf.dataRate, decimals=2)} s to "
                                      f"t={np.round(stop_block / self.abf.dataRate, decimals=2)} s")
                                frames_to_add = list(np.linspace(start=start_block, stop=stop_block,
                                                                 num=nframes_per_block).astype(int))
                                active_frames = np.concatenate((active_frames, frames_to_add), axis=None)

                        active_frames = np.array(active_frames)

                        self.ci_frames_indices = active_frames
                        self.sampling_rate_calcium_imaging = 1 / (((self.timestamps_in_ms[self.ci_frames_indices[-1]] - \
                                                                    self.timestamps_in_ms[
                                                                        self.ci_frames_indices[0]]) / 1000) / len(
                            self.ci_frames_indices))
                        print(f"ABF to NWB: sampling rate calcium imaging {self.sampling_rate_calcium_imaging}")

                        # given the conversion factor to get the timestamps in sec
                        # we record them in ms to have a better precision

                        ci_frames_time_series = TimeSeries(
                            name="ci_frames",
                            data=np.transpose(self.ci_frames_indices),  # ci_frames_bool,
                            timestamps=np.array(self.timestamps_in_sec[self.ci_frames_indices]),
                            # self.timestamps_in_sec
                            # conversion=0.001,
                            unit='s')
                        # record the data as an acquisition
                        # to recover the data do: nwb_file.get_acquisition(name=name_channel)
                        self.nwb_file.add_acquisition(ci_frames_time_series)

        else:
            print(f"ABF sampling rate is at least 50 kHz")
            binary_frames_data = np.zeros(len(self.frames_data), dtype="int8")
            binary_frames_data[self.frames_data >= threshold_value] = 1
            binary_frames_data[self.frames_data < threshold_value] = 0
            # +1 due to the shift of diff
            # contains the index at which each frame from the movie is matching the abf signal
            # length should be 12500
            self.ci_frames_indices = np.where(np.diff(binary_frames_data) == 1)[0] + 1
            # then we want to determine the size of the breaks between each movie segment if there are some
            diff_active_frames = np.diff(self.ci_frames_indices)
            # calculating the gap threshold above which we estimate the movie recording has been on hold
            median_bw_two_frames = np.median(diff_active_frames)
            frames_gap_threshold = median_bw_two_frames + 5 * np.std(diff_active_frames)  # 5 is usually good
            self.gap_indices = np.where(diff_active_frames > frames_gap_threshold)[0]
            # first we calculate the sampling rate of the movie
            print(f"N Gaps in CI movie: {len(self.gap_indices)}")
            if len(self.gap_indices) == 0:
                self.sampling_rate_calcium_imaging = 1 / (((self.timestamps_in_ms[self.ci_frames_indices[-1]] -
                                                            self.timestamps_in_ms[self.ci_frames_indices[0]]) / 1000) / len(
                    self.ci_frames_indices))
            else:
                # contains the sampling rate of each movie recorded
                movies_sampling_rate = []
                for i, gap_index in enumerate(self.gap_indices):
                    first_frame_segment = 0 if i == 0 else self.gap_indices[i - 1] + 1
                    # estimating the sampling rate of the movie
                    segment_time_in_ms = self.timestamps_in_ms[self.ci_frames_indices[gap_index]] - \
                                         self.timestamps_in_ms[self.ci_frames_indices[first_frame_segment]]
                    movies_sampling_rate.append(1 / ((segment_time_in_ms / 1000) / (gap_index - first_frame_segment + 1)))
                    # print(f"movie_sampling_rate {movie_sampling_rate} Hz")
                    # print(f"gap in frames {gap_in_sec*movie_sampling_rate}")

                # estimating the sampling rate of the movie on the last segment
                segment_time_in_ms = self.timestamps_in_ms[self.ci_frames_indices[-1]] - \
                                     self.timestamps_in_ms[self.ci_frames_indices[self.gap_indices[-1] + 1]]
                movies_sampling_rate.append(
                    1 / ((segment_time_in_ms / 1000) / (len(self.ci_frames_indices) - (self.gap_indices[-1] + 1))))
                self.sampling_rate_calcium_imaging = np.mean(movies_sampling_rate)
            print(f"Movie sampling rate: {self.sampling_rate_calcium_imaging} Hz")

            # given the conversion factor to get the timestamps in sec
            # we record them in ms to have a better precision
            # ci_frames_bool = np.zeros(len(self.timestamps_in_sec), dtype='bool')
            # ci_frames_bool[self.ci_frames_indices] = True
            ci_frames_time_series = TimeSeries(
                name="ci_frames",
                data=np.transpose(self.ci_frames_indices),  # ci_frames_bool,
                timestamps=np.array(self.timestamps_in_sec[self.ci_frames_indices]),  # self.timestamps_in_sec
                # conversion=0.001,
                unit='s')
            # record the data as an acquisition
            # to recover the data do: nwb_file.get_acquisition(name=name_channel)
            self.nwb_file.add_acquisition(ci_frames_time_series)

            if (not self.fusion_movie_segments) and (len(self.gap_indices) > 0):
                # pause_time_intervals = TimeIntervals
                columns_pause = []
                columns_pause.append({"name": "start_time", "description": "Start time of epoch, in seconds"})
                columns_pause.append({"name": "stop_time", "description": "Stop time of epoch, in seconds"})
                columns_pause.append({"name": "start_original_frame",
                                      "description": "Frame after which the pause starts, using frames from the"
                                                     "original concatenated movie"})
                columns_pause.append({"name": "stop_original_frame",
                                      "description": "Frame at which the pause ends, using frames from the "
                                                     "original concatenated movie"})
                pause_time_intervals = self.nwb_file.create_time_intervals(name="ci_recording_on_pause",
                                                                           description='Intervals that correspond to '
                                                                                       'the time of last frame recorded '
                                                                                       'before the pause, and stop_time '
                                                                                       'is the time of the first frame '
                                                                                       'recorded after the pause, during calcium imaging'
                                                                                       'recording.',
                                                                           columns=columns_pause)
                for i, gap_index in enumerate(self.gap_indices):
                    # print(f"gap_index {gap_index}")
                    # gap_in_ms = self.timestamps_in_ms[self.ci_frames_indices[gap_index + 1]] - \
                    #              self.timestamps_in_ms[self.ci_frames_indices[gap_index]]
                    # gap_in_frames = (gap_in_ms / 1000) * self.sampling_rate_calcium_imaging
                    # the gap in frames is rounded in the floor.

                    # we save as a TimeInterval the interval during which the calcium imaging movie recording
                    # is on pause. First value is the time of last frame recorded before the pause, and stop_time
                    # is the time of the first frame recorded after the pause
                    # print("self.nwb_file.add_epoch")
                    # issue with add_epoch, it does work but after saving, when loading the nwb_file, there is no
                    # epoch. Solution using add_time_intervals inspired by this issue
                    # https://github.com/NeurodataWithoutBorders/pynwb/issues/958
                    # TODO: See to report an issue on the github
                    # self.nwb_file.add_epoch(start_time=self.timestamps_in_sec[self.ci_frames_indices[gap_index]],
                    #                         stop_time=self.timestamps_in_sec[self.ci_frames_indices[gap_index + 1]],
                    #                         timeseries=ci_frames_time_series,
                    #                         tags=['ci_recording_on_pause'])
                    data_dict = {}
                    data_dict["start_time"] = self.timestamps_in_sec[self.ci_frames_indices[gap_index]]
                    data_dict["stop_time"] = self.timestamps_in_sec[self.ci_frames_indices[gap_index + 1]]
                    data_dict["start_original_frame"] = gap_index
                    data_dict["stop_original_frame"] = gap_index + 1
                    pause_time_intervals.add_row(data_dict)

                    # we add those intervals during which the CI recording is on pause as invalid_time
                    # so those time intervals will be removed from analysis'
                    self.nwb_file.add_invalid_time_interval(
                        start_time=self.timestamps_in_sec[self.ci_frames_indices[gap_index]],
                        stop_time=self.timestamps_in_sec[self.ci_frames_indices[gap_index + 1]])

    def detect_run_periods(self, run_data, min_speed):
        """
        Using the data from the abf regarding the speed of the animal on the treadmill, return the speed in cm/s
        at each timestamps as well as period when the animal is moving (using min_speed threshold)

        Args:
            run_data (list): Data from the subject run
            min_speed (float): Minimum speed

        Returns:
            mvt_periods (list): List of movements periods
            speed_during_movement_periods (list) : List of subject speed during movements
            speed_by_time (list) : List of subject speed by time

        """
        nb_period_by_wheel = 500
        wheel_diam_cm = 2 * math.pi * 1.75
        cm_by_period = wheel_diam_cm / nb_period_by_wheel
        binary_mvt_data = np.zeros(len(run_data), dtype="int8")
        speed_by_time = np.zeros(len(run_data))
        is_running = np.zeros(len(run_data), dtype="int8")

        binary_mvt_data[run_data >= 4] = 1
        d_times = np.diff(binary_mvt_data)
        pos_times = np.where(d_times == 1)[0] + 1
        for index, pos in enumerate(pos_times[1:]):
            run_duration = pos - pos_times[index - 1]
            run_duration_s = run_duration / self.abf.dataRate
            # in cm/s
            speed = cm_by_period / run_duration_s
            if speed >= min_speed:
                speed_by_time[pos_times[index - 1]:pos] = speed
                is_running[pos_times[index - 1]:pos] = 1

        #  1024 cycle = 1 tour de roue (= 2 Pi 1.5) -> Vitesse (cm / temps pour 1024 cycles).
        # the period of time between two 1 represent a run
        mvt_periods = get_continous_time_periods(is_running)
        mvt_periods = merging_time_periods(time_periods=mvt_periods,
                                           min_time_between_periods=0.5 * self.abf.dataRate)

        speed_during_mvt_periods = []
        for period in mvt_periods:
            speed_during_mvt_periods.append(speed_by_time[period[0]:period[1] + 1])
        return mvt_periods, speed_during_mvt_periods, speed_by_time

    def process_run_data(self, run_channel):
        """
        Using the information in run_channel, will add to the nwb_file the speed of the subject at each acquisition
        frame of the movie in cm/s

        Args:
            run_channel (int) : Run channel

        """
        self.abf.setSweep(sweepNumber=0, channel=run_channel)
        run_data = self.abf.sweepY
        mvt_periods, speed_during_mvt_periods, speed_by_time = \
            self.detect_run_periods(run_data=run_data, min_speed=0.5)

        # Create a Speed Signal and Save it for display BADASS GUI
        speed_signal_name = "SpeedSignal"
        speed_by_time_signal = speed_by_time
        speed_by_time_signal_timestamps = self.timestamps_speed_in_sec

        final_speed_sr = 1000
        downsampling_step = int(self.abf.dataRate / final_speed_sr)
        # down-sample like we don't care
        speed_signal = speed_by_time_signal[0::downsampling_step]
        speed_signal_ts = speed_by_time_signal_timestamps[0::downsampling_step]

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

        behavior_timeseries.create_timeseries(name=speed_signal_name, data=np.transpose(speed_signal), unit='cm/s',
                                              starting_time=speed_signal_ts[0],
                                              rate=float(final_speed_sr),
                                              description='Mouse speed from abf file down-sampled at 1kHz')
        print(f"Creating 'SpeedSignal' signal for display purpose in BADASS")

        # Create Speed at each imaging frame for analysis and Save it as a time serie
        speed_by_frame = speed_by_time[self.ci_frames_indices + self.first_frame_index]

        behavior_timeseries.create_timeseries(name='running_speed_by_frame', data=np.transpose(speed_by_frame),
                                              description='Mouse speed on the belt at each imaging frame',
                                              timestamps=np.array(self.timestamps_in_sec[self.ci_frames_indices]),
                                              unit='cm/s')
        print(f"Creating 'running_speed_by_frame' time series "
              f"(the speed at each frame acquisition in cm/s) for analysis purpose")

    def compute_position(self, run_data, direction_data, belt_length):
        n_bins = len(run_data)
        distance = np.zeros(n_bins, dtype=float)

        nb_period_by_wheel = 500
        wheel_diam_cm = 2 * math.pi * 1.75
        cm_by_period = wheel_diam_cm / nb_period_by_wheel

        binary_mvt_data = np.zeros(len(run_data), dtype="int8")
        binary_mvt_data[run_data >= 4] = 1
        d_times = np.diff(binary_mvt_data)
        pos_times = np.where(d_times == 1)[0] + 1

        correlation_time_ms = 25
        window_size = int((correlation_time_ms / 1000) * self.abf.dataRate)
        for index, pos_bin in enumerate(pos_times[1:]):
            # Find the mouse direction: based on phase shift between speed channel et direction channel
            window_start = max(0, (pos_bin - window_size))
            window_stop = min((pos_bin + window_size), n_bins)
            position_ch1 = run_data[window_start: window_stop]
            position_ch2 = direction_data[window_start: window_stop]
            xcorr_vect = np.correlate(position_ch1, position_ch2, mode="full")
            xcorr_vect_center = (len(xcorr_vect) - 1) / 2
            max_corr = np.argmax(xcorr_vect)
            if xcorr_vect_center >= max_corr:
                direction = 1
            else:
                direction = -1

            # Increment mouse position:
            #  add cm_by_period each time we find the onset of a period and reset distance to 0 at belt length
            distance[pos_times[index - 1]:pos_bin] = distance[pos_times[index - 1] - 1] + direction * cm_by_period
            if distance[pos_times[index - 1] - 1] + direction * cm_by_period > belt_length:
                distance[pos_times[index - 1]:pos_bin] = distance[pos_times[index - 1]:pos_bin] - belt_length

        return distance

    def process_position_data(self, run_channel, direction_channel, belt_length):
        # Open speed channel
        self.abf.setSweep(sweepNumber=0, channel=run_channel)
        run_data = self.abf.sweepY
        # Open direction channel
        self.abf.setSweep(sweepNumber=0, channel=direction_channel)
        direction_data = self.abf.sweepY

        position_by_time = self.compute_position(run_data=run_data, direction_data=direction_data,
                                                 belt_length=belt_length)

        # Create a Position Signal and Save it for display BADASS GUI
        position_signal_name = "PositionSignal"
        position_by_time_signal = position_by_time
        position_by_time_signal_timestamps = self.timestamps_speed_in_sec

        final_pos_sr = 1000
        downsampling_step = int(self.abf.dataRate / final_pos_sr)
        # downsample like we don't care
        position_signal = position_by_time_signal[0::downsampling_step]
        position_signal_ts = position_by_time_signal_timestamps[0::downsampling_step]

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
        behavior_timeseries.create_timeseries(name=position_signal_name, data=np.transpose(position_signal),
                                              unit="cm/s", starting_time=position_signal_ts[0],
                                              rate=float(final_pos_sr),
                                              description='Mouse position from abf file down-sampled at 1kHz')
        print(f"Creating 'PositionSignal' signal for display purpose in BADASS")

        # Create Position at each imaging frame for analysis and Save it as a time serie
        position_by_frame = position_by_time[self.ci_frames_indices + self.first_frame_index]

        # Add position as recommended: https://pynwb.readthedocs.io/en/latest/pynwb.behavior.html
        if 'behavior' in self.nwb_file.processing:
            behavior_nwb_module = self.nwb_file.processing['behavior']
        else:
            behavior_nwb_module = self.nwb_file.create_processing_module(name="behavior",
                                                                         description="behavioral data")
        try:
            mouse_position = behavior_nwb_module.get(name='Position')
        except KeyError:
            mouse_position = Position(name='Position')
            behavior_nwb_module.add_data_interface(mouse_position)

        mouse_position.create_spatial_series(name="mouse_position", data=np.transpose(position_by_frame),
                                             reference_frame="Zero is the belt stitching",
                                             timestamps=np.array(self.timestamps_in_sec[self.ci_frames_indices]),
                                             description="Absolute position (in cm) of the mouse on the "
                                                         "belt at each imaging frame",
                                             control=None, control_description=None)

        print(f"Creating 'Position' spatial time series named 'mouse_position' "
              f"(the position at each frame acquisition in cm) for analysis purpose")









