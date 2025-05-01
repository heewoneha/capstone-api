"""OpenAI API service module."""

import base64
import re
import requests
import openai
from io import BytesIO
from typing import Optional
from PIL import Image
from app.services.constant import (
    BackgroundType,
    OPEN_AI_API_KEY,
    IMAGE_SIZE,
    EMPTY_BACKGROUND_BASE_IMAGE_PATH,
    IMAGE_MODEL_NAME,
)


def validate_png_base64(image_base64: str, x_cd_user_id: str) -> BytesIO:
    """If the input is a base64-encoded PNG image, decode it and return a BytesIO object. Else, raise a ValueError.

    Args:
        image_base64 (str): The original base64 image data.
        x_cd_user_id (str): The UUID of the user.
    Raises:
        ValueError: _base64 image data is not valid
        ValueError: _only PNG images are supported

    Returns:
        BytesIO: A BytesIO object containing the decoded image data.
    """
    if image_base64.startswith("data:image"):
        header, b64data = image_base64.split(",", 1)
        match = re.match(r"^data:image/(\w+);base64", header)
        image_format = match.group(1).lower() if match else None
    else:
        b64data = image_base64
        image_format = None

    try:
        image_bytes = base64.b64decode(b64data)
        image = Image.open(BytesIO(image_bytes)).convert("RGBA")
    except Exception:
        value_error_message = "Invalid base64 image input"
        raise ValueError(value_error_message)
    
    if image_format and image_format != "png":
        value_error_message = f"Only PNG images are supported (got {image_format})"
        raise ValueError(value_error_message)
    
    output = BytesIO(image_bytes)
    image.save(output, format="PNG")
    output.name = f"{x_cd_user_id}.png"
    output.seek(0)

    return output


def generate_background_image(background_type: BackgroundType, text: Optional[str], image_base64: Optional[str], x_cd_user_id: str) -> str:
    """Generate a background image using OpenAI API.

    Args:
        background_type (BackgroundType): The type of background to generate.
        text (Optional[str]): The text prompt for the image generation.
        image_base64 (Optional[str]): The image data for the image generation.
        x_cd_user_id (str): The UUID of the user.

    Raises:
        Exception: When the image generation fails, an exception is raised with the error message.
        Exception: Exception: When the background type is not supported.
        Exception: Exception: When the image URL is not found in the OpenAI response.

    Returns:
        str: base64-encoded PNG image
    """
    client = openai.OpenAI(api_key=OPEN_AI_API_KEY)

    if background_type in [BackgroundType.IMAGE, BackgroundType.TEXT_IMAGE]:
        if not image_base64:
            error_message = "image_base64 is required for TEXT_IMAGE background type"
            raise Exception(error_message)
        try:
            image_file = validate_png_base64(image_base64=image_base64, x_cd_user_id=x_cd_user_id)
        except ValueError as e:
            error_message = f"Invalid base64 image input, Exception={str(e)}"
            raise Exception(error_message)

    if background_type == BackgroundType.TEXT:
        response = client.images.generate(
            model=IMAGE_MODEL_NAME,
            prompt=text,
            n=1,
            size=IMAGE_SIZE,
        )
    elif background_type == BackgroundType.IMAGE:
        # Return the original image if the background type is RAW IMAGE
        return base64.b64encode(image_file.getvalue()).decode("utf-8")
    elif background_type == BackgroundType.TEXT_IMAGE:
        response = client.images.edit(
            image=image_file,
            prompt=text,
            n=1,
            size=IMAGE_SIZE,
        )
    elif background_type == BackgroundType.NONE:
        with open(EMPTY_BACKGROUND_BASE_IMAGE_PATH, "rb") as f:
            empty_image_bytes = f.read()
        return base64.b64encode(empty_image_bytes).decode("utf-8")
    else:
        error_message = f"Unsupported background type: {background_type}"
        raise Exception(error_message)

    image_url = getattr(response.data[0], "url", None)

    if not image_url:
        error_message = "Failed to generate image URL from OpenAI response"
        raise Exception(error_message)
    
    try:
        image_response = requests.get(image_url, stream=True)
        image_response.raise_for_status()
        image_bytes = image_response.content
        return base64.b64encode(image_bytes).decode("utf-8")
    except requests.RequestException as e:
        error_message = f"Failed to download image from OpenAI URL: {str(e)}"
        raise Exception(error_message)
