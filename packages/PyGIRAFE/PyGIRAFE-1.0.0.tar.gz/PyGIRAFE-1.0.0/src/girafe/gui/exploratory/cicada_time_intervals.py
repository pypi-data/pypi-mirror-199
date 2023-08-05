from .cicada_exploratory_widgets import TimeIntervalsMainWidget, TimeIntervalsConfigWidget
import numpy as np
# from cicada.utils.misc import get_continous_time_periods
# from datetime import datetime
# import time
import uuid
import sys


class TimeIntervalsManager:
    """
    Allows communication between the main widget that displays the time intervals and the configuration panel (widget)

    """
    def __init__(self, data_to_explore, min_timestamp, max_timestamp, main_window, parent,
                 current_timestamp,
                 go_to_timestamp_fct):
        self.data_to_explore = data_to_explore
        self.min_timestamp = min_timestamp
        self.max_timestamp = max_timestamp
        self.main_window = main_window
        self.parent = parent
        self.go_to_timestamp_fct = go_to_timestamp_fct
        # the ti tag to which new time interval will be added by default when created then the user can click on a
        # a button to change its place
        self.default_ti_tag = None

        # keep a reference to the selected time interval.
        # allows to delete it or move it to another tag
        # if None means no time interval is selected
        self.selected_time_interval = None

        self.main_widget = TimeIntervalsMainWidget(data_to_explore=self.data_to_explore,
                                                   min_timestamp=min_timestamp, max_timestamp=max_timestamp,
                                                   current_timestamp=current_timestamp,
                                                   ti_manager=self,
                                                   parent=self.parent,
                                                   main_window=self.main_window,
                                                   to_connect_to_main_window=True)

        # contains the buttons
        # to open a widget on its own, set parent to None, then call show() method and don't add the widget to a layout
        # and set to_connect_to_main_window to True
        self.config_widget = TimeIntervalsConfigWidget(time_intervals_manager=self,
                                                       current_timestamp=current_timestamp,
                                                       data_to_explore=self.data_to_explore,
                                                       main_window=self.main_window,
                                                       parent=self.parent,
                                                        to_connect_to_main_window=True)

        self.time_intervals_dict = dict()

        self.create_intervals_from_data_to_explore()

    def link_x_view(self, widgets_to_link):
        """
        Link the x view of the time interval widget to some other widgets
        Args:
            widgets_to_link: list of widgets

        Returns:

        """
        for widget_to_link in widgets_to_link:
            widget_to_link.link_to_view(view_to_link=self.main_widget.view_box)

    def set_current_timestamp(self, timestamp, from_line_moved=False):
        """
        Change the timestamp in  elements of the IntervalManager
        Args:
            timestamp:
            from_line_moved:

        Returns:

        """
        self.main_widget.set_current_timestamp(timestamp=timestamp, from_line_moved=from_line_moved)
        self.config_widget.set_current_timestamp(timestamp=timestamp)
        # updating time_interval_tags instance in order to change the buttons activation colors
        for ti_tag in self.time_intervals_dict.values():
            ti_tag.set_current_timestamp(timestamp=timestamp)

    def get_displayed_range(self):
        """
        Return the range displayed on the main plot
        Returns: 2 float tuple

        """
        return self.main_widget.get_displayed_range()

    def get_intervals_data(self, category):
        """
        Return a dict with as key the name of the tags and as value a 2d np.array (2*n_intervals)
        lines representing first_timestamp and second_timestamp
        Returns:

        """
        intervals_data_dict = dict()
        for ti_name, ti_tag in self.time_intervals_dict.items():
            if ti_tag.get_category() == category:
                intervals_data_dict[ti_name] = ti_tag.get_intervals_data()
        return intervals_data_dict

    def go_to_timestamp(self, timestamp, from_line_moved=False):
        """
        Call a function outside the scope of this class
        Args:
            timestamp:
            from_line_moved: means it was called by a line moved by the user

        Returns:

        """
        self.go_to_timestamp_fct(timestamp, from_line_moved=from_line_moved)

    def get_main_widget(self):
        return self.main_widget

    def get_selected_time_interval(self):
        """
        Return the selected time interval, or None if none is selected
        Returns:

        """
        return self.selected_time_interval

    def get_time_interval(self, tag_name):
        """
        Return the TimeInterval instance with tag_name if exists, None otherwise
        Args:
            tag_name:

        Returns:

        """
        if tag_name in self.time_intervals_dict:
            return self.time_intervals_dict[tag_name]
        return None

    def interval_name_available(self, name):
        """
        Return True if name is not already used by an interval times
        Args:
            name:

        Returns:

        """
        return not (name in self.time_intervals_dict)

    def create_time_intervals(self, interval_name, category, time_intervals_data=None, erase_previous_one=False):
        """

        Args:
            interval_name:
            category:
            time_intervals_data: 2d array (2 x n_intervals)
            erase_previous_one:

        Returns:

        """
        already_exists = not self.interval_name_available(name=interval_name)
        if already_exists and (not erase_previous_one):
            return
        if already_exists:
            # then we delete it
            self.delete_interval_name(interval_name=interval_name)
        ti_tag = TimeIntervalTag(name=interval_name, time_intervals_data=time_intervals_data,
                                 min_timestamp=self.min_timestamp, max_timestamp=self.max_timestamp,
                                 ti_manager=self, category=category)
        self.time_intervals_dict[interval_name] = ti_tag

    def add_predictions(self, interval_name, predictions_data):
        """
        Add predictions from TADA
        Args:
            interval_name: (str)
            predictions_data: (2d array, shape (2, n_times), line 0: timestamps is sec, line 2: predictions float between
            0 & 1

        Returns:

        """
        interval_name_absent = self.interval_name_available(name=interval_name)
        if interval_name_absent:
            print(f"Interval {interval_name} is unknown. Predictions can't be added")
            return

        self.main_widget.plot_predictions(timestamps=predictions_data[0], predictions=predictions_data[1],
                                          time_interval_name=interval_name)

    def rename_interval(self, old_name, new_name):
        """

        Args:
            old_name:
            new_name:

        Returns:

        """
        self.time_intervals_dict[old_name].rename(new_name)
        self.time_intervals_dict[new_name] = self.time_intervals_dict[old_name]
        # removing reference in the dict, does'nt delete the TimeIntervalTag otherwise
        del self.time_intervals_dict[old_name]
        self.main_widget.rename_time_interval(old_name, new_name)

    def delete_interval_name(self, interval_name):
        """
        Just delete it from the internal list. remove the buttons and the plot as well
        Args:
            interval_name:

        Returns:

        """
        if interval_name not in self.time_intervals_dict:
            return
        ti_tag = self.time_intervals_dict[interval_name]
        # removing the buttons in the config panel
        ti_tag.ti_buttons.remove_widgets()
        ti_tag.delete_all_time_intervals()
        # now removing the infinte_line in mainWidget and updating the plot
        self.main_widget.remove_time_interval_name(interval_name)
        del self.time_intervals_dict[interval_name]
        if self.default_ti_tag is not None:
            if ti_tag.name == self.default_ti_tag.name:
                self.default_ti_tag = None
            # then we need to select a new default_ti_tag
            if len(self.time_intervals_dict) > 0:
                # randomly
                keys = list(self.time_intervals_dict.keys())
                new_default_ti_tag = self.time_intervals_dict[keys[0]]
                self.default_ti_tag = new_default_ti_tag
                # change select mode
                new_default_ti_tag.deselect_default_check_box()

    def get_config_widget(self):
        return self.config_widget

    def create_intervals_from_data_to_explore(self):
        """
        Create intervals from the data_to_explore
        Return a dict that contains the time intervals, each one being a
        Returns:

        """
        # for interval_name, time_intervals_data in initial_time_intervals_dict.items():
        # self.create_time_intervals(interval_name=interval_name, time_intervals_data=time_intervals_data)
        intervals_names = self.data_to_explore.get_intervals_names()

        behavior_epoch_names = self.data_to_explore.get_behavioral_epochs_names()

        for intervals_name in intervals_names:
            time_intervals_data = self.data_to_explore.get_interval_times(interval_name=intervals_name)

            if time_intervals_data is None:
                continue
            # time_intervals_data: 2d np.array of int (2 x n_time_intervals)
            #         first line is the first timestamps of the time_interval, 2nd the second timestamps
            self.create_time_intervals(interval_name=intervals_name, category=TimeIntervalsConfigWidget.GENERAL_CATEGORY,
                                       time_intervals_data=time_intervals_data)
            # TODO: add the intervals data
            # self.create_time_intervals(interval_name=intervals_name, time_intervals_data=time_intervals_data)

        for epoch_name in behavior_epoch_names:
            time_intervals_data = self.data_to_explore.get_behavioral_epochs_times(epoch_name=epoch_name)

            if time_intervals_data is None:
                continue
            # time_intervals_data: 2d np.array of int (2 x n_time_intervals)
            #         first line is the first timestamps of the time_interval, 2nd the second timestamps
            self.create_time_intervals(interval_name=epoch_name, category=TimeIntervalsConfigWidget.BEHAVIOR_CATEGORY,
                                       time_intervals_data=time_intervals_data)
            # TODO: add the intervals data
            # self.create_time_intervals(interval_name=intervals_name, time_intervals_data=time_intervals_data)

    def get_n_tags(self):
        return len(self.time_intervals_dict)


