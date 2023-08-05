from cicada.analysis.cicada_analysis import CicadaAnalysis
from cicada.utils.misc import get_continous_time_periods
from cicada.utils.misc import from_timestamps_to_frame_epochs
from cicada.utils.misc import get_yang_frames, print_info_dict
from time import time
import os
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class CicadaActivityIntervalsRatioAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        long_description = '<p align="center"><b>Defined statistically epoch associated cells</b></p><br>'
        long_description = long_description + 'Allows the user to defined epochs. For each epoch we then look for each' \
                                              ' cell if it is more active during the considered epoch than expected by ' \
                                              'chance. If yes we consider the cell as associated to the epoch. <br><br>'
        long_description = long_description + 'Return a cell table (each row is a cell) containing cell information' \
                                              ' and whether it is associated to all defined epochs.<br><br>'
        long_description = long_description + 'Return a session table. Containing for all sessions the proportion of ' \
                                              'cell associated to each epoch. The proportion is computed for different ' \
                                              'populations if possible.<br><br>'
        long_description = long_description + 'Data are saved in csv and xlxs formats. Customized plots are done'

        CicadaAnalysis.__init__(self, name="Epochs associated cells", family_id="Epochs",
                                short_description="Evaluate the proportion of cell associated to an epoch",
                                long_description=long_description,
                                config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaActivityIntervalsRatioAnalysis(config_handler=self.config_handler)
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
            rrs_names = data_to_analyse.get_roi_response_series_list(keywords_to_exclude=None)
            raster_in_rrs_keys = False
            for rrs_name in rrs_names:
                if 'raster' in rrs_name:
                    raster_in_rrs_keys = True
                    return True
                else:
                    continue
            if raster_in_rrs_keys is False:
                self.invalid_data_help = f"Analysis is so far based on inferred raster plot, " \
                                         f"not implemented on traces yet"
                return False

        return True

    def set_arguments_for_gui(self):
        """

        Returns:

        """
        CicadaAnalysis.set_arguments_for_gui(self)

        self.add_roi_response_series_arg_for_gui(short_description="Neuronal activity to use", long_description=None)

        all_epochs = []
        for data_to_analyse in self._data_to_analyse:
            all_epochs.extend(data_to_analyse.get_behavioral_epochs_names())
        all_epochs = list(np.unique(all_epochs))
        self.add_choices_for_groups_for_gui(arg_name="epochs_names", choices=all_epochs,
                                            with_color=True,
                                            mandatory=False,
                                            short_description="Epochs composition",
                                            long_description="Define epoch name and composition",
                                            family_widget="epochs")

        self.add_int_values_arg_for_gui(arg_name="n_surrogates", min_value=10, max_value=10000,
                                        short_description="Number of surrogates raster to compute cell-epoch association",
                                        default_value=100, family_widget="figure_config_surrogate")

        self.add_int_values_arg_for_gui(arg_name="percentile", min_value=95, max_value=100,
                                        short_description="Percentile of surrogate distribution to compute cell-epoch association",
                                        default_value=99, family_widget="figure_config_surrogate")

        self.add_bool_option_for_gui(arg_name="specify_twitches_duration", true_by_default=False,
                                     short_description="Arbitrary set twitch duration",
                                     family_widget="figure_config_twitches_duration")

        self.add_int_values_arg_for_gui(arg_name="twitches_duration", min_value=100, max_value=1500,
                                        short_description="Duration after twitch to define 'twitch-related' transient (ms)",
                                        default_value=1000, family_widget="figure_config_twitches_duration")

        self.add_bool_option_for_gui(arg_name="save_table", true_by_default=True,
                                     short_description="Save results in table",
                                     family_widget="figure_config_saving")

        self.add_bool_option_for_gui(arg_name="save_figure", true_by_default=True,
                                     short_description="Save figure",
                                     family_widget="figure_config_saving")

        self.add_bool_option_for_gui(arg_name="do_not_show_unclassified", true_by_default=True,
                                     short_description="Do not use 'Unclassified' cell type as a reference population",
                                     family_widget="figure_config_celltypes")

        representations = ["strip", "swarm", "violin", "box", "bar", "boxen"]
        self.add_choices_arg_for_gui(arg_name="representation", choices=representations,
                                     default_value="box", short_description="Kind of plot to use",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        x_ax = ["Age", "SubjectID", "Session", "Population"]
        self.add_choices_arg_for_gui(arg_name="x_axis", choices=x_ax,
                                     default_value="Age", short_description="Variable to use for x axis groups",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        possible_hues = ["Age", "SubjectID", "Session", "Population", "None"]
        self.add_choices_arg_for_gui(arg_name="hue", choices=possible_hues,
                                     default_value="Population",
                                     short_description="Variable to use for x axis sub-groups",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        palettes = ["muted", "deep", "pastel", "Blues"]
        self.add_choices_arg_for_gui(arg_name="palettes", choices=palettes,
                                     default_value="muted", short_description="Color palette for x-axis subgroups",
                                     long_description="In that case figure facecolor and figure edsgecolor are useless",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        self.add_image_format_package_for_gui()

        self.add_color_arg_for_gui(arg_name="background_color", default_value=(0, 0, 0, 1.),
                                   short_description="background color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="fig_facecolor", default_value=(1, 1, 1, 1.),
                                   short_description="Figure face color",
                                   long_description="Useless if a 'hue' is specified, in such a case use 'palette'",
                                   family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="axis_color", default_value=(1, 1, 1, 1.),
                                   short_description="Axes color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="labels_color", default_value=(1, 1, 1, 1.),
                                   short_description="Label color",
                                   long_description=None, family_widget="figure_config_color")

        policies = ["Arial", "Cambria", "Rosa", "Times", "Calibri"]
        self.add_choices_arg_for_gui(arg_name="font_type", choices=policies,
                                     default_value="Arial", short_description="Font type",
                                     multiple_choices=False,
                                     family_widget="figure_config_label")

        weights = ["light", "normal", "bold", "extra bold"]
        self.add_choices_arg_for_gui(arg_name="fontweight", choices=weights,
                                     default_value="normal", short_description="Font Weight",
                                     multiple_choices=False,
                                     family_widget="figure_config_label")

        self.add_int_values_arg_for_gui(arg_name="font_size", min_value=1, max_value=100,
                                        short_description="Font size",
                                        default_value=10, family_widget="figure_config_label")

    def update_original_data(self):
        """
        To be called if the data to analyse should be updated after the analysis has been run.
        :return: boolean: return True if the data has been modified
        """
        pass

    def run_analysis(self, **kwargs):
        """
        testa
        :param kwargs:
          segmentation

        :return:
        """
        CicadaAnalysis.run_analysis(self, **kwargs)

        verbose = kwargs.get("verbose", True)

        roi_response_series_dict = kwargs["roi_response_series"]

        epochs_names = kwargs.get("epochs_names")
        if (epochs_names is None) or len(epochs_names) == 0:
            print(f"No epochs selected, no analysis")
            self.update_progressbar(time_started=self.analysis_start_time, increment_value=100)
            return

        n_surrogates = kwargs.get("n_surrogates")

        percentile = kwargs.get("percentile")

        specify_twitches_duration = kwargs.get("specify_twitches_duration")

        save_table = kwargs.get("save_table")

        save_figure = kwargs.get("save_figure")

        path_results = self.get_results_path()

        do_not_show_unclassified = kwargs.get("do_not_show_unclassified")

        x_axis_name = kwargs.get("x_axis")

        hue = kwargs.get("hue")

        kind = kwargs.get("representation")

        palette = kwargs.get("palettes")

        background_color = kwargs.get("background_color")

        fig_facecolor = kwargs.get("fig_facecolor")

        axis_color = kwargs.get("axis_color")

        labels_color = kwargs.get("labels_color")

        font_size = kwargs.get("font_size")

        fontweight = kwargs.get("fontweight")

        fontfamily = kwargs.get("font_type")

        # image package format
        save_formats = kwargs["save_formats"]
        if save_formats is None:
            save_formats = "pdf"

        dpi = kwargs.get("dpi", 100)

        width_fig = kwargs.get("width_fig")

        height_fig = kwargs.get("height_fig")

        with_timestamp_in_file_name = kwargs.get("with_timestamp_in_file_name", True)

        start_time = time()

        print("Detection of epoch associated cells: coming soon...")

        n_sessions = len(self._data_to_analyse)

        global_behavior_associated_cells = pd.DataFrame()
        global_single_cell_info_table = pd.DataFrame()
        group_name_list = []
        for session_index, session_data in enumerate(self._data_to_analyse):
            # Get Session Info
            info_dict = session_data.get_sessions_info()
            session_identifier = info_dict['identifier']

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

            # Get Data Timestamps
            neuronal_data_timestamps = session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_info)
            duration_s = neuronal_data_timestamps[len(neuronal_data_timestamps) - 1] - neuronal_data_timestamps[0]
            duration_m = duration_s / 60
            if verbose:
                print(f"Acquisition last for : {duration_s} seconds // {duration_m} minutes ")

            # Get Neuronal Data
            neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)
            raster_dur = neuronal_data
            [n_cells, n_frames] = raster_dur.shape
            if verbose:
                print(f"N cells: {n_cells}, N frames: {n_frames}")

            # Get Cell-type Data and build cell-type list
            cell_indices_by_cell_type = session_data.get_cell_indices_by_cell_type(roi_serie_keys=
                                                                                   roi_response_serie_info)
            cell_type_list = []
            for cell in range(n_cells):
                cell_type_list.append("Unclassified")

            for key, info in cell_indices_by_cell_type.items():
                cell_type = key.capitalize()
                indexes = cell_indices_by_cell_type.get(key)
                tmp_n_cell = len(indexes)
                for cell in range(tmp_n_cell):
                    tmp_ind = indexes[cell]
                    cell_type_list[tmp_ind] = cell_type

            # Check Data with respect to the specific analysis
            population = np.unique(cell_type_list)
            population_list = population.tolist()
            population_list.insert(0, "All-cells")
            if "Unclassified" in population_list and do_not_show_unclassified:
                population_list.remove("Unclassified")
            n_populations = len(population_list)

            if verbose:
                print(f"Working on data to obtain the number of spikes in group for all cell")

            # Building raster plot from rasterdur
            raster = np.zeros((n_cells, n_frames))
            for cell in range(n_cells):
                tmp_tple = get_continous_time_periods(raster_dur[cell, :])
                for tple in range(len(tmp_tple)):
                    onset = tmp_tple[tple][0]
                    raster[cell, onset] = 1

            # Get total spike
            total_spikes = np.sum(raster, axis=1)

            # Get the sampling rate and number of frames to consider after twitches
            sampling_rate = session_data.get_ci_movie_sampling_rate(only_2_photons=True)
            twitches_duration = kwargs.get("twitches_duration")
            twitches_duration = twitches_duration / 1000
            frames_delay = int(np.round(twitches_duration * sampling_rate))

            # Building spike counts vector for each main epoch
            # Loop on each defined main epoch
            n_spikes_by_epoch_dict = dict()
            spikes_in_epoch = np.zeros((n_cells,), dtype=int)
            active_frames = []
            group_names = []
            for epoch_group_name, epoch_info in epochs_names.items():
                if len(epoch_info) != 2:
                    continue
                group_names.append(epoch_group_name)

                # Check whether this main epoch is the one of twitches
                name_to_check = epoch_group_name.lower()
                twitches_group = False
                if name_to_check.find('twi') != -1:
                    twitches_group = True

                epochs_names_in_group = epoch_info[0]

                # Loop on all the epochs included in the main epoch
                epochs_frames_in_group = []
                for epoch_name in epochs_names_in_group:
                    # looking in behavior or intervals
                    epochs_timestamps = session_data.get_interval_times(interval_name=epoch_name)
                    if epochs_timestamps is None:
                        epochs_timestamps = session_data.get_behavioral_epochs_times(epoch_name=epoch_name)
                    if epochs_timestamps is None:
                        # means this session doesn't have this epoch name
                        continue
                    # now we want to get the intervals time_stamps and convert them in frames
                    intervals_frames = from_timestamps_to_frame_epochs(time_stamps_array=epochs_timestamps,
                                                                       frames_timestamps=neuronal_data_timestamps,
                                                                       as_list=True)
                    epochs_frames_in_group.extend(intervals_frames)
                active_frames.extend(epochs_frames_in_group)

                n_events_in_main_epoch = len(epochs_frames_in_group)
                n_spikes_in_main_epoch = np.zeros((n_cells,), dtype=int)
                for event in range(n_events_in_main_epoch):
                    start_event = epochs_frames_in_group[event][0]
                    start = np.min((start_event, n_frames - 1))
                    if twitches_group is True and specify_twitches_duration is True:
                        end_event = epochs_frames_in_group[event][0] + frames_delay
                    else:
                        end_event = epochs_frames_in_group[event][1]
                    end = np.min((end_event, n_frames))
                    frames_to_take = np.arange(start, end)
                    n_spikes = np.sum(raster[:, frames_to_take], axis=1)
                    n_spikes_in_main_epoch = n_spikes_in_main_epoch + n_spikes
                n_spikes_by_epoch_dict[epoch_group_name] = n_spikes_in_main_epoch
                spikes_in_epoch = spikes_in_epoch + n_spikes_in_main_epoch

            # Get spikes in rest and add to dictionary
            spikes_in_rest = total_spikes - spikes_in_epoch
            if 'Rest' not in n_spikes_by_epoch_dict.keys():
                n_spikes_by_epoch_dict['Rest'] = spikes_in_rest

            # Get 'Rest' frames:
            rest_fames_list = get_yang_frames(total_frames=n_frames, yin_frames=active_frames)[1]

            if verbose:
                print(f"Number of spikes in each group for all cell is obtained")
                print(f"Working on rolled raster to get a statistical threshold")

            if verbose:
                print(f"Starting to obtain the {n_surrogates} rolled rasters")
            rnd_rasters = np.zeros((n_cells, n_frames, n_surrogates))
            for surrogate in range(n_surrogates):
                for cell in range(n_cells):
                    rnd_rasters[cell, :, surrogate] = np.roll(raster[cell, :], np.random.randint(1, n_frames))
            if verbose:
                print(f"{n_surrogates} rasters obtained")

            # Building random spike counts vector for each main epoch
            # Loop on each defined main epoch
            spike_threshold_for_group_dict = dict()
            for epoch_group_name, epoch_info in epochs_names.items():
                if len(epoch_info) != 2:
                    continue

                # Check whether this main epoch is the one of twitches
                name_to_check = epoch_group_name.lower()
                twitches_group = False
                if name_to_check.find('twi') != -1:
                    twitches_group = True

                epochs_names_in_group = epoch_info[0]

                # Loop on all the epochs included in the main epoch
                epochs_frames_in_group = []
                for epoch_name in epochs_names_in_group:
                    # looking in behavior or intervals
                    epochs_timestamps = session_data.get_interval_times(interval_name=epoch_name)
                    if epochs_timestamps is None:
                        epochs_timestamps = session_data.get_behavioral_epochs_times(epoch_name=epoch_name)
                    if epochs_timestamps is None:
                        # means this session doesn't have this epoch name
                        continue
                    # now we want to get the intervals time_stamps and convert them in frames
                    intervals_frames = from_timestamps_to_frame_epochs(time_stamps_array=epochs_timestamps,
                                                                       frames_timestamps=neuronal_data_timestamps,
                                                                       as_list=True)
                    epochs_frames_in_group.extend(intervals_frames)

                n_events_in_main_epoch = len(epochs_frames_in_group)
                n_rnd_spikes_in_group = np.zeros((n_cells, n_surrogates), dtype=int)
                for event in range(n_events_in_main_epoch):
                    start_event = epochs_frames_in_group[event][0]
                    start = np.min((start_event, n_frames))
                    if twitches_group is True and specify_twitches_duration is True:
                        end_event = epochs_frames_in_group[event][0] + frames_delay
                    else:
                        end_event = epochs_frames_in_group[event][1]
                    end = np.min((end_event, n_frames - 1))
                    frames_to_take = np.arange(start, end)
                    n_rnd_spikes = np.sum(rnd_rasters[:, frames_to_take, :], axis=1)
                    n_rnd_spikes_in_group = n_rnd_spikes_in_group + n_rnd_spikes

                spike_threshold_for_group = np.percentile(n_rnd_spikes_in_group, percentile, axis=1)
                spike_threshold_for_group_dict[epoch_group_name] = spike_threshold_for_group

            rest_rnd_raster = rnd_rasters[:, rest_fames_list, :]
            rnd_spikes_rest = np.sum(rest_rnd_raster, axis=1)
            spikes_threshold_rest = np.percentile(rnd_spikes_rest, percentile, axis=1)

            if 'Rest' not in spike_threshold_for_group_dict.keys():
                spike_threshold_for_group_dict['Rest'] = spikes_threshold_rest

            if verbose:
                print(f"Statistical threshold for significant association cell-epoch is obtained")

            # Create pd.DataFrame for global result
            age_list = [info_dict['age'] for k in range(n_populations)]
            weight_list = [info_dict['weight'] for k in range(n_populations)]
            session_identifier_list = [info_dict['identifier'] for k in range(n_populations)]
            animal_id_list = [info_dict['subject_id'] for k in range(n_populations)]
            sum_up_data = {'Age': age_list, 'Weight': weight_list, 'SubjectID': animal_id_list,
                           'Session': session_identifier_list, 'Population': population_list}
            behavior_associated_cells_table = pd.DataFrame(sum_up_data)

            # Create pd.DataFrame for single cell result
            age_list = [info_dict['age'] for k in range(n_cells)]
            weight_list = [info_dict['weight'] for k in range(n_cells)]
            session_identifier_list = [info_dict['identifier'] for k in range(n_cells)]
            animal_id_list = [info_dict['subject_id'] for k in range(n_cells)]
            sum_up_data2 = {'Age': age_list, 'Weight': weight_list, 'SubjectID': animal_id_list,
                            'Session': session_identifier_list, 'Cell#': np.arange(n_cells),
                            'Cell-Type': cell_type_list}
            single_cell_info_table = pd.DataFrame(sum_up_data2)

            for group_key, data in n_spikes_by_epoch_dict.items():
                n_spikes = n_spikes_by_epoch_dict.get(group_key)
                threshold = spike_threshold_for_group_dict.get(group_key)
                group_associated_cell = np.zeros((n_cells,), dtype=bool)
                for cell in range(n_cells):
                    if n_spikes[cell] >= threshold[cell]:
                        group_associated_cell[cell] = True
                column_name = str(group_key) + '_associated_cell'
                single_cell_info_table[column_name] = group_associated_cell

                associated_prop_all_cells = len(np.where(group_associated_cell)[0]) / n_cells
                proportions_list_for_group = [associated_prop_all_cells]

                for key, info in cell_indices_by_cell_type.items():
                    if key == "unclassified" and do_not_show_unclassified:
                        continue
                    else:
                        indexes = cell_indices_by_cell_type.get(key)
                        group_associated_celltype = group_associated_cell[indexes]
                        associated_prop_celltype = len(np.where(group_associated_celltype)[0]) / len(indexes)
                        proportions_list_for_group.append(associated_prop_celltype)

                # Append a new column of each group define in the GUI
                behavior_associated_cells_table[group_key] = proportions_list_for_group

            global_behavior_associated_cells = global_behavior_associated_cells.append(behavior_associated_cells_table,
                                                                                       ignore_index=True)
            global_single_cell_info_table = global_single_cell_info_table.append(single_cell_info_table,
                                                                                 ignore_index=True)

            group_name_list.append(group_names)
            self.update_progressbar(start_time, 100 / n_sessions)

        # Save results in table
        if save_table:
            if verbose:
                print(f"----------------------------------- SAVINGS --------------------------------------")
            path_results = self.get_results_path()
            path_table_xls = os.path.join(f'{path_results}', f'epochs_associated_cells_table.xlsx')
            path_table_csv = os.path.join(f'{path_results}', f'epochs_associated_cells_table.csv')
            path_cell_table_xls = os.path.join(f'{path_results}', f'epochs_associated_single_cells_table.xlsx')
            path_cell_table_csv = os.path.join(f'{path_results}', f'epochs_associated_single_cells_table.csv')
            if save_table:
                global_behavior_associated_cells.to_excel(path_table_xls)
                global_behavior_associated_cells.to_csv(path_table_csv)
                global_single_cell_info_table.to_excel(path_cell_table_xls)
                global_single_cell_info_table.to_csv(path_cell_table_csv)
                if verbose:
                    print(f"Data save as excel and csv files")

        # Use group name
        group_name_list = np.unique(group_name_list)
        my_set = set(group_name_list)
        new_group_name_list = list(my_set)
        new_group_name_list.append('Rest')

        # Do Some Plots
        if verbose:
            print(f"----------------------------------- DO PLOTS --------------------------------------")

        # Do the plot according to GUI requirements
        if hue == "None":
            hue = None
            palette = None

        for index, name in enumerate(new_group_name_list):

            ylabel = " Proportion of " + name + " associated cells "
            filename = name + "_associated_cells_"

            y_axis_name = name

            fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                    gridspec_kw={'height_ratios': [1]},
                                    figsize=(width_fig, height_fig), dpi=dpi)
            ax1.set_facecolor(background_color)
            fig.patch.set_facecolor(background_color)

            svm = sns.catplot(x=x_axis_name, y=y_axis_name, hue=hue, data=global_behavior_associated_cells,
                              hue_order=None,
                              kind=kind, orient=None, color=fig_facecolor, palette=palette, ax=ax1)

            ax1.set_ylabel(ylabel, fontsize=font_size, labelpad=20, fontweight=fontweight, fontfamily=fontfamily)
            ax1.yaxis.label.set_color(labels_color)
            ax1.xaxis.label.set_color(labels_color)
            ax1.spines['left'].set_color(axis_color)
            ax1.spines['right'].set_color(background_color)
            ax1.spines['bottom'].set_color(background_color)
            ax1.spines['top'].set_color(background_color)
            ax1.yaxis.set_tick_params(labelsize=font_size)
            ax1.xaxis.set_tick_params(labelsize=font_size)
            ax1.tick_params(axis='y', colors=axis_color)
            ax1.tick_params(axis='x', colors=axis_color)

            fig.tight_layout()
            if save_figure and (path_results is not None):
                # transforming a string in a list
                if isinstance(save_formats, str):
                    save_formats = [save_formats]
                time_str = ""
                if with_timestamp_in_file_name:
                    time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
                for save_format in save_formats:
                    if not with_timestamp_in_file_name:
                        fig.savefig(os.path.join(f'{path_results}', f'{filename}.{save_format}'),
                                    format=f"{save_format}",
                                    facecolor=fig.get_facecolor())
                    else:
                        fig.savefig(os.path.join(f'{path_results}', f'{filename}{time_str}.{save_format}'),
                                    format=f"{save_format}",
                                    facecolor=fig.get_facecolor())
            plt.close()


