import yaml
import os
from random import randint
import importlib.util
from girafe.preprocessing.utils import module_name_to_class_name

def instantiate_girafe_data_wrapper(wrapper_file_name):
    """

    Args:
        wrapper_file_name:

    Returns: (wrapper_id, data_format, format_file_name, class_instance) or None if an error occurs (file not
    existing, or wrong format)

    """
    # now we extract the name of the format if available
    # one way: https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    # another: https://stackoverflow.com/questions/2349991/how-to-import-other-python-files

    # exec, but dangerous
    # exec(new_data_file_name)

    # path option
    # import sys
    # sys.path.append(os.path.abspath(os.path.dirname(new_data_file_name)))
    if (not os.path.isfile(wrapper_file_name)) or (not wrapper_file_name.endswith(".py")):
        print(f"Not a valid wrapper file: {wrapper_file_name}")
        return None

    # name of the class based on the file_name
    class_name = module_name_to_class_name(os.path.basename(wrapper_file_name)[:-3])
    spec = importlib.util.spec_from_file_location("girafe.data_wrapper", wrapper_file_name)
    new_data_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(new_data_module)
    class_instance = getattr(new_data_module, class_name)
    if not hasattr(class_instance, "DATA_FORMAT"):
        print(f"No field DATA_FORMAT found in {class_name}")
        return None

    if not hasattr(class_instance, "WRAPPER_ID"):
        print(f"No field WRAPPER_ID found in {class_name}")
        return None

    data_format = getattr(class_instance, "DATA_FORMAT")
    wrapper_id = getattr(class_instance, "WRAPPER_ID")

    return wrapper_id, data_format, wrapper_file_name, class_instance

