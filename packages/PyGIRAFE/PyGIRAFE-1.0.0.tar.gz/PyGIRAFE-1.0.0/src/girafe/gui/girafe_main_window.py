from qtpy.QtWidgets import *
from qtpy import QtGui
from qtpy import QtCore
from qtpy.QtCore import Qt
import os
from copy import deepcopy
import sys
from functools import partial
import girafe.preprocessing.utils as utils
import yaml
# from cicada.gui.exploratory.cicada_exploratory_main import ExploratoryMainWindow
from girafe.gui.girafe_analysis_tree_gui import AnalysisTreeApp
from girafe.gui.girafe_analysis_overview import AnalysisOverview
from girafe.gui.girafe_analysis_parameters_gui import AnalysisPackage
from girafe.gui.girafe_group_sort import SessionsWidget
from girafe.gui.girafe_all_group import AllGroups
import platform
from sortedcontainers import SortedDict
import numpy as np

import ctypes


class GirafeMainWindow(QMainWindow):
    """Main window of the GUI"""
    def __init__(self, config_handler, data_format, data_wrapper, analyses_instances):
        """

        Args:
            config_handler:
            data_format: (str)
            data_analysis_wrapper: Instance of GirafeAnalysisFormatWrapper
            analyses_instances:
        """
        super().__init__()
        # To display an the window icon as the application icon in the task bar on Windows
        if platform.system() == "Windows":
            myappid = u'cossart.cicada.gui.alpha'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        my_path = os.path.abspath(os.path.dirname(__file__))
        self.setWindowIcon(QtGui.QIcon(os.path.join(my_path, 'icons/svg/cicada_open_focus.svg')))

        # instances of GirafeAnalysis classes
        self.analyses_instances = analyses_instances
        self.data_wrapper = data_wrapper
        # data format choose in the initial config
        self.data_format = data_format

        # ----- misc attributes -----
        self.labels = []
        self.to_add_labels = []

        # attributes concerning menus, groups etc...
        self.group_menu_actions = dict()
        # associated to each action name an id that link it to the corresponding attribution in CicadaWrapperInstance
        self.actions_names_id = dict()

        # TODO: Describe those variables
        # key is the group name, values are a list of list of 2 str: the str represent the id of the session data,
        # and the second str the path to the file/directory to load the data such as it was when the group was created
        # the idea behind having the id and the path is to be able to either select the id in the list already loaded
        # if present, otherwise loading the data if the file/directory is valid.
        self.groups_data = dict()
        self.grouped_labels = []

        # allows to access config param
        self.config_handler = config_handler

        self.createActions()
        self.createMenus()
        self.object_created = []
        self.labels = []
        self.setWindowTitle(f"GIRAFE - {self.data_format}")

        screenGeometry = QApplication.desktop().screenGeometry()
        # making sure the window is not bigger than the dimension of the screen
        width_window = min(1500, screenGeometry.width())
        # width_window = screenGeometry.width()
        height_window = min(800, screenGeometry.height())
        self.resize(width_window, height_window)
        self.param_list = []
        # list of param (id of the param used to group the items in the tree)
        self.param_group_list = []
        # indicated if groups are available ? See if useful ?
        self.grouped = False
        # indicate if the items are sorted
        # self.sorted = False
        self.nwb_path_list = dict()
        # contains the data, will be instances of GirafeAnalysisFormatWrapper
        # the key is the identifier of the data file, value is the instance
        self.data_dict = SortedDict()

        self.openWindow()
        self.groupMenu.setEnabled(True)
        self.selectGroupMenu.setEnabled(True)
        self.load_group_from_config()

        # to uncomment so the last dataset open be automatically uploaded
        self.load_data_from_config()

    def load_group_from_config(self):
        """
        Load groups from a YAML file in the config folder.
        If groups exist it will activate the menu for groups (to select them...)
        :return:
        """
        my_path = os.path.abspath(os.path.dirname(__file__))

        group_file_name = os.path.join(my_path, "../config/group.yaml")
        # initializing the groups
        self.groups_data = dict()

        if not os.path.isfile(group_file_name):
            return

        with open(group_file_name, 'r') as stream:
            groups_from_yaml_file = yaml.safe_load(stream)

        if (groups_from_yaml_file is not None) and (self.data_wrapper.WRAPPER_ID in groups_from_yaml_file):
            self.groups_data = groups_from_yaml_file[self.data_wrapper.WRAPPER_ID]
        else:
            self.groups_data = dict()

        self.grouped_labels = []
        if self.groups_data:
            self.grouped = True
            for data_id_and_path_list in self.groups_data.values():
                data_id_list = [data_id for data_id, data_path in data_id_and_path_list]
                self.grouped_labels.append(data_id_list)
                # for file in id_and_path:
                #     if self.data_wrapper.is_data_valid(data_ref=file):
                #         data_wrapper = self.data_wrapper(data_ref=file)
                #         self.data_dict[data_wrapper.identifier] = data_wrapper
                #         data_id_list.append(data_wrapper.identifier)
                self.grouped_labels.append(data_id_list)
            # self.showGroupMenu.setEnabled(True)
            # self.addGroupDataMenu.setEnabled(True)
            self.selectGroupMenu.setEnabled(True)
            self.populate_menu()
        else:
            # self.showGroupMenu.setEnabled(False)
            # self.addGroupDataMenu.setEnabled(False)
            self.selectGroupMenu.setEnabled(False)
            # self.showGroupMenu.clear()
            self.selectGroupMenu.clear()
            # self.addGroupDataMenu.clear()

        # self.addGroupDataMenu.setEnabled(True)

    def load_data_from_config(self):
        """Check if the last dir opened is saved in config and load it automatically"""
        self.labels = []
        self.to_add_labels = []
        dir_name = self.config_handler.get_files_to_analyse_dir_names(data_format=self.data_format)

        if dir_name is not None:
            # for dir_name in dir_names:
            self.load_data_from_dir(dir_name=dir_name, method='clear')

    def open_new_dataset(self):
        """Open a directory"""

        self.labels = []
        self.to_add_labels = []
        self.nwb_path_list = dict()
        self.grouped_labels = []
        self.file_dialog = QFileDialog(self, "Select Directory")

        # setting options
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.DontUseCustomDirectoryIcons

        self.file_dialog.setOptions(options)
        self.file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        if self.file_dialog.exec_() == QDialog.Accepted:
            dir_name = self.file_dialog.selectedFiles()[0]  # returns a list
            self.file_dialog.setDirectory(dir_name)
            self.load_data_from_dir(dir_name=dir_name, method='clear')

    def add_data(self):
        """Open a directory"""

        self.to_add_labels = []
        self.file_dialog = QFileDialog(self, "Select Directory")

        # setting options
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.DontUseCustomDirectoryIcons

        self.file_dialog.setOptions(options)
        self.file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        if self.file_dialog.exec_() == QDialog.Accepted:
            dir_name = self.file_dialog.selectedFiles()[0]  # returns a list
            self.file_dialog.setDirectory(dir_name)
            self.load_data_from_dir(dir_name=dir_name, method='add')

    def load_data_from_dir(self, dir_name, method):
        """
        Load data (currently only NWB) from selected directory

        Args:
            dir_name (str): Path to data
            method (str): String to choose whether to add data to the existing dataset or open a new one,
             takes two values : 'add' or 'clear'

        """

        # TODO: deal with the different format
        # TODO: decide if we should add those nwb to the ones already opened (if that's the case)
        #  or erase the ones present and replace them by the new one.
        #  probably best to have 2 options on the menu open new, and something like add data
        file_and_dir_names = []
        # look for filenames in the first directory, if we don't break, it will go through all directories
        for (dirpath, dirnames, local_filenames) in os.walk(dir_name):
            file_and_dir_names.extend(local_filenames)
            file_and_dir_names.extend(dirnames)
            break
        for file_and_dir_name in file_and_dir_names:
            if self.data_wrapper.is_data_valid(data_ref=os.path.join(dir_name, file_and_dir_name)):
                data_wrapper = self.data_wrapper(data_ref=os.path.join(dir_name, file_and_dir_name))
                self.data_dict[data_wrapper.identifier] = data_wrapper
                self.nwb_path_list[data_wrapper.identifier] = os.path.join(dir_name, file_and_dir_name)
                self.to_add_labels.append(data_wrapper.identifier)
        self.labels = self.labels + self.to_add_labels
        # checking there is at least one data file loaded
        if len(self.data_dict) > 0:
            if method == 'clear':
                self.musketeers_widget.session_widget.populate(self.labels, method)
            else:
                self.musketeers_widget.session_widget.populate(self.to_add_labels, method)
            # self.sortMenu.setEnabled(True)
            self.groupMenu.setEnabled(True)
            # then we save the last location opened in the yaml file in config
            self.save_last_data_location(dir_name=dir_name)

    def save_last_data_location(self, dir_name):
        """
        Keep path to last data directory selected in a YAML in config

        Args:
            dir_name (str): Path to data to be saved

        """
        self.config_handler.update_files_to_analyse_dir_names(data_format=self.data_format, dir_name=dir_name)

    def populate_menu(self):
        """Populate the menu to load groups"""
        # self.showGroupMenu.clear()
        # self.addGroupDataMenu.clear()
        self.selectGroupMenu.clear()
        counter = 0
        for group_name in self.groups_data.keys():
            counter += 1
            group_act = QAction(group_name, self)
            group_act.triggered.connect(partial(self.select_group, group_name, True))
            self.selectGroupMenu.addAction(group_act)

    def select_group(self, group_name, unchecking_checked_items=True):
        """
        Select all sessions of a group, load them if they are not loaded yet. Unselect other sessions

        Args:
            group_name (str) : Name of the group saved in YAML
            unchecking_checked_items (bool): if True, then the previously checked items are unchecked, and only
            items in the group is loaded

        """
        if group_name not in self.groups_data:
            return

        # unselect all items
        if unchecking_checked_items:
            self.musketeers_widget.session_widget.uncheck_all()

        # list of data_id that belongs to the group and exists we need to select
        items_to_select = []
        new_data_loaded = False
        for data_id, data_path in self.groups_data[group_name]:
            # now we check if the session with given id is already loaded, if so we select it
            # if now, we tried to load it and then select it

            # data_id = id_and_path[0]
            # data_path = id_and_path[1]

            if data_id not in self.data_dict:
                if os.path.exists(data_path) and self.data_wrapper.is_data_valid(data_ref=data_path):
                    data_wrapper = self.data_wrapper(data_ref=data_path)
                    self.data_dict[data_id] = data_wrapper
                    items_to_select.append(data_id)
                    new_data_loaded = True
            else:
                items_to_select.append(data_id)

        if new_data_loaded:
            # update the display with new data
            self.update_session_widget()

        for item_to_select in items_to_select:
            self.musketeers_widget.session_widget.select_item(item_to_select)

    def createMenus(self):
        """Create menu bar and put some menu in it"""

        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.addAct)
        self.fileMenu.addSeparator()
        # self.fileMenu.addAction(self.showSessionAct)
        self.fileMenu.addAction(self.exitAct)

        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.viewMenu = QMenu("&View", self)

        # self.sortMenu = QMenu("Sort by", self.viewMenu, enabled=False)
        self.groupMenu = QMenu("Group by", self.viewMenu, enabled=False)

        # self.showGroupMenu = QMenu("Load Group", self.fileMenu, enabled=False)
        # self.addGroupDataMenu = QMenu('Add Group', self.fileMenu, enabled=False)
        self.selectGroupMenu = QMenu("Select group", self.fileMenu, enabled=True)
        # self.fileMenu.addMenu(self.showGroupMenu)
        # self.fileMenu.addMenu(self.addGroupDataMenu)
        self.fileMenu.addMenu(self.selectGroupMenu)
        self.fileMenu.addAction(self.seeAllGroupAct)
        self.viewMenu.addMenu(self.groupMenu)


        # Add filters to "Group by"
        self.create_group_menu()
        for q_action in self.group_menu_actions.values():
            self.groupMenu.addAction(q_action)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)

    def create_group_menu(self):
        """Create group menu"""
        self.group_menu_actions = SortedDict()

        # using the groups defined in the wrapper
        action_group_dict = self.data_wrapper.grouped_by()

        for action_name in action_group_dict.keys():
            q_action = QAction(action_name, self, checkable=True)
            q_action.triggered.connect(partial(self.uncheck_group, action_name))
            q_action.triggered.connect(partial(self.on_group, action_name))
            self.group_menu_actions[action_name] = q_action

    def createActions(self):
        """Create some QAction"""

        self.openAct = QAction("&Open new dataset...", self, shortcut="Ctrl+O", triggered=self.open_new_dataset)
        self.addAct = QAction("&Add data to current dataset...", self, shortcut="Ctrl+P", triggered=self.add_data)
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.exitAct.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.aboutAct = QAction("&About", self, triggered=self.about)
        self.aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)
        # self.showSessionAct = QAction("&Show session", self, triggered=self.openWindow)
        self.showGroupAct = QAction("&Show all groups", self)
        self.seeAllGroupAct = QAction('&See all groups', self, triggered=self.see_all_groups)


    def see_all_groups(self):
        """Display a widget with all existing groups"""
        self.all_group_window = AllGroups(widget='main', parent=self)
        if self.groups_data:
            self.all_group_window.populate_list(self.groups_data.keys())
        self.all_group_window.show()
        self.object_created.append(self.all_group_window)

    def uncheck_group(self, action_name):
        """
        Uncheck group menu parameter

        Args:
            param (str): Parameter name to uncheck

        """
        self.param_group_list = []
        for name, q_action in self.group_menu_actions.items():
            if action_name == name:
                continue
            q_action.setChecked(False)

    def on_group(self, param, state):
        """
        Give group list and parameters value to populate QListWidget

        Args:
            param (str): Parameter to group by
            state (int): State of the checkbox
        """
        self.grouped = True
        if state > 0:  # From unchecked to checked
            # self.sorted = False
            # self.uncheck_all_sort()
            self.musketeers_widget.session_widget.update_text_filter(param)
            if param not in self.param_group_list:
                self.param_group_list.append(param)

            dict_group = SortedDict()
            # data is an instance of CicadaAnalysisWrapper
            for data in self.data_dict.values():
                # param_id = self.actions_names_id.get(param, param)
                # if param_id.lower().startswith("has"):
                #     continue
                action_group_dict = self.data_wrapper.grouped_by()
                attribute_id = action_group_dict[param]
                if not hasattr(data, attribute_id):
                    value = None
                else:
                    # testing if it's callable
                    value = getattr(data, attribute_id)
                    if callable(value):
                        value = value()

                if value is None:
                    value = "NA"
                else:
                    if isinstance(value, str) and ("_" in value):
                        pass
                    else:
                        # changing it as int or float, use
                        try:
                            value = int(value)
                        except ValueError:
                            try:
                                value = np.round(float(value), 3)
                            except ValueError:
                                pass
                value = utils.ComparableItem(value=value)
                if value not in dict_group:
                    # print(f"value {str(value)}")
                    dict_group[value] = []
                dict_group[value].append(data)

            self.musketeers_widget.session_widget.form_group(dict_group)
        else:  # From checked to unchecked
            if param in self.param_group_list:
                if len(self.param_group_list) == 1:
                    self.param_group_list = []
                else:
                    self.param_group_list.remove(param)
            self.grouped = False
            self.musketeers_widget.session_widget.update_text_filter()
            self.musketeers_widget.session_widget.populate(self.labels)

    def delete_groups_session(self, groups_to_delete, update_yaml_file=True):
        """
        Delete one or multiple groups of session, update the yaml file
        :param groups_to_delete: (str or list) one or multiple group name
        :param update_yaml_file: (bool) if True, the yaml file is updated
        :return:
        """

        if isinstance(groups_to_delete, str):
            groups_to_delete = [groups_to_delete]

        for group_name in groups_to_delete:
            if group_name in self.groups_data:
                del self.groups_data[group_name]

        self.musketeers_widget.session_widget.update_group_config_yaml_file()

    def update_session_widget(self):
        """
        Should be called when the list of items to be displayed in the session widget has been updated
        and we want to populate the session widget with the new items, but keeping the actual configuration (same
        selected items, same organization by group or lists)
        :return:
        """
        checked_items = self.musketeers_widget.session_widget.get_checked_items()

        if self.grouped and len(self.param_group_list) > 0:
            self.on_group(param=self.param_group_list[0], state=1)
        # elif self.sorted and len(self.param_group_list) > 0:
        #     self.on_sort(param=self.param_group_list[0], state=1)
        else:
            self.labels = [identifier for identifier in self.data_dict.keys()]
            self.musketeers_widget.session_widget.populate(self.labels, method='clear')
        # reselecting the same items as before
        self.musketeers_widget.session_widget.uncheck_all()
        for checked_item in checked_items:
            self.musketeers_widget.session_widget.select_item(checked_item)

    def about(self):
        """Small about QMessageBox for the project"""
        self.about_box = QDialog()
        my_path = os.path.abspath(os.path.dirname(__file__))
        self.about_box.setWindowIcon(QtGui.QIcon(os.path.join(my_path, 'icons/svg/cicada_open_focus.svg')))
        self.about_box.setWindowTitle("About CICADA")
        self.object_created.append(self.about_box)
        self.about_box.setMinimumSize(275, 125)
        vlayout = QVBoxLayout()

        github_layout = QHBoxLayout()
        icon_label_github = QLabel()
        icon_label_github.setScaledContents(True)
        icon_label_github.setMaximumSize(48, 48)
        icon_github_box = QtGui.QPixmap(os.path.join(my_path, 'icons/svg/github-logo.svg'))
        icon_label_github.setPixmap(icon_github_box)
        label_github_box = QLabel(self.about_box)
        label_github_box.setAlignment(Qt.AlignCenter)
        label_github_box.setTextFormat(Qt.RichText)
        label_github_box.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label_github_box.setOpenExternalLinks(True)
        label_github_box.setText("<a href=\"https://github.com/pappyhammer/cicada\">Github link!</a>")
        github_layout.addWidget(icon_label_github)
        github_layout.addWidget(label_github_box)

        doc_layout = QHBoxLayout()
        icon_label_doc = QLabel()
        icon_label_doc.setScaledContents(True)
        icon_label_doc.setMaximumSize(48, 48)
        icon_doc_box = QtGui.QPixmap(os.path.join(my_path, 'icons/svg/doc.svg'))
        icon_label_doc.setPixmap(icon_doc_box)
        label_doc_box = QLabel(self.about_box)
        label_doc_box.setAlignment(Qt.AlignCenter)
        label_doc_box.setTextFormat(Qt.RichText)
        label_doc_box.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label_doc_box.setOpenExternalLinks(True)
        label_doc_box.setText("<a href=\"https://readthedocs.org/\">Documentation link!</a>")
        doc_layout.addWidget(icon_label_doc)
        doc_layout.addWidget(label_doc_box)

        vlayout.addLayout(github_layout)
        vlayout.addLayout(doc_layout)
        self.about_box.setLayout(vlayout)
        self.about_box.show()

    def openWindow(self):
        """Open all widgets in a CentralWidget and call some menus that needed those widgets"""
        # self.showSessionAct.setEnabled(False)
        self.musketeers_widget = MusketeersWidget(config_handler=self.config_handler,
                                                  analyses_instances=self.analyses_instances,
                                                  cicada_main_window=self)
        self.setCentralWidget(self.musketeers_widget)
        self.saveGroupMenu = QAction('Create Group', self.fileMenu)
        self.fileMenu.addAction(self.saveGroupMenu)
        self.saveGroupMenu.triggered.connect(self.musketeers_widget.session_widget.save_group)

    def closeEvent(self, event):
        """
        Close all analyses windows on main window close
        """

        self.object_created = utils.flatten(self.object_created)
        copied_list = self.object_created.copy()
        for obj in copied_list:
            if isinstance(obj, AnalysisPackage):
                obj.close()
            else:
                obj.close()
                self.object_created.remove(obj)

        if self.object_created:
            event.ignore()
        else:
            self.close()


