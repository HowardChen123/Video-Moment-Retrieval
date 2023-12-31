from scenedetect import detect, AdaptiveDetector, ContentDetector, ThresholdDetector
import cv2
import numpy as np
import os
import shutil

def find_scenes(video_path):
    scene_list = detect(video_path, ContentDetector())
    return scene_list

def extract_frames(video_path, scenes, folder_path, total_limit=5):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Clean up the folder path
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)

    # Extract the first frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(os.path.join(folder_path, 'frame_start.jpg'), frame)

    # Calculate the interval for frame extraction, excluding the first and last frames
    interval = max(1, (total_frames - 2) // (total_limit - 2))
    extracted_count = 1

    for start_time, end_time in scenes:
        if extracted_count >= total_limit - 1:
            break
        start_frame = max(1, int(start_time.get_frames()) + 1)  # Skip the first frame
        end_frame = min(total_frames - 2, int(end_time.get_frames()) - 1)  # Skip the last frame

        for frame_num in range(start_frame, end_frame, interval):
            if extracted_count >= total_limit - 1:
                break
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(os.path.join(folder_path, f'frame_{frame_num}.jpg'), frame)
                extracted_count += 1

    # Extract the last frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(os.path.join(folder_path, 'frame_end.jpg'), frame)

    cap.release()

if __name__ == "__main__":
    for i in range(1, 12):
        # Video file path
        video_file_path = f'example/algorithm_video/transnetv2/segments/{i}/segment_{i}.mp4'
        folder_path = f'example/algorithm_video/transnetv2/segments/{i}/frames/'

        # Find scenes with an adjusted threshold if necessary
        scenes = find_scenes(video_file_path)  # Adjust the threshold value as needed

        # Extract frames with specified number or fallback to start, end, and between
        extract_frames(video_file_path, scenes, folder_path)