from cicada.preprocessing.convert_to_nwb import ConvertToNWB
from cicada.utils.cell_type_utils import read_cell_type_categories_yaml_file
import numpy as np


class ConvertCellTypeToNWB(ConvertToNWB):
    """Class to convert Calcium Imaging movies to NWB"""
    def __init__(self, nwb_file):
        """
        Initialize some parameters
        Args:
             nwb_file (NWB.File) : NWB file object
        """
        super().__init__(nwb_file)
        # array of length the number of cell, and value an int representing a cell type
        self.cell_type_codes = None
        # array of length the number of cell, and value a string representing a cell type
        self.cell_type_names = None

    def convert(self, **kwargs):
        """Convert the data and add to the nwb_file

        Args:
            **kwargs: arbitrary arguments
        """
        super().convert(**kwargs)

        # ### setting parameters ####
        cell_type_predictions_file = kwargs.get("cell_type_predictions_file", None)

        if cell_type_predictions_file is None:
            print(f"No cell type predictions file in {self.__class__.__name__}")
            return

        # predictions_threshold = kwargs.get("predictions_threshold", 0.5)
        unknown_cell_type_name = kwargs.get("unknown_cell_type_name", "unknown")
        cell_type_config_file = kwargs.get("cell_type_config_file", None)
        if cell_type_config_file is None:
            print(f"No cell type config file in {self.__class__.__name__}")
            return

        cell_type_from_code_dict, cell_type_to_code_dict, multi_class_arg = \
            read_cell_type_categories_yaml_file(yaml_file=cell_type_config_file, using_multi_class=2)

        cell_type_predictions = np.load(cell_type_predictions_file)
        if cell_type_predictions_file.endswith(".npz"):
            cell_type_predictions = cell_type_predictions["predictions"]
        # binary_cell_type_predictions = np.zeros(cell_type_predictions.shape, dtype="int8")
        # binary_cell_type_predictions[cell_type_predictions > predictions_threshold] = 1

        # cell_type_from_code_dict: key int representing the code of the cell type, value str representing the cell type
        # print(f"ConvertCellTypeToNWB cell_type_from_code_dict {cell_type_from_code_dict}")

        # cell_type_to_code_dict: has a key cell type name and as value their code (int).
        # Several names can have the same code
        # print(f"ConvertCellTypeToNWB cell_type_to_code_dict {cell_type_to_code_dict}")

        self.cell_type_codes = []
        # array of length the number of cell, and value a string representing a cell type
        self.cell_type_names = []

        for cell in np.arange(len(cell_type_predictions)):
            if np.sum(cell_type_predictions) == 0:
                # if the code is superior to the number of code, then it means the cell type is unknown
                # we put it as n_classes + 1 to get None later on
                code = cell_type_predictions.shape[1]
            else:
                code = np.argmax(cell_type_predictions[cell])

            self.cell_type_codes.append(code)
            self.cell_type_names.append(cell_type_from_code_dict.get(code, unknown_cell_type_name))

        # need to be an uint8 type to be put in NWB
        self.cell_type_codes = np.asarray(self.cell_type_codes, dtype="uint8")