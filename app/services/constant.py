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

class DanceName(str, Enum):
    """Enum for dance names."""
    ANXIETY = "anxiety"
    HIPLET_99 = "hiplet_99"
    TIRAMISU_CAKE = "tiramisu_cake"
    BUMBLEBEE = "bumblebee"
    GROOVE = "groove"

AZURE_STORAGE_CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
AZURE_STORAGE_CONNECTION_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_PUBLIC_STORAGE_CONTAINER_NAME = os.getenv("AZURE_PUBLIC_STORAGE_CONTAINER_NAME")
AZURE_PUBLIC_CONNECTION_STRING = os.getenv("AZURE_PUBLIC_CONNECTION_STRING")

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

BACKGROUND_DIR = "background"
CHARACTER_DIR = "character"
RESULT_DIR = "result"

IMAGE_CONTENT_TYPE_EXTENSION_MAP = {
    "image/png": "png",
}

IMAGE_MODEL_NAME = "gpt-image-1"

IMAGE_SIZE = "1024x1024"

IMAGES_DIR = "images"
EMPTY_BACKGROUND_IMAGE_FILE_NAME = "empty_background.png"

LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
EMPTY_BACKGROUND_BASE_IMAGE_PATH = os.path.join(LOCAL_PATH, IMAGES_DIR, EMPTY_BACKGROUND_IMAGE_FILE_NAME)

MODEL_SOURCE_DIR = os.path.join(LOCAL_PATH, "tmp_model_sources")
MODEL_RESULT_DIR = os.path.join(LOCAL_PATH, "tmp_model_results")

VIDEO_CODEC = "libx264"
VIDEO_FPS = 30
