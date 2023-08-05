from girafe.analysis.girafe_analysis_format_wrapper import GirafeAnalysisFormatWrapper
from pynwb.ophys import ImageSegmentation, TwoPhotonSeries, Fluorescence, PlaneSegmentation, DfOverF
from pynwb.image import ImageSeries
from pynwb.base import TimeSeries
import os
from pynwb import NWBHDF5IO
import numpy as np


class GirafeAnalysisNwbWrapper(GirafeAnalysisFormatWrapper):

    DATA_FORMAT = "CI_DATA"

    WRAPPER_ID = "NWB_CI"

    """
    Allows to communicate with the nwb format
    """

    def __init__(self, data_ref, load_data=True):
        GirafeAnalysisFormatWrapper.__init__(self, data_ref=data_ref, data_format="nwb", load_data=load_data)
        self._nwb_data = None
        if self.load_data_at_init:
            self.load_data()

    @staticmethod
    def is_data_valid(data_ref):
        """
        Check if the data can be an input for this wrapper as data_ref
        Args:
            data_ref: file or directory

        Returns: a boolean

        """
        if not os.path.isfile(data_ref):
            return False

        if data_ref.endswith(".nwb"):
            return True

        return False

    def load_data(self):
        GirafeAnalysisFormatWrapper.load_data(self)
        io = NWBHDF5IO(self._data_ref, 'r')
        self._nwb_data = io.read()
        # if we close it, then later on we have an exception such as: ValueError: Not a dataset (not a dataset)
        # io.close()

    @staticmethod
    def grouped_by():
        """
        Indicate by which factor the data can be grouped
        ex: age, species, contains behavior, categories of age..
        :return: a dictionary with key the name of the group (str) that will be displayed in the GUI, and as value
        the a sring representing either an argument or a method of the wrapper class (hasattr() and callable() will be
        use to get them)
        """
        groups_dict = dict()

        groups_dict["Age"] = "age_sort"
        groups_dict["Genotype"] = "genotype"
        groups_dict["Species"] = "species"
        groups_dict["Subject ID"] = "subject_id"
        groups_dict["Sex"] = "sex"
        groups_dict["Weight"] = "weight"
        # with or without behavior and if from piezzo or camera and manual or citnps
        groups_dict["Behavior epochs status"] = "behavior_epochs_status"
        groups_dict["Raster status"] = "raster_status"
        groups_dict["Cell type status"] = "cell_types_status"
        groups_dict["CI pause status"] = "ci_pause_status"
        groups_dict["With red ins cell type"] = "with_red_ins_cell_type"
        groups_dict["ABF status"] = "abf_status"
        groups_dict["FOV plan location"] = "image_plane_location"
        groups_dict["Belt type"] = "belt_type"

        return groups_dict

    # --------------------------------------------------------
    # --------------------------------------------------------
    #  Methods for menu grouping sessions
    # --------------------------------------------------------
    # --------------------------------------------------------
    def behavior_epochs_status(self):
        behavior_epochs_names = self.get_behavioral_epochs_names()
        if len(behavior_epochs_names) == 0:
            return "No behavior epochs"

        # check if there is a behavior movie
        behavior_movies = self.get_behavior_movies()
        if len(behavior_movies) == 0:
            return "Behavior epochs from piezo"

        # then we look in epoch names from "twitches" it means it comes from CITNPS
        if "twitches" in behavior_epochs_names:
            return "Behavior epochs from CITNPS"

        return "Behavior epochs with manual GT"

    def abf_status(self):
        """
        Using neuronal data and timestamps to infer if the abf has been used to create the NWB
        :return:
        """
        roi_response_series_dict = self.get_roi_response_series()
        for ophys_name, ophys_dict in roi_response_series_dict.items():
            for fluo_name, roi_response_series in ophys_dict.items():
                for roi_response_name in roi_response_series:
                    if "raster" in roi_response_name.lower():
                        neuronal_data_timestamps = self.get_roi_response_serie_timestamps(keys=[ophys_name, fluo_name,
                                                                                                roi_response_name],
                                                                                          verbose=False)
                        if (len(neuronal_data_timestamps) > 2) and \
                                (neuronal_data_timestamps[1] - neuronal_data_timestamps[0] != 1):
                            return "With ABF"
        return "No ABF"

    def with_red_ins_cell_type(self):
        cell_types = self.get_all_cell_types()
        if len(cell_types) == 0:
            return "Without red INs"

        if "red_ins" in cell_types:
            return "With red INs"
        return "Without red INs"

    def ci_pause_status(self):
        if 'ci_recording_on_pause' in self.get_intervals_names():
            return "CI on pause epochs"

        return "No CI on pause"

    def raster_status(self):
        roi_response_series_dict = self.get_roi_response_series()
        for ophys_name, ophys_dict in roi_response_series_dict.items():
            for fluo_name, roi_response_series in ophys_dict.items():
                for roi_response_name in roi_response_series:
                    if "raster" in roi_response_name.lower():
                        return "Raster available"
        return "no raster"

    def cell_types_status(self):
        """
        Return the cells types in a string, or a message saying no cell types
        :return:
        """
        cell_types = self.get_all_cell_types()
        if len(cell_types) == 0:
            return "NA"

        return ", ".join(cell_types)

    def image_plane_location(self):
        img_plan = self.get_imaging_plan_location(only_2_photons=True)
        if img_plan is None:
            return "NA"
        return img_plan

    def belt_type(self):
        belt_type = self.get_belt_type()
        return belt_type

    def age_sort(self):
        nwb_age = self._nwb_data.subject.age
        return nwb_age

    # --------------------------------------------------------
    # --------------------------------------------------------
    #  End methods for menu grouping sessions
    # --------------------------------------------------------
    # --------------------------------------------------------

    @property
    def identifier(self):
        return self._nwb_data.identifier

    @property
    def age(self):
        """
            Age of the subject (int), in days or months
            :return: None if age unknown, int otherwise, months or days is found with age_unit
        """
        nwb_age = self._nwb_data.subject.age
        if nwb_age in [None, '', ' ']:
            return None
        else:
            int_age = nwb_age[1: -1]

            try:
                return int(int_age)
            except ValueError:
                return int_age

    @property
    def age_unit(self):
        """
            Unit for the animal age
            :return:'D' for days, 'M' for months
        """
        nwb_age = self._nwb_data.subject.age
        if nwb_age in [None, '', ' ']:
            return None
        else:
            age_scale = nwb_age[-1]

        return age_scale

    @property
    def genotype(self):
        """
            Genotype of the subject
            :return: None if age unknown
        """
        return self._nwb_data.subject.genotype

    @property
    def species(self):
        """
            Species of the subject
            :return: None if age unknown
        """
        return self._nwb_data.subject.species

    @property
    def subject_id(self):
        """
         Id of the subject
         :return: None if subject_id unknown
        """
        return self._nwb_data.subject.subject_id

    @property
    def session_id(self):
        """
         Id of the subject
         :return: None if subject_id unknown
        """
        return self._nwb_data.session_id

    @property
    def weight(self):
        """
         Id of the subject
         :return: None if weight unknown
        """
        weight = self._nwb_data.subject.weight
        if weight in [None, '', ' ']:
            return None
        else:
            return weight

    @property
    def sex(self):
        """
         Sex (gender) of the subject
         :return: None if sex unknown
        """
        return self._nwb_data.subject.sex

    @property
    def lab(self):
        return self._nwb_data.lab

    @property
    def experimenter(self):
        if self._nwb_data.experimenter is not None:
            return self._nwb_data.experimenter[0]

    def get_segmentations(self):
        """

        Returns: a dict that for each step till plane_segmentation represents the different option.
        First dict will have as keys the name of the modules, then for each modules the value will be a new dict
        with keys the ImageSegmentation names and then the value will be a list representing the segmentation plane

        """
        segmentation_dict = dict()
        for name_mod, mod in self._nwb_data.modules.items():
            segmentation_dict[name_mod] = dict()
            no_keys_added = True
            for key, value in mod.data_interfaces.items():
                # we want to check that the object in Module is an Instance of ImageSegmentation
                if isinstance(value, ImageSegmentation):
                    no_keys_added = False
                    image_seg = value
                    # key is the name of segmentation, and value a list of plane_segmentation
                    segmentation_dict[name_mod][key] = []
                    # print(f"get_segmentations {name_mod} key {key}")
                    for plane_seg_name in image_seg.plane_segmentations.keys():
                        # print(f"get_segmentations plane_seg_name {plane_seg_name}")
                        segmentation_dict[name_mod][key].append(plane_seg_name)
            if no_keys_added:
                del segmentation_dict[name_mod]

        # it could be empty, but if it would matter, it should have been check by method check_data in GirafeAnalysis
        return segmentation_dict

    def get_signals_info(self):
        """

            Returns: a dict that for each step till the TimeSeries name represents the different option.
            First dict will have as keys the name of the modules, then for each modules the value will be
            the name of the TimeSeries representing the signal

        """
        signal_dict = dict()
        for name_mod, mod in self._nwb_data.modules.items():
            signal_dict[name_mod] = []
            no_keys_added = True
            for key, value in mod.data_interfaces.items():
                # we want to check that the object in Module is an Instance of Timeseries
                if isinstance(value, TimeSeries):
                    signal_dict[name_mod].append(key)
                    no_keys_added = False
            if no_keys_added:
                del signal_dict[name_mod]

        return signal_dict

    def get_signal_by_keyword(self, keyword, exact_keyword=False):
        """
        Look for a signal with this keyword. Returns the first instance found that matches it.
        Args:
            keyword: (str)
            exact_keyword: (bool) if True, the name of the TimeSeries representing the signal should be the same
            as keyword, otherwise keyword should be in the name of the TimeSeries

        Returns: a two 1d array representing a signal and its timestamps.
            If no sginal with this keyword found, return None, None

        """
        for name_mod, mod in self._nwb_data.modules.items():
            for key, value in mod.data_interfaces.items():
                # we want to check that the object in Module is an Instance of TimeSeries
                if isinstance(value, TimeSeries):
                    valid_key = False
                    if exact_keyword:
                        if keyword == key:
                            valid_key = True
                    else:
                        if keyword in key:
                            valid_key = True
                    if valid_key:
                        data = np.array(value.data)
                        timestamps = value.timestamps
                        if timestamps is None:
                            timestamps = (np.arange(0, len(data)) * (1/value.rate)) + value.starting_time
                        return np.transpose(data), np.array(timestamps)

        return None, None

    def get_signal_keys(self):
        """
        Return a list of str representing the key of the signals available.
        Signals are TimeSeries instance registered as data interfaces in modules.
        Returns:

        """
        keys = []
        for name_mod, mod in self._nwb_data.modules.items():
            for key, value in mod.data_interfaces.items():
                # we want to check that the object in Module is an Instance of TimeSeries
                if isinstance(value, TimeSeries):
                    keys.append(key)

        return keys

    def get_roi_response_serie_data(self, keys):
        """

        Args:
            keys: lsit of string allowing to get the roi repsonse series wanted

        Returns:

        """
        if len(keys) < 3:
            return None

        if keys[0] not in self._nwb_data.modules:
            return None

        if keys[1] not in self._nwb_data.modules[keys[0]].data_interfaces:
            return None

        if keys[2] not in self._nwb_data.modules[keys[0]].data_interfaces[keys[1]].roi_response_series:
            return None

        return np.transpose(np.array(self._nwb_data.modules[keys[0]].
                                     data_interfaces[keys[1]].roi_response_series[keys[2]].data))

    def get_roi_response_serie_data_by_keyword(self, keys, keyword):
        """
        Return a dict with other last key data
        Args:
            keys: list of string allowing to get the  roi response series in data_interfaces
            keyword:
        Returns:
        """
        if len(keys) < 2:
            return dict()
        if keys[0] not in self._nwb_data.modules:
            return dict()
        if keys[1] not in self._nwb_data.modules[keys[0]].data_interfaces:
            return dict()
        result_dict = dict()
        for key_data, rrs in self._nwb_data.modules[keys[0]].data_interfaces[keys[1]].roi_response_series.items():

            if isinstance(keyword, str):
                if keyword in key_data:
                    result_dict[key_data] = np.transpose(np.array(rrs.data))

            all_key_in_key_data = []
            if isinstance(keyword, list):
                for key in keyword:
                    if key in key_data:
                        all_key_in_key_data.append('True')
                        continue
                    else:
                        all_key_in_key_data.append('False')

                if all(all_key_in_key_data):
                    result_dict[key_data] = np.transpose(np.array(rrs.data))
                    return result_dict
                else:
                    return dict()

        return result_dict

    def get_all_cell_types(self):
        """
        Return a list of all cell types identified in this session. If the list is empty, it means the type of the cells
        is not identified
        Returns:

        """
        cell_types = []
        for name_mod, mod in self._nwb_data.modules.items():
            for key, fluorescence in mod.data_interfaces.items():
                # we want to check that the object in Module is an Instance of pynwb.ophys.Fluorescence
                if isinstance(fluorescence, Fluorescence):
                    for name_rrs, rrs in fluorescence.roi_response_series.items():
                        cell_type_names = rrs.control_description
                        if cell_type_names is not None:
                            cell_types.extend(list(cell_type_names))
        # keeping only unique values
        return list(set(cell_types))

    def get_cell_indices_by_cell_type(self, roi_serie_keys):
        """
        Return a dict with key the cell_type name and value an array of int representing the cell indices of this type
        Args:
            roi_serie_keys:

        Returns:

        """
        rrs = self._get_roi_response_serie(keys=roi_serie_keys)
        if rrs is None:
            return {}

        # rrs.control is an array (uint8) as long as n_cells, with a code for each cell type
        # rrs.control_description is the list of cell type names, as long as n_cells
        if rrs.control_description is not None:
            cell_type_names = list(set(rrs.control_description))
        else:
            cell_type_names = []
        code_by_cell_type = dict()
        for cell_type_name in cell_type_names:
            index = list(rrs.control_description).index(cell_type_name)
            code_by_cell_type[cell_type_name] = rrs.control[index]

        cell_type_names.sort()

        cell_indices_by_cell_type = dict()
        for cell_type_name in cell_type_names:
            code = code_by_cell_type[cell_type_name]
            cell_indices_by_cell_type[cell_type_name] = np.where(np.array(rrs.control) == code)[0]

        return cell_indices_by_cell_type

    def _get_roi_response_serie(self, keys):
        """

        Args:
            keys: list of string allowing to get the roi repsonse series wanted

        Returns:

        """
        if len(keys) < 3:
            return None

        if keys[0] not in self._nwb_data.modules:
            return None

        if keys[1] not in self._nwb_data.modules[keys[0]].data_interfaces:
            return None

        if keys[2] not in self._nwb_data.modules[keys[0]].data_interfaces[keys[1]].roi_response_series:
            return None

        return self._nwb_data.modules[keys[0]].data_interfaces[keys[1]].roi_response_series[keys[2]]

    def get_roi_response_serie_timestamps(self, keys, verbose=True):
        """

        Args:
            keys: lsit of string allowing to get the roi repsonse series wanted
            verbose: print info

        Returns:

        """
        if len(keys) < 3:
            return None

        if keys[0] not in self._nwb_data.modules:
            return None

        if keys[1] not in self._nwb_data.modules[keys[0]].data_interfaces:
            return None

        if keys[2] not in self._nwb_data.modules[keys[0]].data_interfaces[keys[1]].roi_response_series:
            return None

        rrs = self._nwb_data.modules[keys[0]].data_interfaces[keys[1]].roi_response_series[keys[2]]

        rrs_ts = rrs.timestamps

        if rrs_ts is not None:
            if verbose:
                print(f"Timestamps directly provided for this RoiResponseSeries ({keys[2]})")
            return rrs_ts
        else:
            if verbose:
                print(f"Timestamps not directly provided for this RoiResponseSeries ({keys[2]})")
            rrs_start_time = rrs.starting_time
            rrs_rate = rrs.rate
            if (rrs_rate is not None) and (rrs_rate < 1):
                if verbose:
                    print(f"Found a rate of {np.round(rrs_rate, decimals=3)} Hz, assume it is in fact 1/rate. "
                          f"New rate: {np.round(1 / rrs_rate, decimals=2)} Hz.")
                rrs_rate = 1 / rrs_rate
            if (rrs_start_time is not None) and (rrs_rate is not None):
                if verbose:
                    print(f"Build timestamps from starting time ({rrs_start_time} s) and "
                          f"rate ({np.round(rrs_rate, decimals=2)} Hz)")
                n_times = rrs.data.shape[0]
                rrs_ts = (np.arange(0, n_times) * (1/rrs_rate)) + rrs_start_time
                return rrs_ts
            else:
                if verbose:
                    print(f"Starting time and rate not provided neither, no timestamps can be returned")
                return None

    def get_roi_response_series(self, keywords_to_exclude=None):
        """
                param:
                keywords_to_exclude: if not None, list of str, if one of neuronal data has this keyword,
                then we don't add it to the choices

                Returns: a list or dict of objects representing all roi response series (rrs) names
                rrs could represents raw traces, or binary raster, and its link to a given segmentation.
                The results returned should allow to identify the segmentation associated.
                Object could be strings, or a list of strings, that identify a rrs and give information
                how to get there.

        """
        rrs_dict = dict()
        for name_mod, mod in self._nwb_data.modules.items():
            rrs_dict[name_mod] = dict()
            for key, fluorescence in mod.data_interfaces.items():
                # we want to check that the object in Module is an Instance of pynwb.ophys.Fluorescence
                if (isinstance(fluorescence, Fluorescence)) or (isinstance(fluorescence, DfOverF)):
                    rrs_dict[name_mod][key] = []
                    for name_rrs, rrs in fluorescence.roi_response_series.items():
                        if keywords_to_exclude is not None:
                            to_exclude = False
                            for keyword in keywords_to_exclude:
                                if keyword in name_rrs:
                                    to_exclude = True
                                    break
                            if to_exclude:
                                continue
                        rrs_dict[name_mod][key].append(name_rrs)
                    if len(rrs_dict[name_mod][key]) == 0:
                        del rrs_dict[name_mod][key]
            if len(rrs_dict[name_mod]) == 0:
                del rrs_dict[name_mod]

        # then we remove modules without Fluorescence instances
        # keys_to_remove = []
        # for key, value_dict in rrs_dict.items():
        #     if len(value_dict) == 0:
        #         keys_to_remove.append(key)
        # for key in keys_to_remove:
        #     del rrs_dict[key]
        return rrs_dict

    def get_roi_response_series_list(self, keywords_to_exclude=None):
        """
                param:
                keywords_to_exclude: if not None, list of str, if one of neuronal data has this keyword,
                then we don't add it to the list

                Returns: a list with all roi response series (rrs) names

        """
        rrs_names_list = []
        for name_mod, mod in self._nwb_data.modules.items():
            for key, fluorescence in mod.data_interfaces.items():
                # we want to check that the object in Module is an Instance of pynwb.ophys.Fluorescence
                if (isinstance(fluorescence, Fluorescence)) or (isinstance(fluorescence, DfOverF)):
                    for name_rrs, rrs in fluorescence.roi_response_series.items():
                        if keywords_to_exclude is not None:
                            to_exclude = False
                            for keyword in keywords_to_exclude:
                                if keyword in name_rrs:
                                    to_exclude = True
                                    break
                            if to_exclude:
                                continue
                        rrs_names_list.append(name_rrs)
        rrs_list_names = np.unique(rrs_names_list)
        return rrs_list_names

    def get_pixel_mask(self, segmentation_info):
        """
        Return pixel_mask which is a list of list of pair of integers representing the pixels coordinate (x, y) for each
        cell. the list length is the same as the number of cells.
        Args:
            segmentation_info: a list of 3 elements: first one being the name of the module, then the name
            of image_segmentation and then the name of the segmentation plane.

        Returns:

        """
        if len(segmentation_info) < 3:
            return None

        name_module = segmentation_info[0]
        mod = self._nwb_data.modules[name_module]

        name_mode = segmentation_info[1]
        name_plane_seg = segmentation_info[2]
        plane_seg = mod[name_mode].get_plane_segmentation(name_plane_seg)

        if 'pixel_mask' in plane_seg:
            print("Found pixel mask in plane segmentation")
            return plane_seg['pixel_mask']
        else:
            print("No pixel mask found in plane segmentation")
            if 'image_mask' not in plane_seg:
                print(f"No image mask found in plane segmentation")
                return None
            else:
                print("Found image mask in plane segmentation: Convert it to pixel mask")
                img_mask = plane_seg['image_mask']
                img_mask_data = img_mask[:]
                image_masks = list(img_mask_data)
                n_cells = len(image_masks)
                pixel_masks = []
                print(f"{n_cells} image masks to convert to pixel masks")
                for cell in range(n_cells):
                    if (cell > 0) and (cell % 250 == 0):
                        print(f"{cell} cells converted")
                    img_mask = image_masks[cell]
                    pixel_mask = PlaneSegmentation.image_to_pixel(img_mask)
                    pixel_masks.append(pixel_mask)
                return pixel_masks

    def contains_ci_movie(self, consider_only_2_photons):
        """
        Indicate if the data object contains at least one calcium imaging movie represented by an instance of
        pynwb.image.ImageSeries
        Args:
            consider_only_2_photons: boolean, it True means we consider only 2 photons calcium imaging movies,
            if other exists but not 2 photons, then False will be return
        Returns: True if it's the case, False otherwise

        """
        # a TwoPhotonSeries is an instance of ImageSeries
        has_one = False
        for key, acquisition_data in self._nwb_data.acquisition.items():
            if consider_only_2_photons:
                if isinstance(acquisition_data, TwoPhotonSeries):
                    has_one = True
            else:
                if isinstance(acquisition_data, ImageSeries):
                    has_one = True
        if not has_one:
            return False

        return True

    def get_behavior_movies(self, key_to_identify="behavior"):
        """
                Return a dict with as key a string identifying the movie, and as value a dict of behavior movies
                a string as file_name if external, or a 3d array
                Args:
                    key_to_identify: string, key to identify that a movie is a behavior movie

                Returns:

        """
        behavior_movies_dict = dict()
        # print(f"self._nwb_data.acquisition.keys() {list(self._nwb_data.acquisition.keys())}")
        for key, acquisition_data in self._nwb_data.acquisition.items():
            if key_to_identify not in key:
                continue
            if isinstance(acquisition_data, ImageSeries):
                image_series = acquisition_data
                if image_series.format == "external":
                    movie_file_name = image_series.external_file[0]
                    movie_data = movie_file_name
                    behavior_movies_dict[key] = movie_data

        return behavior_movies_dict

    def get_ci_movies(self, only_2_photons):
        """
        Return a dict with as key a string identifying the movie, and as value a dict of CI movies
        a string as file_name if external, or a 3d array
        Args:
            only_2_photons: return only the 2 photon movies

        Returns:

        """
        ci_movies_dict = dict()

        for key, acquisition_data in self._nwb_data.acquisition.items():
            if only_2_photons:
                if isinstance(acquisition_data, ImageSeries) and \
                        (not isinstance(acquisition_data, TwoPhotonSeries)):
                    continue

            if isinstance(acquisition_data, ImageSeries):
                image_series = acquisition_data
                if image_series.format == "external":
                    movie_file_name = image_series.external_file[0]
                    movie_data = movie_file_name
                else:
                    movie_data = image_series.data
                ci_movies_dict[key] = movie_data

        return ci_movies_dict

    def get_ci_movies_sample(self, only_2_photons, n_frames=2000):
        """
        Return a dict with as key a string identifying the movie, and as value a dict of CI movies
        a string as file_name if external, or a 3d array
        Args:
            only_2_photons: return only the 2 photon movies
            n_frames: number of frames to take from movie to serve as data sample

        Returns:

        """
        ci_movies_dict = dict()

        for key, acquisition_data in self._nwb_data.acquisition.items():
            if only_2_photons:
                if isinstance(acquisition_data, ImageSeries) and \
                        (not isinstance(acquisition_data, TwoPhotonSeries)):
                    continue

            if isinstance(acquisition_data, ImageSeries):
                image_series = acquisition_data
                if image_series.format == "external":
                    movie_file_name = image_series.external_file[0]
                    movie_data = movie_file_name
                else:
                    if n_frames < len(image_series.data[:, 0, 0]):
                        movie_data = image_series.data[0:n_frames, :, :]
                    else:
                        movie_data = image_series.data[:]
                ci_movies_dict[key] = movie_data

        return ci_movies_dict

    def get_ci_movie_sampling_rate(self, only_2_photons=False, ci_movie_name=None):
        """

        Args:
            only_2_photons: if True only 2 photons one are considere
            ci_movie_name: (string) if not None, return the sampling rate for a given ci_movie, otherwise the first
            one found

        Returns: (float) sampling rate of the movie, return None if no movie is found

        """

        for key, acquisition_data in self._nwb_data.acquisition.items():
            if ci_movie_name is not None and (key != ci_movie_name):
                continue
            if only_2_photons:
                if isinstance(acquisition_data, ImageSeries) and \
                        (not isinstance(acquisition_data, TwoPhotonSeries)):
                    continue

            if isinstance(acquisition_data, ImageSeries):
                image_series = acquisition_data
                return image_series.rate

        return None

    def get_rrs_sampling_rate(self, keys):
        """

        Args:

        Returns: (float) sampling rate of the movie, return None if no sampling rate is found

        """
        rrs = self._get_roi_response_serie(keys=keys)

        sampling_rate = rrs.rate
        if sampling_rate is not None:
            print(f"Sampling rate is directly provided in {keys[2]}")
            print(f"Sampling rate: {sampling_rate} Hz")
            return sampling_rate
        else:
            print(f"Sampling rate is not directly provided in {keys[2]}:"
                  f" Estimate rate from timestamps of first 100 frames")
            rrs_ts_sample = rrs.timestamps[0: 100]
            if rrs_ts_sample is None:
                print(f"Found neither rate nor timestamps")
                return None
            else:
                sampling_rate = np.round(1 / (np.nanmedian(np.diff(rrs_ts_sample))), decimals=2)
                print(f"Sampling rate: {sampling_rate} Hz")
                return sampling_rate

    def get_identifier(self, session_data):
        """
        Get the identifier of one of the data to analyse
        Args:
            session_data: Data we want to know the identifier

        Returns: A hashable object identfying the data

        """
        return session_data.identifier

    def get_intervals_names(self):
        """
        Return a list representing the intervals contains in this data
        Returns:

        """
        if self._nwb_data.intervals is None:
            return []
        # TODO: include that it can be a generic table with different stimulation epochs with the same name ie 'epochs'
        # each name can contain a table with different epochs
        # (see NWBs from Allen)
        intervals = []
        for name_interval in self._nwb_data.intervals.keys():
            intervals.append(name_interval)
        return intervals

    def get_interval_as_data_frame(self, interval_name):
        """
        Return an interval time as a pandas data frame.
        Args:
            interval_name: Name of the interval to retrieve

        Returns: None if the interval doesn't exists or a pandas data frame otherwise

        """
        if interval_name not in self._nwb_data.intervals:
            return None
        return self._nwb_data.intervals[interval_name].to_dataframe()

    def get_interval_times(self, interval_name):
        """
        Return an interval times (start and stop in seconds) as a numpy array of 2*n_times.
        Args:
            interval_name: Name of the interval to retrieve

        Returns: None if the interval doesn't exists or a 2d array

        """
        if interval_name not in self._nwb_data.intervals:
            return None

        df = self._nwb_data.intervals[interval_name].to_dataframe()

        # TODO: See to make it more modulable in case someone will use another name
        if ("start_time" not in df) or \
                ("stop_time" not in df):
            return None
        # TODO: include that it can be a generic table with different stimulation epochs (see NWBs from Allen)
        # time series
        start_time_ts = df["start_time"]
        stop_time_ts = df["stop_time"]

        # it shouldn't be the case
        if len(start_time_ts) != len(stop_time_ts):
            print(f"len(start_time_ts) {len(start_time_ts)} != {len(stop_time_ts)} len(stop_time_ts)")
            return None

        data = np.zeros((2, len(start_time_ts)))
        data[0] = np.array(start_time_ts)
        data[1] = np.array(stop_time_ts)

        return data

    def get_behavioral_epochs_names(self):
        """
        The name of the different behavioral
        Returns:

        """
        if 'behavior' not in self._nwb_data.processing:
            if 'Behavior' not in self._nwb_data.processing:
                return []

        try:
            behavior_nwb_module = self._nwb_data.processing['behavior']
        except KeyError:
            behavior_nwb_module = self._nwb_data.processing['Behavior']

        try:
            behavioral_epochs = behavior_nwb_module.get(name='BehavioralEpochs')
        except KeyError:
            return []
        # a dictionary containing the IntervalSeries in this BehavioralEpochs container
        interval_series = behavioral_epochs.interval_series

        return list(interval_series.keys())

    def get_behavioral_epochs_times(self, epoch_name):
        """
        Return an interval times (start and stop in seconds) as a numpy array of 2*n_times.
        Args:
            epoch_name: Name of the interval to retrieve

        Returns: None if the interval doesn't exists or a 2d array

        """
        if 'behavior' not in self._nwb_data.processing:
            if 'Behavior' not in self._nwb_data.processing:
                return []

        try:
            behavior_nwb_module = self._nwb_data.processing['behavior']
        except KeyError:
            behavior_nwb_module = self._nwb_data.processing['Behavior']

        try:
            behavioral_epochs = behavior_nwb_module.get(name='BehavioralEpochs')
        except KeyError:
            return None
        # a dictionary containing the IntervalSeries in this BehavioralEpochs container
        interval_series = behavioral_epochs.interval_series

        if epoch_name not in interval_series:
            return None

        interval_serie = interval_series[epoch_name]

        # data: >0 if interval started, <0 if interval ended.
        # timestamps: Timestamps for samples stored in data
        # so far we use only one type of integer, but otherwise as describe in the doc:
        """
        Stores intervals of data. The timestamps field stores the beginning and end of intervals. 
        The data field stores whether the interval just started (>0 value) or ended (<0 value). 
        Different interval types can be represented in the same series by using multiple key values 
        (eg, 1 for feature A, 2 for feature B, 3 for feature C, etc). The field data stores an 8-bit integer. 
        This is largely an alias of a standard TimeSeries but that is identifiable as representing 
        time intervals in a machine-readable way.
        """
        data = interval_serie.data
        time_stamps = interval_serie.timestamps

        data = np.zeros((2, int(len(time_stamps) / 2)))
        index_data = 0
        for i in np.arange(0, len(time_stamps), 2):
            data[0, index_data] = time_stamps[i]
            data[1, index_data] = time_stamps[i+1]
            index_data += 1

        return data

    def get_interval_original_frames(self, interval_name):
        """
        Return an interval times (start and stop in frames) as a numpy array of 2*n_times.
        Args:
            interval_name: Name of the interval to retrieve

        Returns: None if the interval doesn't exists or a 2d array

        """
        if interval_name not in self._nwb_data.intervals:
            return None

        df = self._nwb_data.intervals[interval_name].to_dataframe()

        # TODO: See to make it more modulable in case someone will use another name
        if ("start_original_frame" not in df) or \
                ("stop_original_frame" not in df):
            return None

        # time series
        start_frame = df["start_original_frame"]
        stop_frame = df["stop_original_frame"]

        # it shouldn't be the case
        if len(start_frame) != len(stop_frame):
            print(f"len(start_time_ts) {len(start_frame)} != {len(stop_frame)} len(stop_time_ts)")
            return None

        data = np.zeros((2, len(start_frame)))
        data[0] = np.array(start_frame)
        data[1] = np.array(stop_frame)

        return data

    def __str__(self):
        """
        Return a string representing the session. Here session.identifier
        :return:
        """
        return self._nwb_data.identifier

    def get_behaviors_movie_time_stamps(self):
        """
        return a dict with key the cam id and value np.array with the timestamps of each frame of the behavior movie
        return None if non available
        Returns:

        """
        time_stamps_dict = dict()

        for name, acquisition_data in self._nwb_data.acquisition.items():
            if name.startswith("cam_"):
                time_stamps_dict[name] = np.array(acquisition_data.timestamps)

        return time_stamps_dict

    def get_ci_movie_time_stamps(self):
        """
        return a np.array with the timestamps of each frame of the CI movie
        return None if non available
        Returns:

        """
        if "ci_frames" not in self._nwb_data.acquisition:
            print(f"No 'ci frames' time serie in this NWB")
            return None
        ci_frames_time_serie = self._nwb_data.acquisition["ci_frames"]
        ci_frames_ts = ci_frames_time_serie.timestamps
        ci_frames_ts = ci_frames_ts[:]

        return ci_frames_ts

    def get_timestamps_range(self):
        """
        Return a tuple of float representing the first and last time stamp with movie recording
        (behavior or ci movie)
        Returns:

        """
        min_time_stamp = None
        max_time_stamp = 0
        ci_movie_time_stamps = self.get_ci_movie_time_stamps()
        if ci_movie_time_stamps is not None:
            max_time_stamp = max(max_time_stamp, np.max(ci_movie_time_stamps))
            min_time_stamp = np.min(ci_movie_time_stamps)

        behavior_time_stamps_dict = self.get_behaviors_movie_time_stamps()
        for behavior_name, behavior_time_stamps in behavior_time_stamps_dict.items():
            max_time_stamp = max(max_time_stamp, np.max(behavior_time_stamps))
            if min_time_stamp is None:
                min_time_stamp = np.min(behavior_time_stamps)
            else:
                min_time_stamp = min(min_time_stamp, np.min(behavior_time_stamps))

        return min_time_stamp, max_time_stamp

    def get_mouse_speed_info(self):
        """

        Returns:

        """
        # First start with what we were doing (changed 17/02/2022 in convert_abf_to_nwb)
        scan_nwb_file = False
        if "running_speed" in self._nwb_data.acquisition:
            print("Found 'running_speed' in acquisitions")
            mouse_speed = self._nwb_data.acquisition["running_speed"]
            # print(f"mouse_speed: {mouse_speed}")
            if mouse_speed.description is not None:
                print(f"Description: {mouse_speed.description}")
            speed = mouse_speed.data
            # print(f"speed: {speed}")
            speed_by_time = speed[:]
            if speed_by_time is not None:
                return np.transpose(speed_by_time)
            else:
                return None
        # Else look in 'BehavioralTimeSeries' (inspired by NWB from Giocomo lab NWBs found on DANDI)
        else:
            print("No 'speed' found as acquisition: Look for 'Speed' in "
                  "BehavioralTimeSeries in a 'behavior' processsing module")
            bhv_time_series_names = self.get_behavioral_time_series_names()
            good_name = None
            for bhv_time_series_name in bhv_time_series_names:
                if 'speed' in bhv_time_series_name:
                    good_name = bhv_time_series_name
                    break
            if good_name is not None:
                print(f"Get the '{good_name}' time series from 'BehavioralTimeSeries'")
                bhv = self._nwb_data.processing['behavior']
                bhv_timeseries = bhv.get(name='BehavioralTimeSeries')
                time_series = bhv_timeseries.time_series
                speed_times_series = time_series.get(good_name)
                if speed_times_series.description is not None:
                    print(f"Description: {speed_times_series.description}")
                speed_unit = speed_times_series.unit
                speed_data = speed_times_series.data[:]
                if speed_unit in ['m', 'm/s', 'm.s-1']:
                    speed_data = speed_data * 100
                return np.transpose(speed_data)
            else:
                print(f"No 'speed' found yet. Scan the NWB file")
                scan_nwb_file = True

        if scan_nwb_file:
            nwb_objects = self._nwb_data.objects
            objects_list = [data for key, data in nwb_objects.items()]
            data_to_take = None
            for ind, obj in enumerate(objects_list):
                if 'speed' in obj.name:
                    data_to_take = obj
                    break
                else:
                    continue
            if data_to_take is None:
                print(f"No object with 'speed' in its name found, return None")
                return None
            else:
                speed_data = data_to_take.data[:]
                prt = data_to_take.parent
                prt_name = prt.name
                prt_type = prt.neurodata_type
                prt_names_list = [prt_name]
                prt_type_list = [prt_type]
                while prt_type != "NWBFile":
                    up_prt = prt.parent
                    prt_names_list.append(up_prt.name)
                    prt_type_list.append(up_prt.neurodata_type)
                    prt_type = up_prt.neurodata_type
                    prt = up_prt
                print(f"Found a '{data_to_take.name}' {data_to_take.neurodata_type}. "
                      f"From 'parents' named : {prt_names_list} with type: {prt_type_list}")
                return np.transpose(speed_data)

    def get_mouse_position_info(self):
        """

        Returns:

        """
        if 'behavior' not in self._nwb_data.processing:
            return None
        scan_nwb_file = False
        # Start by what we are doing using the SpatialSeries in Position
        behavior_nwb_module = self._nwb_data.processing['behavior']
        try_from_bhv_timeseries = False
        try:
            position_spatial_series = behavior_nwb_module.get(name='Position')
        except KeyError:
            try_from_bhv_timeseries = True
            position_spatial_series = None

        if try_from_bhv_timeseries is False:
            mouse_position_spatial_series = position_spatial_series.get_spatial_series(name="mouse_position")
            print(f"Get the 'mouse_position' spatial series from 'SpatialSeries' in 'Position'")

            if mouse_position_spatial_series.description is not None:
                print(f"Description: {mouse_position_spatial_series.description}")

            position_by_time = mouse_position_spatial_series.data[:]

            if len(position_by_time) == 0:
                print(f"Length of found spatial series is 0, return None")
                return None

            return np.transpose(position_by_time)

        # Look for position in 'BehavioralTimeSeries' (Giocomo lab do this way)
        else:
            bhv_time_series_names = self.get_behavioral_time_series_names()
            good_name = None
            for bhv_time_series_name in bhv_time_series_names:
                if 'pos' in bhv_time_series_name:
                    good_name = bhv_time_series_name
                    break
            bhv = self._nwb_data.processing['behavior']
            try:
                bhv_timeseries = bhv.get(name='BehavioralTimeSeries')
            except KeyError:
                print(f"No 'BehavioralTimeSeries' return None")
                return None
            time_series = bhv_timeseries.time_series
            if good_name is not None:
                print(f"Get the '{good_name}' time series from 'BehavioralTimeSeries'")
                position_times_series = time_series.get(good_name)
                if position_times_series.description is not None:
                    print(f"Description: {position_times_series.description}")
                position = position_times_series.data[:]
                if position_times_series.unit in ['m', 'm/s', 'm.s-1']:
                    position = position * 100
                return np.transpose(position)
            else:
                print(f"No 'Position' found yet. Scan the NWB file")
                scan_nwb_file = True

        if scan_nwb_file:
            nwb_objects = self._nwb_data.objects
            objects_list = [data for key, data in nwb_objects.items()]
            data_to_take = None
            for ind, obj in enumerate(objects_list):
                if 'position' in obj.name:
                    data_to_take = obj
                    break
                else:
                    continue
            if data_to_take is None:
                print(f"No object with 'position' in its name found, return None")
                return None
            else:
                position_data = data_to_take.data[:]
                prt = data_to_take.parent
                prt_name = prt.name
                prt_type = prt.neurodata_type
                prt_names_list = [prt_name]
                prt_type_list = [prt_type]
                while prt_type != "NWBFile":
                    up_prt = prt.parent
                    prt_names_list.append(up_prt.name)
                    prt_type_list.append(up_prt.neurodata_type)
                    prt_type = up_prt.neurodata_type
                    prt = up_prt
                print(f"Found a '{data_to_take.name}' {data_to_take.neurodata_type}. "
                      f"From 'parents' named : {prt_names_list} with type: {prt_type_list}")
                return np.transpose(position_data)

    def get_opto_stimulation_time_serie(self):
        # TODO: put ogen in a much proper way when we'll do ogen experiment
        """

        Returns:

        """
        if "ogen_stim" not in self._nwb_data.acquisition:
            return None
        ogen_stim = self._nwb_data.acquisition["ogen_stim"]
        opto_stim = ogen_stim.data
        opto_stm_ts = ogen_stim.timestamps
        optogenetic_stim = opto_stim[:]
        optogenetic_stim_ts = opto_stm_ts[:]

        return optogenetic_stim, optogenetic_stim_ts

    def get_acquisition_names(self):
        """

        Returns:

        """

        acquisitions = self._nwb_data.acquisition
        names = acquisitions.keys()
        names_list = list(names)

        return names_list

    def get_ci_movie_dimension(self, only_2_photons=False, ci_movie_name=None):
        # Try to get dimensions from TwoPhotonSeries.dimension
        for key, acquisition_data in self._nwb_data.acquisition.items():
            if ci_movie_name is not None and (key != ci_movie_name):
                continue
            if only_2_photons:
                if isinstance(acquisition_data, ImageSeries) and \
                        (not isinstance(acquisition_data, TwoPhotonSeries)):
                    continue

            if isinstance(acquisition_data, ImageSeries):
                image_series = acquisition_data
                dimensions = image_series.dimension[:]
                # dimensions should be n_times x n_lines x n_cols ('z', 'y', 'x' when open in Fiji)
                if len(dimensions) == 3:
                    print(f"Found 3 dimensions in 'TwoPhotonSeries.dimension': assume it is n_times x n_lines x n_cols")
                    n_lines = image_series.dimension[1]
                    n_cols = image_series.dimension[2]

                if len(dimensions) == 2:
                    # mean it is likely that number of frames is not given
                    print(f"Found only 2 dimensions in 'TwoPhotonSeries.dimension': "
                          f"take them as n_lines x n_cols if it is a square")
                    n_lines = image_series.dimension[0]
                    n_cols = image_series.dimension[1]
                    if n_lines != n_cols:
                        print(f"The 2 dimensions are not the same: not sure which one is 'n_lines' / 'n_cols'")
                        n_lines = None
                        n_cols = None

                if (n_lines is not None) and (n_cols is not None):
                    print(f"Dimensions extracted")
                    return n_lines, n_cols
                else:
                    print(f"Try to get the dimensions from 'tiff' movie shape")
                    n_lines = image_series.data[0, :, :].shape[0]
                    n_cols = image_series.data[0, :, :].shape[1]
                    if (n_lines is not None) and (n_cols is not None):
                        print(f"Dimensions of CI movie given from shape of 'tiff' data")
                        return n_lines, n_cols
                    else:
                        print(f"No dimension returned")
                        return None, None

    def get_ci_dimension_from_img_mask(self, segmentation_info):
        if len(segmentation_info) < 3:
            return None

        name_module = segmentation_info[0]
        mod = self._nwb_data.modules[name_module]

        name_mode = segmentation_info[1]
        name_plane_seg = segmentation_info[2]
        plane_seg = mod[name_mode].get_plane_segmentation(name_plane_seg)

        if 'image_mask' not in plane_seg:
            print("No 'image_mask' provided to extract image size")
            return None, None
        else:
            img_mask = plane_seg['image_mask']
            img_mask_data = img_mask[:]
            image_masks = list(img_mask_data)
            first_mask = image_masks[0]
            n_lines, n_cols = first_mask.shape
            print(f"Dimensions of CI movie given by shape of the 'image_mask' of the cell 0")
            return n_lines, n_cols

    def get_imaging_plan_location(self, only_2_photons=False, ci_movie_name=None):
        """

        Args:
            only_2_photons: if True only 2 photons one are considere
            ci_movie_name: (string) if not None, return the sampling rate for a given ci_movie, otherwise the first
            one found

        Returns: (str) imaging plan location

        """

        for key, acquisition_data in self._nwb_data.acquisition.items():
            if ci_movie_name is not None and (key != ci_movie_name):
                continue
            if only_2_photons:
                if isinstance(acquisition_data, ImageSeries) and \
                        (not isinstance(acquisition_data, TwoPhotonSeries)):
                    continue

            if isinstance(acquisition_data, ImageSeries):
                image_series = acquisition_data
                return image_series.imaging_plane.location

        return None

    def get_belt_type(self):
        session_description = self._nwb_data.session_description
        if "uncued" in session_description:
            return "Uncued belt"
        elif "cued" in session_description:
            return "Cued belt"
        else:
            return 'NA'

    def get_sessions_info(self):
        info_dict = dict()
        if self.identifier is not None:
            session_identifier = str(self.identifier)
        else:
            session_identifier = 'Unknown identifier'
        info_dict['identifier'] = session_identifier

        if self.subject_id is not None:
            animal_id = self.subject_id
        else:
            animal_id = 'Unknown subject'
        info_dict['subject_id'] = animal_id

        if self.session_id is not None:
            session_id = self.session_id
        else:
            session_id = 'Unknown session'
        info_dict['session_id'] = session_id

        if self.age is not None:
            try:
                animal_age = int(self.age)
            except ValueError:
                animal_age = int(0)
        else:
            animal_age = int(0)
        info_dict['age'] = animal_age

        if self.age_unit is not None:
            age_unit = self.age_unit
        else:
            age_unit = 'NS'
        info_dict['age_unit'] = age_unit

        if self.weight is not None:
            animal_weight = self.weight
            if animal_weight[-1] == 'g':
                animal_weight = animal_weight[0: -1]
            animal_weight = float(animal_weight)
        else:
            animal_weight = float(0)
        info_dict['weight'] = animal_weight

        return info_dict

    def get_behavioral_time_series_names(self):
        """
        The name of the different behavioral
        Returns:

        """
        if 'behavior' not in self._nwb_data.processing:
            return []

        behavior_nwb_module = self._nwb_data.processing['behavior']
        try:
            behavioral_timeseries = behavior_nwb_module.get(name='BehavioralTimeSeries')
        except KeyError:
            return []
        # a dictionary containing the IntervalSeries in this BehavioralEpochs container
        time_series = behavioral_timeseries.time_series

        return list(time_series.keys())

    def get_stimulus_names(self):
        # Based on Giocomo example not sure it is how it should be done
        if self._nwb_data.stimulus is None:
            print(f"No 'stimulus' found in this NWB")
            return None
        else:
            stim_names = self._nwb_data.stimulus.keys()
            return stim_names

    def has_epoch_table(self):
        nwb_objects = self._nwb_data.objects
        objects_list = [data for key, data in nwb_objects.items()]
        data_to_take = None
        for ind, obj in enumerate(objects_list):
            if 'epoch' in obj.name:
                data_to_take = obj
                break
            else:
                continue
        if data_to_take is None:
            return False
        else:
            return True

    def get_epochs_names_from_table(self):
        if not self.has_epoch_table():
            return None
        else:
            # Get the epoch table object
            nwb_objects = self._nwb_data.objects
            objects_list = [data for key, data in nwb_objects.items()]
            data_to_take = None
            for ind, obj in enumerate(objects_list):
                if 'epoch' in obj.name:
                    data_to_take = obj
                    break
                else:
                    continue

            column_names = data_to_take.colnames
            variable_columns = []
            variable_columns_values = []
            epoch_dicts = []
            for col_index, col_name in enumerate(column_names):
                if col_name == 'start_time' or col_name == 'stop_time':
                    continue
                else:
                    col_val = data_to_take.get(col_name)
                    col_val_data = col_val.data[:]
                    unique_col_val_data = np.unique(col_val_data[~np.isnan(col_val_data)])
                    is_variable = len(unique_col_val_data) > 1
                    is_index = len(np.unique(col_val_data[~np.isnan(col_val_data)])) == len(col_val.data[:])
                    is_times_series = 'timeseries' in col_name
                    unique_col_val_data = list(unique_col_val_data)
                    if is_variable and (not is_index) and (not is_times_series):
                        variable_columns.append(col_name)
                        variable_columns_values.append(unique_col_val_data)
                epoch_dict = dict(zip(variable_columns, variable_columns_values))
                epoch_dicts.append(epoch_dict)
            return epoch_dicts

    def get_epochs_timestamps_from_table(self, requirements_dict):
        if not self.has_epoch_table():
            return None
        else:
            # Get the epoch table object
            nwb_objects = self._nwb_data.objects
            objects_list = [data for key, data in nwb_objects.items()]
            data_to_take = None
            for ind, obj in enumerate(objects_list):
                if 'epoch' in obj.name:
                    data_to_take = obj
                    break
                else:
                    continue
            epoch_data_frame = data_to_take.to_dataframe()
            for column_name, column_requirements in requirements_dict.items():
                column_values_type = type(epoch_data_frame[column_name].values[0])
                column_requirements = [column_values_type(requirement) for requirement in column_requirements]
                epoch_data_frame = epoch_data_frame.loc[epoch_data_frame[column_name].isin(column_requirements)]
            n_epochs = len(epoch_data_frame.index)
            epochs_timestamps = np.zeros((2, n_epochs))
            epochs_timestamps[0, :] = np.array(epoch_data_frame.get('start_time').values[:])
            epochs_timestamps[1, :] = np.array(epoch_data_frame.get('stop_time').values[:])

            # Try to see if it is really timestamps and not frames
            epoch_start_timestamps_frac = [value % 1 for value in epochs_timestamps[0, :]]
            is_all_zero_starts = all(number == 0 for number in epoch_start_timestamps_frac)
            epoch_stop_timestamps_frac = [value % 1 for value in epochs_timestamps[1, :]]
            is_all_zero_stops = all(number == 0 for number in epoch_stop_timestamps_frac)

            if is_all_zero_starts and is_all_zero_stops:
                print(f"Seems like 'start_time' and 'stop_time' in epoch table are given in frames instead of seconds")
                time_unit = "frames"
            else:
                time_unit = "seconds"

            return epochs_timestamps, time_unit

    def has_trial_table(self):
        nwb_objects = self._nwb_data.objects
        objects_list = [data for key, data in nwb_objects.items()]
        data_to_take = None
        for ind, obj in enumerate(objects_list):
            if 'trial' in obj.name:
                data_to_take = obj
                break
            else:
                continue
        if data_to_take is None:
            return False
        else:
            return True

    def get_trials_names_from_table(self):
        if not self.has_trial_table():
            return None
        else:
            # Get the trial table object
            nwb_objects = self._nwb_data.objects
            objects_list = [data for key, data in nwb_objects.items()]
            data_to_take = None
            trial_dicts = []
            for ind, obj in enumerate(objects_list):
                if 'trial' in obj.name:
                    data_to_take = obj
                    break
                else:
                    continue

            column_names = data_to_take.colnames
            variable_columns = []
            variable_columns_values = []
            for col_index, col_name in enumerate(column_names):
                if col_name == 'start_time' or col_name == 'stop_time':
                    continue
                else:
                    col_val = data_to_take.get(col_name)
                    col_val_data = col_val.data[:]
                    unique_col_val_data = np.unique(col_val_data[~np.isnan(col_val_data)])
                    is_variable = len(unique_col_val_data) > 1
                    is_index = len(np.unique(col_val_data[~np.isnan(col_val_data)])) == len(col_val.data[:])
                    is_times_series = 'timeseries' in col_name
                    unique_col_val_data = list(unique_col_val_data)
                    if is_variable and (not is_index) and (not is_times_series):
                        variable_columns.append(col_name)
                        variable_columns_values.append(unique_col_val_data)
                trial_dict = dict(zip(variable_columns, variable_columns_values))
                trial_dicts.append(trial_dict)
            return trial_dicts

    def get_trials_timestamps_from_table(self, requirements_dict):
        if not self.has_trial_table():
            return None
        else:
            # Get the epoch table object
            nwb_objects = self._nwb_data.objects
            objects_list = [data for key, data in nwb_objects.items()]
            data_to_take = None
            for ind, obj in enumerate(objects_list):
                if 'trial' in obj.name:
                    data_to_take = obj
                    break
                else:
                    continue
            trial_data_frame = data_to_take.to_dataframe()
            for column_name, column_requirements in requirements_dict.items():
                column_values_type = type(trial_data_frame[column_name].values[0])
                column_requirements = [column_values_type(requirement) for requirement in column_requirements]
                trial_data_frame = trial_data_frame.loc[trial_data_frame[column_name].isin(column_requirements)]
            n_epochs = len(trial_data_frame.index)
            epochs_timestamps = np.zeros((2, n_epochs))
            epochs_timestamps[0, :] = np.array(trial_data_frame.get('start_time').values[:])
            epochs_timestamps[1, :] = np.array(trial_data_frame.get('stop_time').values[:])

            # Try to see if it is really timestamps and not frames
            epoch_start_timestamps_frac = [value % 1 for value in epochs_timestamps[0, :]]
            is_all_zero_starts = all(number == 0 for number in epoch_start_timestamps_frac)
            epoch_stop_timestamps_frac = [value % 1 for value in epochs_timestamps[1, :]]
            is_all_zero_stops = all(number == 0 for number in epoch_stop_timestamps_frac)

            if is_all_zero_starts and is_all_zero_stops:
                print(f"Seems like 'start_time' and 'stop_time' in trial table are given in frames instead of seconds")
                time_unit = "frames"
            else:
                time_unit = "seconds"

            return epochs_timestamps, time_unit







