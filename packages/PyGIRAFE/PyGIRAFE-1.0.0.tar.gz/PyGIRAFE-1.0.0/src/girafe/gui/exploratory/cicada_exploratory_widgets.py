"""
Contains the widgets that compose the exploratory gui.
Each widget is an instance of ***
"""
from qtpy.QtWidgets import *
import pyqtgraph as pg
from .cicada_roi import PolyLineROI
from pyqtgraph import LinearRegionItem
from qtpy.QtCore import Qt
from qtpy import QtCore
import pyqtgraph.ptime as ptime
import os
from cicada.utils.display.videos import OpenCvVideoReader, TiffVideoReader, ArrayVideoReader
from abc import ABC, abstractmethod
from PyQt5 import QtCore as Core
from qtpy import QtGui
import numpy as np
from cicada.utils.misc import get_continous_time_periods, find_nearest
from cicada.gui.exploratory.cicada_finite_regions import FiniteLinearRegionItem, FiniteLine
import cv2
from cicada.utils.display.colors import BREWER_COLORS


class ExploratoryWidgetModel(ABC):

    def __init__(self, data_to_explore, main_window=None, to_connect_to_main_window=True):
        # data_to_explore should be an instance of GirafeAnalysisFormatWrapper
        self.data_to_explore = data_to_explore
        self.main_window = main_window
        self.to_connect_to_main_window = to_connect_to_main_window

        # TODO: See to add a method that convert a frame to ms timestamps and one that for a given timestamps
        #  returning the corresponding frame.

    def keyPressEvent(self, event):
        """
        Call when a key is pressed
        Args:
            event:

        Returns:

        """
        # Sending the event to the main window if the widget is in the main window
        if self.main_window and self.to_connect_to_main_window:
            self.main_window.keyPressEvent(event=event)

    # @abstractmethod
    # def get_corresponding_frame_index(self, timestamp):
    #     """
    #     Return the frame index corresponding to this timestamp.
    #     If value is negative or > to the number of frames, it means no frame matches
    #     Args:
    #         timestamp:
    #
    #     Returns:
    #
    #     """
    #     pass

    @abstractmethod
    def set_current_timestamp(self, timestamp):
        """
        Change the timestamp to display
        Args:
            timestamp:

        Returns:

        """
        pass


# to resolve: TypeError: metaclass conflict: the metaclass of a derived class
# must be a (non-strict) subclass of the metaclasses of all its bases
# might not be a good idea to do multiple-heritage with a Qclass
# solution from: https://stackoverflow.com/questions/28720217/multiple-inheritance-metaclass-conflict
# http://www.phyast.pitt.edu/~micheles/python/metatype.html
class FinalMeta(type(ExploratoryWidgetModel), type(QWidget)):
    pass


class GraphicsLayoutMeta(type(ExploratoryWidgetModel), type(pg.GraphicsLayoutWidget)):
    pass


class PgMeta(type(ExploratoryWidgetModel), type(pg.PlotWidget)):
    pass


class CiVideoConfigWidget(ExploratoryWidgetModel, QWidget, metaclass=FinalMeta):
    """
    Configuration panel for CI movie
    """

    def __init__(self, data_to_explore, display_rois, existing_rois_ids, current_timestamp,
                 ci_video_widget, parent, main_window, to_connect_to_main_window):
        ExploratoryWidgetModel.__init__(self, data_to_explore=data_to_explore, main_window=main_window,
                                        to_connect_to_main_window=to_connect_to_main_window)
        QWidget.__init__(self, parent=parent)
        self.ci_video_widget = ci_video_widget
        self.parent = parent
        self.current_timestamp = current_timestamp
        self.display_rois = display_rois

        # allows the widget to be expanded in vertical but not in the horizonal axis
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        # --------------- GUI -------------------
        self.setWindowTitle("Time intervals tags")

        self.main_layout = QVBoxLayout()
        self.scrollArea = QScrollArea()
        # ScrollBarAlwaysOff = 1
        # ScrollBarAlwaysOn = 2
        # ScrollBarAsNeeded = 0
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.main_layout.addWidget(self.scrollArea)

        self.scroll_area_widget_contents = QWidget()
        self.scrollArea.setWidget(self.scroll_area_widget_contents)
        self.layout = QVBoxLayout(self.scroll_area_widget_contents)
        # we add stretch now and we will insert new widget before the stretch
        self.layout.addStretch(1)
        # ==============================
        self.setLayout(self.main_layout)

        self.title_label = QLabel("Calcium Imaging config panel")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.title_label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.layout.insertWidget(self.layout.count() - 1, self.title_label)

        self.display_rois_layout = QHBoxLayout()
        self.display_rois_layout.addStretch(1)
        self.display_rois_check_box = QCheckBox()
        self.display_rois_check_box.stateChanged.connect(self.change_display_rois_status)
        self.display_rois_check_box.setChecked(self.display_rois)
        self.display_rois_check_box.setText("Display contours")
        self.display_rois_layout.addWidget(self.display_rois_check_box)
        self.display_rois_layout.addStretch(1)
        self.layout.insertLayout(self.layout.count() - 1, self.display_rois_layout)

        self.rois_cb_layout = RoisComboBoxesLayout(all_choices=existing_rois_ids, ci_video_widget=self.ci_video_widget)
        self.layout.insertLayout(self.layout.count() - 1, self.rois_cb_layout)

    def change_display_rois_status(self):
        """
        Returns:

        """
        self.ci_video_widget.change_rois_display_status()
        self.display_rois = not self.display_rois

    def get_corresponding_frame_index(self, timestamp):
        """
        Return the frame index corresponding to this timestamp.
        If value is negative or > to the number of frames, it means no frame matches
        Args:
            timestamp:

        Returns:

        """
        pass

    def set_current_timestamp(self, timestamp):
        """
        Change the timestamp to display
        Args:
            timestamp:

        Returns:

        """
        self.current_timestamp = timestamp


class MyRoisQComboBox(QComboBox):
    """
    Special instance of ComboBox allowing to handle change so that it is connected to other combo_boxes
    """

    def __init__(self, fct_to_call_at_change, with_empty_choice, choices=None):
        """
        init
        """
        QComboBox.__init__(self)
        self.next_combo_box = None
        # function that should be called when a change has been done
        self.fct_to_call_at_change = fct_to_call_at_change
        # List of choices
        # the next combo_box will be filled with the choices left if one is chosen, otherwise will be empty
        if choices is not None:
            if with_empty_choice:
                self.addItem("", "")
            self.choices = choices
            for choice_id in self.choices:
                self.addItem(str(choice_id), str(choice_id))
        else:
            # it should never get there
            self.choices = [""]
        self.currentIndexChanged.connect(self.selection_change)

    def get_content(self, including_following_ones=True):
        """
        Return the content as a list of str, only one element if including_following_ones is set to False,
        or a str for combo_box (empty str not being counted for)
        Args:
            including_following_ones:

        Returns:

        """
        current_text = self.currentText()
        if current_text == "":
            return []
        if (not including_following_ones) or (self.next_combo_box is None):
            return [current_text]

        content_list = [current_text]
        content_list.extend(self.next_combo_box.get_content())
        return content_list

    def selection_change(self, index):
        """
        Called if the selection is changed either by the user or by the code
        Args:
            index:

        Returns:

        """

        # it should not be empty
        if self.count() == 0:
            return

        if self.next_combo_box is None:
            if self.fct_to_call_at_change is not None:
                self.fct_to_call_at_change()
            return

        current_text = self.currentText()

        if current_text == "":
            # then we empty the following combo_box
            self.empty_it()
            if self.fct_to_call_at_change is not None:
                self.fct_to_call_at_change()
            return
        if current_text not in self.choices:
            # should not happen
            return

        # copying the list
        content_next_combo_box = list(self.choices)
        content_next_combo_box.remove(current_text)

        # removing previous items
        self.next_combo_box.clear()

        # adding new ones
        # first adding an empty one
        self.next_combo_box.addItem("", "")
        for choice_id in content_next_combo_box:
            # need to put 2 arguments, in order to be able to find it using findData
            self.next_combo_box.addItem(str(choice_id), str(choice_id))
        # to make combo_box following the next ones will be updated according to the content at the index 0
        self.next_combo_box.setCurrentIndex(0)

        if self.fct_to_call_at_change is not None:
            self.fct_to_call_at_change()

    def empty_it(self):
        self.clear()
        # TODO: do action so the main widget know that something changed
        if self.next_combo_box is not None:
            self.next_combo_box.empty_it()


