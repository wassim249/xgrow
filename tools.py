import io
import os

import requests
from PIL import Image
from langchain.tools import tool

from xposter import XPoster


class XTools:
    @tool("Generate art image")
    def generate_image(prompt: str) -> str:
        """Generates an image from a prompt
        Args:
            prompt (str): The prompt to generate the image from.
        Returns:
            str: The path to the generated image
        """
        if os.path.exists(os.path.abspath(f"data/images/{prompt}.jpg")):
            return os.path.abspath(f"data/images/{prompt}.jpg")
        if not os.path.exists("data/images"):
            os.makedirs("data/images")
        api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

        def query(payload):
            response = requests.post(api_url, headers=headers, json=payload)
            return response.content

        threed_style = 'cute modern disney style, Pixar 3d portrait, ultra detailed, gorgeous, 8k render, cinematic lighting,aesthetic,beautiful,technology,ambient background,orange yellow theme'
        pixel_art_style = 'pixel-art, blocky, pixel art style, 8-bit graphics, colorful,aesthetic'
        image_bytes = query({
            "inputs": f'{prompt} {threed_style}',
            "negative_prompts": "horror, dark, scary, creepy, evil, sinister, spooky, terrifying, frightening"
        })
        image = Image.open(io.BytesIO(image_bytes))
        abs_path = os.path.abspath(f"data/images/{prompt}.jpg")
        image.save(abs_path)

        print(f"Image generated from prompt: {prompt}")

        return abs_path

    @staticmethod
    @tool("Verify tweet length")
    def verify_tweet_length(tweet_text: str) -> bool:
        """Verifies if the tweet text length is less than or equal to 280 characters
        args:
        tweet_text (str): The tweet post-content

        returns:
        bool: If the tweet text length is less than or equal to 280 characters or not

        """
        if len(tweet_text) <= 280:
            print("Tweet length is less than or equal to 280 characters")
            return True
        else:
            print("Tweet length is more than 280 characters")
            return False

    @staticmethod
    @tool("Post tweet on twitter")
    def post_tweet(tweet_text: str, thumbnail_path: str) -> str:
        """Adds a tweet to the Twitter account
        args:
        tweet_text (str): The tweet post-content
        thumbnail_path (str): The tweet post thumbnail image

        returns:
        str: If the tweet has been posted successfully or not

        """
        output = (XPoster(username=os.getenv("X_USERNAME"), password=os.getenv("X_PASSWORD"))
                  .post_tweet(tweet_text, thumbnail_path))

        return output