from cicada.preprocessing.convert_to_nwb import ConvertToNWB
import hdf5storage
import numpy as np
from pynwb.ophys import Fluorescence


class ConvertNeuralActivityToNWB(ConvertToNWB):
    def __init__(self, nwb_file):
        ConvertToNWB.__init__(self, nwb_file)
        self.ci_frames = None
        self.data_id = None
        self.cell_type_codes = None
        # filtered means we removed the cells'code with code in self.cell_type_codes_to_remove
        self.cell_type_codes_filtered = None
        self.cell_type_names = None
        self.cell_type_names_filtered = None
        self.cell_type_codes_to_remove = []

    def convert(self, **kwargs):
        """Convert the data and add it to the nwb_file

        Args:
            **kwargs: arbitrary arguments
        """
        super().convert(**kwargs)

        self.data_id = kwargs.get("data_id", None)
        # identify the data (for ex: "all_cells", "INs" etc...)
        if self.data_id is None:
            # not mandatory
            print(f"No data_id in class {self.__class__.__name__}")
            return

        if "ci_frames" not in self.nwb_file.acquisition:
            print(f"No ci_frames available in the acquisition of the nwb_file")
            # return
            self.ci_frames = None
        else:
            self.ci_frames = self.nwb_file.acquisition["ci_frames"]

        # cells to be removed according to their cell type
        # using the cell type code to identify them
        self.cell_type_codes_to_remove = kwargs.get("cell_type_codes_to_remove", [])

        if isinstance(self.cell_type_codes_to_remove, int):
            self.cell_type_codes_to_remove = [self.cell_type_codes_to_remove]
        elif not isinstance(self.cell_type_codes_to_remove, list):
            # then empty list
            self.cell_type_codes_to_remove = []

        # list of int and str representing the code and name of cell type of each cell
        # the length is the number of cells
        # could be None if cell type is not known
        self.cell_type_codes = kwargs.get("cell_type_codes", None)
        self.cell_type_codes_filtered = None if self.cell_type_codes is None else []
        self.cell_type_names = kwargs.get("cell_type_names", None)
        self.cell_type_names_filtered = None if self.cell_type_names is None else []

        if "cascade_raster" in kwargs:
            descr = kwargs.get("descr", None)
            if descr is None:
                neuronal_data_descr = "raster"
            else:
                neuronal_data_descr = descr
            cascade_raster_path = kwargs.get("cascade_raster")
            if cascade_raster_path is not None:
                cascade_raster = self.load_predictions(cascade_raster_path, do_cascade=True)
                self.save_neuronal_data_in_nwb(neuronal_data=cascade_raster,
                                               neuronal_data_descr=neuronal_data_descr)
                return

        # segmentation_tool = kwargs.get("segmentation_tool")
        # print(f"segmentation_tool {segmentation_tool}")
        # if not segmentation_tool:
        #     raise Exception(f"'segmentation_tool' argument should be pass to convert "
        #                     f"function in class {self.__class__.__name__}")

        predictions_file = kwargs.get("predictions", None)
        if predictions_file is None:
            print(f"No predictions given to convert neural activity.")
            return

        threshold_predictions = kwargs.get("threshold_predictions")
        predictions_keyword = kwargs.get("predictions_keyword")
        if not threshold_predictions:
            threshold_predictions = 0.5
        self.load_predictions(predictions_file, threshold_predictions=threshold_predictions,
                              predictions_keyword=predictions_keyword)

    def load_predictions(self, predictions_file, threshold_predictions=0.5, predictions_keyword=None, do_cascade=False):
        """

        Args:
            predictions_file:
            threshold_predictions:
            predictions_keyword:

        Returns:

        """
        if predictions_file.endswith(".mat"):
            data = hdf5storage.loadmat(predictions_file)
            predictions = data["predictions"]
        elif predictions_file.endswith(".npy"):
            predictions = np.load(predictions_file)
        elif predictions_file.endswith(".npz"):
            predictions = np.load(predictions_file)["predictions"]
        else:
            print(f"predictions file {predictions_file} extension not available for preprocessing")
            return

        if (self.cell_type_codes is not None) and (len(self.cell_type_codes_to_remove) > 0):
            # then we remove from predictions the cell to remove according to their cell type
            # first counting how many cells left
            n_cells_left = 0
            for cell in np.arange(predictions.shape[0]):
                if self.cell_type_codes[cell] in self.cell_type_codes_to_remove:
                    continue
                # print(f"For cell {cell}, {self.cell_type_names[cell]}, sum activity {np.sum(predictions[cell, :])}")
                self.cell_type_codes_filtered.append(self.cell_type_codes[cell])
                self.cell_type_names_filtered.append(self.cell_type_names[cell])
                n_cells_left += 1

            new_predictions = np.zeros((n_cells_left, *predictions.shape[1:]))

            print(f"Removing {predictions.shape[0] - n_cells_left} out of {predictions.shape[0]} "
                  f"cells from predictions "
                  f"whose cell type codes are {self.cell_type_codes_to_remove}")

            new_cell_index = 0
            for cell in np.arange(predictions.shape[0]):
                if self.cell_type_codes[cell] in self.cell_type_codes_to_remove:
                    continue

                new_predictions[new_cell_index] = predictions[cell]
                new_cell_index += 1

            predictions = new_predictions

        if do_cascade is False:
            # then we produce the raster dur based on the predictions using threshold the prediction_threshold
            n_cells = predictions.shape[0]
            # TODO: take in consideration frames_to_add
            n_frames = predictions.shape[1]
            predicted_raster_dur = np.zeros((n_cells, n_frames), dtype="int8")
            for cell in np.arange(len(predictions)):
                pred = predictions[cell]
                if len(pred.shape) == 1:
                    predicted_raster_dur[cell, pred >= threshold_predictions] = 1
                elif (len(pred.shape) == 2) and (pred.shape[1] == 1):
                    pred = pred[:, 0]
                    predicted_raster_dur[cell, pred >= threshold_predictions] = 1
                elif (len(pred.shape) == 2) and (pred.shape[1] == 3):
                    # real transient, fake ones, other (neuropil, decay etc...)
                    # keeping predictions about real transient when superior
                    # to other prediction on the same frame
                    max_pred_by_frame = np.max(pred, axis=1)
                    real_transient_frames = (pred[:, 0] == max_pred_by_frame)
                    predicted_raster_dur[cell, real_transient_frames] = 1
                elif pred.shape[1] == 2:
                    # real transient, fake ones
                    # keeping predictions about real transient superior to the threshold
                    # and superior to other prediction on the same frame
                    max_pred_by_frame = np.max(pred, axis=1)
                    real_transient_frames = np.logical_and((pred[:, 0] >= threshold_predictions),
                                                           (pred[:, 0] == max_pred_by_frame))
                    predicted_raster_dur[cell, real_transient_frames] = 1
            self.save_neuronal_data_in_nwb(neuronal_data=predicted_raster_dur,
                                           neuronal_data_descr=f'raster dur {predictions_keyword}')

        return predictions

    def save_neuronal_data_in_nwb(self, neuronal_data, neuronal_data_descr):
        """

        Args:
            neuronal_data: 2d array: n_cells * n_frames
            neuronal_data_descr: (str) description neuronal data

        Returns:

        """
        print(f"neuronal_data.shape {neuronal_data.shape}")
        n_cells = neuronal_data.shape[0]
        # TODO: take in consideration frames_to_add
        n_frames = neuronal_data.shape[1]

        mod = self.nwb_file.modules['ophys']
        image_segmentaton = mod.get(f"{self.data_id}")
        if image_segmentaton is None:
            print(f"No image_segmentation named {self.data_id} found while converting in ConvertNeuralActivityToNWB")
            return
        plan_segmentation = image_segmentaton.get_plane_segmentation('my_plane_seg')

        # print(f"mod {mod}")

        try:
            fluorescence = mod.get('fluorescence_' + self.data_id)
        except KeyError:
            fluorescence = Fluorescence(name=('fluorescence_' + self.data_id))
            mod.add_data_interface(fluorescence)

        rt_region = plan_segmentation.create_roi_table_region('all cells', region=list(np.arange(n_cells)))

        if self.ci_frames is None:
            self.ci_frames = np.arange(n_frames)
            rrs = fluorescence.create_roi_response_series(name=neuronal_data_descr,
                                                          data=np.transpose(neuronal_data), unit="lumens",
                                                          rois=rt_region, timestamps=self.ci_frames,
                                                          description=neuronal_data_descr,
                                                          control=self.cell_type_codes_filtered,
                                                          control_description=self.cell_type_names_filtered)
        else:
            if n_frames != len(np.array(self.ci_frames.timestamps)):
                print(
                    f"Careful {self.nwb_file.identifier} has a different number "
                    f"of frames {n_frames} in the predictions "
                    f"than in the calcium imaging movie {len(np.array(self.ci_frames.timestamps))}")
            rrs = fluorescence.create_roi_response_series(name=neuronal_data_descr,
                                                          data=np.transpose(neuronal_data), unit="lumens",
                                                          rois=rt_region, timestamps=self.ci_frames.timestamps,
                                                          description=neuronal_data_descr,
                                                          control=self.cell_type_codes_filtered,
                                                          control_description=self.cell_type_names_filtered)

        print(f"- Creating Roi Response Series with neuronal data: {neuronal_data_descr} of shape:"
              f"{(np.transpose(neuronal_data)).shape}")

