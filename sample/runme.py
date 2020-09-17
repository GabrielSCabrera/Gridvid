'''
    EXAMPLE SCRIPT
    Royalty-free video downloaded from:
    https://pexels.com/photo/traffic-on-an-intersection-road-in-a-city-3121459/

    This script loads the video file called `video_sample.mp4`, located in the
    same directory as this script.

    Next, it creates a grid of 5x5 lines (not including the borders) and saves
    the new data to the file `grid_sample.mp4`.
'''
from gridvid import Video
from pathlib import Path

directory = Path('')
video = Video.from_file(filename = 'video_sample.mp4', directory = directory)
video.create_grid((5,9))
video.save(filename = 'grid_sample', directory = directory)
