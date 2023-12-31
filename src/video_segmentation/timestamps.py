import ffmpeg
import re
import json

video_fn = "example/algorithm_video/Top 5 Most Common Graph Algorithms for Coding Interviews.mp4"

# Run FFmpeg with the showinfo filter
_, out = (
    ffmpeg
    .input(video_fn)
    .output('pipe:', format='rawvideo', pix_fmt='rgb24', s='48x27', vf='showinfo')
    .run(capture_stdout=True, capture_stderr=True)
)

# Decode stdoutv for processing
out = out.decode('utf-8')

# Regular expression to match showinfo output lines with frame information
regex = r"n:\s*(\d+).+pts_time:(\d+\.\d+)"

# Parse the stderr output to extract frame numbers and timestamps
frame_info = re.findall(regex, out)
frame_numbers = [int(info[0]) for info in frame_info]
timestamps = [float(info[1]) for info in frame_info]

dictionary = {key: value for key, value in zip(frame_numbers, timestamps)}
with open('example/algorithm_video/transnetv2/frameID_timestamps.json', 'w') as f:
    json.dump(dictionary, f)