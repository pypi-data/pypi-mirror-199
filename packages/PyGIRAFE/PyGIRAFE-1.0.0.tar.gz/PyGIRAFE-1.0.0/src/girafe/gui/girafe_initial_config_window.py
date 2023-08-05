from qtpy.QtWidgets import *
from qtpy import QtCore, QtGui
from qtpy.QtCore import Qt

from girafe.gui.girafe_main_window import GirafeMainWindow
from girafe.gui.girafe_config_handler import instantiate_girafe_data_wrapper
from girafe.preprocessing.utils import module_name_to_class_name
from sortedcontainers import SortedDict

import platform
import os
import pathlib
import glob
import ctypes
import importlib.util
import yaml


class MyQComboBox(QComboBox):
    """
    Special instance of ComboBox allowing to handle change so that it is connected to other combo_boxes
    """

    def __init__(self, selection_change):
        """
        init
        """
        QComboBox.__init__(self)

        self.currentIndexChanged.connect(selection_change)


def extract_analyses_from_dir(dir_name, config_handler):
    """

    Args:
        dir_name:
        config_handler: ConfigHandler instance

    Returns: dict key is a the name of the analysis, value is a list with analysis instance and the Python file_name

    """
    analyses_dict = dict()
    modules = glob.glob(os.path.join(dir_name, "*.py"))
    all_analyses_files = [f for f in modules if os.path.isfile(f) and not f.startswith(".")
                   and not f.endswith('__init__.py')]

    for analysis_file in all_analyses_files:
        class_name = module_name_to_class_name(os.path.basename(analysis_file)[:-3])
        spec = importlib.util.spec_from_file_location("girafe.data_analyses", analysis_file)
        new_data_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(new_data_module)
        if hasattr(new_data_module, class_name):
            class_instance = getattr(new_data_module, class_name)
            analysis_instance = class_instance(config_handler=config_handler)
            analyses_dict[analysis_instance.name] = [analysis_instance, analysis_file]

    return analyses_dict


class InitialConfigWindow(QMainWindow):

    # window that display the initial config choices
    def __init__(self, config_handler):
        super().__init__()

        # To display an the window icon as the application icon in the task bar on Windows
        if platform.system() == "Windows":
            myappid = u'girafe.gui.alpha'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        my_path = os.path.abspath(os.path.dirname(__file__))
        self.setWindowIcon(QtGui.QIcon(os.path.join(my_path, 'icons/svg/cicada_open_focus.svg')))

        # allows to access config param
        self.config_handler = config_handler

        self.setWindowTitle("GIRAFE initial config")

        screenGeometry = QApplication.desktop().screenGeometry()
        # making sure the window is not bigger than the dimension of the screen
        width_window = min(500, screenGeometry.width())
        # width_window = screenGeometry.width()
        height_window = min(900, screenGeometry.height())
        self.resize(width_window, height_window)

        self.central_widget = InitialConfigCentralWidget(config_handler=config_handler,
                                                         main_window=self)

        self.setCentralWidget(self.central_widget)

        self.show()


