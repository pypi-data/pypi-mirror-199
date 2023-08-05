from cicada.analysis.cicada_analysis import CicadaAnalysis
from cicada.utils.misc import split_string
# from time import time
from threading import Thread
from qtpy.QtCore import QThread
from qtpy import QtCore
import sys
import time

def except_hook(cls, exception, traceback):
    """Redirect exception to std.err so we can display stack trace on exceptions"""
    sys.__excepthook__(cls, exception, traceback)


class EmittingErrStream(QtCore.QObject):
    """Class managing the std.err redirection"""

    def __init__(self, parent=None):
        self.parent = parent
        self.terminal = sys.stderr
        self.errWritten = QtCore.Signal(str)

    def write(self, text):
        """
        Override of the write function used to display output
        Args:
            text (str): Python output from stdout

        """

        # Add thread name to the output when writting in the the widget
        # current_thread = QThread.currentThread()
        # thread_text = text + str(current_thread.name)
        self.terminal.write(str(text))
        # dir_path = current_thread.cicada_analysis.get_results_path()
        # self.parent.errOutputWritten(thread_text, dir_path)

    def flush(self):
        pass

class EmittingStream(QtCore.QObject):
    """Class managing the std.out redirection"""

    def __init__(self, parent=None):
        self.parent = parent
        self.terminal = sys.stdout
        self.textWritten = QtCore.Signal(str)

    def write(self, text):
        """
        Override of the write function used to display output
        Args:
            text (str): Python output from stdout

        """
        # Add thread name to the output when writting in the the widget
        # current_thread = QThread.currentThread()
        # thread_text = text + str(current_thread.name)
        self.terminal.write(str(text))
        # dir_path = current_thread.cicada_analysis.get_results_path()
        # self.parent.normalOutputWritten(thread_text, dir_path)

    def flush(self):
        pass


class CitnpsWorker(QtCore.QThread):
    """Thread to manage multiple analysises at the same time"""

    # Signals to update the progress bar in the analysis window and overview
    updateProgress = QtCore.Signal(float, float, float)
    updateProgress2 = QtCore.Signal(str, float, float)

    def __init__(self, name, analysis_fct, parent):
        """

        Args:
            name (str): Analysis ID, should be unique
            analysis_fct (function): the analysis run in the thread
        """
        QtCore.QThread.__init__(self)
        self.name = name
        self.crashed = False
        self.parent = parent
        self.run_state = False
        self.analysis_fct = analysis_fct

    def run(self):
        """Run the analysis"""
        self.run_state = True
        sys.stdout = EmittingStream(self.parent)
        sys.excepthook = except_hook
        # Comment to debug, else we will get unhandled python exception
        # sys.stderr = EmittingErrStream(self.parent)
        print("RUN BABY RUN")
        self.analysis_fct()
        # self.setProgress(self.name, new_set_value=100)
        self.run_state = False

    def setProgress(self, name, time_elapsed=0, increment_value=0, new_set_value=0):
        """
        Emit the new value of the progress bar and time remaining

        Args:
            name (str): Analysis ID
            time_elapsed (float): Start elpased (in sec)
            increment_value (float): Value that should be added to the current value of the progress bar
            new_set_value (float):  Value that should be set as the current value of the progress bar


        """
        self.updateProgress.emit(time_elapsed, increment_value, new_set_value)
        self.updateProgress2.emit(name, increment_value, new_set_value)


class CicadaCitnpsAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        A list of
        :param data_to_analyse: list of data_structure
        :param family_id: family_id indicated to which family of analysis this class belongs. If None, then
        the analysis is a family in its own.
        :param data_format: indicate the type of data structure. for NWB, NIX
        """
        CicadaAnalysis.__init__(self, name="CITNPS", family_id="Behavior pre-processing",
                                short_description="Use CITNPS to extract bodyparts' movements",
                                config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

        self.session_identifier = None
        self.citnps_movies_dict = dict()
        self.movie_queue_size = 2000
        self.bodyparts_dict = dict()

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaCitnpsAnalysis(config_handler=self.config_handler)
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

        if len(self._data_to_analyse) > 1:
            self.invalid_data_help = f"Analysis for one session only, {len(self._data_to_analyse)} were given"
            return False

        try:
            from citnps.citnps_main_window import run_citnps
        except ImportError:
            self.invalid_data_help = "citnps package not installed"
            return False

        for data_to_analyse in self._data_to_analyse:
            behavior_movies = data_to_analyse.get_behavior_movies()
            if len(behavior_movies) == 0:
                self.invalid_data_help = f"No behavior movies in " \
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

        behavior_movies_dict = self._data_to_analyse[0].get_behavior_movies()

        for behavior_movie_key in behavior_movies_dict.keys():
            self.add_field_text_option_for_gui(arg_name=behavior_movie_key + "_id", default_value="",
                                          short_description=f"ID for {behavior_movie_key}",
                                          long_description=None, family_widget="behavior_movie")

        self.add_int_values_arg_for_gui(arg_name="movie_queue_size", min_value=100, max_value=5000,
                                        short_description="Queue size for loading movie's frames",
                                        default_value=2000, family_widget="behavior_movie")

        self.add_choices_for_groups_for_gui(arg_name="bodyparts_by_movie", choices=[],
                                            with_color=False,
                                            mandatory=False,
                                            add_custom_group_field=True,
                                            custom_group_processor_fct=split_string,
                                            short_description="Bodyparts to analyse for each movie",
                                            long_description="Indicate which bodypart to analyse, the group names should "
                                                             "correspond to the movie names, each bodypart should be "
                                                             "separate by a blank space",
                                            family_widget="bodyparts")

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

        # ------- figures config part -------
        save_formats = kwargs["save_formats"]
        if save_formats is None:
            save_formats = "pdf"

        dpi = kwargs.get("dpi", 100)

        width_fig = kwargs.get("width_fig")

        height_fig = kwargs.get("height_fig")

        with_timestamps_in_file_name = kwargs.get("with_timestamp_in_file_name", True)

        self.movie_queue_size = kwargs.get("movie_queue_size")

        bodyparts_by_movie = kwargs.get("bodyparts_by_movie")
        if (bodyparts_by_movie is None) or len(bodyparts_by_movie) == 0:
            print(f"No bodyparts selected, no analysis")
            self.update_progressbar(time_started=self.analysis_start_time, increment_value=100)
            return

        self.bodyparts_dict = dict()
        for movie_id, bodyparts in bodyparts_by_movie.items():
            # the second element is a color or None
            self.bodyparts_dict[movie_id] = bodyparts[0]
        print(f"bodyparts_dict {self.bodyparts_dict}")

        session_data = self._data_to_analyse[0]
        n_sessions = len(self._data_to_analyse)

        self.session_identifier = session_data.identifier

        behavior_movies_dict = self._data_to_analyse[0].get_behavior_movies()
        self.citnps_movies_dict = dict()
        # getting the movie ids and the movie file
        for behavior_movie_key, movie_file in behavior_movies_dict.items():
            movie_id = kwargs.get(behavior_movie_key + "_id")
            self.citnps_movies_dict[movie_id] = movie_file

        # t = Thread(target=self.start_citnps, args=())
        # t.daemon = True
        # t.start()
        # self.start_citnps()
        # thread = QThread.create(self.start_citnps)
        worker = CitnpsWorker(name="toto", analysis_fct=self.start_citnps, parent=self)
        worker.start()
        i = 0
        while True:
            time.sleep(5.0)
            i += 1
            if i > 1000:
                break

        self.update_progressbar(time_started=self.analysis_start_time, increment_value=100) # / (n_sessions+1))

        print(f"CITNPS analysis run in {time.time() - self.analysis_start_time} sec")

    def start_citnps(self):
        from citnps.citnps_main_window import run_citnps
        print("start_citnps")
        run_citnps(movies_dict=self.citnps_movies_dict, from_cicada=True, data_id=self.session_identifier,
                   movie_queue_size=self.movie_queue_size, bodyparts_dict=self.bodyparts_dict)