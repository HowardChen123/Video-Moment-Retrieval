from transnetv2 import TransNetV2

class VideoSceneDetector:
    def __init__(self, video_path):
        self.video_path = video_path
        self.model = TransNetV2()

    def detect_scenes(self):
        _, single_frame_predictions, _ = self.model.predict_video(self.video_path)
        scenes = self.model.predictions_to_scenes(single_frame_predictions)
        return scenes

# Example usage
if __name__ == "__main__":
    # video_path = "example/algorithm_video/Top 5 Most Common Graph Algorithms for Coding Interviews.mp4"
    video_path = "example/MSR-VTT-1kA/test_1k_compress/video7020.mp4"
    scene_detector = VideoSceneDetector(video_path)
    scenes = scene_detector.detect_scenes()
    print(scenes)

    # import numpy as np
    # np.save("example/algorithm_video/transnetv2/scenes.npy", scenes)
