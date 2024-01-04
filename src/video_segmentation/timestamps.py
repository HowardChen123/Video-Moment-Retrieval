import ffmpeg
import re
import json

class FrameTimestampMapper:
    def __init__(self, video_fn):
        self.video_fn = video_fn

    def extract_frames(self):
        # Run FFmpeg with the showinfo filter
        _, out = (
            ffmpeg
            .input(self.video_fn)
            .output('pipe:', format='rawvideo', pix_fmt='rgb24', s='48x27', vf='showinfo')
            .run(capture_stdout=True, capture_stderr=True)
        )
        # Decode stdout for processing
        out = out.decode('utf-8')
        return out

    def parse_frame_info(self, output):
        # Regular expression to match showinfo output lines with frame information
        regex = r"n:\s*(\d+).+pts_time:(\d+\.\d+)"
        # Parse the output to extract frame numbers and timestamps
        frame_info = re.findall(regex, output)
        return {int(info[0]): float(info[1]) for info in frame_info}

    def save_to_json(self, frame_data, output_fn):
        with open(output_fn, 'w') as f:
            json.dump(frame_data, f)

if __name__ == "__main__":
    # Example usage
    video_fn = "example/algorithm_video/Top 5 Most Common Graph Algorithms for Coding Interviews.mp4"
    output_fn = 'example/algorithm_video/transnetv2/frameID_timestamps.json'

    extractor = FrameTimestampMapper(video_fn)
    output = extractor.extract_frames()
    frame_data = extractor.parse_frame_info(output)
    print(frame_data)
    # extractor.save_to_json(frame_data, output_fn)