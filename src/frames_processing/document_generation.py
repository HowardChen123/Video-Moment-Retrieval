import sys
sys.path.append('src/frames_processing')

import os
from closed_captions import ClosedCaptionMatcher
from frames_description import ImageAnalyzer

class DocumentGenerator:
    def __init__(self, caption_matcher, image_analyzer, folder_path):
        self.caption_matcher = caption_matcher
        self.image_analyzer = image_analyzer
        self.folder_path = folder_path

    @staticmethod
    def save_document(doc, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

        with open(file_path, 'w') as file:
            file.write(f"Segment: {doc['segment']}\n")
            file.write(f"Time Interval: {', '.join(doc['time_interval'])}\n")
            file.write(f"Closed Captions:\n{doc['closed_captions']}\n")
            file.write(f"Image Analysis:\n{doc['image_analysis']}")

    def generate_documents(self):
        documents = []
        captions_for_segments = self.caption_matcher.match_captions_to_segments()
        for segment in os.listdir(self.folder_path):
            segment_path = os.path.join(self.folder_path, segment, 'frames')
            if os.path.isdir(segment_path):
                image_paths = [os.path.join(segment_path, img) for img in os.listdir(segment_path) if img.endswith('.jpg')]
                image_analysis_result = self.image_analyzer.analyze_images(image_paths)

                # Assuming video_segments is a list of tuples (start, end) for each segment
                segment_index = int(segment) - 1
                time_interval = self.caption_matcher.video_segments[segment_index]
                cc_result = captions_for_segments[tuple(time_interval)]

                document = {
                    "segment": int(segment),
                    "time_interval": time_interval,
                    "closed_captions": cc_result,
                    "image_analysis": image_analysis_result
                }
                documents.append(document)
                DocumentGenerator.save_document(document, os.path.join(self.folder_path, segment, 'document.txt'))

        return documents


if __name__ == "__main__":
    # Example usage
    import numpy as np
    srt_file = 'example/algorithm_video/[English (auto-generated)] Top 5 Most Common Graph Algorithms for Coding Interviews [DownSub.com].srt'
    video_segments = np.load("example/algorithm_video/transnetv2/scenes_timestamp.npy")

    caption_matcher = ClosedCaptionMatcher(srt_file, video_segments)
    image_analyzer = ImageAnalyzer()

    folder_path = 'example/algorithm_video/transnetv2/segments'
    doc_generator = DocumentGenerator(caption_matcher, image_analyzer, folder_path)
    documents = doc_generator.generate_documents()