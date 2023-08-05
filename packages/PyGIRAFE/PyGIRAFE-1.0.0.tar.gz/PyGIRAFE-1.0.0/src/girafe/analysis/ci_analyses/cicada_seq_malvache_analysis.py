from cicada.analysis.cicada_analysis import CicadaAnalysis
from time import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import os
import scipy.stats as scistats
from scipy.ndimage import gaussian_filter1d
from cicada.utils.sequences.malvache.utils import step1_pca, covnorm, normalize_array_0_255
from cicada.utils.signal import gaussblur1D, norm01, gauss_blur
from cicada.utils.display.rasters import plot_with_imshow
from cicada.utils.misc import fill_gaps_in_continuous_periods, get_continous_time_periods, print_info_dict


class CicadaSeqMalvacheAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        CicadaAnalysis.__init__(self, name="Malvache's sequences detection", family_id="Sequences detection",
                                short_description="Villette et al. 2015", config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaSeqMalvacheAnalysis(config_handler=self.config_handler)
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
                self.invalid_data_help = f"No Roi Response Series available in " \
                    f"{data_to_analyse.identifier}"
                return False

        return True

    def set_arguments_for_gui(self):
        """

        Returns:

        """
        CicadaAnalysis.set_arguments_for_gui(self)

        self.add_roi_response_series_arg_for_gui(short_description="Neuronal activity to use: Select raw calcium traces",
                                                 long_description=None)

        self.add_int_values_arg_for_gui(arg_name="np_pc_max", min_value=1, max_value=15,
                                        short_description="Number of PC to try",
                                        default_value=10, long_description=None, family_widget="PCA")

        self.add_bool_option_for_gui(arg_name="split_data_for_pca", true_by_default=False,
                                     short_description="Split data set to 'train' PCA on part of the data",
                                     family_widget="PCA")

        self.add_int_values_arg_for_gui(arg_name="training_prctage", min_value=50, max_value=100,
                                        short_description="Percentage of run epochs in PCA training data set",
                                        default_value=75,
                                        long_description="If 'Speed' is not available this percentage will "
                                                         "directly be applied to the number of CI frames",
                                        family_widget="PCA")

        self.add_int_values_arg_for_gui(arg_name="speed_threshold", min_value=1, max_value=10,
                                        short_description="Threshold on speed to detect run epochs",
                                        default_value=1, long_description=None, family_widget="Speed")

        self.add_bool_option_for_gui(arg_name="merge_run_epochs", true_by_default=True,
                                     short_description="Merge close run epochs",
                                     family_widget="Speed")

        self.add_int_values_arg_for_gui(arg_name="max_run_pause", min_value=1, max_value=50,
                                        short_description="Maximal duration of pause between run epochs to merge (in CI frames)",
                                        default_value=4, long_description=None, family_widget="Speed")

        self.add_int_values_arg_for_gui(arg_name="minimal_run_duration", min_value=1, max_value=10,
                                        short_description="Minimal run duration to look for order (s)",
                                        default_value=2, long_description=None, family_widget="Speed")

        self.add_bool_option_for_gui(arg_name="save_position_speed_plots", true_by_default=True,
                                     short_description="Save plot of Speed and Position",
                                     family_widget="figure_plot1")

        self.add_int_values_arg_for_gui(arg_name="n_subplots", min_value=1, max_value=10,
                                        short_description="Number of subplots",
                                        default_value=4, long_description=None, family_widget="figure_plot")

        display_choices = ["speed", "binary speed", "position"]
        self.add_choices_arg_for_gui(arg_name="display", choices=display_choices,
                                     default_value="speed",
                                     short_description="Display speed, binary speed or position below sequences heatmap",
                                     multiple_choices=False,
                                     family_widget="figure_plot")

        self.add_color_arg_for_gui(arg_name="background_color", default_value=(0, 0, 0, 1.),
                                   short_description="Background color",
                                   long_description=None, family_widget="figure_colors")

        sequences_maps = ["hot", "jet", "afmhot", "gist_heat"]
        self.add_choices_arg_for_gui(arg_name="sequences_cmap", choices=sequences_maps,
                                     default_value="hot", short_description="Sequences color map",
                                     multiple_choices=False,
                                     family_widget="figure_colors")

        self.add_color_arg_for_gui(arg_name="speed_line_color", default_value=(1, 1, 0, 1.),
                                   short_description="Speed or Position color",
                                   long_description=None, family_widget="figure_colors")

        self.add_bool_option_for_gui(arg_name="show_yaxis_titles", true_by_default=True,
                                     short_description="Show y axis titles",
                                     family_widget="figure_label")

        self.add_bool_option_for_gui(arg_name="hide_x_label", true_by_default=True,
                                     short_description="Hide x-axis label",
                                     family_widget="figure_label")

        self.add_bool_option_for_gui(arg_name="hide_cell_idx", true_by_default=True,
                                     short_description="Hide cell index label",
                                     family_widget="figure_label")

        self.add_bool_option_for_gui(arg_name="hide_speed_y_values", true_by_default=False,
                                     short_description="Hide y-axis speed values",
                                     family_widget="figure_label")

        self.add_int_values_arg_for_gui(arg_name="axis_labels_size", min_value=0.1, max_value=20,
                                        short_description="Axis label size",
                                        default_value=5, long_description=None, family_widget="figure_label")

        self.add_int_values_arg_for_gui(arg_name="ticks_label_size", min_value=0.1, max_value=20,
                                        short_description="axis ticks label size",
                                        default_value=2, long_description=None, family_widget="figure_label")

        self.add_color_arg_for_gui(arg_name="ticks_label_color", default_value=(1, 1, 0.5, 1.),
                                   short_description="Labels color",
                                   long_description=None, family_widget="figure_label")

        self.add_bool_option_for_gui(arg_name="without_ticks", true_by_default=True,
                                     short_description="Remove ticks on plot",
                                     family_widget="figure_axis")

        self.add_color_arg_for_gui(arg_name="axis_color", default_value=(1, 1, 0.5, 1.),
                                   short_description="Axis color",
                                   long_description=None, family_widget="figure_axis")

        self.add_image_format_package_for_gui()

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
          segmentation

        :return:
        """
        CicadaAnalysis.run_analysis(self, **kwargs)

        verbose = kwargs.get("verbose", True)

        roi_response_series_dict = kwargs["roi_response_series"]

        np_pc_max = kwargs.get("np_pc_max")

        split_data_for_pca = kwargs.get("split_data_for_pca")

        training_prctage = kwargs.get("training_prctage")

        speed_threshold = kwargs.get("speed_threshold")

        merge_run_epochs = kwargs.get("merge_run_epochs")

        max_run_pause = kwargs.get("max_run_pause")

        minimal_run_duration = kwargs.get("minimal_run_duration")

        n_subplots = kwargs.get("n_subplots", 4)

        bckground_color = kwargs.get("background_color")

        sequences_cmap = kwargs.get("sequences_cmap")

        display = kwargs.get("display")

        speed_color = kwargs.get("speed_line_color")

        with_yaxis_title = kwargs.get("show_yaxis_titles")

        without_ticks = kwargs.get("without_ticks")

        hide_x_label = kwargs.get("hide_x_label")

        hide_cell_idx = kwargs.get("hide_cell_idx")

        hide_speed_y_values = kwargs.get("hide_speed_y_values")

        axis_labels_size = kwargs.get("axis_labels_size")

        ticks_label_size = kwargs.get("ticks_label_size")

        ticks_label_color = kwargs.get("ticks_label_color")

        axis_color = kwargs.get("axis_color")

        save_position_speed_plots = kwargs.get("save_position_speed_plots")

        # image package format
        save_formats = kwargs["save_formats"]
        if save_formats is None:
            save_formats = "pdf"

        start_time = time()
        print("Malvache sequences detection: coming soon...")
        n_sessions = len(self._data_to_analyse)
        print(f"{n_sessions} sessions to analyse")

        correlation_general_table = pd.DataFrame()
        for session_index, session_data in enumerate(self._data_to_analyse):
            # Get Session Info
            info_dict = session_data.get_sessions_info()
            session_identifier = info_dict['identifier']
            # TODO: understand memory load
            if verbose:
                print(f" ")
                print(f"------------------ ONGOING SESSION: {session_identifier} -------------------- ")
                print(f"----------------------------- SESSION INFO ---------------------------------- ")
                print_info_dict(info_dict)
                print(f" ")

            # Get Data
            if isinstance(roi_response_series_dict, dict):
                roi_response_serie_info = roi_response_series_dict[session_identifier]
            else:
                roi_response_serie_info = roi_response_series_dict

            if verbose:
                print(f"Selected ROI response serie: {roi_response_serie_info[2]}")
            # Get the data assuming raw traces were selected
            neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)
            if verbose:
                print(f"N cells: {neuronal_data.shape[0]}, N frames: {neuronal_data.shape[1]}")
            neuronal_data_timestamps = session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_info)
            traces = neuronal_data
            n_cells, n_times = traces.shape

            # Get mouse speed by frame: extract speed by frame, is_running, and n run epochs
            if verbose:
                print(f" ")
                print(f"Getting mouse speed at each CI frames")
            speed = session_data.get_mouse_speed_info()

            if speed is not None:
                if len(speed) > n_times:
                    if verbose:
                        print(f"Last {len(speed) - n_times} imaging frames were cut, speed was cut as well")
                    speed = speed[0: n_times, ]
                is_running = np.zeros(len(speed), dtype=bool)
                speed = np.reshape(speed, (n_times, 1))
                if save_position_speed_plots:
                    if verbose:
                        print(f"Plot speed at each frame")
                    # TODO: just add a plot of position by frames and make it on demand
                    fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                            gridspec_kw={'height_ratios': [1]},
                                            figsize=(20, 20), dpi=300)
                    ax1.set_facecolor('white')
                    fig.patch.set_facecolor('white')
                    ax1.plot(speed, lw=2, color='black')
                    ax1.spines['left'].set_color('black')
                    ax1.spines['right'].set_color('white')
                    ax1.spines['bottom'].set_color('black')
                    ax1.spines['top'].set_color('white')
                    ax1.set_ylabel('Speed (cm/s)', fontsize=23)
                    ax1.set_xlabel('Time (Imaging frame)', fontsize=23)
                    ax1.yaxis.set_tick_params(labelsize=18)
                    ax1.xaxis.set_tick_params(labelsize=18)
                    fig.tight_layout()
                    fig.savefig(os.path.join(self.get_results_path(), f'{session_identifier}_Speed.pdf'))
                    plt.close('all')

                is_running[np.where(speed >= speed_threshold)[0]] = True
                n_run_epochs_before_merge = len(get_continous_time_periods(is_running))
                if verbose:
                    print(f" ")
                    print(f"{n_run_epochs_before_merge} run epochs detected")
                if merge_run_epochs:
                    if verbose:
                        print(f"Merge run epochs if separated by less than {max_run_pause} imaging frames")
                    merged_is_running = fill_gaps_in_continuous_periods(boolean_serie=is_running,
                                                                        max_gap_size=max_run_pause)
                    n_run_epochs_after_merge = len(get_continous_time_periods(merged_is_running))
                    if verbose:
                        print(f"{n_run_epochs_after_merge} run epochs after merging")
                    binary_runs = 1 * merged_is_running
                    n_run_epochs = n_run_epochs_after_merge
                else:
                    binary_runs = 1 * is_running
                    n_run_epochs = n_run_epochs_before_merge
            else:
                is_running = np.zeros(n_times, dtype=bool)
                binary_runs = 1 * is_running
                n_run_epochs = 0

            # Get mouse position by frame
            if verbose:
                print(f" ")
                print(f"Getting mouse position at each CI frames")
            position = session_data.get_mouse_position_info()
            if position is not None:
                if len(position) > n_times:
                    if verbose:
                        print(f"Last {len(position) - n_times} imaging frames were cut, position was cut as well")
                    position = position[0: n_times, ]
                position = np.reshape(position, (n_times, 1))
                if save_position_speed_plots:
                    # TODO: just add a plot of position by frames and make it on demand
                    if verbose:
                        print(f"Plot position at each frame")
                    fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                            gridspec_kw={'height_ratios': [1]},
                                            figsize=(20, 20), dpi=300)
                    ax1.set_facecolor('white')
                    fig.patch.set_facecolor('white')
                    ax1.plot(position, lw=2, color='black')
                    ax1.spines['left'].set_color('black')
                    ax1.spines['right'].set_color('white')
                    ax1.spines['bottom'].set_color('black')
                    ax1.spines['top'].set_color('white')
                    ax1.set_ylabel('Distance (cm)', fontsize=23)
                    ax1.set_xlabel('Time (Imaging frame)', fontsize=23)
                    ax1.yaxis.set_tick_params(labelsize=18)
                    ax1.xaxis.set_tick_params(labelsize=18)
                    fig.tight_layout()
                    fig.savefig(os.path.join(self.get_results_path(), f'{session_identifier}_Position.pdf'))
                    plt.close('all')

            # Split data set for 'training' and 'testing' PCA
            if split_data_for_pca:
                if verbose:
                    print(f" ")
                    print(f"Splitting data set before PCA")
                if speed is not None:
                    if verbose:
                        print(f"Split base on the number of run epochs")
                    n_run_epochs_training = int(n_run_epochs * (training_prctage / 100))
                    run_epoch_start_stop = get_continous_time_periods(binary_runs)
                    last_training_run_frame = run_epoch_start_stop[n_run_epochs_training - 1][1]
                    first_testing_run_frame = run_epoch_start_stop[n_run_epochs_training][0]
                    spliting_frame = int(np.median([last_training_run_frame, first_testing_run_frame]))
                    traces_in_pca = traces[:, 0:spliting_frame]
                    traces_for_test = traces[:, spliting_frame:]
                    if verbose:
                        print(f"Data for PCA 'training': {traces_in_pca.shape[0]} cells, {traces_in_pca.shape[1]} frames, "
                              f"{n_run_epochs_training} run epochs")
                else:
                    if verbose:
                        print(f"Split base on the number of frames")
                    traces_in_pca = traces[:, 0:int(n_times * (training_prctage / 100))]
                    if verbose:
                        print(f"Data for PCA: {traces_in_pca.shape[0]} cells, {traces_in_pca.shape[1]} frames")
            else:
                traces_in_pca = traces
                n_run_epochs_training = n_run_epochs
                spliting_frame = int(n_times)

            # Get CI movie sampling rate
            if verbose:
                print(f" ")
            sampling_rate_hz = session_data.get_ci_movie_sampling_rate(only_2_photons=True)
            if sampling_rate_hz is None:
                sampling_rate_hz = session_data.get_rrs_sampling_rate(keys=roi_response_serie_info)

            # ------------------------------------------------------------------------------------------------------ #
            # ----------------------- DO PCA ON DATA SET (FULL DATA OR TRAINING DATA IF SPLIT) --------------------- #
            # ------------------------------------------------------------------------------------------------------ #
            # Apply Gauss blur on raw traces do PCA on traces (full data set or part of it)
            arnaud_version = True
            # TODO: find out about why we divide by 20 to adjust to general cases with different rates
            if arnaud_version:
                traces_gauss = gaussblur1D(traces_in_pca, traces_in_pca.shape[1] / 20, 1)
                _, pc_time_course = step1_pca(traces_gauss, np_pc_max)

            sorted_cells_all = []
            sorted_indices_all = []
            dc_all = []
            shift_dc_all = []
            n_dc_all = []
            if verbose:
                print(f" ")
                print(f"Run PCA on 'PCA' data set")
                print(f"PC time course: {pc_time_course.shape[0]} PCs, {pc_time_course.shape[1]} frames")
            # TODO : find the meaning of dt and replace it by something like 20 * sampling_rate
            dt = 200
            for pc_number in np.arange(np_pc_max):
                if verbose:
                    print(f"Find sequences with PCA for PC # {pc_number}: Ongoing")
                sig_ref = np.diff(pc_time_course[pc_number, :])
                # calculate shifted trace
                cor_1d = np.zeros(n_cells)
                shift_1d = np.zeros(n_cells)
                for i in np.arange(n_cells):
                    tmp = covnorm(traces_in_pca[i, :], np.real(sig_ref), dt)
                    cor_1d[i] = np.max(tmp)
                    shift_1d[i] = np.where(tmp == cor_1d[i])[0][0] - dt - 1
                    # shift_1d[i] = np.where(tmp == cor_1d[i])[0] - dt - 1
                # Find the cells ('dc' for distance cells) that correlates well with pc time course
                img_cor_1d = normalize_array_0_255(cor_1d)
                ret2, th2 = cv2.threshold(img_cor_1d, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                dc = np.where(img_cor_1d > ret2)[0]
                dc_all.append(dc)
                # count 'dc' cells and pick them from traces matrix (take all frames)
                n_dc = len(dc)
                n_dc_all.append(n_dc)
                traces_dc = traces[dc, :]
                # Normalize raw traces before display in figure
                for i in np.arange(n_dc):
                    traces_gauss = gaussian_filter1d(traces_dc[i, :], 2, 0)
                    traces_dc[i, :] = norm01(traces_gauss)
                    traces_dc[i, :] = traces_dc[i, :] - np.median(traces_dc[i, :])

                shift_dc = shift_1d[dc]
                sorted_shift_dc = np.sort(shift_dc)
                sorted_shift_dc_ts = sorted_shift_dc / sampling_rate_hz
                sorted_indices = np.argsort(shift_dc)
                sorted_cells = dc[sorted_indices]

                sorted_cells_all.append(sorted_cells)
                shift_dc_all.append(shift_dc)
                sorted_indices_all.append(sorted_indices)

                blur_speed = False
                if speed is not None:
                    if blur_speed:
                        speed_blur = gauss_blur(speed, n_times / 10)
                        speed_for_plot = speed_blur
                    else:
                        speed_for_plot = speed
                else:
                    speed_for_plot = None
                    binary_runs = None

                if display == "speed":
                    variable_to_plot = speed_for_plot
                    y_label_suplot = "Speed"
                elif display == "binary speed":
                    variable_to_plot = binary_runs
                    y_label_suplot = "Run"
                else:
                    variable_to_plot = position
                    y_label_suplot = "Position"

                t = np.arange(n_times) / sampling_rate_hz

                if verbose:
                    print(f"Find sequences with PCA for PC # {pc_number}: Done")
                    print(f"Find sequences with PCA for PC # {pc_number}: Plot the results")
                filename = f"{session_identifier}_sequences_PC{pc_number}"

                plot_with_imshow(raster=traces_dc[sorted_indices],
                                 speed_array=variable_to_plot,
                                 path_results=self.get_results_path(),
                                 file_name=filename, n_subplots=n_subplots, axes_list=None,
                                 vmin=0, vmax=None,
                                 without_ticks=without_ticks,
                                 y_ticks_labels=sorted_indices, y_ticks_labels_size=ticks_label_size,
                                 y_ticks_labels_color=ticks_label_color,
                                 fig=None, show_color_bar=False,
                                 hide_x_labels=hide_x_label,
                                 x_ticks_labels_color=ticks_label_color,  x_ticks_labels_size=ticks_label_size,
                                 values_to_plot=None, cmap=sequences_cmap, show_fig=False, save_formats=save_formats,
                                 lines_to_display=None,
                                 lines_color="white",
                                 lines_width=1,
                                 lines_band=0,
                                 lines_band_color="white",
                                 lines_band_alpha=0.5,
                                 reverse_order=False,
                                 background_color=bckground_color,
                                 show_yaxis_title=with_yaxis_title,
                                 speeed_line_color=speed_color,
                                 ylabel_fontsize=axis_labels_size,
                                 axis_color=axis_color,
                                 hide_cell_index=hide_cell_idx,
                                 hide_speed_values=hide_speed_y_values,
                                 y_label_suplot=y_label_suplot)

                if verbose:
                    print(f"Find sequences with PCA for PC # {pc_number}: Write text files result")

                with open(os.path.join(self.get_results_path(),
                                       f"{session_identifier}_sequences_PC{pc_number}_sorted_cells.txt"),
                          "w", encoding='UTF-8') as file:
                    file.write(f"Sorted cells" + '\n')
                    ind = 0
                    for i in sorted_cells:
                        file.write(f"{i}")
                        if ind < len(sorted_cells) - 1:
                            file.write(" ")
                        ind += 1
                    file.write(f"" + '\n')

                with open(os.path.join(self.get_results_path(),
                                       f"{session_identifier}_sequences_PC{pc_number}_cell_shifts.txt"),
                          "w", encoding='UTF-8') as file:
                    file.write(f"Cell shift" + '\n')
                    ind = 0
                    for i in sorted_shift_dc:
                        file.write(f"{int(i)}")
                        if ind < len(sorted_shift_dc) - 1:
                            file.write(" ")
                        ind += 1
                    file.write(f"" + '\n')

                if verbose:
                    print(f"Find sequences with PCA for PC # {pc_number}: Write xlsx file result")

                table_dict = {"Order in seq": np.arange(n_dc), "Cell indice": sorted_cells,
                              "Frame shift": sorted_shift_dc, "Time shift":  sorted_shift_dc_ts}
                table = pd.DataFrame(table_dict)

                path_table_xls = os.path.join(self.get_results_path(),
                                              f"{session_identifier}_sequences_PC{pc_number}_table.xlsx")

                table.to_excel(path_table_xls)

            # ------------------------------------------------------------------------------------------------------ #
            # ----------------------------------- DO PCA ON TEST DATA SET (IF SPLIT) ------------------------------- #
            # ----------------------------------------------(STEFANIA)---------------------------------------------- #
            do_stefania_method = True
            if split_data_for_pca and do_stefania_method:
                if verbose:
                    print(f" ")
                    print(f"Run PCA on test data set")

                # PCA ON 'TEST' SET
                arnaud_version = True
                if arnaud_version:
                    traces_gauss = gaussblur1D(traces_for_test, traces_for_test.shape[1] / 20, 1)
                    _, pc_time_course_test = step1_pca(traces_gauss, np_pc_max)

                shift_test_all = []
                sorted_ind_all = []

                print(f"PC time course: {pc_time_course_test.shape[0]} PCs, {pc_time_course_test.shape[1]} frames")
                # TODO : find the meaning of dt and replace it by something like 20 * sampling_rate
                dt = 200
                # GET THE ORDER WITH PCA
                for pc_number in np.arange(np_pc_max):
                    if verbose:
                        print(f"Find order with PCA for PC # {pc_number}: Ongoing")
                    sig_ref = np.diff(pc_time_course_test[pc_number, :])
                    # calculate shifted trace
                    cor_1d = np.zeros(n_cells)
                    shift_1d = np.zeros(n_cells)
                    for i in np.arange(n_cells):
                        tmp = covnorm(traces_for_test[i, :], np.real(sig_ref), dt)
                        cor_1d[i] = np.max(tmp)
                        shift_1d[i] = np.where(tmp == cor_1d[i])[0][0] - dt - 1

                    sorted_ind = np.argsort(shift_1d)

                    shift_test_all.append(shift_1d)
                    sorted_ind_all.append(sorted_ind)

                # FINALLY CORRELATE THE ORDER FOUND IN EACH COMPONENT TRAINING VS TEST
                if verbose:
                    print(f" ")
                    print(f"Compare cell order for each component between the two part of the data set")
                fig, axes = plt.subplots(2, 5, figsize=(15, 6.5))

                for pc_number in np.arange(np_pc_max):
                    sel_shift_test = shift_test_all[pc_number][dc_all[pc_number]]
                    sequence_1 = sorted_indices_all[pc_number]
                    sequence_2 = np.argsort(sel_shift_test)

                    order_1 = [i for i in range(len(sequence_1))]
                    order_2 = [j for i, x in enumerate(sequence_1) for j, v in enumerate(sequence_2) if x == v]
                    tau, p = scistats.kendalltau(order_1, order_2)

                    ax = axes[pc_number // 5, pc_number % 5]
                    ax.scatter(order_1, order_2)
                    if p < 0.001:
                        ax.set_title('tau={:.2f}, p<0.001'.format(tau), color='r')
                    else:
                        ax.set_title('tau={:.2f}, p={:.2f}'.format(tau, p), color='r')

                    if pc_number == 5:
                        ax.set_xlabel('Order train')

                        ax.set_ylabel('Order test')

                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    fig.tight_layout()

                    fig.savefig(self.get_results_path() + f'/{session_identifier}_OrderPreservedTrainSel.pdf',
                                bbox_inches='tight')
                if verbose:
                    print(f"Done")

            # TODO: Try to replicate 'NoCamp_Temporal_Stats.m' on selected PC from Arnaud and following
            # Here we want to find the order in each repetition of the sequence for each PC
            if verbose:
                print(f" ")
                print(f"Look for the order in each run epoch for each PC and compare 'individual' order with "
                      f"'global' order")
            result_table = pd.DataFrame()
            fig2, axes2 = plt.subplots(2, 5, figsize=(24, 12))
            fig3, axes3 = plt.subplots(2, 5, figsize=(24, 12))
            for pc_number in np.arange(np_pc_max):
                if verbose:
                    print(f"Ongoing for PC # {pc_number}")
                # Get the distances cells:
                dc = dc_all[pc_number]  # Indexes of cells in the sequences
                n_dc = n_dc_all[pc_number]  # Number of cells in the sequence
                dc_traces = traces[dc, :]  # Traces of cells in sequence
                sorted_cells = sorted_cells_all[pc_number]  # True index of 'best' order for this PC number

                # Get the run epochs
                run_epochs = get_continous_time_periods(binary_runs)
                n_runs = len(run_epochs)

                # For each of the run find the order by correlating trace with pc_time_course
                run_index = 0
                order_table = pd.DataFrame()
                if verbose:
                    print(f"{n_runs} runs to look at")
                # For the figure in case
                fig, axes = plt.subplots(8, int(np.ceil(n_runs / 8)), figsize=(40, 40))
                axes = axes.flatten()

                # Loop on the runs
                kendal_correlation = []
                training_run_correlations = []
                testing_run_correlations = []
                for run in range(n_runs):
                    if verbose and run % 10 == 0 and run > 0:
                        print(f"{run} runs done")
                    run_start = run_epochs[run][0]
                    run_stop = run_epochs[run][1]
                    if run_stop - run_start < minimal_run_duration * sampling_rate_hz:
                        run_index += 1
                        continue
                    # Get the reference signal to correlate with traces during run epoch
                    if run_stop >= spliting_frame:
                        run_belonging = 'Testing'
                        # Taken from Arnaud's code (Villette et al)
                        window = np.arange(run_start, run_stop)
                        sig_ref_run_epoch = np.exp(-(window-np.mean(window)) ** 2 / (4 ** 2))
                    else:
                        run_belonging = 'Training'
                        sig_ref = np.diff(pc_time_course[pc_number, :])
                        sig_ref_run_epoch = sig_ref[run_start: run_stop]

                    # Correlate each dc of the sequence with sig_ref to find the order in this run
                    cor_1d = np.zeros(n_dc)
                    shift_1d = np.zeros(n_dc)
                    for cell in range(n_dc):
                        tmp = covnorm(dc_traces[cell, run_start: run_stop],
                                      np.real(sig_ref_run_epoch), dt)
                        cor_1d[cell] = np.max(tmp)
                        shift_1d[cell] = np.where(tmp == cor_1d[cell])[0][0] - dt - 1

                    # Sort the dc
                    sorted_ind_run = np.argsort(shift_1d)
                    # Get index in originiall form
                    final_run_order = dc[sorted_ind_run]

                    # Put order for each run in table and save
                    order_table[f'run_{run_index}'] = final_run_order
                    path_table_xlsx = os.path.join(self.get_results_path(), f'PC_{pc_number}_order_in_runs.xlsx')
                    order_table.to_excel(path_table_xlsx)

                    # Correlate order from pca with order in this run
                    tau, p = scistats.kendalltau(np.argsort(sorted_cells), np.argsort(final_run_order))
                    ax = axes[run]
                    ax.scatter(np.argsort(sorted_cells), np.argsort(final_run_order))
                    ax.set_xlabel('Order from PCA')
                    ax.set_ylabel('Order in the run')
                    ax.set_title(f'Run_{run_index}')
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    plt.close()

                    # Append tau for this run to the list for boxplots
                    kendal_correlation.append(tau)
                    # Make a difference between training and testing
                    if split_data_for_pca:
                        if run_stop <= spliting_frame:
                            training_run_correlations.append(tau)
                        else:
                            testing_run_correlations.append(tau)

                    # Build a table for result
                    tau_dict = {'Age': [info_dict['age']], 'AnimalID': [info_dict['subject_id']],
                                'Session': [session_identifier], 'PCA #': [pc_number],
                                'Run ID': [run_index],
                                'Run Group': [run_belonging], 'Kendall Tau': [tau], 'Pvalue': [p]}
                    result_table_to_append = pd.DataFrame(tau_dict)
                    run_index += 1

                    # Append table after each run
                    result_table = result_table.append(result_table_to_append, ignore_index=True)

                # FIGURES
                fig.tight_layout()
                fig.savefig(self.get_results_path() + f'/{session_identifier}_PC{pc_number}_'
                                                      f'indiv_runs_corr_with_PCA_order.pdf',
                            bbox_inches='tight')

                # Do one boxplot for each PC with all correlations
                ax2 = axes2[pc_number // 5, pc_number % 5]
                ax2.boxplot(kendal_correlation)
                ax2.set_ylim([-1, 1])
                ax2.set_ylabel('Kendal correlations distribution')
                ax2.set_title(f'PC_{pc_number}')
                ax2.set_xticks([])
                ax2.axhline(y=0, color='b', linestyle='--')
                ax2.spines['left'].set_color('black')
                ax2.spines['right'].set_color('white')
                ax2.spines['bottom'].set_color('white')
                ax2.spines['top'].set_color('white')
                plt.close()

                # Do 2 boxplots for each PC with all correlations for training and testing separated
                dict_for_plot = {'Training runs': training_run_correlations, 'Testing runs': testing_run_correlations}
                ax3 = axes3[pc_number // 5, pc_number % 5]
                ax3.boxplot(dict_for_plot.values())
                ax3.set_xticklabels(dict_for_plot.keys())
                ax3.set_ylim([-1, 1])
                ax3.set_ylabel('Kendal correlations distribution')
                ax3.set_title(f'PC_{pc_number}')
                ax3.axhline(y=0, color='b', linestyle='--')
                ax3.spines['left'].set_color('black')
                ax3.spines['right'].set_color('white')
                ax3.spines['bottom'].set_color('white')
                ax3.spines['top'].set_color('white')
                plt.close()

            fig2.tight_layout()
            fig2.savefig(self.get_results_path() + f'/{session_identifier}_correlations_run_vs_PCA.pdf',
                         bbox_inches='tight')

            fig3.tight_layout()
            fig3.savefig(self.get_results_path() + f'/{session_identifier}_correlations_run_vs_PCA_train_vs_test.pdf',
                         bbox_inches='tight')

            plt.close('all')

            # APPEND TABLE FOR ALL SESSIONS TO SAVE LATER
            correlation_general_table = correlation_general_table.append(result_table, ignore_index=True)

            self.update_progressbar(start_time, 100 / n_sessions)

        # Save general table
        if verbose:
            print(f"Save PCA/run order correlation table")
        correlation_general_table.to_excel(os.path.join(self.get_results_path(), "correlations_table.xlsx"))

        # Build and save summary tables
        correlation_table_noruns = correlation_general_table.drop(columns=['Run Group'])
        first_summary_table = correlation_table_noruns.groupby(['Session', 'PCA #']).agg({'mean', 'median', 'size'})
        second_summary_table = correlation_general_table.groupby(['Session', 'PCA #', 'Run Group']).agg({'mean', 'median', 'size'})
        if verbose:
            print(f"Save PCA/run order correlation table")
        first_summary_table.to_excel(os.path.join(self.get_results_path(), "correlations_table_summary1.xlsx"))
        second_summary_table.to_excel(os.path.join(self.get_results_path(), "correlations_table_summary2.xlsx"))

        if verbose:
            print(f" ")
            print(f"----------------------------------- ANALYSIS DONE --------------------------------------")