class RoiColorButton(QPushButton):
    def __init__(self, color, button_index, fct_to_call_at_change):
        """

        Args:
            color: QColor instance
        """
        QPushButton.__init__(self, "  ")

        self.setToolTip("Select color")
        self.color = color
        self.fct_to_call_at_change = fct_to_call_at_change
        self.clicked.connect(self.open_dialog)
        self.button_index = button_index
        self.update_button_color()

    def open_dialog(self):
        """
                Open the color dialog
                Returns:

                """
        initial = Qt.white
        if self.color is not None:
            initial = self.color
        options = QColorDialog.ColorDialogOption()
        # if self.show_alpha_channel:
        #     options |= QColorDialog.ShowAlphaChannel
        color = QColorDialog.getColor(initial=initial, options=options)

        if color.isValid():
            self.color = color
            self.update_button_color()

    def update_button_color(self):
        """

        Returns:

        """
        if self.color is not None:
            rgb_values = [1 - color_code for color_code in self.color.getRgbF()]
            # the foreground color will be the invert of the selected color, which will be the background of the button
            fg_color = QtGui.QColor()
            fg_color.setRgbF(*rgb_values[:3])
            self.setStyleSheet(f"background-color:{self.color.name()}; color:{fg_color.name()};")
            self.fct_to_call_at_change(color_button=self, button_index=self.button_index)

    def get_color(self):
        """

        Returns: color as a QColor instance

        """
        return self.color


class RoisComboBoxesLayout(QHBoxLayout):
    """
    Layout displaying as many ComboBoxes as all_choices, each combobox being connected to the next one,
    the first has all all_choices, the following none if the first has no choice selected otherwise all all_choices except
    the one selected by the previous comboboxes.
    each combobox is associated to a button allowing the choose the color of the associated ROIs
    """

    def __init__(self, all_choices, ci_video_widget):
        QHBoxLayout.__init__(self)

        self.combo_boxes = []
        self.color_buttons = []
        self.ci_video_widget = ci_video_widget
        self.all_choices = all_choices

        # creating as many ComboBox as choices
        n_choices = len(all_choices)
        combo_box_layout = QVBoxLayout()
        self.addLayout(combo_box_layout)
        color_buttons_layout = QVBoxLayout()
        self.addLayout(color_buttons_layout)
        for choice_index in range(n_choices):
            combo_box = MyRoisQComboBox(choices=all_choices[choice_index:],
                                        with_empty_choice=(choice_index > 0),
                                        fct_to_call_at_change=self.change_in_combo_boxes)
            combo_box_layout.addWidget(combo_box)
            self.combo_boxes.append(combo_box)
            # linking the combo_boxes
            if choice_index > 0:
                self.combo_boxes[-2].next_combo_box = self.combo_boxes[-1]

            color = QtGui.QColor(BREWER_COLORS[choice_index % len(BREWER_COLORS)])
            color_button = RoiColorButton(color=color, button_index=choice_index,
                                          fct_to_call_at_change=self.color_button_updated)
            color_buttons_layout.addWidget(color_button)
            self.color_buttons.append(color_button)

        if len(self.combo_boxes) > 0:
            new_rois = self.combo_boxes[0].get_content()
            colors = []
            for index_roi in range(len(new_rois)):
                colors.append(self.color_buttons[index_roi].get_color())
            self.ci_video_widget.update_current_rois(new_rois=new_rois, colors=colors)

    def color_button_updated(self, color_button, button_index):
        """

        Returns:

        """
        rois_id = self.combo_boxes[button_index].get_content()
        if (rois_id is None) or (rois_id == "") or len(rois_id) == 0:
            return
        rois_id = rois_id[0]
        color = color_button.get_color()
        self.ci_video_widget.update_rois_color(color=color, rois_id=rois_id)

    def change_in_combo_boxes(self):
        """
        Called when a combo box has been changed
        Returns:

        """
        new_rois = self.combo_boxes[0].get_content()
        colors = []
        for index_roi in range(len(new_rois)):
            colors.append(self.color_buttons[index_roi].get_color())

        self.ci_video_widget.update_current_rois(new_rois=new_rois, colors=colors)

class CiVideoWidget(ExploratoryWidgetModel, pg.GraphicsLayoutWidget, metaclass=GraphicsLayoutMeta):
    """
    Used to display Calcium Imaging movie
    """

    def __init__(self, data_to_explore, video_data, timestamps, display_rois, current_timestamp,
                 main_window, to_connect_to_main_window, parent=None,
                 blank_frame_time_delay=0.3,
                 video_format=None):
        """

        Args:
            data_to_explore:
            video_data: can be a string as a video filename or an array representing the file
            timestamps:
            current_timestamp:
            main_window:
            to_connect_to_main_window:
            video_format:
        """
        ExploratoryWidgetModel.__init__(self, data_to_explore=data_to_explore, main_window=main_window,
                                        to_connect_to_main_window=to_connect_to_main_window)
        pg.GraphicsLayoutWidget.__init__(self)

        self.data_to_explore = data_to_explore
        self.surprise_mfh = False
        # instance of ProcessedData
        self.processed_data = None
        self.display_rois = display_rois

        # if this delay between the timestamps and the closest frame is superior to this one
        # then a blank frame will be displayed
        self.blank_frame_time_delay = blank_frame_time_delay

        self.video_reader = None
        if isinstance(video_data, str) and video_format.lower() in ["tiff", "tif"]:
            self.video_reader = TiffVideoReader(video_file_name=video_data)
        elif video_data is not None:
            self.video_reader = ArrayVideoReader(video_data=video_data)

        if self.video_reader is not None:
            self.dimensions = (self.video_reader.height, self.video_reader.width)
            self.n_frames = self.video_reader.length
        else:
            # blank movie
            self.dimensions = (200, 200)
            self.n_frames = 0

        self.timestamps = timestamps
        self.current_timestamp = current_timestamp
        self.current_frame = self.get_corresponding_frame_index(timestamp=self.current_timestamp)

        self.view_box = self.addViewBox(lockAspect=True, row=0, col=0, invertY=True)
        self.view_box.setMenuEnabled(False)
        ## lock the aspect ratio so pixels are always square
        # view.setAspectLocked(True)
        # Do not allow the widget to be expanded
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        ## Create image item
        # border='w' set the color of the border
        # axisOrder indicate the orientation of the image
        # axisOrder='row-major'
        self.image_displayed = pg.ImageItem(axisOrder='row-major', border='w')
        self.view_box.addItem(self.image_displayed)

        ## Set initial view bounds
        # view.setRange(QtCore.QRectF(0, 0, 100, 100))

        data = self._get_frame_data(frame_number=self.current_frame)
        ## Display the data
        self.image_displayed.setImage(data)

        # each value is a list of rois
        self.rois_dict = dict()
        self.current_rois = []

        # def update(roi):
        #     img1b.setImage(roi.getArrayRegion(arr, img1a), levels=(0, arr.max()))
        #     v1b.autoRange()
        #
        # for roi in rois:
        #     roi.sigRegionChanged.connect(update)
        #     v1a.addItem(roi)

        # TODO: See the ImageItem draw tutorial
        """
        ## start drawing with 3x3 brush
        kern = np.array([
            [0.0, 0.5, 0.0],
            [0.5, 1.0, 0.5],
            [0.0, 0.5, 0.0]
        ])
        img.setDrawKernel(kern, mask=kern, center=(1,1), mode='add')
        img.setLevels([0, 10])
        """

    def update_rois_color(self, rois_id, color):
        """
        Update the color of a group of rois
        Args:
            rois_id:
            color: QColor

        Returns:

        """
        rois = self.rois_dict[rois_id]
        for roi in rois:
            roi.setPen(color=color)

    def update_current_rois(self, new_rois, colors):
        """
        List of string, representing the rois id
        Args:
            new_rois:
            colors: list of QColor

        Returns:

        """
        rois_to_remove = list(self.current_rois)
        rois_to_add = []
        for roi_index, rois_id in enumerate(new_rois):
            # we just update the colors
            rois = self.rois_dict[rois_id]
            for roi in rois:
                roi.setPen(color=colors[roi_index])
            if rois_id in self.current_rois:
                # then we keep it there
                # so remove from the list of rois to remove
                rois_to_remove.remove(rois_id)
            else:
                rois_to_add.append(rois_id)
        if self.display_rois:
            self._remove_rois_to_view_box(rois_to_remove)
            self._add_rois_to_view_bow(rois_to_add)
        self.current_rois = new_rois

    def set_processed_data(self, processed_data):
        self.processed_data = processed_data
        cells_coord_dict = self.processed_data.cells_coord_dict
        for coords_key, cells_coord in cells_coord_dict.items():
            coord_contours = cells_coord.coords
            self.rois_dict[coords_key] = []
            for coord_contour_index, coord_contour in enumerate(coord_contours):
                # if coord_contour_index > 10:
                #     break

                roi = PolyLineROI(coord_contour.transpose(), pen=(6, 9), closed=True, movable=False,
                                  invisible_handle=True, alterable=False, no_seq_hover_action=True,
                                  roi_id=coord_contour_index, config_widget=self)

                self.rois_dict[coords_key].append(roi)

            if self.current_rois is None:
                self.current_rois = [coords_key]

        # if self.display_rois:
        #     self._add_rois_to_view_bow(roi_id=self.current_rois[])

    def change_rois_display_status(self):
        if self.display_rois:
            for current_roi in self.current_rois:
                for roi in self.rois_dict[current_roi]:
                    self.view_box.removeItem(roi)
        else:
            self._add_rois_to_view_bow(roi_ids=self.current_rois)
        self.display_rois = not self.display_rois

    def _add_rois_to_view_bow(self, roi_ids):
        for roi_id in roi_ids:
            for roi in self.rois_dict[roi_id]:
                # roi.sigRegionChanged.connect(update)
                self.view_box.addItem(roi)

    def _remove_rois_to_view_box(self, roi_ids):
        for roi_id in roi_ids:
            for roi in self.rois_dict[roi_id]:
                self.view_box.removeItem(roi)

    def get_corresponding_frame_index(self, timestamp):
        frame_index = find_nearest(array=self.timestamps, value=timestamp, is_sorted=True)
        if frame_index >= self.n_frames:
            return -1
        delay = abs(self.timestamps[frame_index] - timestamp)
        if delay >= self.blank_frame_time_delay:
            # -1 means a blank frame will be displayed
            return -1
        return frame_index

    def set_current_timestamp(self, timestamp):
        self.current_timestamp = timestamp
        self.display_frame(frame_number=self.get_corresponding_frame_index(timestamp))

    def switch_surprise_mfh(self):
        """
        Activate or deactivate the surprise
        Returns:

        """
        self.surprise_mfh = not self.surprise_mfh

    def _get_frame_data(self, frame_number):
        """
        Get the data to display as a 3d array, if the frame is negative or > n_frames, then we return
        a blank image
        Args:
            frame_number:

        Returns:

        """

        if (self.video_reader is None) or (frame_number < 0) or (frame_number >= self.n_frames):
            if self.surprise_mfh:
                my_path = os.path.abspath(os.path.dirname(__file__))
                data = cv2.imread(os.path.join(my_path, '../icons/rc/surprise_mfh.jpg'), cv2.IMREAD_GRAYSCALE)  #
                # data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
                data = data[:self.dimensions[0], :self.dimensions[1]]
            else:
                data = np.zeros((self.dimensions[0], self.dimensions[1], 3))
        else:
            data = self.video_reader.get_frame(frame_index=frame_number)

        # # adding contours
        # if not self.surprise_mfh and (self.processed_data is not None):
        #     cells_coord = self.processed_data.cells_coord
        #     cells_coord.add_contours_to_image(image_data=data)
        #     # cv2.drawContours(data, contours, -1, (255, 0, 0), 1)
        #     pass

        return data

    def display_frame(self, frame_number):
        """
        Display the frame frame_number if possible and return the frame displayed then
        Args:
            frame_number:

        Returns: integer representing the frame displayed then or None if the method is not implemented

        """
        if frame_number >= self.n_frames:
            return self.current_frame

        self.current_frame = frame_number
        data = self._get_frame_data(frame_number=self.current_frame)
        ## Display the data
        self.image_displayed.setImage(data)

        return self.current_frame


