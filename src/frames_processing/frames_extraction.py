from scenedetect import detect, ContentDetector
import cv2
import os
import shutil

class SceneFrameExtractor:
    def __init__(self, video_path, folder_path, total_limit=20):
        self.video_path = video_path
        self.folder_path = folder_path
        self.total_limit = total_limit

    def find_scenes(self):
        return detect(self.video_path, ContentDetector())

    def extract_frames(self, scenes):
        cap = cv2.VideoCapture(self.video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Clean up the folder path
        if os.path.exists(self.folder_path):
            shutil.rmtree(self.folder_path)
        os.makedirs(self.folder_path, exist_ok=True)

        # Extract the first frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(os.path.join(self.folder_path, 'frame_0.jpg'), frame)

        # Calculate the interval for frame extraction, excluding the first and last frames
        interval = max(1, (total_frames - 2) // (self.total_limit - 2))
        extracted_count = 1

        for start_time, end_time in scenes:
            if extracted_count >= self.total_limit - 1:
                break
            start_frame = max(1, int(start_time.get_frames()) + 1)  # Skip the first frame
            end_frame = min(total_frames - 2, int(end_time.get_frames()) - 1)  # Skip the last frame

            for frame_num in range(start_frame, end_frame, interval):
                if extracted_count >= self.total_limit - 1:
                    break
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                ret, frame = cap.read()
                if ret:
                    cv2.imwrite(os.path.join(self.folder_path, f'frame_{frame_num}.jpg'), frame)
                    extracted_count += 1

        # Extract the last frame
        end = total_frames - 1
        cap.set(cv2.CAP_PROP_POS_FRAMES, end)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(os.path.join(self.folder_path, f'frame_{end}.jpg'), frame)

        cap.release()

if __name__ == "__main__":
    # for i in range(1, 12):
    #     # Video file path
    #     video_file_path = f'example/algorithm_video/transnetv2/segments/{i}/segment_{i}.mp4'
    #     folder_path = f'example/algorithm_video/transnetv2/segments/{i}/frames/'

    #     # Find scenes with an adjusted threshold if necessary
    #     scenes = find_scenes(video_file_path)  # Adjust the threshold value as needed

    #     # Extract frames with specified number or fallback to start, end, and between
    #     extract_frames(video_file_path, scenes, folder_path)
    video_name = "video7020"
    video_file_path = f'example/MSR-VTT-1kA/test_1k_compress/{video_name}.mp4'
    folder_path = f'example/MSR-VTT-1kA/documents/{video_name}/frames/'

    extractor = SceneFrameExtractor(video_file_path, folder_path)
    scenes = extractor.find_scenes()
    extractor.extract_frames(scenes)