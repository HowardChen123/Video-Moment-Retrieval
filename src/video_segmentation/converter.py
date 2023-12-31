import numpy as np

scenes = np.load("example/algorithm_video/transnetv2/scenes.npy")

print(scenes)

import json

file_path = 'example/algorithm_video/transnetv2/frameID_timestamps.json'

with open(file_path, 'r') as file:
    timestamps_map = json.load(file)
timestamps_map = {int(key): value for key, value in timestamps_map.items()}

result_array = np.empty(scenes.shape, dtype=object)

for i in range(scenes.shape[0]):
    for j in range(scenes.shape[1]):
        key = scenes[i, j]
        if key not in timestamps_map:
            if j == 1:
                key -= 1
            if j == 2:
                key += 1
        result_array[i, j] = timestamps_map.get(key, "Key not found")
result_array[0, 0] = 0.0

def seconds_to_hh_mm_ss_mmm(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds_remainder = seconds % 60
    whole_seconds = int(seconds_remainder)
    milliseconds = int((seconds_remainder - whole_seconds) * 1000)
    return '{:02}:{:02}:{:02}.{:03}'.format(hours, minutes, whole_seconds, milliseconds)

# Apply the conversion to each element in the array
converted_array = np.vectorize(seconds_to_hh_mm_ss_mmm)(result_array)
np.save("example/algorithm_video/transnetv2/scenes_timestamp.npy", converted_array)

print(converted_array)