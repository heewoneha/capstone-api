"""OpenAI API service module."""

import requests
import openai
from typing import Optional
from app.services.constant import (
    BackgroundType,
    OPEN_AI_API_KEY,
    IMAGE_SIZE,
    EMPTY_BACKGROUND_BASE_IMAGE_PATH,
    IMAGE_MODEL_NAME,
)


def generate_background_image(background_type: BackgroundType, text: Optional[str], image_bytes: Optional[bytes]) -> bytes:
    """Generate a background image using OpenAI API.

    Args:
        background_type (BackgroundType): The type of background to generate.
        text (Optional[str]): The text prompt for the image generation.
        image_bytes (Optional[bytes]): The image data for the image generation.

    Raises:
        Exception: When the image generation fails, an exception is raised with the error message.
        Exception: Exception: When the image URL is not found in the OpenAI response.

    Returns:
        bytes: The generated background image in bytes.
    """
    client = openai.OpenAI(api_key=OPEN_AI_API_KEY)

    if background_type == BackgroundType.TEXT:
        response = client.images.generate(
            model=IMAGE_MODEL_NAME,
            prompt=text,
            n=1,
            size=IMAGE_SIZE,
        )
    elif background_type == BackgroundType.IMAGE:
        # Return the original image if the background type is RAW IMAGE
        return image_bytes
    elif background_type == BackgroundType.TEXT_IMAGE:
        response = client.images.edit(
            image=image_bytes,
            prompt=text,
            n=1,
            size=IMAGE_SIZE,
        )
    else:
        with open(EMPTY_BACKGROUND_BASE_IMAGE_PATH, "rb") as f:
            empty_image_bytes = f.read()
        return empty_image_bytes
    
    image_url = response.data[0].url

    if not image_url:
        error_message = "Failed to generate image URL from OpenAI response"
        raise Exception(error_message)
    
    try:
        image_response = requests.get(image_url, stream=True)
        image_response.raise_for_status()
        image_bytes = image_response.content
    except requests.RequestException as e:
        error_message = f"Failed to download image from OpenAI URL: {str(e)}"
        raise Exception(error_message)

    return image_bytes