class TimeIntervalTag:
    # represent one of several time intervals representing the same thing (behavior, etc...)

    def __init__(self, name, ti_manager, min_timestamp, max_timestamp, category, time_intervals_data=None):
        self.name = name
        self.ti_manager = ti_manager
        self.min_timestamp = min_timestamp
        self.max_timestamp = max_timestamp

        # ti_buttons is an instance of TimeIntervalButtons
        # default one if it is the first
        set_as_default = (self.ti_manager.get_n_tags() == 0)
        self.ti_buttons = self.ti_manager.config_widget.create_time_interval_tag(new_name=self.name,
                                                                                 category=category,
                                                                                 ti_tag=self,
                                                                                 set_as_default=set_as_default)
        if set_as_default:
            self.ti_manager.default_ti_tag = self

        self.infinite_line = self.ti_manager.main_widget.add_time_interval_name(name=self.name)

        self.time_intervals_dict = dict()

        if time_intervals_data is not None:
            # now we create time intervals
            # time_intervals_tuple = get_continous_time_periods(time_intervals_data)
            # if len(time_intervals_tuple) > 0:
            #     for period in time_intervals_tuple:
            #         ti = TimeInterval(parent=self, first_value=period[0], last_value=period[1])
            #         self.time_intervals_dict[ti.id] = ti

            if time_intervals_data.shape[1] > 0:
                for index in np.arange(time_intervals_data.shape[1]):
                    ti = TimeInterval(parent=self, first_value=time_intervals_data[0, index],
                                      last_value=time_intervals_data[1, index])
                    if ti.id in self.time_intervals_dict:
                        raise Exception(f"Id of time_interval already exists {ti.id}")
                    self.time_intervals_dict[ti.id] = ti

    def get_category(self):
        return self.ti_buttons.get_category()

    def delete_all_time_intervals(self):
        for ti in self.time_intervals_dict.values():
            self.ti_manager.main_widget.remove_time_interval(time_interval=ti)
        self.time_intervals_dict = dict()

    def get_intervals_data(self):
        """
        Return a 2d np.array (2*n_intervals)
        lines representing first_timestamp and second_timestamp
        Returns:

        """
        intervals_data = np.zeros((2, len(self.time_intervals_dict)))
        for ti_index, ti in enumerate(self.time_intervals_dict.values()):
            intervals_data[0, ti_index] = ti.first_value
            intervals_data[1, ti_index] = ti.last_value

        return intervals_data

    def set_current_timestamp(self, timestamp):
        ti = self.get_interval_by_timestamp(timestamp=timestamp)
        if ti is None:
            self.ti_buttons.change_active_status(activate_it=False)
        else:
            self.ti_buttons.change_active_status(activate_it=True)

    def deselect_default_check_box(self):
        self.ti_buttons.change_default_status()

    def auto_delete(self):
        pass

    def get_interval_by_timestamp(self, timestamp):
        """
        Return the timeinterval that contains this timestamp or None if none exists.
        Considers that time interval don't intersect, if so only one will be return
        Args:
            timestamp:

        Returns:

        """
        for ti in self.time_intervals_dict.values():
            if ti.is_timestamp_in(timestamp):
                return ti
        return None

    def rename(self, new_name):
        # old_name = new_name
        self.name = new_name
        # changing the label associated to the inifinte line
        self.infinite_line.label.setFormat(new_name)
        # no need to modify ti_buttons, as the call should come from it.

    def create_new_time_interval(self, start_timestamp, stop_timestamp):
        """

        Args:
            start_timestamp:
            stop_timestamp:

        Returns:

        """
        ti = TimeInterval(parent=self, first_value=start_timestamp,
                          last_value=stop_timestamp)
        self.time_intervals_dict[ti.id] = ti
        return ti

    def add_time_interval(self, time_interval):
        """
        Add an already time_interval to this tag
        Args:
            time_interval: instance of TimeInterval

        Returns:

        """
        if time_interval.id in self.time_intervals_dict:
            # means it already in
            return
        self.time_intervals_dict[time_interval.id] = time_interval

    def remove_time_interval(self, time_interval):
        """
        Remove a given time_interval
        Args:
            time_interval: instance of TimeInterval

        Returns:

        """
        if time_interval.id not in self.time_intervals_dict:
            return
        # we need to remove it from the plot
        self.ti_manager.main_widget.remove_time_interval(time_interval)
        del self.time_intervals_dict[time_interval.id]
        # we update the time_intervals_data
        # self.update_time_intervals_data()

    def update_time_intervals_data(self):
        """
        Recompute the boolean array representing the
        Returns:

        """
        pass


