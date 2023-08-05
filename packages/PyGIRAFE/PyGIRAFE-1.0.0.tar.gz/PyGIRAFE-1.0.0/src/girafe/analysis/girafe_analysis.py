from abc import ABC, abstractmethod, abstractproperty
from girafe.analysis.girafe_analysis_arguments_handler import AnalysisArgumentsHandler
from girafe.preprocessing.utils import class_name_to_module_name, path_leaf
import importlib
import PyQt5.QtCore as Core
from qtpy.QtCore import QThread
from datetime import datetime
import sys
import os
from time import time
import numpy as np
from girafe.preprocessing.utils import module_name_to_class_name
import inspect
from copy import deepcopy


class GirafeAnalysis(ABC):
    """
    An abstract class that should be inherit in order to create a specific analyse

    """

    def __init__(self, name, short_description, accepted_data_formats, family_id=None, long_description=None,
                 data_to_analyse=None, data_format=None, config_handler=None, gui=True):
        """

        Args:
            name:
            short_description: short string that describe what the analysis is about
             used to be displayed in the GUI among other things
            family_id:  family_id indicated to which family of analysis this class belongs. If None, then
             the analysis is a family in its own.
            accepted_data_formats: list of string identifying the format that are accepted by this analysis (ex:
            [CI_DATA"]
            long_description:
            data_to_analyse:
            data_format:
            config_handler: Instance of ConfigHandler to have access to configuration
        """

        super().__init__()
        # TODO: when the exploratory GUI will be built, think about passing in argument some sort of connector
        #  to the GUI in order to communicate with it and get the results displayed if needed
        self.short_description = short_description
        self.long_description = long_description
        self.accepted_data_formats = accepted_data_formats
        self.progress_bar_overview = None
        self.progress_bar_analysis = None
        self.family_id = family_id
        self.name = name
        self.gui = gui
        self.yaml_name = ''
        self.current_order_index = 0
        self._data_to_analyse = data_to_analyse
        self._data_format = data_format
        self.config_handler = config_handler
        # attribute that will be used to display the reason why the analysis is not possible with the given
        # data passed to it
        self.invalid_data_help = None
        # Initialized in run_analysis, can be used to save in the log file the run time.
        self.analysis_start_time = 0
        self.analysis_arguments_handler = AnalysisArgumentsHandler(cicada_analysis=self)

        # path of the dir where the results will be saved
        self._results_path = None

        if self._data_to_analyse:
            self.set_arguments_for_gui()

    # @abstractproperty
    # def data_to_analyse(self):
    #     pass
    #
    # @abstractproperty
    # def data_format(self):
    #     pass

    def is_data_format_accepted(self, data_format):
        """

        Args:
            data_format:

        Returns: boolean, True is the data format is accepted for this analysis

        """
        return data_format in self.accepted_data_formats

    def get_results_path(self):
        """
        Return the path when the results from the analysis will be saved or None if it doesn't exist yet
        Returns:

        """
        return self._results_path

    def create_results_directory(self, dir_path):
        """
        Will create a directory in dir_path with the name of analysis and time at which the directory is created
        so it can be unique. The attribute _results_path will be updated with the path of this new directory
        Args:
            dir_path: path of the dir in which create the results dir

        Returns: this new directory

        """
        # first we check if dir_path exists
        if (not os.path.exists(dir_path)) or (not os.path.isdir(dir_path)):
            print(f"{dir_path} doesn't exist or is not a directory")
            return

        time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
        self._results_path = os.path.join(dir_path, self.name + f"_{time_str}")
        os.mkdir(self._results_path)

        return self._results_path

    def get_data_identifiers(self):
        """
        Return a list of string representing each data to analyse
        Returns:

        """
        identifiers = []
        identifiers = [data.identifier for data in self._data_to_analyse]
        return identifiers

    @abstractmethod
    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        pass

    # def copy(self):
    #     # print(f"copy self.__module__ {self.__module__}")
    #     # print(f"copy sys.modules[self.__module__] {sys.modules[self.__module__]}")
    #     # print(f"copy sys.modules[self.__module__].__file__ {sys.modules[self.__module__].__file__}")
    #     return deepcopy(self)
    #     module_name = self.__module__
    #     module = importlib.import_module(module_name)
    #     new_class = getattr(module, self.__class__.__name__)
    #     new_object = new_class()
    #
    #     # frame = inspect.stack()[0]
    #     # module = inspect.getmodule(frame[0])
    #     # filename = module.__file__
    #     # print(f"filename {inspect.getfile(self)}")
    #
    #     # class_name = module_name_to_class_name(os.path.basename(__file__)[:-3])
    #     # spec = importlib.util.spec_from_file_location("cicada.data_analyses", __file__)
    #     # new_data_module = importlib.util.module_from_spec(spec)
    #     # spec.loader.exec_module(new_data_module)
    #     # class_instance = getattr(new_data_module, class_name)
    #
    #     new_object = class_instance()
    #     new_object.name = self.name
    #     new_object.yaml_name = self.yaml_name
    #     new_object.short_description = self.short_description
    #     new_object.family_id = self.family_id
    #     new_object.long_description = self.long_description
    #     new_object.set_data(self._data_to_analyse)
    #     new_object.config_handler = self.config_handler
    #     return new_object

    def transfer_attributes_to_tabula_rasa_copy(self, analysis_copy):
        """
        Transfers attributes values from self to a new copy that doesn't have all information yet
        Args:
            analysis_copy:

        Returns:

        """
        analysis_copy.name = self.name
        analysis_copy.yaml_name = self.yaml_name
        analysis_copy.short_description = self.short_description
        analysis_copy.family_id = self.family_id
        analysis_copy.long_description = self.long_description
        analysis_copy.set_data(self._data_to_analyse)
        analysis_copy.config_handler = self.config_handler

    def set_yaml_name(self, name):
        self.yaml_name = name

    def set_data(self, data_to_analyse):
        """
                A list of
                :param data_to_analyse: list of data_structure
        """
        # TODO: don't use data_format, as data_format will be available in the wrapper itself
        if not isinstance(data_to_analyse, list):
            data_to_analyse = [data_to_analyse]
        self._data_to_analyse = data_to_analyse
        # self._data_format = data_format
        # set_arguments_for_gui cllaed in analysis_tree_gui when double_clicked is called
        # self.set_arguments_for_gui()

    @abstractmethod
    def check_data(self):
        """
        Check the data given one initiating the class and return True if the data given allows the analysis
        implemented, False otherwise.
        :return: a boolean
        """
        self.invalid_data_help = None

    def add_argument_for_gui(self, with_incremental_order=True, **kwargs):
        """

        Args:
            **kwargs:
            with_incremental_order: boolean, if True means the order of the argument will be the same as when added

        Returns:

        """
        if with_incremental_order:
            kwargs.update({"order_index": self.current_order_index})
            self.current_order_index += 1

        self.analysis_arguments_handler.add_argument(**kwargs)

    def set_arguments_for_gui(self):
        """
        Need to be implemented in order to be used through the graphical interface.
        super().set_arguments_for_gui() should be call first to instantiate an AnalysisArgumentsHandler and
        create the attribution for results_path
        :return: None
        """
        if not self.gui:
            return

        # creating a new AnalysisArgumentsHandler instance
        self.analysis_arguments_handler = AnalysisArgumentsHandler(cicada_analysis=self)

        if (self.long_description is not None) and isinstance(self.long_description, str) and \
                (len(self.long_description.strip()) > 0):
            self.add_analysis_description_for_gui(description=self.long_description)

        # we order_index at 1000 for it to be displayed at the end
        default_results_path = None
        mandatory = True
        if self.config_handler is not None:
            default_results_path = self.config_handler.default_results_path
            mandatory = False

        results_path_arg = {"arg_name": "results_path", "value_type": "dir",
                            "default_value": default_results_path, "short_description": "Directory to save the results",
                            "with_incremental_order": False, "order_index": 1000, "mandatory": mandatory}

        self.add_argument_for_gui(**results_path_arg)

    def get_data_to_analyse(self):

        """

        :return: a list of the data to analyse
        """
        return self._data_to_analyse

    def update_original_data(self):
        """
        To be called if the data to analyse should be updated after the analysis has been run.
        :return: boolean: return True if the data has been modified
        """
        pass

    @abstractmethod
    def run_analysis(self, **kwargs):
        """
        Run the analysis
        :param kwargs:
        :return:
        """
        self.analysis_start_time = time()

        if "results_path" in kwargs:
            results_path = kwargs["results_path"]
            if self._results_path is None:
                self.create_results_directory(results_path)
                if self.gui:
                    thread = QThread.currentThread()
                    thread.set_results_path(self._results_path)
        if self.yaml_name == '':
            self.yaml_name = path_leaf(self._results_path)
        data_to_include = None
        if "__to_copy_in_new_yaml__" in kwargs:
            # used when the last analysis is re-run through the first window of the GUI
            # See in girafe_initial_config_window.py run_last_analysis()
            data_to_include = kwargs["__to_copy_in_new_yaml__"]
        self.analysis_arguments_handler.save_analysis_arguments_to_yaml_file(path_dir=self._results_path,
                                                                             yaml_file_name=self.yaml_name,
                                                                             data_to_include=data_to_include
                                                                             )
        self.config_handler.update_last_analyse_run_dir_name(dir_name=self._results_path)

    def update_progressbar(self, time_started, increment_value=0, new_set_value=0):
        """

        Args:
            time_started (float): Start time of the analysis
            increment_value (float): Value that should be added to the current value of the progress bar
            new_set_value (float):  Value that should be set as the current value of the progress bar

        """
        time_elapsed = time() - time_started

        if self.gui:
            worker = QThread.currentThread()
            worker.setProgress(name=worker.name, time_elapsed=time_elapsed, increment_value=increment_value,
                               new_set_value=new_set_value)
        else:
            pass

    def add_analysis_description_for_gui(self, description):
        """
        Add a description that will be displayed as a widget on top of the arguments list
        Args:
            description:

        Returns:

        """

        analysis_descr_arg = {"arg_name": "analysis_description", "value_type": "text",
                              "short_description": "Analysis description",
                              "default_value": description,
                              "read_only": True, "mandatory": True, "order_index": 0}

        self.add_argument_for_gui(**analysis_descr_arg)

    def add_ci_movie_arg_for_gui(self, long_description=None):
        """
        Will add an argument for gui, named ci_movie that will list all calcium imaging available for each session
        Returns:

        """
        ci_movies_dict_for_arg = dict()
        for data in self._data_to_analyse:
            ci_movies_dict = data.get_ci_movies(only_2_photons=False)
            for movie_id in ci_movies_dict.keys():
                # we put the identifier of each movie as values
                ci_movies_dict_for_arg[data.identifier] = movie_id

        ci_movie_arg = {"arg_name": "ci_movie", "choices": ci_movies_dict_for_arg,
                        "short_description": "Calcium imaging movie to use", "mandatory": False,
                        "multiple_choices": False}

        if long_description is not None:
            ci_movie_arg.update({"long_description": long_description})

        self.add_argument_for_gui(**ci_movie_arg)

    def add_segmentation_arg_for_gui(self):
        """
            Will add an argument for gui, named segmentation that will list all segmentations available for each session
            Returns:

        """
        segmentation_dict_for_arg = dict()
        for data in self._data_to_analyse:
            segmentation_dict_for_arg[data.identifier] = data.get_segmentations()

        # not mandatory, because one of the element will be selected by the GUI
        segmentation_arg = {"arg_name": "segmentation", "choices": segmentation_dict_for_arg,
                            "short_description": "Segmentation to use", "mandatory": False,
                            "multiple_choices": False}

        self.add_argument_for_gui(**segmentation_arg)

    def add_save_formats_arg_for_gui(self, family_widget=None):
        """
            Add save_formats option, True or False
            Returns:

        """
        format_arg = {"arg_name": "save_formats", "choices": ["pdf", "png", "tiff", "eps"],
                      "default_value": "pdf", "short_description": "Formats in which to save the figures",
                      "multiple_choices": True, "family_widget": family_widget}

        self.add_argument_for_gui(**format_arg)

    def add_open_file_dialog_arg_for_gui(self, arg_name, extensions, mandatory, short_description,
                                         long_description=None,
                                         key_names=None, family_widget=None):
        """
        Allows to add widget to select a file. If key_names is given then multiple option are added,
        one for each key_name
        Args:
            arg_name:
            extensions: str or list of str, ex: "txt"
            mandatory: (boolean)
            short_description:
            long_description:
            key_names: None or list of string
            family_widget:

        Returns:

        """
        open_file_dialog_arg = {"arg_name": arg_name, "value_type": "file",
                                "extensions": extensions,
                                "mandatory": mandatory,
                                "short_description": short_description,
                                "long_description": long_description,
                                "family_widget": family_widget}

        if key_names is not None and len(key_names) > 1:
            open_file_dialog_arg.update({"key_names": key_names})
        self.add_argument_for_gui(**open_file_dialog_arg)

    def add_open_dir_dialog_arg_for_gui(self, arg_name, mandatory, short_description,
                                         long_description=None,
                                         key_names=None, family_widget=None):
        """
        Allows to add widget to select a directory. If key_names is given then multiple option are added,
        one for each key_name
        Args:
            arg_name:
            mandatory: (boolean)
            short_description:
            long_description:
            key_names: None or list of string
            family_widget:

        Returns:

        """
        open_file_dialog_arg = {"arg_name": arg_name, "value_type": "dir",
                                "mandatory": mandatory,
                                "short_description": short_description,
                                "long_description": long_description,
                                "family_widget": family_widget}

        if key_names is not None and len(key_names) > 1:
            open_file_dialog_arg.update({"key_names": key_names})
        self.add_argument_for_gui(**open_file_dialog_arg)

    def add_int_values_arg_for_gui(self, arg_name, min_value, max_value, short_description,
                                   default_value, long_description=None, family_widget=None):
        int_values_arg = {"arg_name": arg_name, "value_type": "int", "min_value": min_value, "max_value": max_value,
                          "long_description": long_description,
                          "default_value": default_value, "short_description": short_description,
                          "family_widget": family_widget}

        self.add_argument_for_gui(**int_values_arg)

    def add_color_arg_for_gui(self, arg_name, default_value, short_description,
                              long_description=None, family_widget=None):
        color_arg = {"arg_name": arg_name, "value_type": "color_with_alpha",
                     "default_value": default_value, "short_description": short_description,
                     "long_description": long_description,
                     "family_widget": family_widget}
        self.add_argument_for_gui(**color_arg)

    def add_dpi_arg_for_gui(self, family_widget):
        """
        Add dpi value
        Args:
            family_widget:

        Returns:

        """
        self.add_int_values_arg_for_gui(arg_name="dpi", min_value=50, max_value=800,
                                        short_description="Dpi (Dots per inches)",
                                        default_value=200,
                                        long_description="Dots per inches (dpi) determines how many pixels the figure comprises",
                                        family_widget=family_widget)

    def add_choices_arg_for_gui(self, arg_name, choices, short_description, default_value,
                                multiple_choices, long_description=None, family_widget=None):
        choices_arg = {"arg_name": arg_name, "choices": choices,
                       "short_description": short_description,
                       "long_description": long_description,
                       "default_value": default_value,
                       "multiple_choices": multiple_choices,
                       "family_widget": family_widget}

        self.add_argument_for_gui(**choices_arg)

    def add_choices_for_groups_for_gui(self, arg_name, choices, with_color, short_description,
                                       long_description=None, family_widget=None, mandatory=False,
                                       add_custom_group_field=False,
                                       custom_group_validation_fct=None, custom_group_processor_fct=None):
        """
        Allows to create group based composed of elements of choices..
        Args:
            arg_name:
            choices:
            with_color: If True, means that we can select a color for each group
            short_description:
            long_description:
            family_widget:
            mandatory: (bool)
            add_custom_group_field: if True, add a text field allowing to name the group to be added
            custom_group_validation_fct: if not None, called when a custom group is created to check the text
            field and validate the name. Return True or False. If False, the field is erased. Instead of False, can
            return a string, in that case a message box will display a message indicating the error
            custom_group_processor_fct: None or function that process the text in the custom group field and return
            a list of string representing the elements in the group. If this fct is None, then the new group will
            just contain one element the content of the text field that can be then processed later on.

        Returns:

        """
        choices_arg = {"arg_name": arg_name, "choices_for_groups": choices,
                       "with_color": with_color,
                       "mandatory": mandatory,
                       "short_description": short_description,
                       "long_description": long_description,
                       "add_custom_group_field": add_custom_group_field,
                       "custom_group_validation_fct": custom_group_validation_fct,
                       "custom_group_processor_fct": custom_group_processor_fct,
                       "family_widget": family_widget}

        self.add_argument_for_gui(**choices_arg)

    def add_field_text_option_for_gui(self, arg_name, default_value,
                                      short_description,
                                      long_description=None, family_widget=None):
        """
        Add a field to add some text
        Returns:

        """
        stim_arg = {"arg_name": arg_name, "value_type": "str",
                    "default_value": default_value, "short_description": short_description,
                    "long_description": long_description,
                    "family_widget": family_widget
                    }
        self.add_argument_for_gui(**stim_arg)

    def add_field_float_option_for_gui(self, arg_name, default_value, mandatory,
                                       short_description,
                                       long_description=None, family_widget=None):
        """
        Add a field to add some float
        Returns:

        """
        float_arg = {"arg_name": arg_name, "value_type": "float", "mandatory": mandatory,
                    "default_value": default_value, "short_description": short_description,
                    "long_description": long_description,
                    "family_widget": family_widget
                    }
        self.add_argument_for_gui(**float_arg)

    def add_bool_option_for_gui(self, arg_name, true_by_default,
                                short_description,
                                long_description=None, family_widget=None):
        """
        Add an option which is a boolean to the menu
        Args:
            arg_name: (string) used to get back the value
            true_by_default: (bool)
            short_description: (str)
            long_description: (string or None)

        Returns:

        """

        bool_arg = {"arg_name": arg_name, "value_type": "bool",
                    "default_value": true_by_default, "short_description": short_description,
                    "long_description": long_description, "family_widget": family_widget}

        self.add_argument_for_gui(**bool_arg)

    def add_verbose_arg_for_gui(self):
        """
        Add verbose option, True or False
        Returns:

        """
        verbose_arg = {"arg_name": "verbose", "value_type": "bool",
                       "default_value": True, "short_description": "Verbose",
                       "long_description": "If selected, some information might be printed during the analysis."}

        self.add_argument_for_gui(**verbose_arg)

    def add_image_format_package_for_gui(self):
        """
        Add a few arguments at once: save_formats, dpi, width_fig & height_fig
        Returns:

        """
        self.add_save_formats_arg_for_gui(family_widget="image_format")
        self.add_dpi_arg_for_gui(family_widget="image_format")
        self.add_int_values_arg_for_gui(arg_name="width_fig", min_value=5, max_value=50,
                                        short_description="Width figure",
                                        default_value=15, long_description=None, family_widget="image_format")
        self.add_int_values_arg_for_gui(arg_name="height_fig", min_value=5, max_value=50,
                                        short_description="Height figure",
                                        default_value=8, long_description=None, family_widget="image_format")
        self.add_bool_option_for_gui(arg_name="xkcd_mode", true_by_default=False,
                                     short_description="Turn on xkcd sketch-style drawing mode",
                                     long_description="For best results, the 'Humor Sans' font should be installed: "
                                                      "it is not included with matplotlib.",
                                     family_widget="image_format")

    def add_with_timestamp_in_filename_arg_for_gui(self):
        """
        Add with_timestamp_in_file_name option, True or False
        Returns:

        """
        verbose_arg = {"arg_name": "with_timestamp_in_file_name", "value_type": "bool",
                       "default_value": True, "short_description": "Timestamp in filename",
                       "long_description": "If selected, a timestamp will be added to filename to identify it."}

        self.add_argument_for_gui(**verbose_arg)

    def add_roi_response_series_arg_for_gui(self, short_description, long_description=None,
                                            keywords_to_exclude=None, arg_name=None, family_widget=None):
        rrs_dict_for_arg = dict()
        for data in self._data_to_analyse:
            rrs_dict_for_arg[data.identifier] = data.get_roi_response_series(keywords_to_exclude=keywords_to_exclude)

        if arg_name is None:
            arg_name = "roi_response_series"
        rrs_arg = {"arg_name": arg_name, "choices": rrs_dict_for_arg,
                   "short_description": short_description, "mandatory": False,
                   "multiple_choices": False, "family_widget": family_widget}

        if long_description is not None:
            rrs_arg.update({"long_description": long_description})

        self.add_argument_for_gui(**rrs_arg)

    def add_intervals_arg_for_gui(self, short_description, arg_name="intervals", long_description=None):
        intervals_dict_for_arg = dict()
        for data in self._data_to_analyse:
            intervals_dict_for_arg[data.identifier] = data.get_intervals_names()

        intervals_arg = {"arg_name": arg_name, "choices": intervals_dict_for_arg,
                         "short_description": short_description, "mandatory": False,
                         "multiple_choices": False}

        if long_description is not None:
            intervals_arg.update({"long_description": long_description})

        self.add_argument_for_gui(**intervals_arg)

    def add_epoch_dict_arg_for_gui(self, short_description, long_description=None, multiple_choices=False,
                                   arg_name=None, family_widget=None):
        for data in self._data_to_analyse:
            dict_list = data.get_epochs_names_from_table()
            for dict_choice in dict_list:
                if arg_name is None:
                    arg_name = "epochs_table"
                epoch_table_arg = {"arg_name": arg_name, "choices": dict_choice,
                                   "short_description": short_description, "mandatory": False,
                                   "multiple_choices": multiple_choices, "family_widget": family_widget}

                if long_description is not None:
                    epoch_table_arg.update({"long_description": long_description})

                self.add_argument_for_gui(**epoch_table_arg)

    def add_trial_dict_arg_for_gui(self, short_description, long_description=None, multiple_choices=False,
                                   arg_name=None, family_widget=None):
        for data in self._data_to_analyse:
            dict_list = data.get_trials_names_from_table()
            for dict_choice in dict_list:
                if arg_name is None:
                    arg_name = "trial_table"
                trial_table_arg = {"arg_name": arg_name, "choices": dict_choice,
                                   "short_description": short_description, "mandatory": False,
                                   "multiple_choices": multiple_choices, "family_widget": family_widget}

                if long_description is not None:
                    trial_table_arg.update({"long_description": long_description})

                self.add_argument_for_gui(**trial_table_arg)


