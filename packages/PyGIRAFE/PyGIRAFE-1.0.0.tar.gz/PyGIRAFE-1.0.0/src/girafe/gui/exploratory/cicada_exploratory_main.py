from qtpy.QtWidgets import *
from qtpy import QtCore, QtGui
from .cicada_exploratory_widgets import BehaviorVideoWidget, CiVideoWidget, CiVideoConfigWidget, SignalWidget
from .cicada_time_intervals import TimeIntervalsManager
from cicada.utils.display.cells_map_utils import CellsCoord
from cicada.utils.misc import get_tree_dict_as_a_list

import platform
import os
import ctypes
import numpy as np
import pyqtgraph as pg


class ProcessedData:

    """
    Use a CicadaAnalysisWrapper instance to extract certain data and process them in order
    to make them accessible in the GUI
    """

    def __init__(self, data_wrapper, ci_movie_dimensions):
        """

        Args:
            data_wrapper: instance of CicadaAnalysisWrapper
        """
        self.data_wrapper = data_wrapper
        self.ci_movie_dimensions = ci_movie_dimensions
        # instance of CellsCoord
        self.cells_coord_dict = dict()
        self._construct_cell_map()

    def get_rois_ids(self):
        """
        Return the list of ids of the different kind or rois
        Returns:

        """
        return list(self.cells_coord_dict.keys())

    def _construct_cell_map(self):
        segmentation_dict = self.data_wrapper.get_segmentations()
        if len(segmentation_dict) == 0:
            # no ROIs registered
            return
        # print(f"segmentation_dict {segmentation_dict}")
        segmentation_infos = get_tree_dict_as_a_list(tree_dict=segmentation_dict)
        # print(f"segmentation_infos {segmentation_infos}")
        # filing the path to the segmentation data
        # for key, dict_info in segmentation_dict.items():
        #     segmentation_info = []
        #     segmentation_info.append(key)
        #     tmp_dict = dict_info[key]
        #     while True:
        #         key = list(tmp_dict.keys())
        #         segmentation_info.append(key)
        #         tmp_dict = tmp_dict[list_keys[0]]
        #         if not isinstance(tmp_dict, dict):
        #             if isinstance(tmp_dict, list):
        #                 segmentation_info.append(tmp_dict[0])
        #             else:
        #                 segmentation_info.append(tmp_dict)
        #             break
        for segmentation_info in segmentation_infos:
            segmentation_id = segmentation_info[-2]
            pixel_mask = self.data_wrapper.get_pixel_mask(segmentation_info=segmentation_info)
            if pixel_mask is not None:
                # pixel_mask of type pynwb.core.VectorIndex
                # each element of the list will be a sequences of tuples of 3 floats representing x, y and a float between
                # 0 and 1 (not used in this case)
                pixel_mask_list = [pixel_mask[cell] for cell in range(len(pixel_mask))]
                # TODO: get the real movie dimensions if available
                self.cells_coord_dict[segmentation_id] = CellsCoord(pixel_masks=pixel_mask_list, from_matlab=False,
                                              nb_lines=self.ci_movie_dimensions[1],
                                              nb_col=self.ci_movie_dimensions[0],
                                              invert_xy_coord=True)


class ExploratorySecondaryWindow(QMainWindow):
    """Main window of the Exploratory GUI"""
    def __init__(self, cicada_main_window, data_to_explore):
        super().__init__(parent=cicada_main_window)
        # QMainWindow.__init__(self)
        self.cicada_main_window = cicada_main_window
        # To display a the window icon as the application icon in the task bar on Windows
        if platform.system() == "Windows":
            myappid = u'cossart.cicada.gui.alpha'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        my_path = os.path.abspath(os.path.dirname(__file__))
        self.setWindowIcon(QtGui.QIcon(os.path.join(my_path, '../icons/svg/cicada_open_focus.svg')))
        self.data_to_explore = data_to_explore
        self.setWindowTitle(f"CICADA BADASS GUI - {self.data_to_explore.identifier}")

        screenGeometry = QApplication.desktop().screenGeometry()
        # making sure the window is not bigger than the dimension of the screen
        width_window = min(1800, screenGeometry.width())
        # width_window = screenGeometry.width()
        height_window = min(1000, screenGeometry.height())
        self.resize(width_window, height_window)