class InitialConfigCentralWidget(QWidget):

    def __init__(self, config_handler, main_window):
        super().__init__(parent=main_window)

        self.main_window = main_window

        self.config_handler = config_handler

        self.analyses_widget = None

        # indicate that the main windown is loading
        self.cicada_main_window_loading = False

        # key is the wrapper_id (str) and value is a tuple with data_format, file_name (python file) and wrapper
        # class_instance
        self.data_format_dict = dict()
        self.data_format_dict.update(config_handler.get_available_data_wrappers())

        self.main_layout = QVBoxLayout()
        # TODO: modify config handler & yaml file
        self.format_layout = QHBoxLayout()
        self.format_layout.addStretch(1)
        # contains the data format available, actually the name display is the name of the wrapper
        # there can be several wrapper for the same data format
        self.current_data_wrapper_name = None
        self.data_wrapper_combo_box = MyQComboBox(selection_change=self.data_format_change)
        self.data_wrapper_combo_box.setToolTip(f"Format of the data to analyse")
        self.empty_string_combo_box = "    "
        for data_wrapper_id in self.data_format_dict.keys():
            # adding space for display purpose
            self.data_wrapper_combo_box.addItem(data_wrapper_id + self.empty_string_combo_box)
        if config_handler.get_last_data_wrapper_used() is not None:
            index = self.data_wrapper_combo_box.findText(config_handler.get_last_data_wrapper_used() +
                                                         self.empty_string_combo_box)
            if index >= 0:
                self.data_wrapper_combo_box.setCurrentIndex(index)

        if self.data_wrapper_combo_box.count() > 0:
            self.current_data_wrapper_name = self.data_wrapper_combo_box.currentText().strip()

        self.format_layout.addWidget(self.data_wrapper_combo_box)

        self.add_format_button = QPushButton("+")
        self.add_format_button.setToolTip("Add new data format")
        self.add_format_button.clicked.connect(self.select_new_data_format)
        self.format_layout.addWidget(self.add_format_button)
        self.format_layout.addStretch(1)
        self.main_layout.addLayout(self.format_layout)

        available_analyses = dict()
        dirs_with_analyses_to_load = config_handler.get_dirs_with_analyses_to_load()
        for dir_name in dirs_with_analyses_to_load:
            available_analyses.update(extract_analyses_from_dir(dir_name, config_handler))

        self.analyses_widget = AnalysesWidget(config_handler=config_handler, main_window=self,
                                              available_analyses=available_analyses,
                                              dirs_with_analyses_loaded=dirs_with_analyses_to_load)

        self.main_layout.addWidget(self.analyses_widget)

        self.run_girafe_layout = QHBoxLayout()
        self.run_girafe_layout.addStretch(1)
        self.v_run_layout = QVBoxLayout()
        self.run_girafe_button = QPushButton("RUN GIRAFE")
        self.run_girafe_button.setToolTip("Run GIRAFE with the given options")
        self.run_girafe_button.clicked.connect(self.run_girafe)
        self.v_run_layout.addWidget(self.run_girafe_button)

        self.run_last_analysis_button = QPushButton("Run last analysis")
        self.run_last_analysis_button.setToolTip("Run last analysis run in GIRAFE.")
        self.run_last_analysis_button.clicked.connect(self.run_last_analysis)
        self.v_run_layout.addWidget(self.run_last_analysis_button)

        self.run_girafe_layout.addLayout(self.v_run_layout)
        self.run_girafe_layout.addStretch(1)

        self.main_layout.addLayout(self.run_girafe_layout)

        self.setLayout(self.main_layout)

    def data_format_change(self, index):
        """
        Called if the data format selected is changed
        Args:
            index:

        Returns:

        """
        # it should not be empty
        if self.data_wrapper_combo_box.count() == 0:
            return

        if self.analyses_widget is None:
            return

        previous_data_format = self.current_data_wrapper_name

        self.current_data_wrapper_name = self.data_wrapper_combo_box.currentText().strip()

        self.analyses_widget.populate(previous_data_wrapper=previous_data_format)

    def keyPressEvent(self, event):
        """

        Args:
            event: Space: play from actual frame

        Returns:

        """
        # setting background picture
        if event.key() == QtCore.Qt.Key_Return:
            self.run_girafe()

    def _add_new_data_format(self, wrapper_id, data_format, format_file_name, class_instance):
        if wrapper_id in self.data_format_dict:
            return

        self.data_format_dict[wrapper_id] = (data_format, format_file_name, class_instance)
        self.data_wrapper_combo_box.addItem(wrapper_id + self.empty_string_combo_box)

    def select_new_data_format(self):
        """
        Open a file dialog to choose a new data format
        Returns:

        """
        file_dialog = QFileDialog(self.main_window, "Choose file implementing a GIRAFE format")

        # setting options
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.DontUseCustomDirectoryIcons
        file_dialog.setOptions(options)

        # ARE WE TALKING ABOUT FILES OR FOLDERS
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Python files (*.py)")

        # OPENING OR SAVING
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)

        # SET THE STARTING DIRECTORY
        # default_value = self.analysis_arg.get_default_value()
        # if default_value is not None and isinstance(default_value, str):
        #     self.file_dialog.setDirectory(default_value)

        # print(f"if file_dialog.exec_() == QDialog.Accepted")
        # print(f"file_dialog.exec_() {file_dialog.exec_()}")
        if file_dialog.exec() == QDialog.Accepted:
            new_data_file_name = file_dialog.selectedFiles()[0]
            wrapper_info = instantiate_girafe_data_wrapper(new_data_file_name)
            if wrapper_info is not None:
                self._add_new_data_format(*wrapper_info)

    def get_selected_data_format(self):
        """
        Return the data format selected in the combobox
        Returns:

        """
        if self.data_wrapper_combo_box.count() == 0:
            return None
        return self.data_format_dict[self.data_wrapper_combo_box.currentText().strip()][0]

    def run_last_analysis(self):
        """
        Run the last analysis
        :return:
        """
        pass
        # available analyses, instances of
        # key is a the name of the analysis, value is a list with analysis instance and the Python file_name
        # self.analyses_widget.available_analyses
        # First we get the name of the last analysis run
        # print(f"self.analyses_widget.available_analyses {list(self.analyses_widget.available_analyses.keys())}")
        #1 ex: ['Clustering variants by distance', 'Compute variants distance', 'Distribution RMS to wild by phenotype', 'Plot age of onset by variant', 'Plot variables vs distance to wild', 'Plot variants on SCN8A channel', 'Variables pairwise correlation']
        last_analyse_run_dir_name = self.config_handler.get_last_analyse_run_dir_name()
        # getting the last part
        last_analyse_name = pathlib.PurePath(last_analyse_run_dir_name).name
        # with timestamps, used to get the yaml_file
        last_analyse_name_with_ts = last_analyse_name
        index_ = last_analyse_name.find("_")
        if index_ >= 0:
            # removing the timestamps
            last_analyse_name = last_analyse_name[:index_]
        # else we assume there is no timestamp
        # print(f"last_analyse_name {last_analyse_name}")
        if last_analyse_name not in self.analyses_widget.available_analyses:
            print(f"{last_analyse_name} not available")
            return
        # GirafeAnalysis
        # 2nd argument is the path & file_name of the python file
        analysis_instance = self.analyses_widget.available_analyses[last_analyse_name][0]
        analysis_instance.gui = False # no GUI involved
        data_format = self.data_format_dict[self.current_data_wrapper_name][0]
        data_to_load_dir_name = self.config_handler.get_files_to_analyse_dir_names(data_format=
                                                               data_format)
        # print(f"data_to_load_dir_name {data_to_load_dir_name}")
        if data_to_load_dir_name is None:
            print(f"No directory to load data from found")
            return

        # we check if there is the yaml file with the parameters used for the analysis
        yaml_file = os.path.join(last_analyse_run_dir_name, last_analyse_name_with_ts + ".yaml")
        if not os.path.isfile(yaml_file):
            print(f"Not found: {yaml_file}")
            return

        data_dict = dict()
        data_wrapper = self.data_format_dict[self.current_data_wrapper_name][2]
        file_and_dir_names = []
        # look for filenames in the first directory, if we don't break, it will go through all directories
        for (dirpath, dirnames, local_filenames) in os.walk(data_to_load_dir_name):
            file_and_dir_names.extend(local_filenames)
            file_and_dir_names.extend(dirnames)
            break
        for file_and_dir_name in file_and_dir_names:
            if data_wrapper.is_data_valid(data_ref=os.path.join(data_to_load_dir_name, file_and_dir_name)):
                data_instance = data_wrapper(data_ref=os.path.join(data_to_load_dir_name, file_and_dir_name))
                data_dict[data_instance.identifier] = data_instance
                # nwb_path_list[data_instance.identifier] = os.path.join(data_to_load_dir_name, file_and_dir_name)
                # to_add_labels.append(data_instance.identifier)
        # print(f"last_analyse_run_dir_name {last_analyse_run_dir_name}")
        # print(f"data_dict len {len(data_dict)}")

        # now we want to select only the data used
        with open(yaml_file, 'r') as stream:
            analysis_args_from_yaml = yaml.load(stream, Loader=yaml.Loader)

        if "session_identifiers" not in analysis_args_from_yaml:
            return

        data_list = [data_dict[key] for key in analysis_args_from_yaml["session_identifiers"]]
        # print(f"len(data_list) {len(data_list)}")
        analysis_instance.set_data(data_to_analyse=data_list)

        # so we can create a copy of this yaml without using the GUI
        to_copy_in_new_yaml = dict()

        kwargs = {}
        for arg_name, args_content in analysis_args_from_yaml.items():
            if "_final_value" not in args_content:
                # not an argument for the analysis
                continue
            to_copy_in_new_yaml[arg_name] = args_content
            kwargs[arg_name] = args_content["_final_value"]

        kwargs["__to_copy_in_new_yaml__"] = to_copy_in_new_yaml
        analysis_instance.run_analysis(**kwargs)

        # analysis_instance.set_arguments_for_gui()
        # analysis_arguments_handler = analysis_instance.analysis_arguments_handler
        # analysis_arguments_handler.load_analysis_argument_from_yaml_file(yaml_file)
        # analysis_package = AnalysisPackage(cicada_analysis=self.copied_data,
        #                                    analysis_name=analysis_instance.name,
        #                                    name=random_id, main_window=self.parent, parent=self,
        #                                    config_handler=self.config_handler)

        # if used again in the GUI
        analysis_instance.gui = True

    def run_girafe(self):
        """
        Open the main window
        Returns:

        """
        if self.cicada_main_window_loading:
            return

        if self.data_wrapper_combo_box.count() == 0:
            return

        analyses_instances = self.analyses_widget.get_analyses_instances()
        if len(analyses_instances) == 0:
            message_box = QMessageBox()
            my_path = os.path.abspath(os.path.dirname(__file__))
            message_box.setWindowIcon(QtGui.QIcon(os.path.join(my_path, 'icons/svg/cicada_open_focus.svg')))
            message_box.setText(f"No analysis selected")
            message_box.exec()
            return

        # we update the configuration file
            # key is the wrapper_id (str) and value is a tuple with data_format and file_name (python file)
        data_format_files = []
        for data_value in self.data_format_dict.values():
            data_format_files.append(data_value[1])

        print(f"")
        self.config_handler.update_config_field(field_name="available_data_wrappers", field_value=data_format_files)
        self.config_handler.update_config_field(field_name="dirs_with_analyses_to_load",
                                                field_value=self.analyses_widget.dirs_with_analyses_loaded)
        self.config_handler.update_config_field(field_name="last_data_wrapper_used",
                                                field_value=self.current_data_wrapper_name)

        self.cicada_main_window_loading = True
        cicada_main_window = GirafeMainWindow(config_handler=self.config_handler,
                                              data_format=self.data_format_dict[self.current_data_wrapper_name][0],
                                              data_wrapper=self.data_format_dict[self.current_data_wrapper_name][2],
                                              analyses_instances=analyses_instances)

        # putting the window at the center of the screen
        # screenGeometry is an instance of Qrect
        screenGeometry = QApplication.desktop().screenGeometry()
        x = (screenGeometry.width() - cicada_main_window.width()) / 2
        y = (screenGeometry.height() - cicada_main_window.height()) / 2
        cicada_main_window.move(x, y)
        cicada_main_window.show()

        self.cicada_main_window_loading = False


