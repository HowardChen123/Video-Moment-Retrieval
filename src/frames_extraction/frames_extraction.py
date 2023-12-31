from scenedetect import detect, AdaptiveDetector, ContentDetector, ThresholdDetector
import cv2
import numpy as np
import os
import shutil

def find_scenes(video_path):
    scene_list = detect(video_path, ContentDetector())
    return scene_list

def extract_frames(video_path, scenes, folder_path, num_frames=5):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Clean up the folder path
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)

    if scenes:
        for start_time, end_time in scenes:
            start_frame = int(start_time.get_frames())
            end_frame = int(end_time.get_frames())

            for frame_num in range(start_frame, end_frame + 1):
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                ret, frame = cap.read()
                if ret:
                    cv2.imwrite(os.path.join(folder_path, f'frame_{frame_num}.jpg'), frame)
    else:
        # No scenes detected: Extract frames at start, end, and evenly spaced in between
        interval = total_frames // (num_frames - 1)
        for i in range(num_frames):
            frame_num = min(i * interval, total_frames - 1)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(os.path.join(folder_path, f'frame_{frame_num}.jpg'), frame)

    cap.release()

# Video file path
video_file_path = 'example/algorithm_video/transnetv2/segments/1/segment_01.mp4'
folder_path = 'example/algorithm_video/transnetv2/segments/1/frames/'

# Find scenes with an adjusted threshold if necessary
scenes = find_scenes(video_file_path)  # Adjust the threshold value as needed

# Extract frames with specified number or fallback to start, end, and between
extract_frames(video_file_path, scenes, folder_path, num_frames=5)