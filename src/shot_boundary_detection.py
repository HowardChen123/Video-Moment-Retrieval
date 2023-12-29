from transnetv2 import TransNetV2

model = TransNetV2()
video_frames, single_frame_predictions, all_frame_predictions = \
    model.predict_video("/path/to/video.mp4")