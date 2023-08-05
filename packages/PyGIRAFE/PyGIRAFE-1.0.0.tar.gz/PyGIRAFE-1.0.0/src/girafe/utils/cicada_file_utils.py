import h5py
import os
import numpy as np


class CicadaFileWriter:

    def __init__(self, file_name):
        self.file_name = file_name
        # just the file
        self.base_name = os.path.basename(self.file_name)
        # removing the extension
        try:
            index_cicada_ext = self.base_name.index(".cinac")
        except ValueError:
            index_cicada_ext = self.base_name.index(".h5")
            # otherwise it will raise an exception
        self.base_name = self.base_name[:index_cicada_ext]
        self.file_already_exists = os.path.isfile(self.file_name)
        # opening with a so we can add segment later on if necessary
        self.cicada_file = h5py.File(self.file_name, 'a')
        self.is_closed = False

    def close_file(self):
        """
        Close the file
        Returns:

        """
        self.cicada_file.close()
        self.is_closed = True

    def add_dataset(self, dataset_name, data, attributes_dict=None, group_name=None):
        """

        Args:
            dataset_name: (str) name of the dataset
            data: np array
            attributes_dict: (dict) key is a string, the name of the attribute, and the value can be a str, an int or
            a small array
            group_name: if not None, str representing the name of a group in which to add the dataset, otherwise it
            is added at the root of the

        Returns:

        """
        if dataset_name in self.cicada_file:
            print(f"{dataset_name} already in the cicada file {self.base_name}")
            return
        group = None
        if group_name is not None and group_name in self.cicada_file:
            group = self.cicada_file[group_name]
        if group is None:
            dataset = self.cicada_file.create_dataset(dataset_name, data=data)
        else:
            dataset = group.create_dataset(dataset_name, data=data)

        if attributes_dict is not None:
            for attr_name, attr_value in attributes_dict.items():
                dataset.attrs[attr_name] = attr_value

    def add_group(self, group_name, data_dict, attributes_dict=None):
        """

        Args:
            group_name: (str) name of the group
            data_dict: dict with one key name of the dataset, value is a dict with one key being "data" with value a
            np array and another key can be "attributes" with value a dict with key attributes names and value the value
            of the attributes (str, int, float, small array)
            attributes_dict: (dict) key is a string, the name of the attribute, and the value can be a str, an int or
            a small array

        Returns:

        """
        if group_name in self.cicada_file:
            print(f"{group_name} already in the cicada file {self.base_name}")
            return
        group = self.cicada_file.create_group(group_name)
        for dataset_name, dataset_dict in data_dict.items():
            if 'data' not in dataset_dict:
                continue
            data = dataset_dict['data']
            attributes_dict = dataset_dict.get("attributes", None)
            self.add_dataset(dataset_name=dataset_name, data=data, attributes_dict=attributes_dict,
                             in_group=group_name)
        if attributes_dict is not None:
            for attr_name, attr_value in attributes_dict.items():
                group.attrs[attr_name] = attr_value


class CicadaFileReader:

    def __init__(self, file_name):
        """

        Args:
            file_name: path + filename of the cinac file
            frames_to_keep: tuple of 2 int representing the first_frame and last_frame of a new segment to keep.
            Useful only if all segments have the same number of frames
        """
        self.file_name = file_name
        # just the file
        self.base_name = os.path.basename(self.file_name)
        # removing the extension
        try:
            index_cicada_ext = self.base_name.index(".cinac")
        except ValueError:
            index_cicada_ext = self.base_name.index(".h5")
            # otherwise it will raise an exception
        self.base_name = self.base_name[:index_cicada_ext]

        # opening with a so we can add segment later on if necessary
        self.cicada_file = h5py.File(self.file_name, 'r')
        self.is_closed = False

    def close_file(self):
        """
        Close the file
        Returns:

        """
        self.cicada_file.close()
        self.is_closed = True

    def get_group_names(self):
        """

        Returns: list of string

        """
        keys_set = set(self.cicada_file.keys())

        return [key for key in keys_set if isinstance(self.cicada_file[key], h5py.Group)]

    def get_dataset_names(self):
        """

                Returns: list of string

        """
        keys_set = set(self.cicada_file.keys())

        return [key for key in keys_set if isinstance(self.cicada_file[key], h5py.Dataset)]

    def get_group_data(self, group_name):
        """

        Args:
            group_name:


        Returns: two dict, first one contain the dataset names as key, and value is a list of 2 values
        (the dataset value, and a dict for dataset attributes), second dict is the attributes from the group
        (name, value)


        """
        if group_name not in self.cicada_file:
            return dict(), dict()

        group_dict = dict()

        group = self.cicada_file[group_name]

        for dataset_name in group.keys():
            group_dict[dataset_name] = self.get_dataset_data(dataset_name=dataset_name, group_name=group_name)

        attrs_dict = dict()
        for attrs_key, attrs_value in group.attrs.items():
            attrs_dict[attrs_key] = attrs_value

        return group_dict, attrs_dict

    def get_dataset_data(self, dataset_name, group_name=None):
        """

        Args:
            dataset_name:
            group_name:
        Returns: dataset value (np array) and a dict with key being attributes names and value the attributes value.
        If dataset_name or group_name don't exist, None, None will be returned

        """
        if group_name is None:
            source = self.cicada_file
        else:
            if group_name not in self.cicada_file:
                return None, None
            source = self.cicada_file[group_name]

        if dataset_name not in source:
            return None, None

        attrs_dict = dict()
        for attrs_key, attrs_value in source.attrs.items():
            attrs_dict[attrs_key] = attrs_value

        return np.array(self.cicada_file[dataset_name]), attrs_dict
