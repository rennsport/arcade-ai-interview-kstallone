"""
Generate images based on user journey
summaries using LangChain DALL-E integration.
"""

import os
import requests
from dotenv import load_dotenv
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

load_dotenv()


def download_image_from_url(url, filepath):
    """Download image from URL and save to filepath"""
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"Image downloaded successfully to: {filepath}")
        return True
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False


def generate_flow_image(force_regenerate=False):
    """Generate a creative image based on the user journey summary"""

    if not os.getenv('OPENAI_API_KEY'):
        print("Please create a .env file with: OPENAI_API_KEY=your_api_key_here")
        return

    summary_file = 'cache/ai-summary-chain.txt'
    image_desc_cache = 'cache/image/image-description.txt'
    image_url_cache = 'cache/image/image-url.txt'
    image_file = 'cache/image/generated-image.png'

    if not os.path.exists(summary_file):
        print("Please run summarize_actions() first to generate the summary")
        return

    # Ensure cache/image directory exists
    os.makedirs('cache/image', exist_ok=True)

    # Check for cached image description and URL
    if not force_regenerate and os.path.exists(image_desc_cache) and os.path.exists(image_url_cache):
        print("Using cached image description and URL:")
        with open(image_desc_cache, 'r') as f:
            cached_description = f.read()
        with open(image_url_cache, 'r') as f:
            cached_url = f.read()

        print("=" * 60)
        print(f"CACHED IMAGE DESCRIPTION: {cached_description}")
        print(f"CACHED IMAGE URL: {cached_url}")
        print("=" * 60)

        if os.path.exists(image_file):
            print(f"Image file found at: {image_file}")
        else:
            print("Image file not found, downloading...")
            download_image_from_url(cached_url, image_file)

        return cached_description, cached_url

    with open(summary_file, 'r') as f:
        user_journey = f.read().strip()

    if not user_journey:
        print("Summary file is empty")
        return

    base_prompt = """Generate a creative image suitable for sharing on social platforms that represents the user flow/journey and would drive engagement. It should be a single image, that captures  the essence of how easy it is to shop on Target.com. Don't use words in the image. Here is a summary of the user journey: {user_journey}"""

    # DALL-E with LangChain
    # https://docs.langchain.com/oss/python/integrations/tools/dalle_image_generator

    llm = OpenAI(temperature=0.9)
    prompt_template = PromptTemplate(
        input_variables=["image_desc"],
        template="Generate a prompt to generate a creative image suitable for sharing on social platforms that represents the user flow/journey. Don't use words in the image. Limit prompt to 1000 characters including whitespace: {image_desc}",
    )

    # Generate the image description using modern LangChain approach
    chain = prompt_template | llm
    image_description = chain.invoke({"image_desc": base_prompt.format(user_journey=user_journey)})

    print("Generated Image Description:")
    print(image_description)

    # Generate the image using DALL-E
    print("Generating image with DALL-E")
    try:
        dalle = DallEAPIWrapper()
        image_url = dalle.run(image_description)

        print(f"Image URL: {image_url}")

        # Save all cached data
        with open(image_desc_cache, 'w') as f:
            f.write(image_description)

        with open(image_url_cache, 'w') as f:
            f.write(image_url)

        print("Downloading image")
        download_image_from_url(image_url, image_file)

        print("=" * 60)
        print(f"GENERATED IMAGE DESCRIPTION: {image_description}")
        print(f"IMAGE URL: {image_url}")
        print(f"IMAGE FILE PATH: {image_file}")
        print("=" * 60)

        return image_description, image_url

    except Exception as e:
        print(f"Error generating image: {e}")
        return image_description, None


if __name__ == "__main__":
    generate_flow_image()
