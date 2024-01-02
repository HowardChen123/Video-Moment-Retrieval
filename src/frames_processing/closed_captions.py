import re
import numpy as np
from datetime import datetime
from intervaltree import IntervalTree

class ClosedCaptionMatcher:
    def __init__(self, srt_file, video_segments):
        self.srt_file = srt_file
        self.video_segments = video_segments
        self.subtitles = self.parse_srt()

    def parse_srt(self):
        with open(self.srt_file, 'r') as file:
            content = file.read()

        patterns = re.compile(r'\d+\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n', re.DOTALL)
        subtitles = patterns.findall(content)
        return [(start.replace(',', '.'), end.replace(',', '.'), text.replace('\n', ' ')) for start, end, text in subtitles]

    @staticmethod
    def time_to_seconds(time_str):
        return datetime.strptime(time_str, '%H:%M:%S.%f').timestamp()

    def match_captions_to_segments(self):
        tree = IntervalTree()
        
        # Insert captions into the interval tree
        for start, end, text in self.subtitles:
            start_sec = self.time_to_seconds(start)
            end_sec = self.time_to_seconds(end)
            tree[start_sec:end_sec] = text

        segment_captions = {}
        for segment_start, segment_end in self.video_segments:
            start_sec = self.time_to_seconds(segment_start)
            end_sec = self.time_to_seconds(segment_end)
            overlapping_captions = tree[start_sec:end_sec]

            # Sort intervals by their start time
            sorted_captions = sorted(overlapping_captions, key=lambda interval: interval.begin)
            captions = [interval.data for interval in sorted_captions]
            segment_captions[(segment_start, segment_end)] = ' '.join(captions)

        return segment_captions

if __name__ == "__main__":

    # Example usage
    srt_file = 'example/algorithm_video/[English (auto-generated)] Top 5 Most Common Graph Algorithms for Coding Interviews [DownSub.com].srt'
    video_segments = np.load("example/algorithm_video/transnetv2/scenes_timestamp.npy")

    caption_matcher = ClosedCaptionMatcher(srt_file, video_segments)
    captions_for_segments = caption_matcher.match_captions_to_segments()

    # Example: Print captions for the first segment
    first_segment = video_segments[0]
    print(first_segment)
    print(f"Captions for segment {first_segment}:")
    print(captions_for_segments[tuple(first_segment)])