class BehaviorVideoWidget(ExploratoryWidgetModel, pg.GraphicsLayoutWidget, metaclass=GraphicsLayoutMeta):
    """
    Used to display movie of the behavior of a subject
    """

    def __init__(self, data_to_explore, video_file_name, timestamps, current_timestamp=0, parent=None, main_window=None,
                 to_connect_to_main_window=True, surprise_bis=False):
        """

        Args:
            data_to_explore: Wrapper data format
            video_file_name:
            timestamps: np.array of float, give the timestamp of each frame of the movie
            current_timestamp: timestamp to display (the closest will be displayed)
            parent:
            main_window:
            to_connect_to_main_window:
        """
        ExploratoryWidgetModel.__init__(self, data_to_explore=data_to_explore, main_window=main_window,
                                        to_connect_to_main_window=to_connect_to_main_window)
        pg.GraphicsLayoutWidget.__init__(self)

        self.timestamps = timestamps
        self.current_timestamp = current_timestamp
        self.current_frame = self.get_corresponding_frame_index(timestamp=self.current_timestamp)
        self.surprise_mfh = False
        self.surprise_bis = surprise_bis
        # self.resize(400, 300)
        # self.main_layout = QVBoxLayout()
        ## Create window with GraphicsView widget
        # win = pg.GraphicsLayoutWidget()
        # win.show()  ## show widget alone in its own window
        # win.setWindowTitle('pyqtgraph example: ImageItem')
        view = self.addViewBox(lockAspect=True, row=0, col=0, invertY=True)
        view.setMenuEnabled(False)
        ## lock the aspect ratio so pixels are always square
        # view.setAspectLocked(True)
        # Do not allow the widget to be expanded
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        ## Create image item
        # border='w' set the color of the border
        # axisOrder indicate the orientation of the image
        # axisOrder='row-major'
        self.image_displayed = pg.ImageItem(axisOrder='row-major', border='w')
        view.addItem(self.image_displayed)

        ## Set initial view bounds
        # view.setRange(QtCore.QRectF(0, 0, 100, 100))

        self.basename_video_file_name = os.path.basename(video_file_name)
        self.video_reader = OpenCvVideoReader(video_file_name=video_file_name)
        self.dimensions = (self.video_reader.height, self.video_reader.width)
        self.n_frames = self.video_reader.length
        if len(timestamps) != self.n_frames:
            print(f"n timestamps {len(timestamps)} in abf != n frames "
                  f"{self.n_frames} in movie {self.basename_video_file_name}")
        data = self._get_frame_data(frame_number=self.current_frame)

        ## Display the data
        self.image_displayed.setImage(data)
        # self.main_layout.addWidget(win)
        # self.setLayout(self.main_layout)

    def switch_surprise_mfh(self):
        """
        Activate or deactivate the surprise
        Returns:

        """
        self.surprise_mfh = not self.surprise_mfh

    def get_corresponding_frame_index(self, timestamp):
        return find_nearest(array=self.timestamps, value=timestamp, is_sorted=True)

    def set_current_timestamp(self, timestamp):
        self.current_timestamp = timestamp
        self.display_frame(frame_number=self.get_corresponding_frame_index(timestamp))

    def _get_frame_data(self, frame_number):
        """
        Get the data to display as a 3d array, if the frame is negative or > n_frames, then we return
        a blank image
        Args:
            frame_number:

        Returns:

        """
        if frame_number < 0 or frame_number >= self.n_frames:
            if self.surprise_mfh:
                my_path = os.path.abspath(os.path.dirname(__file__))
                if self.surprise_bis:
                    data = cv2.imread(os.path.join(my_path, '../icons/rc/badass_bis.jpg'))
                    data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
                else:
                    data = cv2.imread(os.path.join(my_path, '../icons/rc/badass.jpg'))  # , cv2.IMREAD_GRAYSCALE
                    data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
                # data = data[:self.dimensions[0], :self.dimensions[1]]
            else:
                data = np.zeros((self.dimensions[0], self.dimensions[1], 3))
        else:
            data = self.video_reader.get_frame(frame_index=frame_number)

        return data

    def display_frame(self, frame_number):
        if frame_number >= self.n_frames:
            return self.current_frame

        self.current_frame = frame_number
        data = self._get_frame_data(frame_number=self.current_frame)
        ## Display the data
        self.image_displayed.setImage(data)

        return self.current_frame


class MyViewBox(pg.ViewBox):
    """
    Mixed between RectMode and PanMode.
    Left click drag act like in RectMode
    Right click drag act life left click will act in PanMode (move the view box)
    Allow to zoom.
    Code from pyqtgraph examples
    """

    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        # self.setMouseMode(self.RectMode) ViewBox.PanMode

    def mouseClickEvent(self, ev):
        pass
        ## reimplement right-click to zoom out
        # if ev.button() == QtCore.Qt.RightButton:
        #     self.autoRange()

    def mouseDragEvent(self, ev):
        """
        Right click is used to zoom, left click is use to move the area
        Args:
            ev:

        Returns:

        """
        if ev.button() == QtCore.Qt.RightButton:
            self.setMouseMode(self.PanMode)
            # cheating, by telling it the left button is used instead
            ev._buttons = [QtCore.Qt.LeftButton]
            ev._button = QtCore.Qt.LeftButton
            pg.ViewBox.mouseDragEvent(self, ev)
        elif ev.button() == QtCore.Qt.LeftButton:
            self.setMouseMode(self.RectMode)
            pg.ViewBox.mouseDragEvent(self, ev)
        else:
            # ev.ignore()
            pg.ViewBox.mouseDragEvent(self, ev)


