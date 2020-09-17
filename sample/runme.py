'''
    EXAMPLE SCRIPT

    This script loads the video file called `your_video.mp4`, which should be
    placed in the same directory as this script.

    Next, it creates a grid of 5x5 lines (not including the borders) and saves
    the new data to the file `grid_sample.mp4`.
'''
from gridvid import Video
from pathlib import Path

filename = 'your_video.mp4'

directory = Path('')
video = Video.from_file(filename = filename, directory = directory)
video.create_grid((5,9))
video.save(filename = 'grid_sample', directory = directory)
