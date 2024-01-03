from openai import OpenAI
from moviepy.editor import *
import os

def get_openai_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.readline().strip()
os.environ["OPENAI_API_KEY"] = get_openai_api_key("api_key.txt")

class VideoToTranscript:
    def __init__(self, video_path):
        self.video_path = video_path
        self.client = OpenAI()

    def extract_audio(self):
        video = VideoFileClip(self.video_path)
        return video.audio

    def transcribe_audio(self, audio):
        transcript = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio
        )
        return transcript

if __name__ == "__main__":
  # Example usage
  video_transcriber = VideoToTranscript("example/MSR-VTT-1kA/test_1k_compress/video7026.mp4")
  audio = video_transcriber.extract_audio()
  transcript = video_transcriber.transcribe_audio(audio)
  print(transcript)