class SignalWidget(ExploratoryWidgetModel, pg.PlotWidget, metaclass=PgMeta):
    """
    Used to display a 1d signal
    """

    def __init__(self, data_to_explore, description, signal_data, timestamps, min_timestamp, max_timestamp,
                 go_to_timestamp_fct,
                 current_timestamp=0,
                 main_window=None, to_connect_to_main_window=True, parent=None):
        """

        Args:
            data_to_explore: Wrapper data format
            description (str): would be display in a corner
            signal_data:
            timestamps:  np.array of float, give the timestamp of each frame of the movie
            min_timestamp:
            max_timestamp:
            go_to_timestamp_fct: fct that take as first argument a timestamp, should be called if the current_timestamp
            changed
            current_timestamp: timestamp to display (the closest will be displayed)
            main_window:
            to_connect_to_main_window:
            parent:
        """
        ExploratoryWidgetModel.__init__(self, data_to_explore=data_to_explore, main_window=main_window,
                                        to_connect_to_main_window=to_connect_to_main_window)
        pg.GraphicsLayoutWidget.__init__(self)

        self.view_box = MyViewBox()
        pg.PlotWidget.__init__(self, title=description, parent=parent, viewBox=self.view_box)
        self.description = description
        # allows the widget to be expanded in both axis
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # 230 is the height, the width 300 here doesn't really matter as it is expending
        self.setSceneRect(0, 0, 300, 230)
        self.main_window = main_window
        self.min_timestamp = min_timestamp
        self.max_timestamp = max_timestamp
        self.current_timestamp = current_timestamp
        self.timestamps = timestamps
        self.signal_data = signal_data
        self.go_to_timestamp_fct = go_to_timestamp_fct

        self.data_to_explore = data_to_explore

        self.pg_plot = self.getPlotItem()
        # self.invertY(True)
        # hide the left axis, as the label of each tag is displayed on the line
        # self.pg_plot.hideAxis(axis='left')
        self.pg_plot.hideAxis(axis='bottom')
        # view_box = pg_plot.getViewBox()
        y_min = np.min(self.signal_data)
        y_max = np.max(self.signal_data)
        range_signal = y_max - y_min
        # print(f"y_min {y_min}, y_max {y_max}, range_signal {range_signal}")
        self.view_box.setLimits(xMin=self.min_timestamp - 1, xMax=self.max_timestamp + 1,
                                yMin=y_min - (range_signal / 5), yMax=y_max)
        # range of the plot that can be manipulated
        self.pg_plot.setXRange(self.min_timestamp, self.max_timestamp)
        self.pg_plot.setYRange(y_min - (range_signal / 5), y_max)
        self.pg_plot.setAspectLocked(True)
        # (0,0,255) == "blue"

        color_pen = (0, 0, 255) # dark blue
        color_hover_pen = (100, 149, 237) # lighh blue
        self.current_timestamp_marker = FiniteLine(pos=[self.current_timestamp, 0],
                                                   angle=90, finite_values=None, pen=color_pen, movable=True,
                                                   bounds=[self.min_timestamp, self.max_timestamp],
                                                   hoverPen=color_hover_pen, label=None, labelOpts=None,
                                                   name=None, int_rounding=False,
                                                   new_line_pos_callback=self.line_moved,
                                                   first_line=False,
                                                   time_interval=None)
        self.pg_plot.addItem(item=self.current_timestamp_marker)

        # ploting the signal, with red pen
        self.pg_plot.plot(self.timestamps, self.signal_data, pen=(255, 0, 0))

    def set_current_timestamp(self, timestamp, from_line_moved=False):
        self.current_timestamp = timestamp
        self.current_timestamp_marker.setPos(pos=[timestamp, 0])

    def get_displayed_range(self):
        """
        Return the range of the displayed values in the plot
        Returns:

        """
        return self.pg_plot.getViewBox().viewRange()

    def line_moved(self, new_pos, first_value, time_interval):
        """
        The finite line has been moved. We change the frame displayed in consequence
        Args:
            new_pos:

        Returns:

        """
        self.go_to_timestamp_fct(timestamp=new_pos)

    def link_to_view(self, view_to_link):
        self.view_box.setXLink(view=view_to_link)

    def link_to_signal_y_view(self, signal_widget):
        """
        Link y axis with another signal
        Args:
            signal_widget:

        Returns:

        """
        self.view_box.setYLink(view=signal_widget.view_box)


