from transnetv2 import TransNetV2

model = TransNetV2()
video_frames, single_frame_predictions, all_frame_predictions = \
    model.predict_video("example/algorithm_video/Top 5 Most Common Graph Algorithms for Coding Interviews.mp4")

print(model.predictions_to_scenes(single_frame_predictions))

import numpy as np
np.save("example/algorithm_video/transnetv2/scenes.npy", model.predictions_to_scenes(single_frame_predictions))