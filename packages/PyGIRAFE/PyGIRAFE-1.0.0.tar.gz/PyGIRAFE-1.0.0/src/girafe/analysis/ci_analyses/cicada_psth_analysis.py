from cicada.analysis.cicada_analysis import CicadaAnalysis
from time import time
import numpy as np
from cicada.utils.misc import from_timestamps_to_frame_epochs
from cicada.utils.display.psth import get_psth_values, plot_one_psth, plot_several_psth
import math
from bisect import bisect_right
from cicada.utils.display.colors import BREWER_COLORS
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from cicada.utils.misc import from_timestamps_to_frame_epochs, validate_indices_in_string_format, \
    extract_indices_from_string, print_info_dict
from sortedcontainers import SortedDict
import scipy.stats as stats
import pandas as pd
import seaborn as sns
import os


class CicadaPsthAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        A list of
        :param data_to_analyse: list of data_structure
        :param family_id: family_id indicated to which family of analysis this class belongs. If None, then
        the analysis is a family in its own.
        :param data_format: indicate the type of data structure. for NWB, NIX
        """
        CicadaAnalysis.__init__(self, name="Population level PSTH", family_id="Epochs",
                                short_description="Build PeriStimuli Time Histogram at population level",
                                config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

        # each key is an int representing the age, the value is a list of session_data
        self.sessions_by_age = dict()

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaPsthAnalysis(config_handler=self.config_handler)
        self.transfer_attributes_to_tabula_rasa_copy(analysis_copy=analysis_copy)
        return analysis_copy

    def check_data(self):
        """
        Check the data given one initiating the class and return True if the data given allows the analysis
        implemented, False otherwise.
        :return: a boolean
        """
        super().check_data()

        for session_index, session_data in enumerate(self._data_to_analyse):
            if session_data.DATA_FORMAT != "CI_DATA":
                self.invalid_data_help = f"Non CI_DATA format compatibility not yet implemented: " \
                                         f"{session_data.DATA_FORMAT}"
                return False

        for data_to_analyse in self._data_to_analyse:
            roi_response_series = data_to_analyse.get_roi_response_series()
            if len(roi_response_series) == 0:
                self.invalid_data_help = f"No roi response series available in " \
                                         f"{data_to_analyse.identifier}"
                return False

        # It is also necessary to have epoch to work with, but if None is available, then it won't just be possible
        # to run the analysis

        return True

    def set_arguments_for_gui(self):
        """

        Returns:

        """
        CicadaAnalysis.set_arguments_for_gui(self)

        self.add_roi_response_series_arg_for_gui(short_description="Neural activity to use", long_description=None)

        ages = []
        for session_index, session_data in enumerate(self._data_to_analyse):
            age = session_data.age
            if age not in self.sessions_by_age:
                self.sessions_by_age[age] = []
            self.sessions_by_age[age].append(session_data)
            ages.append(age)
        self.add_choices_for_groups_for_gui(arg_name="sessions_grouped_by_age", choices=np.unique(ages),
                                            with_color=False,
                                            mandatory=False,
                                            short_description="Grouped by age",
                                            long_description="If you select group of ages, PSTH will be produced "
                                                             "averaging PSTH over the session in that age. "
                                                             "You can indicate the "
                                                             "ages in text field, such as '1-4 6 15-17'to "
                                                             "make a group "
                                                             "with age 1 to 4, 6 and 15 to 17. If None are selected, "
                                                             "then a PSTH will be produce for each session.",
                                            family_widget="session_selection",
                                            add_custom_group_field=True,
                                            custom_group_validation_fct=validate_indices_in_string_format,
                                            custom_group_processor_fct=None)

        all_epochs = []
        for data_to_analyse in self._data_to_analyse:
            all_epochs.extend(data_to_analyse.get_intervals_names())
            all_epochs.extend(data_to_analyse.get_behavioral_epochs_names())
        all_epochs = list(np.unique(all_epochs))

        self.add_bool_option_for_gui(arg_name="do_psth_on_one_epoch", true_by_default=False,
                                     short_description="Build PSTH from ONE main epoch ?",
                                     long_description="If yes, build the PSTH only from the behavioral epochs "
                                                      "occurring in this selected main epoch",
                                     family_widget="main epochs")

        self.add_choices_for_groups_for_gui(arg_name="psth_period", choices=all_epochs,
                                            with_color=False,
                                            mandatory=False,
                                            short_description="Select 1 epoch to build PSTH on this main epoch",
                                            long_description="Select 1 epoch to restrict PSTH analysis to the "
                                                             "behavioral epochs occurring during this epoch",
                                            family_widget="main epochs")

        self.add_choices_for_groups_for_gui(arg_name="epochs_names", choices=all_epochs,
                                            with_color=False,
                                            mandatory=False,
                                            short_description="Epochs",
                                            long_description="Select epochs for which you want to build PSTH",
                                            family_widget="epochs")

        self.add_bool_option_for_gui(arg_name="do_fusion_epochs", true_by_default=False,
                                     short_description="Fusion epochs ?",
                                     long_description="If checked, within a group epochs that overlap "
                                                      "will be fused so they represent "
                                                      "then one epoch.",
                                     family_widget="epochs")

        self.add_bool_option_for_gui(arg_name="filter_consecutive_movements", true_by_default=False,
                                     short_description="Remove movements separated by less time than psth range",
                                     long_description=None,
                                     family_widget="epochs")

        if len(self._data_to_analyse) == 1 and self._data_to_analyse[0].has_epoch_table():
            self.add_bool_option_for_gui(arg_name="from_epoch_table", true_by_default=False,
                                         short_description="Build PSTH from epoch table",
                                         family_widget="epochs_table")
            self.add_epoch_dict_arg_for_gui(short_description="Define epochs to group from epoch table",
                                            long_description=None,
                                            multiple_choices=True,
                                            arg_name='epoch_table', family_widget="epochs_table")

        if len(self._data_to_analyse) == 1 and self._data_to_analyse[0].has_trial_table():
            self.add_bool_option_for_gui(arg_name="from_trial_table", true_by_default=False,
                                         short_description="Build PSTH from trial table",
                                         family_widget="trials_table")
            self.add_trial_dict_arg_for_gui(short_description="Define trials to group from trial table",
                                            long_description=None,
                                            multiple_choices=True,
                                            arg_name='trial_table', family_widget="trials_table")

        all_cell_types = []
        for data_to_analyse in self._data_to_analyse:
            all_cell_types.extend(data_to_analyse.get_all_cell_types())

        all_cell_types = list(set(all_cell_types))

        self.add_choices_for_groups_for_gui(arg_name="cells_groups", choices=all_cell_types,
                                            with_color=True,
                                            mandatory=False,
                                            short_description="Groups of cells",
                                            long_description="If you select cells's groups, a PSTH will be created "
                                                             "for each cells'group and session. You can indicate the "
                                                             "cell indices in text field, such as '1-4 6 15-17'to "
                                                             "make a group "
                                                             "with cell 1 to 4, 6 and 15 to 17.",
                                            family_widget="cell_type",
                                            add_custom_group_field=True,
                                            custom_group_validation_fct=validate_indices_in_string_format,
                                            custom_group_processor_fct=None)

        self.add_choices_arg_for_gui(arg_name="session_color_choice", choices=["default_color", "brewer", "spectral"],
                                     short_description="Colors for session plots",
                                     default_value="default_color",
                                     multiple_choices=False, long_description=None,
                                     family_widget="session_color_config")

        self.add_color_arg_for_gui(arg_name="session_default_color", default_value=(0, 0, 0, 1.),
                                   short_description="Default color for session",
                                   long_description=None, family_widget="session_color_config")

        self.add_int_values_arg_for_gui(arg_name="psth_range", min_value=50, max_value=20000,
                                        short_description="Range of the PSTH (ms)",
                                        default_value=10000, family_widget="psth_config")

        self.add_int_values_arg_for_gui(arg_name="low_percentile", min_value=1, max_value=49,
                                        short_description="Low percentile",
                                        default_value=25, family_widget="psth_config")

        self.add_int_values_arg_for_gui(arg_name="high_percentile", min_value=51, max_value=99,
                                        short_description="High percentile",
                                        default_value=75, family_widget="psth_config")

        self.add_choices_arg_for_gui(arg_name="ref_in_epoch", choices=["start", "end", "middle"],
                                     short_description="Reference point to center PSTH",
                                     long_description="Determine which part of the epoch to center the PSTH on",
                                     default_value="start",
                                     multiple_choices=False, family_widget="psth_config")

        self.add_bool_option_for_gui(arg_name="work_on_traces", true_by_default=False,
                                     short_description="Do PSTH on traces",
                                     long_description=None,
                                     family_widget="psth_config")

        self.add_choices_arg_for_gui(arg_name="traces_normalization", choices=["raw", "df/f", "z-score"],
                                     short_description="Normalize traces for PSTH",
                                     long_description=None,
                                     default_value="df/f",
                                     multiple_choices=False, family_widget="psth_config")

        self.add_bool_option_for_gui(arg_name="average_all_traces", true_by_default=False,
                                     short_description="Average all traces to do psth on mean trace signal",
                                     long_description=None,
                                     family_widget="psth_config")

        self.add_choices_arg_for_gui(arg_name="plot_style_option", choices=["lines", "bars"],
                                     short_description="Options to display the PSTH",
                                     default_value="lines",
                                     multiple_choices=False, long_description=None, family_widget="plot_config")

        self.add_bool_option_for_gui(arg_name="plots_with_same_y_scale", true_by_default=True,
                                     short_description="Same scale for Y axis",
                                     long_description=None,
                                     family_widget="plot_config")

        self.add_bool_option_for_gui(arg_name="average_fig", true_by_default=False,
                                     short_description="Add a figure that average all sessions",
                                     long_description=None,
                                     family_widget="plot_config")

        self.add_bool_option_for_gui(arg_name="one_fig_by_group_and_epoch", true_by_default=False,
                                     short_description="Plot a single figure for each group and each type of epoch",
                                     long_description=None,
                                     family_widget="plot_config")

        self.add_choices_arg_for_gui(arg_name="x_axis_scale", choices=["ms", "sec", "min"],
                                     short_description="X-axis scale",
                                     default_value="sec",
                                     multiple_choices=False, long_description=None, family_widget="plot_config")

        self.add_bool_option_for_gui(arg_name="with_surrogates", true_by_default=False,
                                     short_description="Use surrogate to define a threshold of activation",
                                     long_description=None,
                                     family_widget="surrogates")

        self.add_choices_arg_for_gui(arg_name="surrogate_method", choices=["single cell roll", "population roll"],
                                     short_description="Option for roll",
                                     long_description="How the roll will be done: either roll each cell independently"
                                                      "(will conserve a structured activity at single cell level but "
                                                      "remove structure at population level) "
                                                      "or roll all cells by the same value (population roll: it will"
                                                      "preserve structured activity at population level, synchronous"
                                                      "event are still observed but at random time point compared to "
                                                      "stimulation)",
                                     default_value="single cell roll",
                                     multiple_choices=False, family_widget="surrogates")

        self.add_int_values_arg_for_gui(arg_name="n_surrogates", min_value=10, max_value=10000,
                                        short_description="Number of surrogates",
                                        default_value=500, family_widget="surrogates")

        self.add_int_values_arg_for_gui(arg_name="low_percentile_surrogate", min_value=1, max_value=49,
                                        short_description="Low percentile in surrogate",
                                        default_value=5, family_widget="surrogates")

        self.add_int_values_arg_for_gui(arg_name="high_percentile_surrogate", min_value=51, max_value=99,
                                        short_description="High percentile in surrogate",
                                        default_value=95, family_widget="surrogates")

        self.add_color_arg_for_gui(arg_name="surrogate_color", default_value=(0.31, 0, 0, 1.),
                                   short_description="Default color for surrogate",
                                   long_description=None, family_widget="surrogates")

        self.add_int_values_arg_for_gui(arg_name="ticks_labels_size", min_value=1, max_value=50,
                                        short_description="Ticks' label size",
                                        default_value=20, family_widget="police")
        self.add_int_values_arg_for_gui(arg_name="axis_label_size", min_value=1, max_value=100,
                                        short_description="Axis' label size",
                                        default_value=30, family_widget="police")
        self.add_int_values_arg_for_gui(arg_name="axis_label_pad", min_value=1, max_value=50,
                                        short_description="Axis' label pad",
                                        default_value=20, family_widget="police")
        self.add_int_values_arg_for_gui(arg_name="legend_police_size", min_value=1, max_value=50,
                                        short_description="Legend's police size",
                                        default_value=20, family_widget="police")
        self.add_int_values_arg_for_gui(arg_name="ticks_length", min_value=1, max_value=20,
                                        short_description="Ticks' length",
                                        default_value=6, family_widget="police")
        self.add_int_values_arg_for_gui(arg_name="ticks_width", min_value=1, max_value=5,
                                        short_description="Ticks' width",
                                        default_value=2, family_widget="police")

        self.add_color_arg_for_gui(arg_name="background_color", default_value=(1, 1, 1, 1.),
                                   short_description="Background color",
                                   long_description=None, family_widget="police")

        self.add_color_arg_for_gui(arg_name="color_v_line", default_value=(0, 0, 0, 1.),
                                   short_description="Color of the zero vertical line",
                                   long_description=None, family_widget="police")

        self.add_int_values_arg_for_gui(arg_name="color_v_line_width", min_value=1, max_value=10,
                                        short_description="Width of the zero vertical line",
                                        default_value=5, family_widget="police")

        self.add_color_arg_for_gui(arg_name="color_ticks", default_value=(0, 0, 0, 1.),
                                   short_description="Ticks' color",
                                   long_description=None, family_widget="police")

        self.add_color_arg_for_gui(arg_name="axes_label_color", default_value=(0, 0, 0, 1.),
                                   short_description="Axes' label color",
                                   long_description=None, family_widget="police")

        self.add_bool_option_for_gui(arg_name="top_border_visible", true_by_default=False,
                                     short_description="Top border visible",
                                     long_description=None,
                                     family_widget="police")

        self.add_bool_option_for_gui(arg_name="bottom_border_visible", true_by_default=False,
                                     short_description="Bottom border visible",
                                     long_description=None,
                                     family_widget="police")

        self.add_bool_option_for_gui(arg_name="right_border_visible", true_by_default=False,
                                     short_description="Right border visible",
                                     long_description=None,
                                     family_widget="police")

        self.add_bool_option_for_gui(arg_name="left_border_visible", true_by_default=False,
                                     short_description="Left border visible",
                                     long_description=None,
                                     family_widget="police")

        self.add_color_arg_for_gui(arg_name="axes_border_color", default_value=(0, 0, 0, 1.),
                                   short_description="Axes' border color",
                                   long_description=None, family_widget="police")

        self.add_image_format_package_for_gui()

        self.add_verbose_arg_for_gui()

        self.add_with_timestamp_in_filename_arg_for_gui()

    def update_original_data(self):
        """
        To be called if the data to analyse should be updated after the analysis has been run.
        :return: boolean: return True if the data has been modified
        """
        pass

    def run_analysis(self, **kwargs):
        """
        test
        :param kwargs:
        :return:
        """
        CicadaAnalysis.run_analysis(self, **kwargs)

        roi_response_series_dict = kwargs["roi_response_series"]

        do_psth_on_one_epoch = kwargs.get("do_psth_on_one_epoch")

        psth_period = kwargs.get("psth_period")

        verbose = kwargs.get("verbose", True)

        from_epoch_table = kwargs.get("from_epoch_table")

        epoch_table = kwargs.get("epoch_table")

        from_trial_table = kwargs.get("from_trial_table")

        trial_table = kwargs.get("trial_table")

        epochs_names = kwargs.get("epochs_names")
        if (epochs_names is None) or len(epochs_names) == 0:
            if (epoch_table is None) and (trial_table is None):
                print(f"No epochs selected, no analysis")
                self.update_progressbar(time_started=self.analysis_start_time, increment_value=100)
                return

        cells_groups_dict = kwargs.get("cells_groups")
        # used to know if there are or not cell type groups
        no_cell_type_groups_tag = "_no_cell_type_groups_"

        # allows to compute a significant threshold
        with_surrogates = kwargs.get("with_surrogates", False)
        surrogate_method = kwargs.get("surrogate_method")
        n_surrogates = kwargs.get("n_surrogates", 500)
        low_percentile_surrogate = kwargs.get("low_percentile_surrogate")
        high_percentile_surrogate = kwargs.get("high_percentile_surrogate")
        surrogate_fcts_to_apply = [np.nanmedian, lambda x: np.nanpercentile(x, low_percentile_surrogate),
                                   lambda x: np.nanpercentile(x, high_percentile_surrogate)]
        surrogate_color = kwargs.get("surrogate_color")

        # ------- figures config part -------
        save_formats = kwargs["save_formats"]
        if save_formats is None:
            save_formats = "pdf"

        dpi = kwargs.get("dpi", 100)

        width_fig = kwargs.get("width_fig")

        height_fig = kwargs.get("height_fig")

        ref_in_epoch = kwargs.get("ref_in_epoch")

        ticks_labels_size = kwargs["ticks_labels_size"]
        axis_label_size = kwargs["axis_label_size"]
        axis_label_pad = kwargs["axis_label_pad"]
        legend_police_size = kwargs["legend_police_size"]
        ticks_length = kwargs["ticks_length"]
        ticks_width = kwargs["ticks_width"]

        background_color = kwargs["background_color"]
        color_v_line = kwargs["color_v_line"]
        color_v_line_width = kwargs["color_v_line_width"]
        color_ticks = kwargs["color_ticks"]
        axes_label_color = kwargs["axes_label_color"]

        top_border_visible = kwargs["top_border_visible"]
        right_border_visible = kwargs["right_border_visible"]
        bottom_border_visible = kwargs["bottom_border_visible"]
        left_border_visible = kwargs["left_border_visible"]

        axes_border_color = kwargs["axes_border_color"]

        psth_range_in_ms = kwargs.get("psth_range")
        psth_range_in_sec = psth_range_in_ms / 1000

        filter_consecutive_movements = kwargs.get("filter_consecutive_movements", False)

        # normalize neuronal data, for each cell
        work_on_traces = kwargs.get("work_on_traces")
        traces_normalization = kwargs.get("traces_normalization")

        # average all ROIs fluo to keep the average trace only
        average_all_traces = kwargs.get("average_all_traces", False)

        # if True then the plots should have the same Y axis scale
        plots_with_same_y_scale = kwargs.get("plots_with_same_y_scale", True)

        with_timestamps_in_file_name = kwargs.get("with_timestamp_in_file_name", True)

        session_color_choice = kwargs.get("session_color_choice")

        session_default_color = kwargs.get("session_default_color")

        one_fig_by_group_and_epoch = kwargs.get("one_fig_by_group_and_epoch")

        x_axis_scale = kwargs.get("x_axis_scale", "sec")

        # TODO: Add option to plot a "significant threshold" line using surrogates
        #  Would mean take each neuronal_data roll them x times, keep the max value of each surrogate
        #  an take the 95th percentile at each frames to determine thresholds ?
        #

        # ------- figures config part -------

        # we can either run the PSTH on all data from all session
        # or do a PSTH for each session individually and produce as many plots
        # or add option to group sessions for example by age

        # dict results from widget
        groups_by_age_from_widget = kwargs.get("sessions_grouped_by_age")

        # first we create a dict that will identify group of session by an id
        # a group could be just a session
        # dict key is a string, value is a list of CicadaAnalysisWrapper instances
        session_group_ids_dict = dict()

        # key is the session_group_id (str), value is a color (tuple of 4 floats)
        session_group_color_dict = dict()

        # take as key a session identifier and return the group_id it is part of
        session_to_group_id_mapping = dict()

        # then we have a dict with key epoch_name, value is a dict with key session_group_id and value a list of 2
        # elements: the time (in sec) of each value time of the PSTH, and PSTH data: list of length the number of fct
        # used each list being a list of float of length the number of timestamps
        psth_data_by_epoch_dict = dict()

        # same structure than psth_data_by_epoch_dict but at the end instead of the data, there is a dict
        # with keys the count for the different legends such as
        # number of subjects, number of sessions, number of cells, number of epochs
        psth_legends_by_epoch_dict = dict()

        # same than 2 others but the value is a list of all max_values of each neuronal_data psth median values
        # then percentile can be applied
        psth_surrogates_by_epoch_dict = dict()
        # create surrogate data with median and not max
        psth_rnd_data_by_epoch_dict = dict()

        # then we have a dict with key session_group_id, value is a dict with key epoch_name and value a list of 2
        # elements: the time (in sec) of each value time of the PSTH, and PSTH data: list of length the number of fct
        # used each list being a list of float of length the number of timestamps
        psth_data_by_session_group_dict = dict()

        # same structure than psth_data_by_session_group_dict but at the end instead of the data, there is a dict
        # with keys the count for the different legends such as
        # number of subjects, number of sessions, number of cells, number of epochs
        psth_legends_by_session_group_dict = dict()

        # same than 2 others but the value is a list of all max_values of each neuronal_data psth median values
        # then percentile can be applied
        psth_surrogates_by_session_group_dict = dict()
        # create surrogate data with median and not max
        psth_rnd_data_by_session_group_dict = dict()

        epochs_color_dict = dict()
        if from_epoch_table:
            epoch_group_name = 'Epoch from table'
            epochs_color_dict[epoch_group_name] = session_default_color
        elif from_trial_table:
            epoch_group_name = 'Trial from table'
            epochs_color_dict[epoch_group_name] = session_default_color
        else:
            for epoch_group_name, epoch_info in epochs_names.items():
                if len(epoch_info) != 2:
                    continue
                epochs_color_dict[epoch_group_name] = epoch_info[1]

        n_sessions = len(self._data_to_analyse)

        low_percentile = kwargs.get("low_percentile", 25)
        high_percentile = kwargs.get("high_percentile", 75)

        fcts_to_apply = [np.nanmedian, lambda x: np.nanpercentile(x, low_percentile),
                         lambda x: np.nanpercentile(x, high_percentile)]

        # fcts_to_apply = [np.nanmean, lambda x: np.nanmean(x) - 2 * np.nanstd(x),
        #                  lambda x: np.nanmean(x) + 2 * np.nanstd(x)]

        # first building the groups
        if len(groups_by_age_from_widget) > 0:
            # print(f"groups_by_age_from_widget {groups_by_age_from_widget}")
            # return
            for session_group_id, session_group_info in groups_by_age_from_widget.items():
                # session_group_info is a list with 2 elements, the second one is a color code
                # (4 float between 0 and 1) or None if not color option is activated.
                # For exemple: {'5-6': [['5', '6'], (1.0, 1.0, 1.0, 1.0)], '7-10': [['7-10'], (1.0, 1.0, 1.0, 1.0)]}
                # the first element is either a list of string representing int, or a list of more complex int like
                # 7-10 meaning from p7 to p10
                ages_in_group = []
                age_codes_in_group = session_group_info[0]
                group_color = session_group_info[1]
                for age_code in age_codes_in_group:
                    try:
                        age = int(age_code)
                        ages_in_group.append(age)
                    except ValueError:
                        ages_in_group.extend(extract_indices_from_string(age_code))

                session_group_ids_dict[session_group_id] = []
                session_group_color_dict[session_group_id] = group_color
                for age in ages_in_group:
                    if age in self.sessions_by_age:
                        sessions = self.sessions_by_age[age]
                        for session_data in sessions:
                            session_identifier = session_data.identifier
                            session_to_group_id_mapping[session_identifier] = session_group_id
                            session_group_ids_dict[session_group_id].append(session_data)

        else:
            # each session is its own group
            for session_index, session_data in enumerate(self._data_to_analyse):
                session_identifier = session_data.identifier
                session_to_group_id_mapping[session_identifier] = session_identifier
                session_group_ids_dict[session_identifier] = [session_data]
                session_group_color_dict[session_identifier] = session_default_color

        highest_sampling_rate = 0
        lowest_sampling_rate = 100000
        for session_index, session_data in enumerate(self._data_to_analyse):
            # Get Session Info
            info_dict = session_data.get_sessions_info()
            session_identifier = info_dict['identifier']

            if session_identifier not in session_to_group_id_mapping:
                # if the session does not belong to any group, we skip it
                continue
            if verbose:
                print(f" ")
                print(f"------------------ ONGOING SESSION: {session_identifier} -------------------- ")
                print(f"----------------------------- SESSION INFO ---------------------------------- ")
                print_info_dict(info_dict)
                print(f" ")

            if isinstance(roi_response_series_dict, dict):
                roi_response_serie_info = roi_response_series_dict[session_identifier]
            else:
                roi_response_serie_info = roi_response_series_dict

            neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)

            # Get CI movie sampling rate
            sampling_rate_hz = session_data.get_ci_movie_sampling_rate(only_2_photons=True)
            if sampling_rate_hz is None:
                sampling_rate_hz = session_data.get_rrs_sampling_rate(keys=roi_response_serie_info)

            if sampling_rate_hz > highest_sampling_rate:
                highest_sampling_rate = sampling_rate_hz
            if sampling_rate_hz < lowest_sampling_rate:
                lowest_sampling_rate = sampling_rate_hz

            one_frame_duration = 1000 / sampling_rate_hz
            psth_range_in_frames = math.ceil(psth_range_in_ms / one_frame_duration)

            if work_on_traces:
                if traces_normalization == 'raw':
                    if verbose:
                        print(f"Use raw traces in PSTH")
                if traces_normalization == 'df/f':
                    for cell, trace in enumerate(neuronal_data):
                        neuronal_data[cell] = (trace - np.median(trace)) / np.median(trace)
                if traces_normalization == 'z-score':
                    for cell in np.arange(len(neuronal_data)):
                        neuronal_data[cell, :] = stats.zscore(neuronal_data[cell])
                if average_all_traces:
                    # This would average all fluorescence traces in a single trace (use only for neuropil / axon imaging)
                    avg_trace = np.mean(neuronal_data, axis=0)
                    avg_traces = np.zeros((len(neuronal_data), len(avg_trace)))
                    for cell in range(len(neuronal_data)):
                        avg_traces[cell, :] = avg_trace
                    neuronal_data = avg_traces

            neuronal_data_timestamps = session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_info)
            if from_epoch_table:
                epoch_group_name = 'Epoch from table'
                epochs_names[epoch_group_name] = epoch_table
            if from_trial_table:
                epoch_group_name = 'Trial from table'
                epochs_names[epoch_group_name] = trial_table
            for epoch_group_name, epoch_info in epochs_names.items():
                if len(epoch_info) != 2:
                    if not (from_epoch_table or from_trial_table):
                        continue
                if from_epoch_table or from_trial_table:
                    epochs_names_in_group = [epoch_info]
                else:
                    epochs_names_in_group = epoch_info[0]
                # epoch_color = epoch_info[1]

                # TODO: take into consideration invalid epochs, and remove the one in invalid section
                epochs_frames_in_group = []
                invalid_times = session_data.get_interval_times(interval_name="invalid_times")
                extended_invalid_times = None
                invalid_times_are_sorted = False

                # first we extent the invalid times to take into consideration the range of PSTH
                if invalid_times is not None:
                    invalid_times_are_sorted = np.all(np.diff(invalid_times[1]) >= 0)
                    extended_invalid_times = np.zeros(invalid_times.shape)
                    for index in range(invalid_times.shape[1]):
                        start_ts = invalid_times[0, index]
                        stop_ts = invalid_times[1, index]
                        start_ts = max(0, start_ts - psth_range_in_sec)
                        stop_ts = stop_ts + psth_range_in_sec
                        extended_invalid_times[0, index] = start_ts
                        extended_invalid_times[1, index] = stop_ts
                # print(f"session_data.get_intervals_names() {session_data.get_intervals_names()}")
                if extended_invalid_times is not None:
                    print(f"Among {epoch_group_name}, containing : {epochs_names_in_group} we remove:")
                for epoch_name in epochs_names_in_group:
                    # looking in behavior or intervals
                    convert_timestamps_to_frames = True
                    if isinstance(epoch_name, str):
                        # Get interval timestamps
                        epochs_timestamps = session_data.get_interval_times(interval_name=epoch_name)
                        # Get behavioral timestamps
                        if epochs_timestamps is None:
                            epochs_timestamps = session_data.get_behavioral_epochs_times(epoch_name=epoch_name)
                        if epochs_timestamps is None:
                            # means this session doesn't have this epoch name
                            continue
                    # Get epoch table timestamps
                    if isinstance(epoch_name, dict):
                        epochs_timestamps, time_unit = session_data.get_epochs_timestamps_from_table(
                            requirements_dict=epoch_name)
                        if time_unit == 'frames':
                            convert_timestamps_to_frames = False
                        # Get trial table timestamps
                        if epochs_timestamps is None:
                            epochs_timestamps, time_unit = session_data.get_trials_timestamps_from_table(
                                requirements_dict=epoch_name)
                            if time_unit == 'frames':
                                convert_timestamps_to_frames = False
                        if epochs_timestamps is None:
                            # means this session doesn't have this epoch name
                            continue
                    epochs_are_sorted = np.all(np.diff(epochs_timestamps[1]) >= 0)
                    if extended_invalid_times is not None:
                        # now we want to filter epochs_timestamps
                        # we loop over each invalid epoch to remove the epoch that overlap it
                        # TODO: not super efficient, see to make it more efficient
                        filtered_epochs_timestamps = np.zeros(epochs_timestamps.shape)
                        n_epochs_kept = 0
                        last_epoch_kept_index = 0
                        in_invalid = 0
                        to_close_of_previous = 0
                        out_of_main_epoch = 0
                        if verbose:
                            print(f"Before removing epochs we have: {epochs_timestamps.shape[1]} {epoch_name}")
                        for epoch_index in range(epochs_timestamps.shape[1]):
                            epoch_start_ts = epochs_timestamps[0, epoch_index]
                            epoch_stop_ts = epochs_timestamps[1, epoch_index]
                            if epoch_index == 0:
                                previous_epoch_start_ts = 0
                            else:
                                previous_epoch_start_ts = epochs_timestamps[0, last_epoch_kept_index]

                            # if ordered, and the epoch if superior at the last invalid frames known
                            # we can skip it (if we don't do psth on one epoch or filter consecutive movements)
                            if (filter_consecutive_movements is False) and (do_psth_on_one_epoch is False):
                                if invalid_times_are_sorted and epochs_are_sorted and \
                                        (epoch_start_ts > extended_invalid_times[1, -1]):
                                    filtered_epochs_timestamps[:, n_epochs_kept] = epochs_timestamps[:, epoch_index]
                                    n_epochs_kept += 1
                                    continue

                            # Filter movements
                            to_filter = False
                            as_invalid = False

                            # Filter based on invalid times
                            if verbose and epoch_index == 0:
                                print(f"Remove {epoch_name} epochs if they overlap with invalid times")
                            for invalid_index in range(extended_invalid_times.shape[1]):
                                invalid_start_ts = extended_invalid_times[0, invalid_index]
                                invalid_stop_ts = extended_invalid_times[1, invalid_index]

                                if (epoch_start_ts >= invalid_start_ts) and (epoch_start_ts <= invalid_stop_ts):
                                    to_filter = True
                                    as_invalid = True
                                    in_invalid += 1
                                    break
                                if (epoch_stop_ts >= invalid_start_ts) and (epoch_stop_ts <= invalid_stop_ts):
                                    to_filter = True
                                    as_invalid = True
                                    in_invalid += 1
                                    break
                                if (epoch_start_ts <= invalid_start_ts) and (epoch_stop_ts >= invalid_stop_ts):
                                    to_filter = True
                                    as_invalid = True
                                    in_invalid += 1
                                    break

                            # Filter based on the main epoch selection
                            if do_psth_on_one_epoch and as_invalid is False:
                                keys_list = list(psth_period.keys())
                                psth_epoch_name = keys_list[0]
                                epoch_to_get = psth_period.get(psth_epoch_name)
                                epoch_to_get = (epoch_to_get[0])[0]
                                main_psth_epoch_timestamps = session_data.get_behavioral_epochs_times(
                                    epoch_name=epoch_to_get)
                                n_epochs_in_main_epoch = main_psth_epoch_timestamps.shape[1]
                                main_epoch_start = main_psth_epoch_timestamps[0, 0]
                                main_epoch_stop = main_psth_epoch_timestamps[1, 0]
                                if verbose and epoch_index == 0:
                                    if n_epochs_in_main_epoch == 1:
                                        print(
                                            f"Remove {epoch_name} epochs if they do not occur during : {epoch_to_get}, "
                                            f"(the main epoch selected) occurring between "
                                            f"t0 = {np.round(main_epoch_start, decimals=2)} s and "
                                            f"t1 = {np.round(main_epoch_stop, decimals=2)} s")
                                    else:
                                        print(
                                            f"Remove {epoch_name} epochs if they do not occur during : {epoch_to_get}, "
                                            f"(the main epoch selected) made of {n_epochs_in_main_epoch} sub-epochs")
                                epoch_is_in_main_epoch = False
                                for sub_epoch in range(n_epochs_in_main_epoch):
                                    main_epoch_start = main_psth_epoch_timestamps[0, sub_epoch]
                                    main_epoch_stop = main_psth_epoch_timestamps[1, sub_epoch]
                                    if epoch_start_ts > main_epoch_start and epoch_stop_ts < main_epoch_stop:
                                        epoch_is_in_main_epoch = True
                                        break
                                    else:
                                        continue
                                if epoch_is_in_main_epoch is False:
                                    to_filter = True
                                    out_of_main_epoch += 1

                            # Filter based on temporal distance from previous movement
                            if filter_consecutive_movements and to_filter is False:
                                if verbose and epoch_index == 0:
                                    print(f"Remove {epoch_name} epochs if they follow the previous kept {epoch_name}"
                                          f" by less than PSTH range ({2*psth_range_in_ms / 1000} s) ")
                                if (epoch_start_ts - previous_epoch_start_ts) <= 2 * psth_range_in_sec:
                                    to_filter = True
                                    to_close_of_previous += 1

                            if not to_filter:
                                filtered_epochs_timestamps[:, n_epochs_kept] = epochs_timestamps[:, epoch_index]
                                n_epochs_kept += 1
                                last_epoch_kept_index = epoch_index

                        filtered_epochs_timestamps = filtered_epochs_timestamps[:, :n_epochs_kept]
                        n_epochs_filtered = epochs_timestamps.shape[1] - filtered_epochs_timestamps.shape[1]
                        if verbose:
                            print(f"{n_epochs_filtered} {epoch_name} epochs removed: {in_invalid} in invalid frames, "
                                  f"{to_close_of_previous} too close from previous, {out_of_main_epoch} "
                                  f"out of main epoch")
                            print(f"{filtered_epochs_timestamps.shape[1]} {epoch_name} epochs left")
                        epochs_timestamps = filtered_epochs_timestamps

                    # session_data.get_interval_times()
                    # now we want to get the intervals time_stamps and convert them in frames
                    # list of list of 2 int
                    if convert_timestamps_to_frames:
                        intervals_frames = from_timestamps_to_frame_epochs(time_stamps_array=epochs_timestamps,
                                                                           frames_timestamps=neuronal_data_timestamps,
                                                                           as_list=True)
                    else:
                        intervals_frames = [(int(epochs_timestamps[0, i]), int(epochs_timestamps[1, i])) for i in
                                            range(epochs_timestamps.shape[1])]
                    epochs_frames_in_group.extend(intervals_frames)
                if extended_invalid_times is not None:
                    print(f" ")
                session_group_id = session_to_group_id_mapping[session_identifier]
                # then we have a dict with key epoch_name, value is a dict with key
                # session_group_id and value the PSTH data
                if epoch_group_name not in psth_data_by_epoch_dict:
                    # alpha_numeric_comparator make sure "10" will be after "1"
                    psth_data_by_epoch_dict[epoch_group_name] = dict()
                    psth_legends_by_epoch_dict[epoch_group_name] = dict()
                    psth_surrogates_by_epoch_dict[epoch_group_name] = dict()
                    psth_rnd_data_by_epoch_dict[epoch_group_name] = dict()

                # if no cells group selected, then we use all cells
                if len(cells_groups_dict) == 0:
                    cells_groups_dict[no_cell_type_groups_tag] = None

                cell_indices_by_cell_type = session_data.get_cell_indices_by_cell_type(roi_serie_keys=
                                                                                       roi_response_serie_info)

                for cells_group_name, cells_group_info in cells_groups_dict.items():

                    cell_indices_in_group = []

                    if cells_group_name not in psth_data_by_epoch_dict[epoch_group_name]:
                        psth_data_by_epoch_dict[epoch_group_name][cells_group_name] = \
                            SortedDict(alpha_numeric_comparator)
                        psth_legends_by_epoch_dict[epoch_group_name][cells_group_name] = \
                            SortedDict(alpha_numeric_comparator)
                        psth_surrogates_by_epoch_dict[epoch_group_name][cells_group_name] = \
                            SortedDict(alpha_numeric_comparator)
                        psth_rnd_data_by_epoch_dict[epoch_group_name][cells_group_name] = \
                            SortedDict(alpha_numeric_comparator)
                    if cells_group_name not in psth_data_by_session_group_dict:
                        psth_data_by_session_group_dict[cells_group_name] = SortedDict(alpha_numeric_comparator)
                        psth_legends_by_session_group_dict[cells_group_name] = SortedDict(alpha_numeric_comparator)
                        psth_surrogates_by_session_group_dict[cells_group_name] = SortedDict(alpha_numeric_comparator)
                        psth_rnd_data_by_session_group_dict[cells_group_name] = SortedDict(alpha_numeric_comparator)

                    if cells_group_name == no_cell_type_groups_tag:
                        cell_indices_in_group = np.arange(len(neuronal_data))
                    else:
                        if len(cells_group_info) != 2:
                            continue
                        cells_names_in_group = cells_group_info[0]
                        cells_group_color = cells_group_info[1]
                        for cells_name in cells_names_in_group:
                            # then we extract the cell_indices from the cells_group_name
                            # it is either a string representing the cell_type or a series of indices
                            if cells_name in cell_indices_by_cell_type:
                                cell_indices = cell_indices_by_cell_type[cells_name]
                            else:
                                cell_indices = np.array(extract_indices_from_string(cells_name))
                            if len(cell_indices) == 0:
                                continue
                            # making sure we are on the boundaries
                            cell_indices_in_group.extend(list(cell_indices[np.logical_and(cell_indices >= 0,
                                                                                          cell_indices < len(
                                                                                              neuronal_data))]))
                    cell_indices_in_group = np.array(cell_indices_in_group)
                    # if no cells, we skip it
                    if len(cell_indices_in_group) == 0:
                        continue

                    # TODO: See for fusioning epochs from a same group so there are extended
                    # y_values is a list of the same length as fct_to_apply,
                    # containing a list of float of size '(range_value*2)+1'
                    psth_frames_indices, psth_values = get_psth_values(data=neuronal_data[cell_indices_in_group],
                                                                       epochs=epochs_frames_in_group,
                                                                       ref_in_epoch=ref_in_epoch,
                                                                       range_value=psth_range_in_frames,
                                                                       fcts_to_apply=fcts_to_apply)
                    if with_surrogates:
                        print(f"Do the surrogate PSTH from: {n_surrogates} surrogates")
                        # Keep only the max median value of each surrogate psth
                        surrogate_max_values = []
                        # Will be use to take the median, low, high percentiles of the x surrogates at each time point
                        surrogate_median_values = np.zeros((len(psth_frames_indices), n_surrogates), dtype=float)
                        surrogate_low_perc_values = np.zeros((len(psth_frames_indices), n_surrogates), dtype=float)
                        surrogate_high_perc_values = np.zeros((len(psth_frames_indices), n_surrogates), dtype=float)
                        # Loop on the n surrogates
                        for index_surrogate in range(n_surrogates):
                            surrogate_neuronal_data = np.copy(neuronal_data[cell_indices_in_group])
                            if surrogate_method == "single cell roll":
                                if verbose and index_surrogate == 0:
                                    print(f"Proceed to independent rolling of all cells")
                                for cell in np.arange(len(surrogate_neuronal_data)):
                                    roll_value = np.random.randint(1, surrogate_neuronal_data.shape[1])
                                    surrogate_neuronal_data[cell, :] = np.roll(surrogate_neuronal_data[cell, :], shift=roll_value)
                            if surrogate_method == "population roll":
                                if verbose and index_surrogate == 0:
                                    print(f"Proceed to identical rolling of all cells")
                                roll_value = np.random.randint(1, surrogate_neuronal_data.shape[1])
                                surrogate_neuronal_data = np.roll(surrogate_neuronal_data, shift=roll_value, axis=1)

                            surro_psth_frames_indices, surro_psth_values = get_psth_values(
                                data=surrogate_neuronal_data,
                                epochs=epochs_frames_in_group,
                                ref_in_epoch=ref_in_epoch,
                                range_value=psth_range_in_frames,
                                fcts_to_apply=surrogate_fcts_to_apply)
                            # Append the max values of the psth:
                            surrogate_max_values.append([np.max(surro_psth_values[0])])
                            # print(f"max of surro_psth_values[0]: {np.max(surro_psth_values[0])}")
                            # surrogate_max_values.extend([np.max(surro_psth_values[0])])
                            # Create a matrix in which each column is the median value of a surrogate psth
                            surrogate_median_values[:, index_surrogate] = surro_psth_values[0]
                            surrogate_low_perc_values[:, index_surrogate] = surro_psth_values[1]
                            surrogate_high_perc_values[:, index_surrogate] = surro_psth_values[2]
                        # take the median at each time point for low prctile, median and high prctile of the surrogates
                        surrogate_median_psth_values = np.nanmedian(surrogate_median_values, axis=1)
                        surrogate_low_per_psth_values = np.nanmedian(surrogate_low_perc_values, axis=1)
                        surrogate_high_per_psth_values = np.nanmedian(surrogate_high_perc_values, axis=1)
                        surrogate_psth_values = [surrogate_median_psth_values, surrogate_low_per_psth_values,
                                                 surrogate_high_per_psth_values]

                        if session_group_id not in psth_data_by_epoch_dict[epoch_group_name][cells_group_name]:
                            psth_surrogates_by_epoch_dict[epoch_group_name][cells_group_name][session_group_id] = []
                        psth_surrogates_by_epoch_dict[epoch_group_name][cells_group_name][session_group_id].extend(
                            surrogate_max_values)

                        if session_group_id not in psth_surrogates_by_session_group_dict[cells_group_name]:
                            psth_surrogates_by_session_group_dict[cells_group_name][session_group_id] = dict()
                        if epoch_group_name not in psth_surrogates_by_session_group_dict[cells_group_name][
                            session_group_id]:
                            psth_surrogates_by_session_group_dict[cells_group_name][session_group_id][
                                epoch_group_name] = []
                        psth_surrogates_by_session_group_dict[cells_group_name][session_group_id][
                            epoch_group_name].extend(surrogate_max_values)

                    # putting indices in msec
                    psth_frames_indices = np.array(psth_frames_indices)
                    psth_times = psth_frames_indices * 1000 / sampling_rate_hz
                    if session_group_id not in psth_data_by_epoch_dict[epoch_group_name][cells_group_name]:
                        psth_data_by_epoch_dict[epoch_group_name][cells_group_name][session_group_id] = []
                        psth_rnd_data_by_epoch_dict[epoch_group_name][cells_group_name][session_group_id] = []
                        psth_legends_by_epoch_dict[epoch_group_name][cells_group_name][session_group_id] = dict()
                        legends_dict = psth_legends_by_epoch_dict[epoch_group_name][cells_group_name][session_group_id]
                        legends_dict["subjects"] = []
                        legends_dict["n_sessions"] = 0
                        legends_dict["n_cells"] = 0
                        legends_dict["n_epochs"] = 0

                    psth_data_by_epoch_dict[epoch_group_name][cells_group_name][session_group_id].append(
                        [psth_times, psth_values])
                    if with_surrogates:
                        psth_rnd_data_by_epoch_dict[epoch_group_name][cells_group_name][session_group_id].append(
                            [psth_times, surrogate_psth_values])

                    legends_dict = psth_legends_by_epoch_dict[epoch_group_name][cells_group_name][session_group_id]
                    legends_dict["subjects"].append(session_data.subject_id)
                    legends_dict["n_sessions"] += 1
                    legends_dict["n_cells"] += len(cell_indices_in_group)
                    legends_dict["n_epochs"] += len(epochs_frames_in_group)

                    # then we have a dict with key session_group_id, value is a dict with key epoch_name
                    # and value the PSTH data
                    if session_group_id not in psth_data_by_session_group_dict[cells_group_name]:
                        psth_data_by_session_group_dict[cells_group_name][session_group_id] = dict()
                        psth_rnd_data_by_session_group_dict[cells_group_name][session_group_id] = dict()
                        psth_legends_by_session_group_dict[cells_group_name][session_group_id] = dict()

                    if epoch_group_name not in psth_data_by_session_group_dict[cells_group_name][session_group_id]:
                        psth_data_by_session_group_dict[cells_group_name][session_group_id][epoch_group_name] = []
                        psth_rnd_data_by_session_group_dict[cells_group_name][session_group_id][epoch_group_name] = []
                        # number of subjects, number of sessions, number of cells, number of epochs
                        psth_legends_by_session_group_dict[cells_group_name][session_group_id][
                            epoch_group_name] = dict()
                        legends_dict = psth_legends_by_session_group_dict[cells_group_name][session_group_id][
                            epoch_group_name]
                        legends_dict["subjects"] = []
                        legends_dict["n_sessions"] = 0
                        legends_dict["n_cells"] = 0
                        legends_dict["n_epochs"] = 0

                    psth_data_by_session_group_dict[cells_group_name][session_group_id][epoch_group_name].append(
                        [psth_times, psth_values])
                    if with_surrogates:
                        psth_rnd_data_by_session_group_dict[cells_group_name][session_group_id][epoch_group_name].append(
                            [psth_times, surrogate_psth_values])

                    legends_dict = psth_legends_by_session_group_dict[cells_group_name][session_group_id][
                        epoch_group_name]
                    legends_dict["subjects"].append(session_data.subject_id)
                    legends_dict["n_sessions"] += 1
                    legends_dict["n_cells"] += len(cell_indices_in_group)
                    legends_dict["n_epochs"] += len(epochs_frames_in_group)

            self.update_progressbar(time_started=self.analysis_start_time, increment_value=100 / (n_sessions + 1))
        # first we determine the bins to use
        # using the lowest sampling_rate to get the biggest bins
        step_in_ms = 1000 / lowest_sampling_rate
        bins_edges = np.arange(-psth_range_in_ms, psth_range_in_ms + step_in_ms, step_in_ms)
        bins_edges[-1] = psth_range_in_ms
        # print(f"bins_edges {bins_edges}")
        # print(f"len(bins_edges) {len(bins_edges)}, len(psth_times) {len(psth_times)}")
        x_label = f"Duration ({x_axis_scale})"
        y_label = "Activity (%)"
        if work_on_traces:
            if traces_normalization == 'raw':
                y_label = "F"
            if traces_normalization == 'df/f':
                y_label = "DF/F"
            if traces_normalization == 'z-score':
                y_label = "F Z-score"

        # We want here to extract the surrogate values if with surrogate
        if with_surrogates:
            rnd_data_table_cells_session_dict_epoch = dict()
            for cells_group_name in psth_rnd_data_by_session_group_dict.keys():
                rnd_data_table_session_dict_epoch = dict()
                for session_group_id, epoch_dict in psth_rnd_data_by_session_group_dict[cells_group_name].items():
                    data_psth = []
                    threshold_values = [] if with_surrogates else None
                    colors_plot = []
                    label_legends = []
                    cells_groups_descr = ""
                    if cells_group_name != no_cell_type_groups_tag:
                        cells_groups_descr = f"_{cells_group_name}"
                    rnd_data_table_dict_epoch = dict()
                    for epoch_group_name, epoch_data_list in epoch_dict.items():
                        # epoch_data_list contains data for each session
                        time_x_values, psth_rnd_values_for_plot = \
                            prepare_psth_values(epoch_data_list, bins_edges, low_percentile_surrogate,
                                                high_percentile_surrogate, work_on_traces=work_on_traces)
                        psth_dict_to_save = {'Time': time_x_values,
                                             'rnd_Median_active_cells': psth_rnd_values_for_plot[0],
                                             f'rnd_Percentile_{low_percentile_surrogate}': psth_rnd_values_for_plot[1],
                                             f'rnd_Percentile_{high_percentile_surrogate}': psth_rnd_values_for_plot[2]}
                        rnd_psth_data_table_to_save = pd.DataFrame(psth_dict_to_save)
                        psth_data_to_save_name = f"rnd_psth_{session_group_id}_{epoch_group_name}_{cells_group_name}"
                        path_results = self.get_results_path()
                        path_psth_data_to_save = os.path.join(f'{path_results}', f'{psth_data_to_save_name}.xlsx')
                        rnd_psth_data_table_to_save.to_excel(path_psth_data_to_save)
                        rnd_data_table_dict_epoch[epoch_group_name] = rnd_psth_data_table_to_save
                    rnd_data_table_session_dict_epoch[session_group_id] = rnd_data_table_dict_epoch
                rnd_data_table_cells_session_dict_epoch[cells_group_name] = rnd_data_table_session_dict_epoch

        # now we plot the PSTH
        if verbose:
            print(f" ")
            print(f"------- Saving the results in '.xlsx' files / Plots all PSTHs -------")
        # we want to make a figure for each session group with all epoch types in it
        for cells_group_name in psth_data_by_session_group_dict.keys():
            for session_group_id, epoch_dict in psth_data_by_session_group_dict[cells_group_name].items():
                data_psth = []
                threshold_values = [] if with_surrogates else None
                colors_plot = []
                label_legends = []
                cells_groups_descr = ""
                if cells_group_name != no_cell_type_groups_tag:
                    cells_groups_descr = f"_{cells_group_name}"
                for epoch_group_name, epoch_data_list in epoch_dict.items():
                    # epoch_data_list contains data for each session
                    time_x_values, psth_values_for_plot = \
                        prepare_psth_values(epoch_data_list, bins_edges, low_percentile, high_percentile,
                                            work_on_traces=work_on_traces)
                    psth_dict_to_save = {'Time': time_x_values, 'Median_active_cells': psth_values_for_plot[0],
                                         f'Percentile_{low_percentile}': psth_values_for_plot[1],
                                         f'Percentile_{high_percentile}': psth_values_for_plot[2]}
                    psth_data_table_to_save = pd.DataFrame(psth_dict_to_save)
                    psth_data_to_save_name = f"psth_{session_group_id}_{epoch_group_name}_{cells_group_name}"
                    path_results = self.get_results_path()
                    path_psth_data_to_save = os.path.join(f'{path_results}', f'{psth_data_to_save_name}.xlsx')
                    psth_data_table_to_save.to_excel(path_psth_data_to_save)

                    if with_surrogates:
                        # get the data from rnd from this same cell/session/epochs
                        rnd_psth_data_table = \
                            rnd_data_table_cells_session_dict_epoch[cells_group_name][session_group_id][epoch_group_name]
                        rnd_psth_data_table = rnd_psth_data_table.drop(columns=['Time'])

                        # Make general table
                        general_data_table = pd.concat([psth_data_table_to_save, rnd_psth_data_table], axis=1)
                        full_psth_data_to_save_name = \
                            f"data_and_rnd_psth_{session_group_id}_{epoch_group_name}{cells_group_name}"
                        path_results = self.get_results_path()
                        full_path_psth_data_to_save = os.path.join(f'{path_results}',
                                                                   f'{full_psth_data_to_save_name}.xlsx')
                        general_data_table.to_excel(full_path_psth_data_to_save)

                    else:
                        general_data_table = psth_data_table_to_save

                    # # Plot from general table
                    if x_axis_scale == 'sec':
                        general_data_table['Time'] = general_data_table['Time'] / 1000
                    if x_axis_scale == 'min':
                        general_data_table['Time'] = general_data_table['Time'] / 6000

                    fig, ax = plt.subplots(
                        ncols=1,
                        nrows=1,
                        figsize=(width_fig, height_fig), dpi=dpi)

                    fig_title = f'PSTH_{session_group_id}{cells_group_name}{epoch_group_name}'
                    median_color = session_default_color
                    prctil_color = sns.desaturate(session_default_color, 0.65)
                    if with_surrogates:
                        median_surrogate_color = surrogate_color
                        prctile_surro_color = sns.desaturate(median_surrogate_color, 0.65)
                        colors = [median_color, prctil_color, prctil_color,
                                  median_surrogate_color, prctile_surro_color, prctile_surro_color]
                        column_names = ['Median_active_cells', f'Percentile_{low_percentile}',
                                        f'Percentile_{high_percentile}', 'rnd_Median_active_cells',
                                        f'rnd_Percentile_{low_percentile_surrogate}',
                                        f'rnd_Percentile_{high_percentile_surrogate}']
                    else:
                        colors = [median_color, prctil_color, prctil_color]
                        column_names = ['Median_active_cells', f'Percentile_{low_percentile}',
                                        f'Percentile_{high_percentile}']

                    general_data_table.plot(x="Time",
                                            y=column_names,
                                            kind='line', ax=ax, color=colors, linewidth=2,
                                            subplots=False, sharex=None,
                                            sharey=False, layout=None, figsize=(width_fig, height_fig),
                                            use_index=True, title=fig_title, grid=None,
                                            legend=False, style=None, logx=False,
                                            logy=False, loglog=False, xticks=None, yticks=None, xlim=None,
                                            ylim=None, rot=None, fontsize=None, colormap=None, table=False,
                                            yerr=None, xerr=None, secondary_y=False, sort_columns=False)
                    ax.set_title(fig_title, color=axes_label_color, fontsize=axis_label_size)
                    ax.set_ylabel(y_label, fontsize=axis_label_size, labelpad=20)
                    ax.set_xlabel(x_label, fontsize=axis_label_size, labelpad=20)
                    ax.set_facecolor(background_color)
                    fig.patch.set_facecolor(background_color)
                    ax.yaxis.label.set_color(axes_label_color)
                    ax.xaxis.label.set_color(axes_label_color)
                    ax.spines['left'].set_color(axes_border_color)
                    ax.spines['right'].set_color(background_color)
                    ax.spines['bottom'].set_color(axes_border_color)
                    ax.spines['top'].set_color(background_color)
                    ax.yaxis.set_tick_params(labelsize=axis_label_size)
                    ax.xaxis.set_tick_params(labelsize=axis_label_size)
                    ax.tick_params(axis='y', colors=color_ticks)
                    ax.tick_params(axis='x', colors=color_ticks)

                    fig.tight_layout()

                    file_name = fig_title
                    if isinstance(save_formats, str):
                        save_formats = [save_formats]
                    for save_format in save_formats:
                        fig.savefig(f'{path_results}/{file_name}.{save_format}',
                                    format=f"{save_format}",
                                    facecolor=fig.get_facecolor())
                    plt.close()

                    if x_axis_scale == "sec":
                        time_x_values = [t / 1000 for t in time_x_values]

                    elif x_axis_scale == "min":
                        time_x_values = [t / 60000 for t in time_x_values]

                    data_psth.append([time_x_values, psth_values_for_plot])
                    colors_plot.append(epochs_color_dict[epoch_group_name])

                    if with_surrogates:
                        surrogate_max_values = \
                        psth_surrogates_by_session_group_dict[cells_group_name][session_group_id][
                            epoch_group_name]
                        # print(f"np.percentile(surrogate_max_values, surrogate_percentile) {np.percentile(surrogate_max_values, surrogate_percentile)}")
                        # put them in percentage
                        threshold_values.append(np.percentile(surrogate_max_values, high_percentile_surrogate) * 100)

                    legends_dict = psth_legends_by_session_group_dict[cells_group_name][session_group_id][
                        epoch_group_name]

                    n_subjects = len(set(legends_dict["subjects"]))
                    n_sessions = legends_dict["n_sessions"]
                    n_cells = legends_dict["n_cells"]
                    n_epochs = legends_dict["n_epochs"]
                    label_legends.append(f"{n_epochs} {epoch_group_name}" + "\n" +
                                         f"N={n_subjects}, n={n_sessions}" + "\n" + f"{n_cells} cells")

                plot_several_psth(results_path=self.get_results_path(),
                                  data_psth=data_psth,
                                  colors_plot=colors_plot,
                                  file_name=f"psth_{session_group_id}{cells_groups_descr}",
                                  label_legends=label_legends,
                                  x_label=x_label, y_label=y_label,
                                  color_ticks=color_ticks,
                                  top_border_visible=top_border_visible,
                                  right_border_visible=right_border_visible,
                                  bottom_border_visible=bottom_border_visible,
                                  left_border_visible=left_border_visible,
                                  axes_border_color=axes_border_color,
                                  axes_label_color=axes_label_color,
                                  threshold_line_y_values=None,
                                  with_same_y_scale=plots_with_same_y_scale,
                                  color_v_line=color_v_line, line_width=color_v_line_width,
                                  line_mode=True, background_color=background_color,
                                  figsize=(30, 20),
                                  ticks_labels_size=ticks_labels_size,
                                  axis_label_size=axis_label_size,
                                  axis_label_pad=axis_label_pad,
                                  legend_police_size=legend_police_size,
                                  ticks_length=ticks_length,
                                  ticks_width=ticks_width,
                                  save_formats=save_formats,
                                  summary_plot=True)

        # we want to make a figure for each epoch types and cell_type with all the session group
        for epoch_group_name, session_dict in psth_data_by_epoch_dict.items():
            session_index = 0
            n_sessions = len(session_dict)
            for cells_group_name in session_dict.keys():
                data_psth = []
                # same length as data_psth, display an horizontal line representing a statistical threshold
                threshold_values = [] if with_surrogates else None
                colors_plot = []
                label_legends = []
                cells_groups_descr = ""
                if cells_group_name != no_cell_type_groups_tag:
                    cells_groups_descr = f"_{cells_group_name}"

                for session_group_id, session_data_list in session_dict[cells_group_name].items():
                    time_x_values, psth_values_for_plot = \
                        prepare_psth_values(session_data_list, bins_edges, low_percentile, high_percentile,
                                            work_on_traces=work_on_traces)

                    if x_axis_scale == "sec":
                        time_x_values = [t / 1000 for t in time_x_values]

                    elif x_axis_scale == "min":
                        time_x_values = [t / 60000 for t in time_x_values]

                    data_psth.append([time_x_values, psth_values_for_plot])
                    # "default_color", "brewer", "spectral"
                    if session_group_id in session_group_color_dict:
                        colors_plot.append(session_group_color_dict[session_group_id])
                    elif session_color_choice == "brewer":
                        colors_plot.append(BREWER_COLORS[session_index % len(BREWER_COLORS)])
                    elif session_color_choice == "spectral":
                        colors_plot.append(cm.nipy_spectral(float(session_index + 1) / (n_sessions + 1)))
                    else:
                        colors_plot.append(session_default_color)

                    legends_dict = psth_legends_by_epoch_dict[epoch_group_name][cells_group_name][session_group_id]

                    if with_surrogates:
                        surrogate_max_values = psth_surrogates_by_epoch_dict[epoch_group_name][cells_group_name][
                            session_group_id]
                        # print(f"np.percentile(surrogate_max_values, surrogate_percentile) {np.percentile(surrogate_max_values, surrogate_percentile)}")
                        # put them in percentage
                        threshold_values.append(np.percentile(surrogate_max_values, high_percentile_surrogate) * 100)

                    n_subjects = len(set(legends_dict["subjects"]))
                    n_sessions = legends_dict["n_sessions"]
                    n_cells = legends_dict["n_cells"]
                    n_epochs = legends_dict["n_epochs"]
                    label_legends.append(f"{session_group_id}" + "\n" +
                                         f"{n_epochs} {epoch_group_name}" + "\n" +
                                         f"N={n_subjects}, n={n_sessions}" + "\n" + f"{n_cells} cells")
                    session_index += 1
                plot_several_psth(results_path=self.get_results_path(),
                                  data_psth=data_psth,
                                  colors_plot=colors_plot,
                                  file_name=f"psth_{epoch_group_name}{cells_groups_descr}",
                                  label_legends=label_legends,
                                  x_label=x_label, y_label=y_label,
                                  color_ticks=color_ticks,
                                  top_border_visible=top_border_visible,
                                  right_border_visible=right_border_visible,
                                  bottom_border_visible=bottom_border_visible,
                                  left_border_visible=left_border_visible,
                                  axes_border_color=axes_border_color,
                                  axes_label_color=axes_label_color,
                                  color_v_line=color_v_line, line_width=color_v_line_width,
                                  line_mode=True, background_color=background_color,
                                  threshold_line_y_values=None,
                                  with_same_y_scale=plots_with_same_y_scale,
                                  figsize=(30, 20),
                                  ticks_labels_size=ticks_labels_size,
                                  axis_label_size=axis_label_size,
                                  axis_label_pad=axis_label_pad,
                                  legend_police_size=legend_police_size,
                                  save_formats=save_formats,
                                  summary_plot=True)

        # we want a figure for each epoch session group and each epoch
        if one_fig_by_group_and_epoch:
            for epoch_group_name, session_dict in psth_data_by_epoch_dict.items():
                session_index = 0
                n_sessions = len(session_dict)
                for cells_group_name in session_dict.keys():
                    cells_groups_descr = ""
                    if cells_group_name != no_cell_type_groups_tag:
                        cells_groups_descr = f"_{cells_group_name}"
                    for session_group_id, session_data_list in session_dict[cells_group_name].items():
                        time_x_values, psth_values_for_plot = \
                            prepare_psth_values(session_data_list, bins_edges, low_percentile, high_percentile,
                                                work_on_traces=work_on_traces)
                        if session_color_choice == "brewer":
                            color_plot = BREWER_COLORS[session_index % len(BREWER_COLORS)]
                        elif session_color_choice == "spectral":
                            color_plot = cm.nipy_spectral(float(session_index + 1) / (n_sessions + 1))
                        else:
                            color_plot = session_default_color

                        legends_dict = psth_legends_by_epoch_dict[epoch_group_name][cells_group_name][session_group_id]

                        n_subjects = len(set(legends_dict["subjects"]))
                        n_sessions = legends_dict["n_sessions"]
                        n_cells = legends_dict["n_cells"]
                        n_epochs = legends_dict["n_epochs"]
                        label_legends.append(f"{session_group_id}" + "\n" +
                                             f"{n_epochs} {epoch_group_name}" + "\n" +
                                             f"N={n_subjects}, n={n_sessions}" + "\n" + f"{n_cells} cells")
                        session_index += 1
                        plot_one_psth(results_path=self.get_results_path(),
                                      time_x_values=time_x_values, psth_values=psth_values_for_plot,
                                      color_plot=color_plot,
                                      x_label=x_label, y_label=y_label,
                                      color_ticks=color_ticks,
                                      top_border_visible=top_border_visible,
                                      right_border_visible=right_border_visible,
                                      bottom_border_visible=bottom_border_visible,
                                      left_border_visible=left_border_visible,
                                      axes_border_color=axes_border_color,
                                      axes_label_color=axes_label_color,
                                      color_v_line=color_v_line, label_legend=None, line_width=color_v_line_width,
                                      line_mode=True, background_color=background_color, ax_to_use=None,
                                      figsize=(15, 10),
                                      ticks_labels_size=ticks_labels_size,
                                      axis_label_size=axis_label_size,
                                      axis_label_pad=axis_label_pad,
                                      legend_police_size=legend_police_size,
                                      file_name=f"psth_{epoch_group_name}_{session_group_id}{cells_groups_descr}",
                                      save_formats=save_formats,
                                      put_mean_line_on_plt=False)

        self.update_progressbar(time_started=self.analysis_start_time, increment_value=100 / (n_sessions + 1))
        print(f" ")
        print(f"PSTH analysis DONE -  in {time() - self.analysis_start_time} sec")


def prepare_psth_values(session_data_list, bins_edges, low_percentile, high_percentile, work_on_traces=False):
    if len(session_data_list) == 1:
        session_data = session_data_list[0]
        psth_times, psth_values = session_data
        median_psth_values = fill_bins(bin_edges=bins_edges, data=psth_values[0],
                                       data_time_points=psth_times)

        low_threshold_psth_values = fill_bins(bin_edges=bins_edges, data=psth_values[1],
                                              data_time_points=psth_times)
        high_threshold_psth_values = fill_bins(bin_edges=bins_edges, data=psth_values[2],
                                               data_time_points=psth_times)
    else:
        psth_matrix = np.zeros((0, len(bins_edges) - 1))
        for session_data in session_data_list:
            psth_times, psth_values = session_data
            # print(f"psth_times {psth_times}")
            psth_values_norm = fill_bins(bin_edges=bins_edges, data=psth_values[0],
                                         data_time_points=psth_times)
            psth_values_norm = np.reshape(psth_values_norm, (1, len(psth_values_norm)))
            psth_matrix = np.concatenate((psth_matrix, psth_values_norm))
        median_psth_values = np.nanmedian(psth_matrix, axis=0)
        low_threshold_psth_values = np.nanpercentile(psth_matrix, low_percentile, axis=0)
        high_threshold_psth_values = np.nanpercentile(psth_matrix, high_percentile, axis=0)

    if work_on_traces is False:
        psth_values_for_plot = [median_psth_values * 100, low_threshold_psth_values * 100,
                                high_threshold_psth_values * 100]
    if work_on_traces is True:
        psth_values_for_plot = [median_psth_values, low_threshold_psth_values,
                                high_threshold_psth_values]

    time_x_values = [(t + bins_edges[i + 1]) / 2 for i, t in enumerate(bins_edges[:-1])]

    return time_x_values, psth_values_for_plot


def fill_bins(bin_edges, data, data_time_points):
    """
    Create an array based on bin_edges. If two values are on the same edge, then we put the mean
    Args:
        bin_edges: 1d array representing the edges of the bins
        data: 1d array representing the value to fill in the bins
        data_time_points: time indices of the data values in order to fit them in the good bin

    Returns: a 1d array of length len(bin_edges) -1

    """
    result = np.zeros(len(bin_edges) - 1)

    for value_index, data_value in enumerate(data):
        time_point = data_time_points[value_index]
        # now we want to know in which bin to insert it
        index = bisect_right(bin_edges, time_point) - 1
        if index >= len(result):
            index = len(result) - 1
        # TODO: plan the case when more than 2 values could be on the same bin
        if result[index] > 0:
            # should not happen often
            result[index] = np.mean((result[index], data_value))
        else:
            result[index] = data_value

    return result


def alpha_numeric_comparator(data):
    """
    take a string and return the int that it represents
    :param data: (str)
    :return:
    """
    if len(data) == 0:
        return 99999

    if len(data) == 1 and data[0].isnumeric():
        return int(data[0])
    if len(data) > 1 and data[:2].isnumeric():
        return int(data[:2])
    if data[0].lower() == "p":
        if len(data) == 2 and data[1].isnumeric():
            return int(data[1])
        if len(data) > 2 and data[2] == "-" and data[1].isnumeric():
            return int(data[1])
        if len(data) > 3 and data[3] == "-" and data[1:3].isnumeric():
            return int(data[1:3])
        if len(data) == 3 and data[1:3].isnumeric():
            return int(data[1:3])
    return 99999
