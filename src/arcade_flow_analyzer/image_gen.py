"""
Generate images based on user journey summaries using LangChain DALL-E integration.
"""

import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

load_dotenv()

def generate_flow_image():
    """Generate a creative image based on the user journey summary"""

    if not os.getenv('OPENAI_API_KEY'):
        print("Please create a .env file with: OPENAI_API_KEY=your_api_key_here")
        return

    summary_file = 'cache/ai-summary-chain.txt'

    if not os.path.exists(summary_file):
        print("Please run summarize_actions() first to generate the summary")
        return

    with open(summary_file, 'r') as f:
        user_journey = f.read().strip()

    if not user_journey:
        print("Summary file is empty")
        return

    base_prompt = """Generate a creative image suitable for sharing on social platforms that represents the user flow/journey and would drive engagement. Here is a summary of the user journey: {user_journey}"""

    # Set up the LLM and chain using LangChain approach
    llm = OpenAI(temperature=0.9)
    prompt_template = PromptTemplate(
        input_variables=["image_desc"],
        template="Generate a detailed prompt to generate an image based on the following description: {image_desc}",
    )
    chain = LLMChain(llm=llm, prompt=prompt_template)

    # Generate the image description
    image_description = chain.run(image_desc=base_prompt.format(user_journey=user_journey))

    print("Generated Image Description:")
    print(image_description)

    # Generate the image using DALL-E
    print("Generating image with DALL-E")
    try:
        dalle = DallEAPIWrapper()
        image_url = dalle.run(image_description)

        print(f"Image URL: {image_url}")

        # Save the image description for reference
        with open('cache/image-description.txt', 'w') as f:
            f.write(image_description)

        return image_description, image_url
        
    except Exception as e:
        print(f"Error generating image: {e}")
        return image_description, None


if __name__ == "__main__":
    generate_flow_image()