class ExploratoryMainWindow(QMainWindow):
    """Main window of the Exploratory GUI"""
    def __init__(self, config_handler, cicada_main_window, data_to_explore):
        super().__init__(parent=cicada_main_window)
        # QMainWindow.__init__(self)
        self.cicada_main_window = cicada_main_window
        # To display a the window icon as the application icon in the task bar on Windows
        if platform.system() == "Windows":
            myappid = u'cossart.cicada.gui.alpha'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        my_path = os.path.abspath(os.path.dirname(__file__))
        self.setWindowIcon(QtGui.QIcon(os.path.join(my_path, '../icons/svg/cicada_open_focus.svg')))

        # data_to_explore should be an instance of GirafeAnalysisFormatWrapper
        self.data_to_explore = data_to_explore
        # data_to_explore.get_intervals_names()
        # ----- misc attributes -----
        self.labels = []
        self.to_add_labels = []

        # attributes concerning menus, groups etc...
        self.group_menu_actions = dict()
        # associated to each action name an id that link it to the corresponding attribution in CicadaWrapperInstance
        self.actions_names_id = dict()

        # allows to access config param
        self.config_handler = config_handler

        # self.createActions()
        # self.createMenus()
        self.object_created = []
        self.labels = []
        self.setWindowTitle(f"CICADA BADASS GUI - {self.data_to_explore.identifier}")

        screenGeometry = QApplication.desktop().screenGeometry()
        # making sure the window is not bigger than the dimension of the screen
        width_window = min(1800, screenGeometry.width())
        # width_window = screenGeometry.width()
        height_window = min(1000, screenGeometry.height())
        self.resize(width_window, height_window)

        ## creating widgets to put in the window
        self.central_widget = ExploratoryCentralWidget(config_handler=config_handler,
                                                       data_to_explore=self.data_to_explore,
                                                       exploratory_main_window=self)
        self.setCentralWidget(self.central_widget)

        self.show()

    def keyPressEvent(self, event):
        """

        Args:
            event: Space: play from actual frame

        Returns:

        """
        # setting background picture
        if event.key() == QtCore.Qt.Key_Space:
            if self.central_widget.playing:
                self.central_widget.pause()
            else:
                self.central_widget.start()
        if event.key() == QtCore.Qt.Key_C:
            self.central_widget.set_current_timestep_to_actual_range()
        if event.key() == QtCore.Qt.Key_Plus or event.key() == QtCore.Qt.Key_Up:
            self.central_widget.change_timestamp_step(increment=True)
        if event.key() == QtCore.Qt.Key_Minus or event.key() == QtCore.Qt.Key_Down:
            self.central_widget.change_timestamp_step(increment=False)
        if event.key() == QtCore.Qt.Key_S:
            if self.central_widget.time_intervals_manager.config_widget.ti_start is None:
                self.central_widget.time_intervals_manager.config_widget.mark_ti_start()
            else:
                self.central_widget.time_intervals_manager.config_widget.mark_ti_stop()
        if event.key() == QtCore.Qt.Key_P:
            self.central_widget.ci_video_widget.switch_surprise_mfh()
            for behavior_video_widget in self.central_widget.behavior_video_widgets:
                behavior_video_widget.switch_surprise_mfh()
            # self.central_widget.behavior_video_widget_2.switch_surprise_mfh()
        if event.key() == QtCore.Qt.Key_Left:
            self.central_widget.previous_timestamp()
        if event.key() == QtCore.Qt.Key_Right:
            self.central_widget.next_timestamp()