class ConfigHandler:
    """
    Class used for handling the configuration for the GUI.
    At term, it should also open a config GUI to set the parameters.
    All GUI parameters should be available there.
    """

    def __init__(self, path_to_config_file="../config/config.yaml"):
        my_path = os.path.abspath(os.path.dirname(__file__))
        path_to_config_file = os.path.join(my_path, path_to_config_file)
        self._path_to_config_file = path_to_config_file

        with open(path_to_config_file, 'r') as stream:
            config_dict = yaml.load(stream, Loader=yaml.FullLoader)

        if config_dict is None:
            config_dict = dict()

        self._yaml_analysis_args_dir_name = config_dict.get('yaml_analysis_args_dir_name', None)

        self._last_data_wrapper_used = config_dict.get('last_data_wrapper_used', None)

        # list of python file implementing wrapper for a data_format
        data_wrapper_file_list = config_dict.get('available_data_wrappers', [])

        # dict with key the wrapper id, and value the data format and .py file implementing the format in a list
        self._available_data_wrappers = dict()
        for file_name in data_wrapper_file_list:
            if not file_name.endswith(".py"):
                continue
            wrapper_info = instantiate_girafe_data_wrapper(file_name)
            if wrapper_info is None:
                continue
            wrapper_id, data_format, wrapper_file_name, class_instance = wrapper_info
            self._available_data_wrappers[wrapper_id] = [data_format, file_name, class_instance]

        if len(self._available_data_wrappers) == 0:
            raise Exception("No wrapper in the config file (config.yaml)")
        # if len(self._available_data_wrappers) == 0:
        #     # then by default we put SCN8A
        #     default_file_name = os.path.join(my_path, "../analysis/...py")
        #     wrapper_info = instantiate_girafe_data_wrapper(default_file_name)
        #     if wrapper_info is not None:
        #         self._available_data_wrappers["SCN8APatient"] = ["SCN8A", default_file_name, wrapper_info[3]]

        # list of directories with analyses files to load
        self._dirs_with_analyses_to_load = config_dict.get('dirs_with_analyses_to_load', [])
        if len(self._dirs_with_analyses_to_load) == 0:
            self._dirs_with_analyses_to_load.append(os.path.join(my_path, "../analysis/ci_analyses"))

        # Dict with key each format
        self._files_to_analyse_dir_names = config_dict.get('data_files_dir_names', dict())

        self._last_data_format_used = config_dict.get('last_data_format_used', None)

        self.current_format = "SCN8APatient"
        if self._last_data_format_used is not None:
            self.current_format = self._last_data_format_used
        elif self._available_data_wrappers is not None and (len(self._available_data_wrappers) > 0) and \
                (self.current_format not in self._available_data_wrappers):
            # then we take the first in the dict
            self.current_format = list(self._available_data_wrappers.keys())[0]

        # Path of the directory where to save new results
        # usually a new directory specific to the analysis done will be created in this directory
        self._default_results_path = config_dict.get('default_results_path', None)

        # useful to know where to open file dialog by default
        # to change it, you have to put it by hands in the config file, it is not modified in the code for now
        self._default_file_dialog_path = config_dict.get('default_file_dialog_path', None)

        self.main_window_bg_pictures_displayed_by_default = True

        self._widget_bg_pictures_folder = dict()
        list_of_widget_ids = ["tree", "initial_config", "overview", "analysis_params", "sessions", "analysis_data"]
        for key, pictures_path in config_dict.items():
            if 'bg_pictures_folder' in key:
                for widget_id in list_of_widget_ids:
                    if widget_id in key:
                        self._widget_bg_pictures_folder[widget_id] = pictures_path
        self._widget_bg_pictures_file_names = dict()

        for widget_id, folder_path in self._widget_bg_pictures_folder.items():
            if folder_path is None:
                continue
            # we list the pictures
            if os.path.isdir(folder_path):
                file_names = []
                for (dirpath, dirnames, local_filenames) in os.walk(folder_path):
                    file_names = local_filenames
                    break
                for file_name in file_names:
                    if (file_name.lower().endswith(".png") or file_name.lower().endswith(".jpg") or
                        file_name.lower().endswith(".jpeg")) and \
                            (not file_name.startswith(".")):
                        if widget_id not in self._widget_bg_pictures_file_names:
                            self._widget_bg_pictures_file_names[widget_id] = []
                        # if os.name == 'nt':
                        #     self._widget_bg_pictures_file_names[widget_id].append(
                        #         folder_path + '/' + file_name)
                        self._widget_bg_pictures_file_names[widget_id].append(os.path.join(
                                folder_path, file_name))

    def update_files_to_analyse_dir_names(self, data_format, dir_name):
        """
        Update the directory to load for a fiven data_format
        Args:
            data_format:
            dir_name:

        Returns:

        """
        if not os.path.isfile(self._path_to_config_file):
            return

        with open(self._path_to_config_file, 'r') as stream:
            config_dict = yaml.safe_load(stream)

        if config_dict is None:
            config_dict = dict()

        if "data_files_dir_names" not in config_dict:
            config_dict["data_files_dir_names"] = dict()
        config_dict["data_files_dir_names"][data_format] = dir_name

        with open(self._path_to_config_file, 'w') as outfile:
            yaml.dump(config_dict, outfile, default_flow_style=False)

    def update_last_analyse_run_dir_name(self, dir_name):
        """
        Update the directory of the last analysis run
        Args:
            dir_name:

        Returns:

        """
        if not os.path.isfile(self._path_to_config_file):
            return

        with open(self._path_to_config_file, 'r') as stream:
            config_dict = yaml.safe_load(stream)

        if config_dict is None:
            config_dict = dict()
        config_dict["last_analyse_run_dir_name"] = dir_name
        with open(self._path_to_config_file, 'w') as outfile:
            yaml.dump(config_dict, outfile, default_flow_style=False)

    def get_last_analyse_run_dir_name(self):
        """
        Get the directory of the last analysis run

        Returns:

        """
        if not os.path.isfile(self._path_to_config_file):
            return

        with open(self._path_to_config_file, 'r') as stream:
            config_dict = yaml.safe_load(stream)

        if config_dict is None:
            config_dict = dict()
        if "last_analyse_run_dir_name" not in config_dict:
            return None

        return config_dict["last_analyse_run_dir_name"]

    def update_config_field(self, field_name, field_value):
        """
        Update a value in the config and update the value in the yaml file
        Args:
            field_name: (str) name of the field
            field_value:

        Returns:

        """

        if not os.path.isfile(self._path_to_config_file):
            return

        with open(self._path_to_config_file, 'r') as stream:
            config_dict = yaml.safe_load(stream)

        if config_dict is None:
            config_dict = dict()
        config_dict[field_name] = field_value
        with open(self._path_to_config_file, 'w') as outfile:
            yaml.dump(config_dict, outfile, default_flow_style=False)

    def get_dirs_with_analyses_to_load(self):
        """

        Returns: list of directories with analyses files to load

        """
        return self._dirs_with_analyses_to_load

    def get_random_main_window_bg_picture(self, widget_id=None):
        """

        Args:
            widget_id: string identifying the widget for which the picture is meant
            could be: "sessions", "tree", "overview"

        Returns:

        """
        # not default background
        if widget_id is None:
            return None

        if widget_id not in self._widget_bg_pictures_file_names:
            # print(f"widget_id unknow {widget_id} in get_random_main_window_bg_picture()")
            return None
        file_names = self._widget_bg_pictures_file_names[widget_id]
        if len(file_names) == 0:
            return None
        pic_index = randint(0, len(file_names) - 1)
        return file_names[pic_index]

    def get_available_data_wrappers(self):
        """

        Returns: dict with key the wrapper id, and value the data format and .py file implementing the format in a list

        """
        return self._available_data_wrappers

    def get_last_data_wrapper_used(self):
        return self._last_data_wrapper_used

    @property
    def main_window_bg_pictures_folder(self):
        return self._main_window_bg_pictures_folder

    @main_window_bg_pictures_folder.setter
    def main_window_bg_pictures_folder(self, value):
        # TODO: update the pictures choice
        self._main_window_bg_pictures_folder = value

    @property
    def yaml_analysis_args_dir_name(self):
        return self._yaml_analysis_args_dir_name

    def get_files_to_analyse_dir_names(self, data_format):
        """
        List of directories
        Returns:

        """
        if self._files_to_analyse_dir_names is None:
            return None
        if data_format not in self._files_to_analyse_dir_names:
            return None
        return self._files_to_analyse_dir_names[data_format]

    @property
    def default_results_path(self):
        return self._default_results_path

    @default_results_path.setter
    def default_results_path(self, value):
        self._default_results_path = value

    @property
    def default_file_dialog_path(self):
        return self._default_file_dialog_path