class MusketeersWidget(QWidget):
    """
    Gather in a layout the 3 main sub-windows composing the gui: displaying the subject sessions,
    the analysis tree and an overview of the running analysis
    """
    def __init__(self, config_handler, analyses_instances, cicada_main_window=None):
        QWidget.__init__(self, parent=cicada_main_window)
        self.cicada_main_window = cicada_main_window
        self.config_handler = config_handler

        self.main_layout = QVBoxLayout()

        self.layout = QHBoxLayout()
        to_analysis_button = QPushButton()
        to_analysis_button.setProperty("cicada", "True")

        self.session_widget = SessionsWidget(cicada_main_window=cicada_main_window,
                                             to_analysis_button=to_analysis_button,
                                             config_handler=self.config_handler)
        self.layout.addWidget(self.session_widget)

        self.layout.addWidget(to_analysis_button)

        to_parameters_button = QPushButton()
        to_parameters_button.setProperty("cicada", "True")

        analysis_tree_app = AnalysisTreeApp(parent=cicada_main_window, to_parameters_button=to_parameters_button,
                                            config_handler=self.config_handler, analyses_instances=analyses_instances)

        self.session_widget.analysis_tree = analysis_tree_app
        self.layout.addWidget(analysis_tree_app)

        self.layout.addWidget(to_parameters_button)

        # analysis_param_widget = AnalysisParametersApp()
        analysis_overview_widget = AnalysisOverview(parent=cicada_main_window, config_handler=self.config_handler)
        analysis_tree_app.analysis_overview = analysis_overview_widget
        self.layout.addWidget(analysis_overview_widget)
        # analysis_tree_app.arguments_section_widget = analysis_param_widget
        # useful to empty the arguments section when we click on the to_analysis_button
        # self.session_widget.arguments_section_widget = analysis_param_widget
        self.session_widget.analysis_overview_widget = analysis_overview_widget

        self.main_layout.addLayout(self.layout)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setAlignment(Qt.AlignCenter)

        try:
            from deepcinac.gui.cinac_gui import launch_cinac_gui
            launch_cinac_gui_button = QPushButton()
            launch_cinac_gui_button.setText("Launch CINAC GUI")
            launch_cinac_gui_button.clicked.connect(launch_cinac_gui)
            self.buttons_layout.addWidget(launch_cinac_gui_button)

            self.empty_label = QLabel()
            self.empty_label.setText("  ")
            self.empty_label.setProperty("empty_label", "True")

            self.buttons_layout.addWidget(self.empty_label)

        except ImportError:
            pass

        # no exploratory GUI
        # launch_exploratory_gui_button = QPushButton()
        # launch_exploratory_gui_button.setText("Badass GUI")
        # launch_exploratory_gui_button.clicked.connect(self.launch_exploratory_gui)
        # self.buttons_layout.addWidget(launch_exploratory_gui_button)

        # launch_cinac_gui_button.setProperty("cicada", "True")

        self.main_layout.addLayout(self.buttons_layout)

        self.setLayout(self.main_layout)

    def launch_exploratory_gui(self):
        # we want to make sure there is only one data selected to launch the GUI
        data_to_explore = self.session_widget.get_data_to_analyse()

        if len(data_to_explore) != 1:
            # display a message
            my_path = os.path.abspath(os.path.dirname(__file__))
            message_box = QMessageBox()
            message_box.setWindowIcon(QtGui.QIcon(os.path.join(my_path, '/icons/svg/cicada_open_focus.svg')))
            message_box.setText(f"You need to select only one session to explore instead of {len(data_to_explore)}")
            message_box.exec()
            return
        data_to_explore = data_to_explore[0]
        exploratory_window = ExploratoryMainWindow(config_handler=self.config_handler,
                                                   cicada_main_window=self.cicada_main_window,
                                                   data_to_explore=data_to_explore)
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - exploratory_window.width()) / 2
        y = (screen_geometry.height() - exploratory_window.height()) / 2
        # exploratory_window.move(x, y)
        # exploratory_window.show()
