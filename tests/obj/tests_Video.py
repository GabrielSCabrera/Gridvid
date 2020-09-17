from gridvid import Video
from pathlib import Path
import numpy as np
import gridvid

def run_all() -> None:
    '''
        Runs all class Video tests;
        returns True if all tests succeed, False otherwise.
    '''
    data_path = gridvid.config.paths.temp_video_directory
    extension = '.mp4'
    filename = 'test_video'

    # Creating Video from Array
    video = Video.noise(100, (1024, 1024), 30, True, filename)
    video.default_extension = extension

    # Creating Video Grid
    video.create_grid((20,20), width = 1)

    # Saving Tenth Frame from Video
    video.save_frame(10)

    # Saving Video to File
    video.save(filename, directory = data_path)

    # Reloading Saved Video
    video_loaded = Video.from_file(filename + extension, data_path)

    # Clearing Temporary Files
    Video.clear_temporary_files()
