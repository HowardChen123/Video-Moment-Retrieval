import subprocess
import numpy as np
import os

# Your 2D numpy array with timestamps
timestamps = np.load("example/algorithm_video/transnetv2/scenes_timestamp.npy")

input_video = 'example/algorithm_video/Top 5 Most Common Graph Algorithms for Coding Interviews.mp4'
base_directory = 'example/algorithm_video/transnetv2/segments/'

# Loop through each timestamp pair and create segments
for i, (start, end) in enumerate(timestamps, 1):
    segment_directory = os.path.join(base_directory, str(i))
    
    # Ensure the segment directory exists
    if not os.path.exists(segment_directory):
        os.makedirs(segment_directory)

    output_segment = os.path.join(segment_directory, f'segment_{i:02}.mp4')
    
    # FFmpeg command to segment the video
    command = [
        'ffmpeg', '-i', input_video,
        '-ss', start,
        '-to', end,
        '-c', 'copy',
        output_segment
    ]

    # Execute the command
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print(f'Segment {i} created: {output_segment}')