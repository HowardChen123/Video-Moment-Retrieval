from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage
import base64
import os

def get_openai_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.readline().strip()
os.environ["OPENAI_API_KEY"] = get_openai_api_key("api_key.txt")

class ImageAnalyzer:
    def __init__(self, api_key_file='api_key.txt', model_name="gpt-4-vision-preview", max_tokens=600):
        self.model = ChatOpenAI(model=model_name, max_tokens=max_tokens)

    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_images(self, image_paths):
        image_messages = []
        for image_path in image_paths:
            base64_image = self.encode_image(image_path)
            image_messages.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})
        msg = self.model.invoke(
            [
                HumanMessage(
                    content=[
                        {"type": "text", "text": "Review these multiple images, which represent frames from a scene, and use a chain-of-thought approach to infer the scene's overall theme or story. Start by briefly noting any common elements or recurring themes across the images. Then, consider what these elements or themes suggest about the video's content. Are there any patterns or consistent messages? Finally, based on these observations, synthesize a summary of the video's likely narrative or main topic. Focus on the overarching story the images collectively convey."},
                        *image_messages
                    ]
                )
            ]
        )
        return msg.content

if __name__ == "__main__":
    # Example usage
    image_analyzer = ImageAnalyzer()
    image_paths = [
        "example/algorithm_video/transnetv2/segments/2/frames/frame_0.jpg",
        "example/algorithm_video/transnetv2/segments/2/frames/frame_8559.jpg"
    ]
    result = image_analyzer.analyze_images(image_paths)
    print(result)