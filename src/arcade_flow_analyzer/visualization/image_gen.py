"""
Generate images based on user journey summaries using OpenAI's 4o image generation API.
"""

import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
import base64

load_dotenv()


# def download_image_from_url(url, filepath):
#     """Download image from URL and save to filepath"""
#     try:
#         response = requests.get(url)
#         response.raise_for_status()

#         with open(filepath, 'wb') as f:
#             f.write(response.content)

#         print(f"Image downloaded successfully to: {filepath}")
#         return True
#     except Exception as e:
#         print(f"Error downloading image: {e}")
#         return False


def generate_flow_image(force_regenerate=False):
    """Generate a creative image based on the user journey summary"""

    if not os.getenv('OPENAI_API_KEY'):
        print("Please create a .env file with: OPENAI_API_KEY=your_api_key_here")
        return

    summary_file = 'cache/ai-summary-chain.txt'
    marketing_image_file = 'cache/image/marketing-image.png'

    if not os.path.exists(summary_file):
        print("Please run summarize_actions() first to generate the summary")
        return

    os.makedirs('cache/image', exist_ok=True)

    # Use cached marketing image if available
    if not force_regenerate and os.path.exists(marketing_image_file):
        print(f"Using cached marketing image: {marketing_image_file}")
        return

    with open(summary_file, 'r') as f:
        user_journey = f.read().strip()

    if not user_journey:
        print("Summary file is empty")
        return

    client = OpenAI()

    prompt = f"""
    You are an expert at marketing and design. Generate a creative image suitable for sharing on social platforms that represents the user flow/journey and would drive engagement. It should be a single image, that captures the essence of how easy it is do what is described in the user journey. Here is a summary of the user journey: {user_journey}
    """

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    # Save the image to cache
    with open(marketing_image_file, "wb") as f:
        f.write(image_bytes)


if __name__ == "__main__":
    generate_flow_image()