class TimeInterval:

    def __init__(self, parent, first_value, last_value):
        """

        Args:
            parent: TimeIntervalTag instance
            first_value: float timestamp
            last_value: float timestamp
        """
        self.parent = parent
        self.ti_manager = self.parent.ti_manager
        # first and last value will be modified by line_moved() method in MainWidget class
        self.first_value = first_value
        self.last_value = last_value
        # indicate if this ti is selected
        self.selected = False
        # is defined a newborn a time interval just created by the user
        # it's color change then
        self.is_newborn = False

        # we use as id the creation time
        #
        # self.id = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
        # using current time
        # self.id = int(time.time()*10**7)
        # with python 3.7 time.time_ns()
        self.id = str(uuid.uuid4())
        self.linear_region = None
        # print(f"time_interval_name {self.parent.name}, values {(first_value, last_value)}")
        self.linear_region = self.ti_manager.main_widget.add_time_interval(time_interval_name=self.parent.name,
                                                                           time_interval=self,
                                                                           values=(self.first_value, self.last_value),
                                                                           selected=self.selected)

    def duplicate(self, new_time_interval_tag):
        """
        Duplicate this time_interval to a new_time_interval_tag
        Args:
            new_time_interval_tag: TimeIntervalTag instance

        Returns:

        """
        return new_time_interval_tag.create_new_time_interval(start_timestamp=self.first_value,
                                                              stop_timestamp=self.last_value)

    def set_first_value(self, first_value):
        self.first_value = first_value

    def set_last_value(self, last_value):
        # print(f"{self.last_value} New last_value {last_value}")
        self.last_value = last_value

    def is_timestamp_in(self, timestamp):
        """
        Check if the timestamp is in the time_interval
        Args:
            timestamp:

        Returns:

        """
        return (timestamp >= (self.first_value-sys.float_info.epsilon)) and \
               (timestamp <= (self.last_value+sys.float_info.epsilon))

    def change_selection(self):
        """
        Change the selection status
        Returns:

        """
        if not self.selected:
            self.selected = True
            if self.ti_manager.selected_time_interval:
                # only one can be selected at once
                # we unselect the other one
                self.ti_manager.selected_time_interval.change_selection()
            self.ti_manager.selected_time_interval = self
        else:
            self.selected = False
            self.ti_manager.selected_time_interval = None
        # updating the color of the linear region
        self.linear_region.update_selected_brush()

    def get_tag(self):
        """
        return the name (tag) of the time interval
        Returns:

        """
        return self.parent.name

    def get_parent(self):
        """
        Return the TimeInterval instance representing the tag it belongs to
        Returns:

        """
        return self.parent

    def remove_from_tag(self):
        """
        remove the time interval from it tag
        Returns:

        """
        self.parent.remove_time_interval(time_interval=self)

    def add_to_tag(self, time_interval_tag):
        self.parent = time_interval_tag
        time_interval_tag.add_time_interval(time_interval=self)
        self.linear_region = self.ti_manager.main_widget.add_time_interval(time_interval_name=self.parent.name,
                                                                           time_interval=self,
                                                                           values=(self.first_value, self.last_value),
                                                                           selected=self.selected,
                                                                           is_newborn=self.is_newborn)

    def change_newborn_status(self):
        self.is_newborn = not self.is_newborn
        # updating the color of the linear region
        self.linear_region.update_newborn_brush()
