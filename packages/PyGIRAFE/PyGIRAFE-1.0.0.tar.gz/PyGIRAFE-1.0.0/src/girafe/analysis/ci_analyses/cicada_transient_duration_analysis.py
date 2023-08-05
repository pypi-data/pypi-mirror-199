from cicada.analysis.cicada_analysis import CicadaAnalysis
from time import time
from datetime import datetime
import numpy as np
from cicada.utils.misc import get_continous_time_periods, print_info_dict
from cicada.utils.stats import compare_two_distributions
from cicada.utils.stats import multiple_comparison_one_factor_effect
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


class CicadaTransientDurationAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        long_description = '<p align="center"><b>Compute mean calcium event duration for all cells</b></p><br>'
        long_description = long_description + 'Use the raster to return the mean transient duration of each cell' \
                                              ' and save in csv and xlxs formats.<br><br>'
        long_description = long_description + 'Do some customized plots with groups and subgroups that can be defined'
        CicadaAnalysis.__init__(self, name="Transients' duration", family_id="Descriptive statistics",
                                short_description="",
                                long_description=long_description, config_handler=config_handler,
                                accepted_data_formats=["CI_DATA"])

    def copy(self):
        """
        Make a copy of the analysis
        Returns:

        """
        analysis_copy = CicadaTransientDurationAnalysis(config_handler=self.config_handler)
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

        cell_types = []
        for session_index, session_data in enumerate(self._data_to_analyse):
            cell_types.extend(session_data.get_all_cell_types())
            cell_types = list(np.unique(cell_types))
        cell_types.insert(0, "all_cells")
        self.add_choices_arg_for_gui(arg_name="cell_to_use", choices=cell_types,
                                     default_value="all_cells",
                                     short_description="Cell type to use to plots and do statistics",
                                     multiple_choices=False,
                                     family_widget="figure_config_celltypes")

        self.add_bool_option_for_gui(arg_name="do_not_show_unclassified", true_by_default=False,
                                     short_description="Do not include 'Unclassified' as a cell-type",
                                     family_widget="figure_config_celltypes")

        self.add_bool_option_for_gui(arg_name="save_table", true_by_default=True,
                                     short_description="Save results in table",
                                     family_widget="figure_config_saving")

        self.add_bool_option_for_gui(arg_name="save_figure", true_by_default=True,
                                     short_description="Save figure",
                                     family_widget="figure_config_saving")

        representations = ["strip", "swarm", "violin", "box", "bar", "boxen"]
        self.add_choices_arg_for_gui(arg_name="representation", choices=representations,
                                     default_value="box", short_description="Kind of plot to use",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        x_ax = ["Age", "SubjectID", "Session", "Celltype", "Weight"]
        self.add_choices_arg_for_gui(arg_name="x_axis", choices=x_ax,
                                     default_value="Age", short_description="Variable to use for x axis groups",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        possible_hues = ["Age", "SubjectID", "Session", "Celltype", "Weight", "None"]
        self.add_choices_arg_for_gui(arg_name="hue", choices=possible_hues,
                                     default_value="Celltype",
                                     short_description="Variable to use for x axis sub-groups",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        palettes = ["muted", "deep", "pastel", "Blues"]
        self.add_choices_arg_for_gui(arg_name="palettes", choices=palettes,
                                     default_value="muted", short_description="Color palette for x-axis subgroups",
                                     long_description="In that case figure facecolor and figure edgecolor are useless",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        cell_comp = []
        for session_index, session_data in enumerate(self._data_to_analyse):
            cell_comp.extend(session_data.get_all_cell_types())
            cell_comp = list(np.unique(cell_comp))
        self.add_choices_arg_for_gui(arg_name="cell_types_to_compare", choices=cell_comp,
                                     default_value="",
                                     short_description="Cell types to compare (all sessions merged)",
                                     multiple_choices=True,
                                     family_widget="figure_config_stats")

        self.add_bool_option_for_gui(arg_name="do_stats", true_by_default=True,
                                     short_description="Try statistical tests",
                                     family_widget="figure_config_stats")

        self.add_int_values_arg_for_gui(arg_name="pvalue", min_value=1, max_value=5,
                                        short_description="p-value (%) for statistical test",
                                        default_value=5, family_widget="figure_config_stats")

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
        test
        :param kwargs:
          segmentation

        :return:
        """
        CicadaAnalysis.run_analysis(self, **kwargs)

        roi_response_series_dict = kwargs["roi_response_series"]

        cell_to_use = kwargs.get("cell_to_use")

        do_not_show_unclassified = kwargs.get("do_not_show_unclassified")

        x_axis_name = kwargs.get("x_axis")

        hue = kwargs.get("hue")

        kind = kwargs.get("representation")

        palette = kwargs.get("palettes")

        cell_types_to_compare = kwargs.get("cell_types_to_compare")

        do_stats = kwargs.get("do_stats")

        pvalue = kwargs.get("pvalue")
        pvalue = pvalue / 100

        verbose = kwargs.get("verbose", True)

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

        save_table = kwargs.get("save_table")

        save_figure = kwargs.get("save_figure")

        dpi = kwargs.get("dpi", 100)

        width_fig = kwargs.get("width_fig")

        height_fig = kwargs.get("height_fig")

        with_timestamp_in_file_name = kwargs.get("with_timestamp_in_file_name", True)

        start_time = time()

        n_sessions = len(self._data_to_analyse)
        if verbose:
            print(f"{n_sessions} sessions to analyse")

        gobal_duration_data_table = pd.DataFrame()
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
            duration_s = neuronal_data_timestamps[len(neuronal_data_timestamps)-1] - neuronal_data_timestamps[0]
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
            type_required = cell_to_use.capitalize()
            if type_required != "All_cells":
                if type_required not in cell_type_list:
                    if verbose:
                        print(f"No {type_required} identified in this session")
                        print(f"Session: {session_identifier} not included in plots and statistics")

            # Building Mean transient duration vector
            durations = []
            for cell in range(n_cells):
                tmp_tple = get_continous_time_periods(raster_dur[cell, :])
                durations_cell = []
                for tple in range(len(tmp_tple)):
                    onset = tmp_tple[tple][0]
                    peak = tmp_tple[tple][1]
                    duration = neuronal_data_timestamps[peak] - neuronal_data_timestamps[onset]
                    durations_cell.append(duration)
                durations.append(durations_cell)

            mean_duration_by_cell = [np.mean(x) for x in durations]

            # Generate pd.DataFrame table #
            age_list = [info_dict['age'] for k in range(n_cells)]
            weight_list = [info_dict['weight'] for k in range(n_cells)]
            session_identifier_list = [info_dict['identifier'] for k in range(n_cells)]
            animal_id_list = [info_dict['subject_id'] for k in range(n_cells)]
            sum_up_data = {'MeanDuration': mean_duration_by_cell, 'Cell#': np.arange(n_cells), 'Celltype': cell_type_list,
                           'Session': session_identifier_list, 'SubjectID': animal_id_list, 'Age': age_list,
                           'Weight': weight_list}
            duration_data_table = pd.DataFrame(sum_up_data)

            # If possible compare across cell types for this session:
            unique_types = np.unique(cell_type_list)
            unique_types_list = unique_types.tolist()
            frequencies_lists = []
            if do_stats and len(unique_types_list) > 1:
                for index, name in enumerate(unique_types_list):
                    table = duration_data_table.query('Celltype == @name')
                    frequencies = table.get("MeanDuration")
                    frequencies_list = frequencies.values.tolist()
                    frequencies_lists.append(frequencies_list)
                if verbose:
                    print(f" ")
                    print(f"--------------------- Basic stats: {session_identifier} ---------------------")
                    print(f"Compare transient frequency across the different cell-types: {unique_types_list}")
                if len(unique_types_list) == 2:
                    compare_two_distributions(frequencies_lists[0], frequencies_lists[1],
                                              pvalues=pvalue, verbose=verbose)
                if len(unique_types_list) > 2:
                    multiple_comparison_one_factor_effect(frequencies_lists, pvalues=pvalue, verbose=verbose,
                                                          sessions_ids=unique_types_list)

            # Generate / append global pd.DataFrame table #
            gobal_duration_data_table = gobal_duration_data_table.append(duration_data_table, ignore_index=True)

            self.update_progressbar(start_time, 100 / n_sessions)

        # Save results in table
        if save_table:
            if verbose:
                print(f" ")
                print(f"----------------------------------- SAVINGS --------------------------------------")
            path_results = self.get_results_path()
            path_table_xlsx = os.path.join(f'{path_results}', f'transient_durations_table.xlsx')
            path_table_csv = os.path.join(f'{path_results}', f'transient_durations_table.csv')
            gobal_duration_data_table.to_excel(path_table_xlsx)
            gobal_duration_data_table.to_csv(path_table_csv)
            if verbose:
                print(f"Data save as excel file")

        # Filter general table on query from the GUI
        if cell_to_use == "all_cells":
            data_table = gobal_duration_data_table
        else:
            type_to_use = cell_to_use.capitalize()
            data_table = gobal_duration_data_table.query('Celltype == @type_to_use')

        if do_not_show_unclassified:
            data_table.drop(data_table.loc[data_table['Celltype'] == "Unclassified"].index, inplace=True)
        n_cells_stats = len(data_table.index)

        # Get Info
        ages = data_table.get("Age")
        ages_list = ages.values.tolist()
        ages_list = np.unique(ages_list)
        n_ages = len(ages_list)

        animals = data_table.get("SubjectID")
        animals_list = animals.values.tolist()
        animals_list = np.unique(animals_list)
        n_animals = len(animals_list)

        sessions = data_table.get("Session")
        sessions_list = sessions.values.tolist()
        sessions_list = np.unique(sessions_list)
        n_sessions = len(sessions_list)

        # Do Some Statistics
        if do_stats:
            if verbose:
                print(f" ")
                print(f"----------------------------------- DO STATS --------------------------------------")
            if cell_to_use == "all_cells":
                if verbose:
                    print(f"N pups: {n_animals}, N sessions: {n_sessions}, N cells: {n_cells_stats}")

                if n_ages > 1:
                    if verbose:
                        print(f"-------------- Compare {cell_to_use} transient's duration across ages ----------------")
                    distribution_by_age = [[] for k in range(n_ages)]
                    for index in range(n_ages):
                        age = ages_list[index]
                        tmp_table = data_table[data_table.Age == age]
                        data = tmp_table.get("MeanDuration")
                        data_list = data.values.tolist()
                        distribution_by_age[index] = data_list
                    multiple_comparison_one_factor_effect(distribution_by_age, pvalues=pvalue, verbose=verbose,
                                                          sessions_ids=ages_list)

                if len(cell_types_to_compare) > 1:
                    frequencies_lists = []
                    for index, key in enumerate(cell_types_to_compare):
                        name = key.capitalize()
                        table = data_table.query('Celltype == @name')
                        frequencies = table.get("MeanDuration")
                        frequencies_list = frequencies.values.tolist()
                        frequencies_lists.append(frequencies_list)
                    if verbose:
                        print(f"------------- Compare {cell_types_to_compare}: all data set --------------")
                    if len(cell_types_to_compare) == 2:
                        compare_two_distributions(frequencies_lists[0], frequencies_lists[1],
                                                  pvalues=pvalue, verbose=verbose)
                    if len(cell_types_to_compare) > 2:
                        multiple_comparison_one_factor_effect(frequencies_lists, pvalues=pvalue, verbose=verbose,
                                                              sessions_ids=cell_types_to_compare)

            else:
                if verbose:
                    print(f"N pups: {n_animals}, N sessions: {n_sessions}, N {cell_to_use}: {n_cells_stats}")
                if n_ages > 1:
                    if verbose:
                        print(f"-------------- Compare {cell_to_use} transient's duration across ages ---------------")
                    distribution_by_age = [[] for k in range(n_ages)]
                    for index in range(n_ages):
                        age = ages_list[index]
                        tmp_table = data_table[data_table.Age == age]
                        data = tmp_table.get("MeanDuration")
                        data_list = data.values.tolist()
                        distribution_by_age[index] = data_list
                    multiple_comparison_one_factor_effect(distribution_by_age, pvalues=pvalue, verbose=verbose,
                                                          sessions_ids=ages_list)

        # Do Some Plots
        if verbose:
            print(f" ")
            print(f"----------------------------------- DO PLOTS --------------------------------------")

        # Do the plot according to GUI requirements
        if hue == "None":
            hue = None
            palette = None

        ylabel = " Transient's mean duration (s)"

        filename = "transient_mean_duration_"

        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(width_fig, height_fig), dpi=dpi)
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)

        svm = sns.catplot(x=x_axis_name, y="MeanDuration", hue=hue, data=data_table,
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