class TimeIntervalsMainWidget(ExploratoryWidgetModel, pg.PlotWidget, metaclass=PgMeta):
    """
    Module that will display the different w intervals along the frames
    """

    def __init__(self, data_to_explore, ti_manager, min_timestamp, max_timestamp,
                 current_timestamp, parent=None, main_window=None,
                 to_connect_to_main_window=True):
        """

        Args:
            data_to_explore:
            ti_manager:
            min_timestamp:
            max_timestamp:
            current_timestamp:
            parent:
            main_window:
            to_connect_to_main_window:
        """
        ExploratoryWidgetModel.__init__(self, data_to_explore=data_to_explore, main_window=main_window,
                                        to_connect_to_main_window=to_connect_to_main_window)
        self.view_box = MyViewBox()
        pg.PlotWidget.__init__(self, parent=parent, viewBox=self.view_box)
        # allows the widget to be expanded in both axis
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.main_window = main_window
        self.min_timestamp = min_timestamp
        self.max_timestamp = max_timestamp
        self.current_timestamp = current_timestamp
        # instance of TimeIntervalsManager
        self.ti_manager = ti_manager

        self.data_to_explore = data_to_explore
        self.ti_plots_item_dict = dict()
        self.ti_linear_region_item_dict = dict()
        self.ti_plots_index_dict = dict()
        # allows to know which indices are free to insert new plot there
        self.available_plot_indices = []
        # start_line represent the InfiniteLine instance representing where the start button has been pressed
        self.start_line = None

        # self.
        ## Create window with GraphicsView widget
        # pg_win = pg.GraphicsLayoutWidget()
        # win.show()  ## show widget alone in its own window
        # win.setWindowTitle('pyqtgraph example: ImageItem')
        # view = self.addViewBox(lockAspect=True, row=0, col=0, invertY=False)
        # view.setMenuEnabled(False)
        # self.setAspectLocked(True)
        self.pg_plot = self.getPlotItem()
        self.invertY(True)
        # hide the left axis, as the label of each tag is displayed on the line
        self.pg_plot.hideAxis(axis='left')
        # view_box = pg_plot.getViewBox()
        self.view_box.setLimits(xMin=self.min_timestamp - 1, xMax=self.max_timestamp + 1)
        # range of the plot that can be manipulated
        self.pg_plot.setXRange(self.min_timestamp, self.max_timestamp)
        self.pg_plot.setAspectLocked(False)
        # (0,0,255) == "blue"
        color_pen = (0, 0, 255)
        color_hover_pen = (100, 149, 237)
        self.current_timestamp_marker = FiniteLine(pos=[self.current_timestamp, 0],
                                                   angle=90, finite_values=None, pen=color_pen, movable=True,
                                                   bounds=[self.min_timestamp, self.max_timestamp],
                                                   hoverPen=color_hover_pen, label=None, labelOpts=None,
                                                   name=None, int_rounding=False,
                                                   new_line_pos_callback=self.line_moved,
                                                   first_line=False,
                                                   time_interval=None)
        self.pg_plot.addItem(item=self.current_timestamp_marker)

    def set_current_timestamp(self, timestamp, from_line_moved=False):
        self.current_timestamp = timestamp
        self.current_timestamp_marker.setPos(pos=[timestamp, 0])
        # updating the
        # print(f"from_line_moved {from_line_moved} timestamp {timestamp}")
        # if not from_line_moved:
        #     padding_around_marker = 60
        #     min_range = max(self.min_timestamp, timestamp-padding_around_marker)
        #     max_range = min(self.max_timestamp, timestamp+padding_around_marker)
        #     self.pg_plot.setXRange(min=min_range, max=max_range, padding=0)

    def get_displayed_range(self):
        """
        Return the range of the displayed values in the plot
        Returns:

        """
        return self.pg_plot.getViewBox().viewRange()

    def keyPressEvent(self, event):
        """
        Reimplemented to catch specific key such as delete
        Args:
            event:

        Returns:

        """

        if event.key() == QtCore.Qt.Key_Delete:
            # if an interval is selected, then we delete it
            selected_ti = self.ti_manager.get_selected_time_interval()
            if selected_ti is not None:
                selected_ti.remove_from_tag()
        else:
            super().keyPressEvent(event=event)

    def add_time_interval_name(self, name):
        """

        Args:
            name:

        Returns:

        """
        if len(self.available_plot_indices) > 0:
            index_plot = np.min(self.available_plot_indices)
            self.available_plot_indices.remove(index_plot)
        else:
            index_plot = len(self.ti_plots_index_dict)
        self.ti_plots_index_dict[name] = index_plot
        # display a red_line
        # plot_item = self.pg_plot.plot(x=np.arange(self.n_frames), y=[index_plot] * self.n_frames,
        #                               pen=(255, 0, 0))
        red_color = (255, 0, 0)
        infinite_line = pg.InfiniteLine(pos=index_plot, angle=0, pen=red_color, movable=False,
                                        bounds=None, hoverPen=red_color, label=name,
                                        labelOpts={"movable": True}, name=None)
        self.pg_plot.addItem(infinite_line)
        self.ti_plots_item_dict[name] = infinite_line
        self.update_range()

        return infinite_line

    def mouse_hover_interval_callback(self, finite_region, hover):
        """
        Called when the mouse is hover an interval
        :param finite_region: instance of FiniteLinearRegionItem
        :param hover: (bool) if the mouse is hover or not
        :return:
        """
        if hover:
            # first and last timestamps of the interval
            region = finite_region.getRegion()
            first_ts = region[0]
            last_ts = region[1]
            duration = last_ts - first_ts
            self.ti_manager.config_widget.update_hover_interval_duration(f"{duration:.2f} sec")
        else:
            self.ti_manager.config_widget.update_hover_interval_duration(" "*50)

    def add_time_interval(self, time_interval, time_interval_name, values, selected=False, is_newborn=False):
        """

        Args:
            time_interval: instance of TimeInterval
            time_interval_name:
            values: list of 2 int representing the first and last frame of the time interval
            selected:
            is_newborn:
        Returns:

        """

        index_plot = self.ti_plots_index_dict[time_interval_name]
        linear_region = MyFiniteLinearRegionItem(values=values,
                                                 time_interval=time_interval,
                                                 finite_values=(index_plot - 0.4, index_plot + 0.4),
                                                 bounds=(self.min_timestamp, self.max_timestamp), int_rounding=False,
                                                 selected=selected, new_line_pos_callback=self.line_moved,
                                                 is_newborn=is_newborn,
                                                 mouse_hover_callback=self.mouse_hover_interval_callback)
        """
        https://srinikom.github.io/pyside-docs/PySide/QtGui/QGraphicsItem.html#PySide.QtGui.QGraphicsItem
        Sets the Z-value of the item to z . 
        The Z value decides the stacking order of sibling (neighboring) items.
         A sibling item of high Z value will always be drawn on top of another sibling item with a lower Z value.

        If you restore the Z value, the item’s insertion order will decide its stacking order.

        The Z-value does not affect the item’s size in any way.

        The default Z-value is 0.
        """
        linear_region.setZValue(-10)
        self.pg_plot.addItem(linear_region)
        self.ti_linear_region_item_dict[time_interval.id] = linear_region
        return linear_region

    def plot_predictions(self, timestamps, predictions, time_interval_name):
        """

        Args:
            timestamps:  1d array, same length as predictions, tiemstamps in sec
            predictions: 1d array, same length as timestamps, float value between 0 and 1
            time_interval_name:

        Returns:

        """
        index_plot = self.ti_plots_index_dict[time_interval_name]

        # main line will represent the 0.5 threshold
        # the blue line will represent the 1 of probability
        self.pg_plot.plot(timestamps, [index_plot - 0.5] * len(timestamps), pen=(0, 0, 255))  # blue
        # self.pg_plot.plot(timestamps, (index_plot + 0.5) - predictions , stepMode=False,
        #                   fillLevel=index_plot + 0.5, brush=(255, 0, 0, 100)) # red
        self.pg_plot.plot(timestamps, (index_plot + 0.5) - predictions, stepMode=False,
                          pen=pg.mkPen(color=(255, 0, 0), width=1, style=QtCore.Qt.DashLine))

    def add_start_line(self, timestamp):
        pen_color = (100, 149, 237)  # cornflowerblue
        self.start_line = pg.InfiniteLine(pos=timestamp, angle=90, pen=pen_color, movable=False,
                                          bounds=None, hoverPen=pen_color, label=None,
                                          labelOpts=None, name=None)
        self.pg_plot.addItem(self.start_line)

    def remove_start_line(self):
        if self.start_line is None:
            return
        self.pg_plot.removeItem(self.start_line)

    def line_moved(self, new_pos, first_value, time_interval):
        """
        One line of a LinearRegion has been moved. We change the frame displayed in consequence
        Args:
            new_pos:

        Returns:

        """
        self.ti_manager.go_to_timestamp(timestamp=new_pos, from_line_moved=True)
        if time_interval is not None:
            if first_value:
                time_interval.set_first_value(first_value=new_pos)
            else:
                time_interval.set_last_value(last_value=new_pos)

    def remove_time_interval(self, time_interval):
        if time_interval.id not in self.ti_linear_region_item_dict:
            return
        item = self.ti_linear_region_item_dict[time_interval.id]
        self.pg_plot.removeItem(item=item)

    def remove_time_interval_name(self, name):
        """
        Remove the line, the LinearRegion should have been removed previously
        Args:
            name:

        Returns:

        """
        infinite_line = self.ti_plots_item_dict[name]
        self.pg_plot.removeItem(item=infinite_line)
        index_plot = self.ti_plots_index_dict[name]
        self.available_plot_indices.append(index_plot)
        del self.ti_plots_item_dict[name]
        del self.ti_plots_index_dict[name]
        self.update_range()

    def update_range(self):
        """
        Update the range according to the number of time interval names
        Returns:

        """
        # we want to reorganize indices

        n_plots = len(self.ti_plots_item_dict)
        if n_plots <= 0:
            return
        indices = list(self.ti_plots_index_dict.values())
        self.pg_plot.setYRange(np.min(indices) - 0.5, np.max(indices) + 0.5)
        self.view_box.setLimits(yMin=np.min(indices) - 0.5, yMax=np.max(indices) + 0.5)

    def rename_time_interval(self, old_name, new_name):
        if old_name not in self.ti_plots_item_dict:
            return

        self.ti_plots_item_dict[new_name] = self.ti_plots_item_dict[old_name]
        self.ti_plots_index_dict[new_name] = self.ti_plots_index_dict[old_name]
        del self.ti_plots_item_dict[old_name]
        del self.ti_plots_index_dict[old_name]

    def update_plot(self):
        pass

    def get_corresponding_frame_index(self, timestamp):
        """
        Return the frame index corresponding to this timestamp.
        If value is negative or > to the number of frames, it means no frame matches
        Args:
            timestamp:

        Returns:

        """
        pass

    def display_frame(self, frame_number):
        pass


class NoWheelQComboBox(QComboBox):
    # deactivate the wheel action over a combo box, to avoid wrong manipulation
    def __init__(self, *args, **kwargs):
        super(NoWheelQComboBox, self).__init__(*args, **kwargs)

    def wheelEvent(self, *args, **kwargs):
        return