class AnalysesListWidget(QListWidget):

    def __init__(self, analyses_widget, config_handler):
        QListWidget.__init__(self)
        self.config_handler = config_handler
        self.special_background_on = False
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # TODO: fixed menu to show subject info
        # self.customContextMenuRequested.connect(self.showContextMenu)
        self.analyses_widget = analyses_widget
        self.arguments_section_widget = None

        if config_handler.main_window_bg_pictures_displayed_by_default:
            self.set_random_background_picture()

    def set_random_background_picture(self):
        """Set a random background picture from the repertory set in the config file"""
        pic_path = self.config_handler.get_random_main_window_bg_picture(widget_id="initial_config")
        if pic_path is None:
            return
        self.setStyleSheet(
            f"border-image:url(\"{pic_path}\")")
        self.special_background_on = True

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_P:
            if self.special_background_on:
                self.setStyleSheet(
                    "background-image:url(\"\"); background-position: center;")
                self.special_background_on = False
            else:
               self.set_random_background_picture()
        elif event.key() == QtCore.Qt.Key_Return:
            self.analyses_widget.main_window.run_girafe()


class AnalysesWidget(QWidget):

    def __init__(self, config_handler, main_window, dirs_with_analyses_loaded, available_analyses=None):

        super().__init__()

        self.main_window = main_window
        # deal with the configuration
        self.config_handler = config_handler

        # the key is the data_format (wrapper in our case) and the value is a list
        # of analysis names that represents the analyses that were selected last time by this format
        self.last_analyses_selected_dict = dict()

        # key is a the name of the analysis, value is a list with analysis instance and the Python file_name
        self.available_analyses = SortedDict()
        if available_analyses is not None:
            self.available_analyses.update(available_analyses)

        self.layout = QVBoxLayout()
        self.hlayout = QHBoxLayout()

        # Create menu to check or uncheck all/none/selected items
        self.selectButton = QToolButton()
        my_path = os.path.abspath(os.path.dirname(__file__))
        self.selectButton.setIcon(QtGui.QIcon(os.path.join(my_path, 'icons/svg/checkbox.svg')))
        self.selectButton.setStyleSheet('border: none;')
        self.selectButton.setPopupMode(QToolButton.InstantPopup)
        self.selectMenu = QMenu()
        self.selectButton.setMenu(self.selectMenu)
        self.selectAllAct = QAction('All')
        self.selectAllAct.triggered.connect(self.check_all)
        self.unselectAllAct = QAction('None')
        self.unselectAllAct.triggered.connect(self.uncheck_all)
        self.unselectSelectedAct = QAction('Uncheck selected')
        self.unselectSelectedAct.triggered.connect(self.uncheck_selected)
        self.selectSelectedAct = QAction('Check selected')
        self.selectSelectedAct.triggered.connect(self.check_selected)
        self.selectMenu.addAction(self.selectAllAct)
        self.selectMenu.addAction(self.unselectAllAct)
        self.selectMenu.addAction(self.unselectSelectedAct)
        self.selectMenu.addAction(self.selectSelectedAct)
        self.hlayout.addWidget(self.selectButton)

        self.q_label_empty = QLabel("  ")
        self.q_label_empty.setAlignment(Qt.AlignCenter)
        self.q_label_empty.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.q_label_empty.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.hlayout.addWidget(self.q_label_empty)

        self.dir_analyses_from_basename_to_full_path = dict()
        self.analyses_dirs_combo_box = QComboBox()
        self.analyses_dirs_combo_box.setToolTip(f"Loaded analyses' directories")
        self.empty_string_combo_box = "    "

        self.dirs_with_analyses_loaded = dirs_with_analyses_loaded
        for dir_name in dirs_with_analyses_loaded:
            self.dir_analyses_from_basename_to_full_path[os.path.basename(dir_name)] = dir_name
            # adding space for display purpose
            self.analyses_dirs_combo_box.addItem(os.path.basename(dir_name) + self.empty_string_combo_box)
        self.hlayout.addWidget(self.analyses_dirs_combo_box)

        self.add_dir_button = QPushButton("+")
        self.add_dir_button.setToolTip("Add new analyses' directory to load")
        self.add_dir_button.clicked.connect(self.add_analyses_dir)
        self.hlayout.addWidget(self.add_dir_button)

        self.remove_dir_button = QPushButton("-")
        self.remove_dir_button.setToolTip("Remove new analyses' directory to load")
        self.remove_dir_button.clicked.connect(self.remove_analyses_dir)
        self.hlayout.addWidget(self.remove_dir_button)

        self.hlayout.addStretch(1)

        self.layout.addLayout(self.hlayout)

        self.hlayout2 = QHBoxLayout()

        self.q_list = AnalysesListWidget(analyses_widget=self, config_handler=self.config_handler)
        self.q_list.doubleClicked.connect(self.double_click_event)
        self.q_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # connecting the button that will fill the analysis tree
        # if to_analysis_button:
        #     to_analysis_button.clicked.connect(self.send_data_to_analysis_tree)

        self.layout.addWidget(self.q_list)
        self.items = []
        # self.populate(self.cicada_main_window.labels)
        self.q_list.itemSelectionChanged.connect(self.on_change)
        self.hlayout2.addLayout(self.layout)
        self.setLayout(self.hlayout2)

        if len(self.available_analyses) > 0:
            self.populate()

    def add_analyses_dir(self):
        """

        Returns:

        """
        file_dialog = QFileDialog(self, "Select Directory with analyses")

        # setting options
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.DontUseCustomDirectoryIcons

        file_dialog.setOptions(options)
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        if file_dialog.exec_() == QDialog.Accepted:
            dir_name = file_dialog.selectedFiles()[0]  # returns a list
            if dir_name not in self.dirs_with_analyses_loaded:
                self.dirs_with_analyses_loaded.append(dir_name)
                self.dir_analyses_from_basename_to_full_path[os.path.basename(dir_name)] = dir_name
                self.analyses_dirs_combo_box.addItem(os.path.basename(dir_name) + self.empty_string_combo_box)
                self.available_analyses.update(extract_analyses_from_dir(dir_name, self.config_handler))
                self.populate(previous_data_wrapper=self.main_window.current_data_wrapper_name)


    def remove_analyses_dir(self):
        """

        Returns:

        """
        if self.analyses_dirs_combo_box.count() == 0:
            return

        current_basename_dir = self.analyses_dirs_combo_box.currentText().strip()

        current_full_dir = self.dir_analyses_from_basename_to_full_path[current_basename_dir]
        self.dirs_with_analyses_loaded.remove(current_full_dir)
        del self.dir_analyses_from_basename_to_full_path[current_basename_dir]
        self.analyses_dirs_combo_box.removeItem(self.analyses_dirs_combo_box.currentIndex())

        # dict key is a the name of the analysis, value is a list with analysis instance and the Python file_name
        analyses_to_remove_dict = extract_analyses_from_dir(dir_name=current_full_dir,
                                                            config_handler=self.config_handler)
        for analyse_name in analyses_to_remove_dict.keys():
            if analyse_name in self.available_analyses:
                del self.available_analyses[analyse_name]

        self.populate(previous_data_wrapper=self.main_window.current_data_wrapper_name)



    def get_analyses_instances(self):
        """

        Returns: the list of analyses instances selected

        """
        analyses_instances_list = []

        for index in range(self.q_list.count()):
            if self.q_list.item(index).checkState() == 2:
                analysis_name = self.q_list.item(index).text()
                if analysis_name in self.available_analyses:
                    analyses_instances_list.append(self.available_analyses[analysis_name][0])

        return analyses_instances_list

    def uncheck_all(self):
        """Uncheck all items"""

        for idx in range(self.q_list.count()):
            self.q_list.item(idx).setCheckState(QtCore.Qt.Unchecked)

    def uncheck_selected(self):
        """Uncheck selected item(s)"""

        for idx in range(self.q_list.count()):
            for item in self.items:
                if self.q_list.item(idx).text() == item:
                    self.q_list.item(idx).setCheckState(QtCore.Qt.Unchecked)

    def check_all(self):
        """Check all items"""

        for idx in range(self.q_list.count()):
            self.q_list.item(idx).setCheckState(QtCore.Qt.Checked)

    def check_selected(self):
        """Check selected item(s)"""

        for idx in range(self.q_list.count()):
            for item in self.items:
                if self.q_list.item(idx).text() == item:
                    self.q_list.item(idx).setCheckState(QtCore.Qt.Checked)

    def on_change(self):
        """Handle change in selection"""

        self.items = [item.text() for item in self.q_list.selectedItems()]

    def get_items(self):
        """
        Returns list of items
        Returns:
            list of items

        """

        return [item for item in self.items]

    def populate(self, method='clear', previous_data_wrapper=None):
        """
        Populate the QListWidget with sessions labels

        Args:
            labels (list): Sessions identifiers
            method (str): In case we don't want to clear the QListWidget
            previous_data_wrapper (str): if not None, allows to save the previous_data_format analyses selected,
            only those analyses will be automatically selected, otherwise all are selected

        """

        if previous_data_wrapper is not None:
            selected_analyses = []
            for index in range(self.q_list.count()):
                if self.q_list.item(index).checkState() == 2:
                    analysis_name = self.q_list.item(index).text()
                    selected_analyses.append(analysis_name)
            self.last_analyses_selected_dict[previous_data_wrapper] = selected_analyses

        if method == 'clear':
            self.q_list.clear()
        # if method == 'add':
        #     for label in labels:
        #         if label not in self.cicada_main_window.labels:
        #             self.cicada_main_window.labels.append(label)
        #     self.cicada_main_window.load_group_from_config()
        items = []
        if self.q_list.count() != 0:
            for index in range(self.q_list.count()):
                items.append(self.q_list.item(index).text())
        for analysis_name, analysis_data in self.available_analyses.items():
            analysis_instance = analysis_data[0]
            invert_op = getattr(analysis_instance, "is_data_format_accepted", None)
            if callable(invert_op):
                wrapper_id = self.main_window.data_wrapper_combo_box.currentText().strip()
                data_format = self.main_window.get_selected_data_format()
                if data_format is None:
                    continue
                data_format_accepted = analysis_instance.is_data_format_accepted(data_format)
                if data_format_accepted and (analysis_name not in items):
                    item = QListWidgetItem()
                    if wrapper_id in self.last_analyses_selected_dict:
                        if str(analysis_name) in self.last_analyses_selected_dict[wrapper_id]:
                            item.setCheckState(QtCore.Qt.Checked)
                        else:
                            item.setCheckState(QtCore.Qt.Unchecked)
                    else:
                        item.setCheckState(QtCore.Qt.Checked)
                    item.setText(str(analysis_name))
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
                    self.q_list.addItem(item)

    def double_click_event(self, clicked_item):
        """
        Handle double click on item in QListWidget.
        Check or uncheck an item or a group on double click.

        Args:
            clicked_item: Double clicked item

        """
        flags = clicked_item.flags()
        if flags & 1:  # Item is selectable, meaning it is a session
            if self.q_list.item(clicked_item.row()).checkState():
                self.q_list.item(clicked_item.row()).setCheckState(QtCore.Qt.Unchecked)
            else:
                self.q_list.item(clicked_item.row()).setCheckState(QtCore.Qt.Checked)
        # else:  # Item is not selectable, meaning it is a separator
        #     row_index = clicked_item.row() + 1
        #     item_is_selectable = True
        #     while item_is_selectable:
        #         if self.q_list.item(row_index).checkState():
        #             self.q_list.item(row_index).setCheckState(QtCore.Qt.Unchecked)
        #         else:
        #             self.q_list.item(row_index).setCheckState(QtCore.Qt.Checked)
        #         try:
        #             if not self.q_list.item(row_index + 1).flags() & 1:
        #                 item_is_selectable = False
        #             row_index += 1
        #         except AttributeError:
        #             item_is_selectable = False