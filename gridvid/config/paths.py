from pathlib import Path

from gridvid.config import defaults

# Main storage directory in `Home/`
package_data = Path.home() / defaults.data_directory

# User-accessible data storage directory in 'Home/Videos/'
user_data = Path.home() / defaults.main_directory / defaults.user_directory

# Directory into which program outputs are saved
output_data = user_data / defaults.outputs_directory

# Directory from which user data is read
input_data = user_data / defaults.inputs_directory

# Where videos are saved after the grid is added
finished_videos = output_data / defaults.finished_videos_directory

# Where images are saved
image_output = output_data / defaults.image_output_directory

# Directory from which user videos are loaded
input_videos = input_data / defaults.input_video_directory

# Directory where videos are temporarily stored
temp_video_directory = output_data / defaults.temp_video_directory

# If necessary, creates the above directories on module initialization
package_data.mkdir(exist_ok = True)
user_data.mkdir(exist_ok = True)
output_data.mkdir(exist_ok = True)
input_data.mkdir(exist_ok = True)
finished_videos.mkdir(exist_ok = True)
image_output.mkdir(exist_ok = True)
input_videos.mkdir(exist_ok = True)
temp_video_directory.mkdir(exist_ok = True)
