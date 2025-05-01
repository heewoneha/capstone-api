"""Constants for the application."""

import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

class BackgroundType(str, Enum):
    """Enum for background types."""
    TEXT = "text"
    IMAGE = "image"
    TEXT_IMAGE = "text_image"
    NONE = "none"

AZURE_STORAGE_CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
AZURE_STORAGE_CONNECTION_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

BACKGROUND_DIR = "background"
CHARACTER_DIR = "character"
RESULT_DIR = "result"

IMAGE_CONTENT_TYPE_EXTENSION_MAP = {
    "image/png": "png",
}

class DanceName(str, Enum):
    """Enum for dance names."""
    ANXIETY = "anxiety"

IMAGE_MODEL_NAME = "dall-e-3"

IMAGE_SIZE = "1024x1024"

IMAGES_DIR = "images"
EMPTY_BACKGROUND_IMAGE_FILE_NAME = "empty_background.png"

LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
EMPTY_BACKGROUND_BASE_IMAGE_PATH = os.path.join(LOCAL_PATH, IMAGES_DIR, EMPTY_BACKGROUND_IMAGE_FILE_NAME)
