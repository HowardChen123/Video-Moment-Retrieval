import sys
sys.path.append('src/frames_processing')
sys.path.append('src/information_retrieval')

import pandas as pd
df = pd.read_csv("example/MSR-VTT-1kA/MSRVTT_JSFUSION_test_sample.csv")
print(df.head())
print(df[['video_id', 'video_path', 'sentence']].head())

# from frames_extraction import SceneFrameExtractor
# from frames_description import ImageAnalyzer
import os

# for video in df['video_id']:
#     print(video)
#     video_file_path = f'example/MSR-VTT-1kA/test_1k_compress/{video}.mp4'
#     folder_path = f'example/MSR-VTT-1kA/documents/{video}/frames/'
#     extractor = SceneFrameExtractor(video_file_path, folder_path)
#     scenes = extractor.find_scenes()
#     extractor.extract_frames(scenes)
    
# image_analyzer = ImageAnalyzer()

# for video in df['video_id']:
#     folder_path = f'example/MSR-VTT-1kA/documents/{video}/frames/'

#     with open(os.path.join(folder_path, 'document.txt'), 'r') as file:
#         content = file.read()

#     # Count the number of characters
#     num_characters = len(content)

#     # Check if the content has less than 200 characters
#     if num_characters < 100:
#         print(os.path.join(folder_path, 'document.txt'))
#         def save_document(doc, file_path):
#             if os.path.exists(file_path):
#                 os.remove(file_path)

#             with open(file_path, 'w') as file:
#                 file.write(doc)
#         print(video)
#         if os.path.isdir(folder_path):
#             image_paths = [os.path.join(folder_path, img) for img in os.listdir(folder_path) if img.endswith('.jpg')]
#             image_analysis_result = image_analyzer.analyze_images(image_paths)
#             save_document(image_analysis_result, os.path.join(folder_path, 'document.txt'))
    
from information_retrieval import DocumentSearcher
document_searcher = DocumentSearcher('example/MSR-VTT-1kA/documents')
df['top1'] = ''
df['top5'] = ''
df['top10'] = ''

for index, row in df.iterrows():
    top1_doc = document_searcher.search_documents(row['sentence'], k=1)
    top1 = top1_doc[0].metadata['source'].split('/')[3] if top1_doc else 'N/A'
    df.at[index, 'top1'] = top1

    top5_doc = document_searcher.search_documents(row['sentence'], k=5)
    top5 = [doc.metadata['source'].split('/')[3] for doc in top5_doc] if top5_doc else ['N/A']
    df.at[index, 'top5'] = top5

    top10_doc = document_searcher.search_documents(row['sentence'], k=10)
    top10 = [doc.metadata['source'].split('/')[3] for doc in top10_doc] if top10_doc else ['N/A']
    df.at[index, 'top10'] = top10

df[['video_id', 'video_path', 'sentence', 'top1', 'top5', 'top10']].to_csv("example/result.csv")

print(df[['video_id', 'video_path', 'sentence', 'top1', 'top5', 'top10']].head())

df = pd.read_csv("example/result.csv")

def calculate_recall(df, column_name):
    correct_matches = sum(row['video_id'] in row[column_name] for _, row in df.iterrows())
    total_ground_truths = len(df)
    return correct_matches / total_ground_truths if total_ground_truths > 0 else 0

recall_top1 = calculate_recall(df, 'top1')
recall_top5 = calculate_recall(df, 'top5')
recall_top10 = calculate_recall(df, 'top10')

print(recall_top1)
print(recall_top5)
print(recall_top10)
