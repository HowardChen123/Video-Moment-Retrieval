import pandas as pd
import os

raw_video_path = 'example/MSR-VTT-1kA/test_1k_compress' # 1k test video path.
test_csv_path = 'example/MSR-VTT-1kA/MSRVTT_JSFUSION_test.csv' # 1k video caption csv.

test_sample_csv_path = 'example/MSR-VTT-1kA/MSRVTT_JSFUSION_test_sample.csv'

sample_num = 100 # you can change this sample_num to be smaller, so that this notebook will be faster.
test_df = pd.read_csv(test_csv_path)
print('length of all test set is {}'.format(len(test_df)))
sample_df = test_df.sample(sample_num, random_state=42)

sample_df['video_path'] = sample_df.apply(lambda x:os.path.join(raw_video_path, x['video_id']) + '.mp4', axis=1)

sample_df.to_csv(test_sample_csv_path)
print('random sample {} examples'.format(sample_num))

df = pd.read_csv(test_sample_csv_path)

print(df[['video_id', 'video_path', 'sentence']].head())