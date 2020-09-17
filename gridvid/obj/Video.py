from multiprocessing import Pool
from pathlib import Path
from typing import Tuple
import os

import matplotlib.pyplot as plt
from numba import njit, prange
import numpy as np
import imageio

from gridvid.config.video_settings import input_extensions
from gridvid.utils.creators import create_unique_name
from gridvid.config import defaults, paths

class Video:

    # CONSTRUCTORS
    @classmethod
    def noise(
    cls, frames:int, shape:Tuple[int], fps:int, grayscale:bool = False,
    filename:str = None, verbose:bool = True) -> 'Video':
        '''
            Returns an instance of Video consisting of random generated noise.
        '''
        data = np.random.randint(
            0, 256, (frames, shape[0], shape[1], 3), dtype = np.uint8
        )
        if grayscale:
            data[:,:,:,0] = data[:,:,:,2]
            data[:,:,:,1] = data[:,:,:,2]

        return cls(data, fps, filename, verbose)

    @classmethod
    def from_file(
    cls, filename:str, directory:Path = None, verbose:bool = True) -> 'Video':
        '''
            To initiate an instance of class Video by referring to the path of a
            video file.
        '''
        err_msg = (
            '\n\nThe class method `from_file` for class `Video` requires that '
            'argument `{}` be of <class \'{}\'>.\n'
        )

        if not isinstance(filename, str):
            raise TypeError(err_msg.format('filename', 'str'))

        if not isinstance(directory, Path):
            raise TypeError(err_msg.format('directory', 'Path'))

        if not isinstance(verbose, bool):
            raise TypeError(err_msg.format('verbose', 'bool'))

        path = directory / filename

        # Check that `path` refers to an existing file
        if not path.exists():
            msg = ('\n\nGiven path cannot be located in filesystem\n')
            raise FileNotFoundError(msg)

        # Raises Exception if `path` is of invalid filetype
        if path.suffix not in input_extensions:
            msg = ( '\n\nUnsupported file extension in given path, supported '
                   f'filetypes are: {",".join(input_extensions)}\n')
            raise IOError(msg)

        # Getting video metadata
        reader = imageio.get_reader(path, 'ffmpeg')
        metadata = reader.get_meta_data()

        # Getting video duration and fps
        fps = int(metadata['fps'])

        # Preparing list of video frames
        video = []
        for frame in reader:
            video.append(frame)

        data = np.array(video, dtype = np.uint8)

        video = cls(data, fps, path.name, verbose)
        video.default_extension = path.suffix
        return video

    def __init__(
    self, data:np.ndarray, fps:int, filename:str = None,
    verbose:bool = True) -> None:
        '''
            To handle video data in a convenient way.  Copies the input array.
        '''
        err_msg = (
            '\n\nThe constructor for class `Video` requires that argument '
            '`{}` be of <class \'{}\'>.'
        )

        if filename is None:
            filename = defaults.video_filename

        if not isinstance(data, np.ndarray):
            raise TypeError(err_msg.format('data', 'np.ndarray'))

        if not isinstance(fps, int):
            raise TypeError(err_msg.format('fps', 'int'))

        if not isinstance(verbose, bool):
            raise TypeError(err_msg.format('verbose', 'bool'))

        if not isinstance(filename, str):
            raise TypeError(err_msg.format('filename', 'str'))

        array_msg = (
            '\n\nThe constructor for class `Video` requires that argument '
            '`data` be a 4-D array of dtype <class \'np.uint8\'>.'
        )
        if data.ndim != 4:
            raise ValueError(array_msg)
        elif data.dtype != np.uint8:
            raise TypeError(array_msg)

        self._filename = filename

        self._data = data.copy()
        self._modified_data = data.copy()
        self._fps = fps
        self._default_extension = input_extensions[0]

    # PROPERTIES
    @property
    def filename(self) -> str:
        '''
            Returns the name of the video file.
        '''
        return self._filename

    @property
    def raw(self) -> np.ndarray:
        '''
            Returns the video data array.
        '''
        return self._data

    @property
    def fps(self) -> int:
        '''
            Returns the video's frames per second count.
        '''
        return self._fps

    @property
    def array(self) -> np.ndarray:
        '''
            Returns a copy of the video array.
        '''
        return self._data.copy()

    @property
    def shape(self) -> Tuple[int]:
        '''
            Returns the shape of the video array as a 4-tuple with:

            (Number of frames, Video Height, Video Width, Color Channels)
        '''
        return self._data.shape

    @property
    def size(self) -> int:
        '''
            Returns the number of elements in the video array
        '''
        return self._data.size

    @property
    def itemsize(self) -> int:
        '''
            Returns the array elements' size in bytes
        '''
        return self._data.itemsize

    def __len__(self) -> int:
        '''
            Returns the number of frames in the video
        '''
        return self._data.shape[0]

    def astype(self, new_type:type) -> np.ndarray:
        '''
            Returns the data array as an array of specified type.
        '''
        return self._data.astype(new_type)

    # GETTER/SETTER METHODS
    def __getitem__(self, key) -> np.ndarray:
        '''
            Returns an element or subset of the video data.
        '''
        return self._data[key]

    def __setitem__(self, key, value) -> None:
        '''
            Sets an element or subset of the video data to a new value.
        '''
        try:
            self._data[key] = value
        except ValueError:
            msg = 'Attempted to set element of Video instance with invalid value.'
            raise ValueError(msg)
        except IndexError:
            msg = 'Attempted to access invalid index on Video instance.'
            raise IndexError(msg)

    # ITERATOR METHODS
    def __iter__(self) -> 'Video':
        '''
            Makes Video instances iterable. Each iteration yields a frame of
            the video as a numpy array of <np.uint8>
        '''
        self.iter_idx = -1
        return self

    def __next__(self) -> np.ndarray:
        '''
            SEE METHOD: __iter__()
        '''
        self.iter_idx += 1
        if self.iter_idx < self._data.shape[0]:
            return self._data[self.iter_idx]
        else:
            raise StopIteration()

    # MODIFIERS
    def create_grid(
    self, shape:Tuple[int], width:int = 1, linecolor:Tuple[int] = None) -> None:
        '''
            Adds a grid to the video.

            `shape` should be a tuple containing two positive integers – the
            first is the number of horizontal lines in the grid, and the second
            is the number of vertical lines in the grid. Does not include image
            boundaries.

            `width` is the width of the grid lines in pixels.  Must be an
            integer greater than or equal to one.

            `linecolor` is an rgb value, i.e. a tuple containing three integers
            in the range [0, 255].
        '''
        if linecolor is None:
            linecolor = (255, 255, 255)

        err_msg = (
            'Method `create_grid` in class `Video` requires that argument '
            '`{}` be of <class \'{}\'>.'
        )

        if not isinstance(shape, tuple):
            raise TypeError(err_msg.format('shape', 'tuple'))

        if not isinstance(width, int):
            raise TypeError(err_msg.format('width', 'int'))

        if not isinstance(linecolor, tuple):
            raise TypeError(err_msg.format('linecolor', 'tuple'))

        err_msg = (
            'Method `create_grid` in class `Video` requires that argument '
            '`{}` be {}'
        )

        cond = [
            len(shape) != 2,
            not isinstance(shape[0], int), shape[0] < 0,
            not isinstance(shape[1], int), shape[1] < 0,
        ]
        if cond[0] or cond[1] or cond[2] or cond[3] or cond[4]:
            msg = (
                'a two-tuple of integers greater than or equal to zero.'
            )
            raise TypeError(err_msg.format('shape', msg))

        if not isinstance(width, int) or width <= 0:
            msg = (
                'an integer greater than or equal to one.'
            )
            raise TypeError(err_msg.format('width', msg))

        err_msg = (
            'Method `create_grid` in class `Video` requires that argument '
            '`{}` be {}'
        )

        cond = [
            len(linecolor) != 3,
            not isinstance(linecolor[0], int), 256 <= linecolor[0] <= 0,
            not isinstance(linecolor[1], int), 256 <= linecolor[1] <= 0,
            not isinstance(linecolor[2], int), 256 <= linecolor[2] <= 0,
        ]

        if cond[0] or cond[1] or cond[2] or cond[3] or cond[4]:
            msg = (
                'a two-tuple of integers greater than or equal to zero.'
            )
            raise TypeError(err_msg.format('shape', msg))

        img_shape = self._data.shape[1:3]
        shape = (shape[0]+2, shape[1]+2)

        rows = np.linspace(0, img_shape[0]-1, shape[0], dtype = np.int64)
        cols = np.linspace(0, img_shape[1]-1, shape[1], dtype = np.int64)

        old_rows = rows.copy()
        old_cols = cols.copy()

        disp = 1
        for i in range(width-1):
            new_rows = old_rows + disp
            invalid_rows = np.where(np.logical_or(
                new_rows < 0, new_rows >= img_shape[0]
            ))
            new_rows = np.delete(new_rows, invalid_rows)

            new_cols = old_cols + disp
            invalid_cols = np.where(np.logical_or(
                new_cols < 0, new_cols >= img_shape[1]
            ))
            new_cols = np.delete(new_cols, invalid_cols)

            rows = np.concatenate([rows, new_rows])
            cols = np.concatenate([cols, new_cols])
            if disp > 0:
                disp = -disp
            elif disp < 0:
                disp = -disp + 1

        rows = np.sort(np.array(list(set(rows)), dtype = np.int64))
        cols = np.sort(np.array(list(set(cols)), dtype = np.int64))

        self._modified_data = self._set_grid(
            self._data, rows, cols, np.array(linecolor, dtype = np.uint8)
        )

    def remove_grid(self):
        '''
            Resets the video and removes any grids added during the program
            runtime (i.e. not included in the loaded video.)
        '''
        self._modified_data = self._data.copy()

    # CREATING/SAVING IMAGES AND VIDEO
    def show(self, frame:int) -> None:
        '''
            Displays a single video frame using matplotlib.pyplot
        '''
        # Check that 'frame' is an integer value
        if not isinstance(frame, int):
            msg = 'Parameter \'frame\' expects an <int>'
            raise TypeError(msg)

        # Extract the specified frame
        image = self.__getitem__(frame)

        # Display the image
        plt.style.use('dark_background')
        plt.imshow(image)
        plt.axis(False)
        plt.show()

    def save_frame(
    self, frame:int, filename:str = None, extension:str = None,
    directory:Path = None) -> None:
        '''
            Saves a single video frame to file using matplotlib.pyplot.
        '''
        err_msg = (
            'The method `save_frame` for class `Video` requires that argument '
            '`{}` be of <class \'{}\'>.'
        )

        if filename is None:
            filename = create_unique_name(prefix = self._filename)

        if extension is None:
            extension = defaults.image_extension

        if directory is None:
            directory = paths.image_output

        if not isinstance(frame, int):
            raise TypeError(err_msg.format('frame', 'int'))

        if not isinstance(filename, str):
            raise TypeError(err_msg.format('filename', 'str'))

        if not isinstance(extension, str):
            raise TypeError(err_msg.format('extension', 'str'))

        if not isinstance(directory, Path):
            raise TypeError(err_msg.format('directory', 'Path'))

        if frame < -self._data.shape[0] or frame >= self._data.shape[0]:
            msg = (
                f'The method `save_frame` for class `Video` requires that '
                f'argument `frame` be an integer in range '
                f'[{-self._data.shape[0]:d}, {self._data.shape[0]-1:d}].'
            )
            raise ValueError(msg)

        path = (directory / filename).with_suffix(extension)

        # Check that 'frame' is an integer value
        if not isinstance(frame, int):
            msg = 'Parameter \'frame\' expects an <int>'
            raise TypeError(msg)

        # Extract the specified frame
        image = self.__getitem__(frame)

        # Save the image
        plt.imsave(path, image)

    def save(
    self, filename:str = None, fps:int = None, extension:str = None,
    directory:Path = None) -> None:
        '''
            Saves the entire video to file, defaults to directory:
                'Videos/Gridvid/Program Output/Videos/'
        '''
        err_msg = (
            'The method `save` for class `Video` requires that argument `{}` '
            'be of <class \'{}\'>.'
        )

        if filename is None:
            filename = create_unique_name(prefix = self._filename)

        if fps is None:
            fps = self._fps

        if extension is None:
            extension = self._default_extension

        if directory is None:
            directory = paths.finished_videos

        if not isinstance(filename, str):
            raise TypeError(err_msg.format('filename', 'str'))

        if not isinstance(fps, int):
            raise TypeError(err_msg.format('fps', 'int'))

        if not isinstance(extension, str):
            raise TypeError(err_msg.format('extension', 'str'))

        if not isinstance(directory, Path):
            raise TypeError(err_msg.format('directory', 'Path'))

        path = directory / (filename + extension)

        with imageio.get_writer(path, fps = fps) as writer:
            for frame in self.__iter__():
                writer.append_data(frame)

    # REMOVING FILES
    @classmethod
    def clear_temporary_files(cls) -> None:
        '''
            Clears the files stored in the temporary directory – location:
                `~/Videos/Gridvid/Program Output/.temporary files/`
        '''
        files = paths.temp_video_directory.glob('*')
        for f in files:
            os.remove(f)

    # PRIVATE METHODS
    @staticmethod
    @njit(cache = True, parallel = True)
    def _set_grid(
    video:np.ndarray, rows:np.ndarray, cols:np.ndarray,
    color:np.ndarray) -> np.ndarray:
        '''
            Private method for replacing the required pixels in `video` with the
            given RGB tuple `color`.
        '''
        for frame in prange(video.shape[0]):
            for row in rows:
                video[frame,row,:] = color
            for col in cols:
                video[frame,:,col] = color

        return video
