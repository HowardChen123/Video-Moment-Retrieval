import numpy as np
import json

class SceneTimestampConverter:
    def __init__(self, scenes, timestamps):
        self.scenes = scenes
        self.timestamps_map = timestamps
        self.result_array = np.empty(self.scenes.shape, dtype=object)

    def convert_timestamps(self):
        for i in range(self.scenes.shape[0]):
            for j in range(self.scenes.shape[1]):
                key = self.scenes[i, j]
                if key not in self.timestamps_map:
                    key = key - 1 if j == 1 else key + 1
                self.result_array[i, j] = self.timestamps_map.get(key, "Key not found")
        self.result_array[0, 0] = 0.0
        return np.vectorize(self.seconds_to_hh_mm_ss_mmm)(self.result_array)

    @staticmethod
    def seconds_to_hh_mm_ss_mmm(seconds):
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        return '{:02}:{:02}:{:02}.{:03}'.format(hours, minutes, int(seconds), milliseconds)


if __name__ == "__main__":
    # Example usage
    scenes_file = "example/algorithm_video/transnetv2/scenes.npy"
    scenes = np.load(scenes_file)

    timestamps_file = 'example/algorithm_video/transnetv2/frameID_timestamps.json'
    def load_timestamps(file_path):
        with open(file_path, 'r') as file:
            timestamps_map = json.load(file)
        return {int(key): value for key, value in timestamps_map.items()}
    frameID_timestamps = load_timestamps(timestamps_file)

    converter = SceneTimestampConverter(scenes, frameID_timestamps)
    converted_array = converter.convert_timestamps()
    print(converted_array)