import numpy as np
# import time
import PIL
from ScanImageTiffReader import ScanImageTiffReader
from PIL import ImageSequence
from abc import ABC, abstractmethod
import os

from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize, destroyAllWindows, VideoCapture
import cv2


def load_tiff_movie(tiff_file_name):
    """
    Load a tiff movie from tiff file name.
    Args:
        tiff_file_name:

    Returns: a 3d array: n_frames * width_FOV * height_FOV

    """
    try:
        # start_time = time.time()
        tiff_movie = ScanImageTiffReader(tiff_file_name).data()
        # stop_time = time.time()
        # print(f"Time for loading movie with ScanImageTiffReader: "
        #       f"{np.round(stop_time - start_time, 3)} s")
    except Exception as e:
        im = PIL.Image.open(tiff_file_name)
        n_frames = len(list(ImageSequence.Iterator(im)))
        dim_y, dim_x = np.array(im).shape
        tiff_movie = np.zeros((n_frames, dim_y, dim_x), dtype="uint16")
        for frame, page in enumerate(ImageSequence.Iterator(im)):
            tiff_movie[frame] = np.array(page)
    return tiff_movie


class VideoReaderWrapper:
    """
        An abstract class that should be inherited in order to create a specific video format wrapper.
        A class can be created using either different packages or aim at specific format.

    """

    def __init__(self):
        self._length = None
        self._width = None
        self._height = None
        self._fps = None

    @property
    def length(self):
        return self._length

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def fps(self):
        return self._fps

    @abstractmethod
    def close_reader(self):
        pass

# TODO make a function or class that will decide which VideoReaderWrapper to use depending on the video
#  format but also the packages available


class ArrayVideoReader(VideoReaderWrapper):

    def __init__(self, video_data):
        """

        Args:
            video_data: np.array of 3d or 4d, with n_frames*height*width*colors
        """
        VideoReaderWrapper.__init__(self)
        self._video_data = video_data
        # if len(self._video_data.shape) == 3:
        #     self._video_data = np.reshape(self._video_data, (self._video_data.shape[0],
        #                                                      self._video_data.shape[1],
        #                                                      self._video_data.shape[2], 1))
        #     print(f"self._video_data.shape {self._video_data.shape}")
        #     color_video = np.zeros((self._video_data.shape[0],
        #                             self._video_data.shape[1],
        #                             self._video_data.shape[2], 3))
        #     for frame_index, frame in enumerate(self._video_data):
        #         color_video[frame_index] = cv2.cvtColor(self._video_data[frame_index], cv2.COLOR_GRAY2RGB)
        #     self._video_data = color_video
        #     print(f"self._video_data.shape {self._video_data.shape}")

        # length in frames
        self._length = len(self._video_data)

        # in pixels
        self._width = self._video_data.shape[2]
        self._height = self._video_data.shape[1]

        # frame per seconds
        self._fps = 1

    def get_frame(self, frame_index):
        if (frame_index >= self._length) or (frame_index < 0):
            return None
        return self._video_data[frame_index]

    def close_reader(self):
        pass


class TiffVideoReader(VideoReaderWrapper):

    def __init__(self, video_file_name, load_video_in_memory=False):
        VideoReaderWrapper.__init__(self)

        self._video_data = None
        self.video_file_name = video_file_name
        self.image_seq_iterator = None
        try:
            # start_time = time.time()
            self._video_data = ScanImageTiffReader(video_file_name).data()
            self.n_frames = len(self._video_data)
            # in pixels
            self._width = self._video_data.shape[2]
            self._height = self._video_data.shape[1]
            print("ScanImageTiffReader successful")
            # stop_time = time.time()
            # print(f"Time for loading movie with ScanImageTiffReader: "
            #       f"{np.round(stop_time - start_time, 3)} s")
        except Exception as e:
            im = PIL.Image.open(video_file_name)
            self.n_frames = len(list(ImageSequence.Iterator(im)))
            self._height, self._width = np.array(im).shape
            self.image_seq_iterator = ImageSequence.Iterator(im)
            if load_video_in_memory:
                self._video_data = np.zeros((self.n_frames, self._height, self._width), dtype="uint16")
                for frame, page in enumerate(ImageSequence.Iterator(im)):
                    self._video_data[frame] = np.array(page)

    def get_frame(self, frame_index):
        if (frame_index >= self._length) or (frame_index < 0):
            return None

        if self._video_data is not None:
            print("self._video_data is not None")
            return self._video_data[frame_index]

        return self.image_seq_iterator[frame_index]

    def close_reader(self):
        pass


class OpenCvVideoReader(VideoReaderWrapper):
    """
    Use OpenCv to read video
    """

    def __init__(self, video_file_name):
        VideoReaderWrapper.__init__(self)

        self.video_file_name = video_file_name
        self.basename_video_file_name = os.path.basename(video_file_name)

        # Create a VideoCapture object and read from input file
        # If the input is the camera, pass 0 instead of the video file name
        self.video_capture = VideoCapture(self.video_file_name)

        if self.video_capture.isOpened() == False:
            raise Exception(f"Error opening video file {self.video_file_name}")

        # length in frames
        self._length = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        # in pixels
        self._width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # frame per seconds
        self._fps = self.video_capture.get(cv2.CAP_PROP_FPS)

        print(f"OpenCvVideoReader init for {self.basename_video_file_name}: "
              f"self.width {self.width}, self.height {self.height}, n frames {self._length}")

    def get_frame(self, frame_index):
        if (frame_index >= self._length) or (frame_index < 0):
            return None

        # The first argument of cap.set(), number 2 defines that parameter for setting the frame selection.
        # Number 2 defines flag CAP_PROP_POS_FRAMES which is
        # a 0-based index of the frame to be decoded/captured next.
        # The second argument defines the frame number in range 0.0-1.0
        # frame_no = frame_index / self._length
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

        # Read the next frame from the video. If you set frame 749 above then the code will return the last frame.
        # 'res' is boolean result of operation, one may use it to check if frame was successfully read.
        res, frame = self.video_capture.read()

        if res:
            return frame
        else:
            return None

    def close_reader(self):
        # When everything done, release the capture
        self.video_capture.release()
        cv2.destroyAllWindows()