class TimeIntervalButtons:
    """
    Contains the buttons for a given time interval so we can change it
    """

    def __init__(self, ti_manager, ti_name, ti_tag, v_box_tag, v_box_remove, v_box_rename,
                 v_box_default, set_as_default, v_box_categories, grid_layout,
                 main_v_box, category,
                 tool_tip=None):
        """

        Args:
            ti_manager:
            ti_name:
            ti_tag: TimeIntervalTag instance
            v_box_tag:
            v_box_remove:
            v_box_rename:
            v_box_default:
            set_as_default:
            main_v_box:
            tool_tip:
        """
        self.ti_manager = ti_manager
        self.ti_button = QPushButton(ti_name)
        self.ti_name = ti_name
        self.ti_manager = ti_manager
        self.ti_tag = ti_tag
        self.grid_layout = grid_layout
        # items in this panel
        self.items_list = []

        n_items = self.grid_layout.count()
        n_col = self.grid_layout.columnCount()
        # print(f"TimeIntervalButtons: n_items {n_items}, n_col {n_col}")
        if n_col == 0:
            self.row_index = 0
        else:
            self.row_index = int(n_items // n_col)

        while True:
            if self.grid_layout.itemAtPosition(self.row_index, 0) is not None:
                self.row_index += 1
            else:
                break

        if tool_tip is not None:
            self.ti_button.setToolTip(tool_tip)
        self.ti_button.clicked.connect(self.tag_button_action)
        # v_box_tag.insertWidget(v_box_tag.count() - 1, self.ti_button)
        self.grid_layout.addWidget(self.ti_button, self.row_index, 0)
        self.items_list.append(self.ti_button)

        # use to know where to put the new time interval
        self.is_default_one = set_as_default
        self.default_checkbox = QCheckBox()
        self.default_checkbox.setToolTip("Set this tag as default")
        self.default_checkbox.setChecked(self.is_default_one)
        self.default_checkbox.stateChanged.connect(self.default_checkbox_action)
        # v_box_default.insertWidget(v_box_default.count() - 1, self.default_checkbox)
        self.grid_layout.addWidget(self.default_checkbox, self.row_index, 1)
        self.items_list.append(self.default_checkbox)

        self.category_combo_box = NoWheelQComboBox()
        self.category_combo_box.setToolTip(f"Category of {ti_name}")
        self.category_combo_box.addItems(TimeIntervalsConfigWidget.CATEGORIES)
        index = self.category_combo_box.findText(category, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.category_combo_box.setCurrentIndex(index)

        # self.category_combo_box.currentText()
        # v_box_categories.insertWidget(v_box_categories.count() - 1, self.category_combo_box)
        self.grid_layout.addWidget(self.category_combo_box, self.row_index, 2)
        self.items_list.append(self.category_combo_box)

        self.remove_ti_button = QPushButton(" - ")
        self.remove_ti_button.setToolTip(f"Remove {ti_name}")
        self.remove_ti_button.clicked.connect(self.delete_interval)
        # v_box_remove.insertWidget(v_box_remove.count() - 1, self.remove_ti_button)
        self.grid_layout.addWidget(self.remove_ti_button, self.row_index, 3)
        self.items_list.append(self.remove_ti_button)

        # self.h_box = QHBoxLayout()
        self.line_edit = QLineEdit()
        self.line_edit.setFixedWidth(100)
        self.line_edit.setText(ti_name)
        self.line_edit.setToolTip(f"New name for {ti_name}")
        self.line_edit.returnPressed.connect(self.rename_interval)
        self.grid_layout.addWidget(self.line_edit, self.row_index, 4)
        self.items_list.append(self.line_edit)
        # self.h_box.addWidget(self.line_edit)

        # self.change_ti_name_button = QPushButton("*")
        # self.change_ti_name_button.setToolTip(f"Rename {ti_name}")
        # self.change_ti_name_button.clicked.connect(self.rename_interval)
        # self.h_box.addWidget(self.change_ti_name_button)

        # v_box_rename.insertLayout(v_box_rename.count() - 1, self.h_box)

    def change_active_status(self, activate_it):
        """
        mean we change the active status. It is considered active if the current timestamps fall during a time_interval
        Returns:

        """
        if activate_it:
            self.ti_button.setStyleSheet("background-color: red")
        else:
            self.ti_button.setStyleSheet("background-color: #505F69")

    def default_checkbox_action(self):
        if self.is_default_one:
            # checkbox can't be deselected except by another checkbox
            self.default_checkbox.setChecked(True)
        else:
            self.is_default_one = True
            if self.ti_manager.default_ti_tag is not None:
                # we deselect the checkbox of the other ti_tag
                self.ti_manager.default_ti_tag.deselect_default_check_box()
            self.ti_manager.default_ti_tag = self.ti_tag

    def change_default_status(self):
        self.is_default_one = not self.is_default_one
        self.default_checkbox.setChecked(self.is_default_one)

    def get_category(self):
        return self.category_combo_box.currentText()

    def tag_button_action(self):
        """
        Call when the button with the name of the tag is clicked
        Either move the currently selected time_interval to this tag, or if None are selected and a recent time_interval
        has been created, then it move it to this tag
        Returns:

        """
        if self.ti_manager.selected_time_interval is not None:
            time_interval = self.ti_manager.selected_time_interval

        elif self.ti_manager.config_widget.last_interval_created is not None:
            time_interval = self.ti_manager.config_widget.last_interval_created
        else:
            return

        if self.ti_manager.config_widget.get_action_on_ti() == TimeIntervalsConfigWidget.MOVE_ACTION:
            # we want to move the selected time_interval to the current tag
            tag_name = time_interval.get_tag()
            if tag_name != self.ti_name:
                # pass
                time_interval.remove_from_tag()
                time_interval.add_to_tag(time_interval_tag=self.ti_manager.get_time_interval(tag_name=self.ti_name))
            else:
                # already in the right tag, we don't do anything
                pass
        elif self.ti_manager.config_widget.get_action_on_ti() == TimeIntervalsConfigWidget.DUPLICATE_ACTION:
            # in that case we want to duplicate this time_interval
            time_interval.duplicate(new_time_interval_tag=self.ti_manager.get_time_interval(tag_name=self.ti_name))

    def rename_interval(self):
        new_name = str(self.line_edit.text())
        if new_name == "":
            return
        if self.ti_name == new_name:
            return
        self.ti_manager.rename_interval(old_name=self.ti_name, new_name=new_name)
        self.ti_name = new_name
        self.ti_button.setText(self.ti_name)

    def delete_interval(self):
        """"""
        confirm_delete_qb = QMessageBox()
        confirm_delete_qb.setWindowTitle("CICADA")
        confirm_delete_qb.setText(f"Are you sure you want to delete {self.ti_name} and its content ?")
        confirm_delete_qb.setStandardButtons(QMessageBox.Yes)
        confirm_delete_qb.addButton(QMessageBox.No)
        confirm_delete_qb.setDefaultButton(QMessageBox.No)
        if confirm_delete_qb.exec() == QMessageBox.Yes:
            self.ti_manager.delete_interval_name(self.ti_name)

    def remove_widgets(self):
        """
        Remove widgets. implementation of the deleteLater method to properly delete the whole widget
        Will be called by self.ti_manager.delete_interval_name method
        Returns:

        """
        try:
            for item in self.items_list:
                self.grid_layout.removeWidget(item)
                item.deleteLater()

            # self.ti_button.deleteLater()
            # self.category_combo_box.deleteLater()
            # self.default_checkbox.deleteLater()
            # self.remove_ti_button.deleteLater()
            # self.line_edit.deleteLater()
            # self.change_ti_name_button.deleteLater()
        except RuntimeError:
            pass


class TimeIntervalsConfigWidget(ExploratoryWidgetModel, QWidget, metaclass=FinalMeta):
    """
    Module that will allow to add/modify/tags and activate the selection of time intervals
    """
    GENERAL_CATEGORY = "General"
    BEHAVIOR_CATEGORY = "Behavior"

    DUPLICATE_ACTION = "Duplicate"
    MOVE_ACTION = "Move"

    CATEGORIES = (GENERAL_CATEGORY, BEHAVIOR_CATEGORY)

    ACTIONS_ON_TI = (DUPLICATE_ACTION, MOVE_ACTION)

    def __init__(self, time_intervals_manager, data_to_explore, current_timestamp,
                 parent=None, main_window=None, to_connect_to_main_window=True):
        ExploratoryWidgetModel.__init__(self, data_to_explore=data_to_explore, main_window=main_window,
                                        to_connect_to_main_window=to_connect_to_main_window)
        QWidget.__init__(self, parent=parent)

        # -------------- data ---------------
        self.data_to_explore = data_to_explore
        self.current_timestamp = current_timestamp

        # manager
        self.ti_manager = time_intervals_manager

        self.main_window = main_window
        # used to mark an event with the start button
        self.ti_start = None
        self.last_interval_created = None
        # allows the widget to be expanded in vertical but not in the horizonal axis
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        # --------------- GUI -------------------
        self.setWindowTitle("Time intervals tags")

        self.main_layout = QVBoxLayout()
        self.scrollArea = QScrollArea()
        # ScrollBarAlwaysOff = 1
        # ScrollBarAlwaysOn = 2
        # ScrollBarAsNeeded = 0
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.main_layout.addWidget(self.scrollArea)

        self.scroll_area_widget_contents = QWidget()
        self.scrollArea.setWidget(self.scroll_area_widget_contents)
        self.layout = QVBoxLayout(self.scroll_area_widget_contents)
        # we add stretch now and we will insert new widget before the stretch
        self.layout.addStretch(1)
        # ==============================
        self.setLayout(self.main_layout)

        self.title_label = QLabel("Time intervals tags")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.title_label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.layout.insertWidget(self.layout.count() - 1, self.title_label)

        self.start_stop_layout = QHBoxLayout()
        self.start_stop_layout.addStretch(1)

        self.start_button = QPushButton("START")
        self.start_button.setToolTip("Mark the current frame as the start of the new time interval")
        self.start_button.clicked.connect(self.mark_ti_start)
        self.start_stop_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("STOP")
        self.stop_button.setToolTip("Mark the current frame as the stop of the new time interval")
        self.stop_button.clicked.connect(self.mark_ti_stop)
        self.start_stop_layout.addWidget(self.stop_button)

        self.start_stop_layout.addStretch(1)
        self.layout.insertLayout(self.layout.count() - 1, self.start_stop_layout)

        self.time_intervals_button_frame_dict = dict()

        self.h_box = QHBoxLayout()

        self.v_box_tag = QVBoxLayout()
        # self.h_box.addLayout(self.v_box_tag)
        self.v_box_default = QVBoxLayout()
        # self.h_box.addLayout(self.v_box_default)
        self.v_box_categories = QVBoxLayout()
        # self.h_box.addLayout(self.v_box_categories)
        self.v_box_remove = QVBoxLayout()
        # self.h_box.addLayout(self.v_box_remove)
        self.v_box_rename = QVBoxLayout()
        # self.h_box.addLayout(self.v_box_rename)
        self.grid_layout = QGridLayout()
        self.h_box.addStretch(1)
        self.h_box.addLayout(self.grid_layout)
        self.h_box.addStretch(1)

        # we can either save the tags in a .yaml file or in the .nwb file
        self.layout.insertLayout(self.layout.count() - 1, self.h_box)

        # --- Action to perform when clicking on the button from a tag to move or duplicate
        # self.action_ti_layout = QHBoxLayout()
        # self.action_ti_layout.addStretch(1)
        self.category_layout = QHBoxLayout()
        self.category_layout.addStretch(1)
        self.action_ti_combo_box = QComboBox()
        self.action_ti_combo_box.setToolTip(f"Action to perform when a time interval is selected")
        self.action_ti_combo_box.addItems(TimeIntervalsConfigWidget.ACTIONS_ON_TI)
        index = self.action_ti_combo_box.findText(TimeIntervalsConfigWidget.MOVE_ACTION,
                                                  QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.action_ti_combo_box.setCurrentIndex(index)
        self.grid_layout.addWidget(self.action_ti_combo_box, 0, 0)
        # # adding empty label so it is aligned to action_ti_combo_box
        self.grid_layout.addWidget(create_empty_label(), 0, 1)
        self.grid_layout.addWidget(create_empty_label(), 0, 2)
        self.grid_layout.addWidget(create_empty_label(), 0, 3)
        self.grid_layout.addWidget(create_empty_label(), 0, 4)

        # self.action_ti_layout.addWidget(self.action_ti_combo_box)

        # self.action_ti_layout.addStretch(1)
        # self.layout.insertLayout(self.layout.count() - 1, self.action_ti_layout)

        self.create_button_layout = QHBoxLayout()
        self.create_button_layout.addStretch(1)
        self.create_line_edit = QLineEdit()
        self.create_line_edit.setText("")
        self.create_line_edit.returnPressed.connect(self.create_time_interval_tag_from_line_edit)
        self.create_button_layout.addWidget(self.create_line_edit)
        self.create_button = QPushButton("  +  ")
        self.create_button.setToolTip("create a new time interval")
        self.create_button.clicked.connect(self.create_time_interval_tag_from_line_edit)
        self.create_button_layout.addWidget(self.create_button)
        self.create_button_layout.addStretch(1)
        self.layout.insertLayout(self.layout.count() - 1, self.create_button_layout)

        self.layout.insertWidget(self.layout.count() - 1, create_empty_label())

        self.category_layout = QHBoxLayout()
        self.category_layout.addStretch(1)
        self.category_combo_box = NoWheelQComboBox()
        self.category_combo_box.setToolTip(f"Category of data to load or save")
        self.category_combo_box.addItems(TimeIntervalsConfigWidget.CATEGORIES)
        index = self.category_combo_box.findText(TimeIntervalsConfigWidget.BEHAVIOR_CATEGORY,
                                                 QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.category_combo_box.setCurrentIndex(index)
        self.category_layout.addWidget(self.category_combo_box)

        self.load_empty_ones_check_box = QCheckBox()
        self.load_empty_ones_check_box.setChecked(False)
        self.load_empty_ones_check_box.setText("Load empty ones ?")
        self.category_layout.addWidget(self.load_empty_ones_check_box)

        self.category_layout.addStretch(1)
        # self.category_combo_box.currentText()
        self.layout.insertLayout(self.layout.count() - 1, self.category_layout)

        self.files_layout = QHBoxLayout()
        # self.files_layout.addStretch(1)
        self.load_tags_button = QPushButton("load tags")
        self.load_tags_button.setToolTip("Load tags from npz file (without time intervals data)")
        self.load_tags_button.clicked.connect(self.load_time_interval_tags)
        self.files_layout.addWidget(self.load_tags_button)
        self.load_check_box = QCheckBox()
        self.load_check_box.setChecked(False)
        self.load_check_box.setText("Erase data ?")
        self.files_layout.addWidget(self.load_check_box)
        self.load_time_intervals_button = QPushButton("load data")
        self.load_time_intervals_button.setToolTip("Load time intervals from npz file")
        self.load_time_intervals_button.clicked.connect(self.load_time_intervals)
        self.files_layout.addWidget(self.load_time_intervals_button)
        self.save_time_intervals_button = QPushButton("save data")
        self.save_time_intervals_button.setToolTip("Save time intervals in a npz file")
        self.save_time_intervals_button.clicked.connect(self.save_time_intervals_as_npz)
        self.files_layout.addWidget(self.save_time_intervals_button)

        # self.files_layout.addStretch(1)
        self.layout.insertLayout(self.layout.count() - 1, self.files_layout)

        self.predictions_files_layout = QHBoxLayout()
        self.load_predictions_button = QPushButton("load TADA predictions")
        self.load_predictions_button.setToolTip("Load TADA predictions from npz file")
        self.load_predictions_button.clicked.connect(self.load_tada_predictions)
        self.predictions_files_layout.addWidget(self.load_predictions_button)
        self.layout.insertLayout(self.layout.count() - 1, self.predictions_files_layout)

        self.hover_interval_duration_layout = QHBoxLayout()
        self.hover_interval_duration_layout.addStretch(1)
        self.hover_interval_duration_label = QLabel(" " * 50)
        self.hover_interval_duration_label.setAlignment(Qt.AlignCenter)
        self.hover_interval_duration_label.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.hover_interval_duration_label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.hover_interval_duration_layout.addWidget(self.hover_interval_duration_label)
        self.hover_interval_duration_layout.addStretch(1)
        self.layout.insertLayout(self.layout.count() - 1, self.hover_interval_duration_layout)

    def update_hover_interval_duration(self, label):
        """

        :return:
        """
        self.hover_interval_duration_label.setText(label)

    def get_action_on_ti(self):
        """
        Return the type of action to do when a tag button is clicked on and a time interval is selected
        Returns:

        """
        return self.action_ti_combo_box.currentText()

    def mark_ti_start(self):
        """
        Called when a new interval start is marked.
        The interval will be created if the button stop is pressed later on
        Returns:

        """
        if self.ti_start is not None:
            self.reinitialize_start_button()
        else:
            self.ti_start = self.current_timestamp
            self.start_button.setStyleSheet("background-color: cornflowerblue")
            self.ti_manager.main_widget.add_start_line(timestamp=self.current_timestamp)

    def mark_ti_stop(self):
        """
        Create a time interval if a start time has been defined
        Returns:

        """
        if self.ti_start is None:
            return

        ti_stop = self.current_timestamp

        # stop should be equal or super to start
        if ti_stop < self.ti_start:
            ti_stop_tmp = ti_stop
            ti_stop = self.ti_start
            self.ti_start = ti_stop_tmp

        default_ti_tag = self.ti_manager.default_ti_tag

        if default_ti_tag is None:
            self.reinitialize_start_button()
            return

        # removing the newborn status to the last interval created
        if self.last_interval_created is not None:
            self.last_interval_created.change_newborn_status()

        self.last_interval_created = default_ti_tag.create_new_time_interval(start_timestamp=self.ti_start,
                                                                             stop_timestamp=ti_stop)
        self.last_interval_created.change_newborn_status()

        self.reinitialize_start_button()

    def reinitialize_start_button(self):
        self.ti_start = None
        self.start_button.setStyleSheet("background-color: #505F69")
        self.ti_manager.main_widget.remove_start_line()

    def load_time_interval_tags(self):
        """
        Just load the tags from a npz file
        If tag already exists, the data of the one existing are kept
        Returns:

        """
        t_i_dict = self.open_time_intervals_file()
        if t_i_dict is None:
            return
        time_intervals_names = list(t_i_dict.keys())
        for interval_name in time_intervals_names:
            if self.interval_name_available(name=interval_name):
                self.ti_manager.create_time_intervals(interval_name=interval_name,
                                                      category=self.category_combo_box.currentText(),
                                                      time_intervals_data=None, erase_previous_one=False)

    def load_time_intervals(self):
        """
        Load time interval from a npz file
        Returns:

        """
        t_i_dict = self.open_time_intervals_file()
        if t_i_dict is None:
            return
        print_epochs_details = True
        if print_epochs_details:
            print(f"Information about epochs of {self.data_to_explore.identifier} loaded")
        first_ts = None
        last_ts = None
        for interval_name, time_intervals_data in t_i_dict.items():
            if len(time_intervals_data.shape) == 1:
                continue
                # TODO: see to transform it in a 2d array, and add option to convert frames from CI in timestamps
                # periods = get_continous_time_periods(time_intervals_data)
                # new_2_array = np.zeros((2, len(periods)))
                # for period_index, period in enumerate(period):
                #     new_2_array[0, period_index] = period[0]
                #     new_2_array[1, period_index] = period[1]
            else:
                load_empty_ones = self.load_empty_ones_check_box.isChecked()
                if time_intervals_data.shape[1] == 0 and (not load_empty_ones):
                    # not loading intervals tags with no intervals
                    continue
                if print_epochs_details and time_intervals_data is not None:
                    total_duration_in_sec = 0
                    for index in np.arange(time_intervals_data.shape[1]):
                        total_duration_in_sec += (time_intervals_data[1, index] - time_intervals_data[0, index])
                        if first_ts is None or (first_ts > time_intervals_data[0, index]):
                            first_ts = time_intervals_data[0, index]
                        if last_ts is None or (last_ts < time_intervals_data[1, index]):
                            last_ts = time_intervals_data[1, index]
                    print(f'# {interval_name}: {time_intervals_data.shape[1]} epochs, '
                          f'total duration {np.round(total_duration_in_sec, 2)} sec')
                self.ti_manager.create_time_intervals(interval_name=interval_name,
                                                      category=self.category_combo_box.currentText(),
                                                      time_intervals_data=time_intervals_data,
                                                      erase_previous_one=self.load_check_box.isChecked())
        if print_epochs_details:
            print(f"First timestamp: {np.round(first_ts)}, last timestamp: {np.round(last_ts)}, "
                  f"range cover by epochs {np.round(last_ts - first_ts)}")
            print("")
    def load_tada_predictions(self):
        """
        Load predictions from deepTADA
        Returns:

        """
        t_i_dict = self.open_time_intervals_file("Loading TADA predictions")
        if t_i_dict is None:
            return
        for behavior_name, predictions in t_i_dict.items():
            self.ti_manager.add_predictions(interval_name=behavior_name,
                                            predictions_data=predictions)

    def open_time_intervals_file(self, title="Loading time intervals"):
        """
        Open a file dialog to select a npz file
        Returns: None if no file has been selected, a dict with tag_name as key and 2d array as value (first and last
        frame of each interval) or 1d array (boolean then)

        """
        # file = str(QFileDialog.getOpenFileName(parent=self.main_window, caption="toto", directory="./")[0])
        # print(f"file {file}")
        file_dialog = QFileDialog(self.main_window, title)

        # setting options
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.DontUseCustomDirectoryIcons
        file_dialog.setOptions(options)

        # ARE WE TALKING ABOUT FILES OR FOLDERS
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Npz files (*.npz)")

        # OPENING OR SAVING
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)

        # SET THE STARTING DIRECTORY
        # default_value = self.analysis_arg.get_default_value()
        # if default_value is not None and isinstance(default_value, str):
        #     self.file_dialog.setDirectory(default_value)

        # print(f"if file_dialog.exec_() == QDialog.Accepted")
        # print(f"file_dialog.exec_() {file_dialog.exec_()}")
        if file_dialog.exec() == QDialog.Accepted:
            npz_file_name = file_dialog.selectedFiles()[0]
            npz_content = np.load(npz_file_name)
            time_intervals_dict = dict()
            for item, value in npz_content.items():
                # print(f"item {item}, value {value}")
                time_intervals_dict[item] = value
            return time_intervals_dict
        return None

    def save_time_intervals_as_npz(self):
        """
        Load time interval from a npz file
        Returns:

        """

        file_dialog = QFileDialog(self, "Saving time intervals")

        # setting options
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.DontUseCustomDirectoryIcons
        file_dialog.setOptions(options)

        # ARE WE TALKING ABOUT FILES OR FOLDERS
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilter("Npz files (*.npz)")

        # OPENING OR SAVING
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)

        # SET THE STARTING DIRECTORY
        # default_value = self.analysis_arg.get_default_value()
        # if default_value is not None and isinstance(default_value, str):
        #     self.file_dialog.setDirectory(default_value)
        if file_dialog.exec_() == QDialog.Accepted:
            npz_file_name = file_dialog.selectedFiles()[0]
            time_intervals_2d_array = self.ti_manager.get_intervals_data(category=self.category_combo_box.currentText())
            # print(f"save_time_intervals_as_npz time_intervals_2d_array {time_intervals_2d_array}")
            np.savez(npz_file_name, **time_intervals_2d_array)

    def interval_name_available(self, name):
        """
        Return True if name is not already used by an interval times
        Args:
            name:

        Returns:

        """
        return self.ti_manager.interval_name_available(name=name)

    def create_time_interval_tag_from_line_edit(self):
        """
        Create a time interval tag
        Returns:

        """
        new_name = str(self.create_line_edit.text())
        if new_name == "":
            return

        # when TimeIntervalTag is instantiate, it calls create_time_interval_tag in self
        # by default behavior_category, then it can be changed later on
        self.ti_manager.create_time_intervals(interval_name=new_name,
                                              category=TimeIntervalsConfigWidget.BEHAVIOR_CATEGORY)

    def create_time_interval_tag(self, new_name, set_as_default, ti_tag, category):
        """

        Args:
            new_name:
            set_as_default: boolean
            ti_tag: TimeIntervalTag instance

        Returns:

        """
        # function called from TimeIntervalTag class at initiation
        # TImeIntervalTags created in the method create_time_intervals in time_interval_manager
        tibf = TimeIntervalButtons(ti_manager=self.ti_manager, ti_name=new_name,
                                   ti_tag=ti_tag, category=category,
                                   v_box_tag=self.v_box_tag,
                                   v_box_default=self.v_box_default, v_box_categories=self.v_box_categories,
                                   main_v_box=self.layout, v_box_remove=self.v_box_remove,
                                   grid_layout=self.grid_layout,
                                   v_box_rename=self.v_box_rename, set_as_default=set_as_default)

        return tibf

    # def delete_interval_name(self, interval_name):
    #     # TODO: See to modify the nwb file or other
    #     del self.time_intervals_button_frame_dict[interval_name]
    #     del self.time_intervals_dict[interval_name]

    def get_corresponding_frame_index(self, timestamp):
        """
        Return the frame index corresponding to this timestamp.
        If value is negative or > to the number of frames, it means no frame matches
        Args:
            timestamp:

        Returns:

        """
        pass

    def set_current_timestamp(self, timestamp):
        """
        Change the timestamp to display
        Args:
            timestamp:

        Returns:

        """
        self.current_timestamp = timestamp


class MyFiniteLinearRegionItem(FiniteLinearRegionItem):
    """
    Are used to display time intervals
    """

    def __init__(self, time_interval, values=[0, 1], finite_values=None, orientation=None, brush=None, movable=True,
                 bounds=None,
                 int_rounding=False, selected=False, new_line_pos_callback=None, is_newborn=False,
                 mouse_hover_callback=None):
        # bounds: are there to limit the extension of the area
        FiniteLinearRegionItem.__init__(self, values=values, finite_values=finite_values, orientation=orientation,
                                        brush=brush,
                                        movable=movable, bounds=bounds, int_rounding=int_rounding,
                                        new_line_pos_callback=new_line_pos_callback, time_interval=time_interval,
                                        mouse_hover_callback=mouse_hover_callback)
        # instance of TimeInterval from cicada_time_intervals.py
        self.time_interval = time_interval

        if brush is None:
            self.non_selected_brush = QtGui.QBrush(QtGui.QColor(0, 0, 255, 150))
        else:
            self.non_selected_brush = brush
        self.selected_brush = QtGui.QBrush(QtGui.QColor(255, 0, 0, 255))
        self.newborn_brush = QtGui.QBrush(QtGui.QColor(255, 255, 0, 200))  # yellow
        if selected:
            self.update_selected_brush()
        # priority goes to newborns
        if is_newborn:
            self.update_newborn_brush()

    def mouseDoubleClickEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            self.time_interval.change_selection()
            # update_selected_brush will be called by time_interval in change_selection() method

    def update_selected_brush(self):
        """
        Should be called if the selection has been changed. The brush will be change accordingly and the item update
        Returns:

        """
        if self.time_interval.selected:
            self.setBrush(self.selected_brush)
        elif self.time_interval.is_newborn:
            self.setBrush(self.newborn_brush)
        else:
            self.setBrush(self.non_selected_brush)
        self.update()

    def update_newborn_brush(self):
        """
        Should be called if the newborn status has been changed.
        The brush will be change accordingly and the item update
        Returns:

        """
        if self.time_interval.is_newborn:
            self.setBrush(self.newborn_brush)
        elif self.time_interval.selected:
            self.setBrush(self.selected_brush)
        else:
            self.setBrush(self.non_selected_brush)
        self.update()


def create_empty_label():
    q_label_empty = QLabel("  ")
    q_label_empty.setAlignment(Qt.AlignCenter)
    q_label_empty.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    q_label_empty.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    return q_label_empty