class ExploratoryCentralWidget(QWidget):

    def __init__(self, config_handler, exploratory_main_window, data_to_explore):
        super().__init__(parent=exploratory_main_window)

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        self.min_timestamp, self.max_timestamp = data_to_explore.get_timestamps_range()
        # print(f"self.min_timestamp {self.min_timestamp}, self.max_timestamp {self.max_timestamp}")
        # define the step in sec when jumping timestamps 0.05 = 20Hz
        self.default_timestamp_step = 0.1
        self.min_timestamp_step = 0.05
        self.max_timestamp_step = 1
        self.timestamp_step_increment = 0.05
        # can be updated trough widget
        self.timestamp_step = self.default_timestamp_step
        self.data_to_explore = data_to_explore
        self.current_timestamp = self.min_timestamp
        self.playing = False
        self.updateTimer = QtCore.QTimer()
        self.updateTimer.timeout.connect(self.next_timestamp)

        self.config_handler = config_handler

        self.main_layout = QVBoxLayout()

        self.h_layout_widgets = QHBoxLayout()

        # ----------------------------------
        #           Behavior widgets
        # ----------------------------------
        self.behaviour_video_layout = QHBoxLayout()
        ci_movie_time_stamps = self.data_to_explore.get_ci_movie_time_stamps()
        ci_movies_dict = self.data_to_explore.get_ci_movies(only_2_photons=True)
        if len(ci_movies_dict) == 0:
            print("cicada_exploratory_main: No calcium imaging movie")
            video_data = None
        else:
            key = list(ci_movies_dict.keys())[0]
            video_data = ci_movies_dict[key]
        display_rois = False
        # ----- Adding calcium imaging movie ------
        self.ci_video_widget = CiVideoWidget(data_to_explore=self.data_to_explore,
                                             video_data=video_data,
                                             display_rois=display_rois,
                                             video_format="tiff",
                                             timestamps=ci_movie_time_stamps, current_timestamp=self.min_timestamp,
                                             parent=self,
                                             main_window=exploratory_main_window,
                                             to_connect_to_main_window=True)
        self.processed_data = ProcessedData(data_wrapper=self.data_to_explore,
                                            ci_movie_dimensions=self.ci_video_widget.dimensions)
        self.ci_video_widget.set_processed_data(processed_data=self.processed_data)
        rois_ids = self.processed_data.get_rois_ids()
        self.ci_movie_config_widget = CiVideoConfigWidget(ci_video_widget=self.ci_video_widget,
                                                          parent=self,
                                                          existing_rois_ids=rois_ids,
                                                          display_rois=display_rois,
                                                          data_to_explore=self.data_to_explore,
                                                          current_timestamp=self.min_timestamp,
                                                          main_window=exploratory_main_window,
                                                          to_connect_to_main_window=True)
        # TODO: Load behavior widgets only if videos available
        behavior_movies_dict = self.data_to_explore.get_behavior_movies()
        if len(behavior_movies_dict) == 0:
            raise Exception("No behavior movies found")
        print(f"behavior_movies_dict {behavior_movies_dict}")
        self.behaviour_video_layout.addWidget(self.ci_movie_config_widget)
        self.behaviour_video_layout.addWidget(self.ci_video_widget)
        self.behaviour_video_layout.addStretch(1)
        behaviors_movie_time_stamps_dict = self.data_to_explore.get_behaviors_movie_time_stamps()
        # print(f"behaviors_movie_time_stamps_dict {list(behaviors_movie_time_stamps_dict.keys())}")
        self.behavior_video_widgets = []
        for key_behavior, video_file_name in behavior_movies_dict.items():
            # key_behavior looks like: "behavior_cam_23109588"
            # and the key for time_stamps is "cam_23109588"
            key_behavior = key_behavior[len("behavior_"):]
            timestamps = behaviors_movie_time_stamps_dict.get(key_behavior)
            manual_behavior_movie_selection = False
            if not os.path.isfile(video_file_name):
                manual_behavior_movie_selection = True
            else:
                behavior_qb = QMessageBox()
                behavior_qb.setWindowTitle("CICADA")
                behavior_qb.setText(f"Do you want to select {key_behavior} behavior movie to use ?")
                behavior_qb.setStandardButtons(QMessageBox.Yes)
                behavior_qb.addButton(QMessageBox.No)
                behavior_qb.setDefaultButton(QMessageBox.No)
                if behavior_qb.exec() == QMessageBox.Yes:
                    manual_behavior_movie_selection = True
            # checking if the file exists, otherwise opening a filedialog
            if manual_behavior_movie_selection:
                file_dialog = QFileDialog(exploratory_main_window, f"Select behavior movie {key_behavior}")

                # setting options
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                options |= QFileDialog.DontUseCustomDirectoryIcons
                file_dialog.setOptions(options)

                # ARE WE TALKING ABOUT FILES OR FOLDERS
                file_dialog.setFileMode(QFileDialog.ExistingFiles)
                # file_dialog.setNameFilter("Avi files (*.avi)")
                file_dialog.setNameFilters(["Avi files (*.avi)", "Mp4 files (*.mp4)"])

                # OPENING OR SAVING
                file_dialog.setAcceptMode(QFileDialog.AcceptOpen)

                # SET THE STARTING DIRECTORY
                # default_value = self.analysis_arg.get_default_value()
                # if default_value is not None and isinstance(default_value, str):
                #     self.file_dialog.setDirectory(default_value)

                # print(f"if file_dialog.exec_() == QDialog.Accepted")
                # print(f"file_dialog.exec_() {file_dialog.exec_()}")
                if file_dialog.exec() == QDialog.Accepted:
                    video_file_name = file_dialog.selectedFiles()[0]
                else:
                    raise Exception(f"No {key_behavior} behavior movie provided")
            behavior_video_widget = BehaviorVideoWidget(data_to_explore=self.data_to_explore,
                                                        video_file_name=video_file_name,
                                                        timestamps=timestamps, current_timestamp=self.min_timestamp,
                                                        parent=self,
                                                        main_window=exploratory_main_window,
                                                        to_connect_to_main_window=True, surprise_bis=True)
            self.behavior_video_widgets.append(behavior_video_widget)
            self.behaviour_video_layout.addWidget(behavior_video_widget)

        self.behaviour_video_layout.addStretch(1)


        self.h_layout_widgets.addStretch(1)
        self.h_layout_widgets.addLayout(self.behaviour_video_layout)
        self.main_layout.addLayout(self.h_layout_widgets)

        # ----------------------------------
        #       Signal widgets
        # ----------------------------------
        # signals_to_display = ["emg", "lfp"]
        signals_to_display = self.data_to_explore.get_signal_keys()
        print(f"signals_to_display {signals_to_display}")
        self.signal_widgets = []
        for signal_key in signals_to_display:
            signal_data, signal_timestamps = self.data_to_explore.get_signal_by_keyword(keyword=signal_key,
                                                                                        exact_keyword=False)
            if signal_data is not None:
                # TODO: See to downsample the signal
                singal_widget = SignalWidget(data_to_explore=self.data_to_explore,
                                             description=signal_key,
                                             signal_data=signal_data,
                                             timestamps=signal_timestamps, current_timestamp=self.min_timestamp,
                                             min_timestamp=self.min_timestamp,
                                             max_timestamp=self.max_timestamp,
                                             parent=self,
                                             go_to_timestamp_fct=self.go_to_timestamp,
                                             main_window=exploratory_main_window,
                                             to_connect_to_main_window=True)
                self.main_layout.addWidget(singal_widget)
                self.signal_widgets.append(singal_widget)
        # link signals on y
        # to remove later
        # if len(self.signal_widgets) > 1:
        #     for signal_index in np.arange(1, len(self.signal_widgets)):
        #         self.signal_widgets[0].link_to_signal_y_view(self.signal_widgets[signal_index])
        #         self.signal_widgets[0].link_to_view(self.signal_widgets[signal_index])

        if len(self.signal_widgets) > 4:
            secondary_window = ExploratorySecondaryWindow(exploratory_main_window, data_to_explore=self.data_to_explore)
            secondary_window_central_widget = QWidget(parent=secondary_window)
            secondary_window.setCentralWidget(secondary_window_central_widget)
            secondary_window_main_layout = QVBoxLayout()
        else:
            secondary_window = None
            secondary_window_central_widget = None
            secondary_window_main_layout = None

            # ----------------------------------
        #       Time Intervals widgets
        # ----------------------------------
        time_intervals_layout = QHBoxLayout()
        self.time_intervals_manager = TimeIntervalsManager(data_to_explore=self.data_to_explore,
                                                           min_timestamp=self.min_timestamp,
                                                           max_timestamp=self.max_timestamp,
                                                           current_timestamp=self.current_timestamp,
                                                           main_window=exploratory_main_window, parent=self,
                                                           go_to_timestamp_fct=self.go_to_timestamp)
        self.time_intervals_manager.link_x_view(widgets_to_link=self.signal_widgets)
        time_intervals_layout.addWidget(self.time_intervals_manager.get_main_widget())
        time_intervals_layout.addWidget(self.time_intervals_manager.get_config_widget())

        # self.h_layout_widgets.addStretch(1)
        # self.h_layout_widgets.addWidget(time_invertvals_widget)
        # self.h_layout_widgets.addLayout(self.behaviour_video_layout)

        # time_intervals_dict = self.get_time_intervals_dict()
        # # contains the buttons
        # # to open a widget on its own, set parent to None, then call show() method and don't add the widget to a layout
        # # and set to_connect_to_main_window to True
        # self.time_invertvals_tags_widget = TimeIntervalsConfigWidget(time_intervals_config_widget=time_invertvals_widget,
        #                                                            n_frames=self.n_frames,
        #                                                            time_intervals_dict=time_intervals_dict,
        #                                                            data_to_explore=self.data_to_explore,
        #                                                            main_window=exploratory_main_window)
        # time_intervals_layout.addWidget(self.time_invertvals_tags_widget)
        # self.time_invertvals_tags_widget.show()
        if secondary_window_main_layout is not None:
            secondary_window_main_layout.addLayout(time_intervals_layout)
        else:
            self.main_layout.addLayout(time_intervals_layout)


        self.frame_slider_layout = QHBoxLayout()
        self.timestamp_label = QLabel("100000.00")
        fm = QtGui.QFontMetrics(self.timestamp_label.font())
        # other options: https://stackoverflow.com/questions/8633433/qt-get-the-pixel-length-of-a-string-in-a-qlabel
        self.timestamp_label.setFixedWidth(fm.width(self.timestamp_label.text()))
        self.timestamp_label.setText(str(np.round(self.current_timestamp, 2)))
        self.timestamp_label.setToolTip("Current timestamp (sec)")
        self.frame_slider = QSlider(QtCore.Qt.Horizontal)
        # self.frame_slider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.frame_slider.setTickInterval(5)
        self.frame_slider.setTracking(False)
        self.frame_slider.setMaximum(self.max_timestamp)
        self.frame_slider.setMinimum(self.min_timestamp)
        self.frame_slider.setEnabled(False)
        # self.frame_slider.valueChanged.connect(self.frame_slider_action)
        self.frame_slider_layout.addWidget(self.frame_slider)
        self.frame_slider_layout.addWidget(self.timestamp_label)

        self.timestamps_step_spin_box = QDoubleSpinBox()
        self.timestamps_step_spin_box.setRange(self.min_timestamp_step, self.max_timestamp_step)
        self.timestamps_step_spin_box.setSingleStep(self.timestamp_step_increment)
        self.timestamps_step_spin_box.setValue(self.timestamp_step)
        # to just disable the text box but not the arrows
        self.timestamps_step_spin_box.lineEdit().setReadOnly(True)
        self.timestamps_step_spin_box.setToolTip("Steps in sec")
        self.timestamps_step_spin_box.valueChanged.connect(self.timestamps_step_value_changed)
        self.frame_slider_layout.addWidget(self.timestamps_step_spin_box)


        # TODO: See to create all the widgets at one place
        #  and then organize all the layouts and add the widgets to the layouts

        if secondary_window_main_layout is not None:
            secondary_window_main_layout.addLayout(self.frame_slider_layout)
            secondary_window_central_widget.setLayout(secondary_window_main_layout)
            secondary_window.show()
        else:
            self.main_layout.addLayout(self.frame_slider_layout)

        self.setLayout(self.main_layout)

    def timestamps_step_value_changed(self, value):
        """
        Called when self.timestamps_step_spin_box value is changed
        Returns:

        """
        self.timestamp_step = value

    def change_timestamp_step(self, increment):
        """
        increment or decrement timestamp_step, change the speed
        Args:
            increment: bool

        Returns:

        """

        if increment:
            if self.timestamp_step + self.timestamp_step_increment > self.max_timestamp_step:
                return
            self.timestamp_step += self.timestamp_step_increment
            self.timestamps_step_spin_box.setValue(self.timestamp_step)
        else:
            if self.timestamp_step - self.timestamp_step_increment < self.min_timestamp_step:
                return
            self.timestamp_step -= self.timestamp_step_increment
            self.timestamps_step_spin_box.setValue(self.timestamp_step)

    def start(self):
        self.playing = True
        self.updateTimer.start(25)

    def pause(self):
        self.playing = False
        self.updateTimer.stop()

    def frame_slider_action(self):
        self.go_to_timestamp(timestamp=self.frame_slider.value())

    def go_to_timestamp(self, timestamp, from_line_moved=False):
        for behavior_video_widget in self.behavior_video_widgets:
            behavior_video_widget.set_current_timestamp(timestamp=timestamp)
        for signal_widget in self.signal_widgets:
            signal_widget.set_current_timestamp(timestamp=timestamp)
        # self.behavior_video_widget_2.set_current_timestamp(timestamp=timestamp)
        self.ci_video_widget.set_current_timestamp(timestamp=timestamp)
        self.time_intervals_manager.set_current_timestamp(timestamp=timestamp, from_line_moved=from_line_moved)
        self.update_timestamp(timestamp=timestamp)

    def set_current_timestep_to_actual_range(self):
        if self.time_intervals_manager is not None:
            # return the range the plot
            range_values = self.time_intervals_manager.get_displayed_range()
            start_time, stop_time = range_values[0][0], range_values[0][1]
            self.go_to_timestamp((start_time + stop_time) / 2)

    def next_timestamp(self):
        time_stamp = self.current_timestamp + self.timestamp_step
        if time_stamp > self.max_timestamp:
            time_stamp = self.min_timestamp
        self.go_to_timestamp(timestamp=time_stamp)

    def previous_timestamp(self):
        time_stamp = self.current_timestamp - self.timestamp_step
        if time_stamp < self.min_timestamp:
            time_stamp = self.max_timestamp
        self.go_to_timestamp(timestamp=time_stamp)

    def update_timestamp(self, timestamp):
        self.current_timestamp = timestamp
        self.frame_slider.setValue(self.current_timestamp)
        self.timestamp_label.setText(str(np.round(self.current_timestamp, 2)))
