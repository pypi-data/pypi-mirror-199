from cicada.preprocessing.convert_to_nwb import ConvertToNWB
from cicada.preprocessing.utils import load_tiff_movie_in_memory, update_frames_to_add
from PIL import ImageSequence
import PIL
import PIL.Image as pil_image
import time
from pynwb.image import ImageSeries
import yaml
import numpy as np
import os
import hdf5storage
from pynwb.base import TimeSeries
from pynwb.device import Device


class ConvertBehaviorMovieToNWB(ConvertToNWB):
    """Class to convert Calcium Imaging movies to NWB"""
    def __init__(self, nwb_file):
        """
        Initialize some parameters
        Args:
             nwb_file (NWB.File) : NWB file object
        """
        super().__init__(nwb_file)

    def convert(self, **kwargs):
        """Convert the data and add to the nwb_file

        Args:
            **kwargs: arbitrary arguments
        """
        super().convert(**kwargs)

        # ### setting parameters ####

        if not kwargs.get("behavior_movie_file_name"):
            # behavior is not mandatory, so no exception
            print(f"No behavior movie found")
            return
            # raise Exception(f"'behavior_movie_file_name' attribute should be pass to convert "
            #                 f"function in class {self.__class__.__name__}")
        behavior_movie_file_name = kwargs["behavior_movie_file_name"]

        # cam_id from abf, only 2 choices
        if "23109588" in behavior_movie_file_name:
            cam_id = "23109588"
        else:
            cam_id = "22983298"

        print(f"behavior_movie_file_name {behavior_movie_file_name}, cam_id {cam_id}")

        behavior_img_series = ImageSeries(name=f'behavior_cam_{cam_id}',
                                          external_file=[behavior_movie_file_name],
                                          starting_frame=[0],
                                          format="external", rate=20.)

        self.nwb_file.add_acquisition(behavior_img_series)
