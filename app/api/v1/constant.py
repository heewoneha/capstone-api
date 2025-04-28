"""Constants for the application."""

from enum import Enum
import os
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

BACKGROUND_DIR = "background"
CHARACTER_DIR = "character"
RESULT_DIR = "result"

CHARACTER_CONTENT_TYPE_EXTENSION_MAP = {
    "image/png": "png",
}

class DanceName(str, Enum):
    """Enum for dance names."""
    ANXIETY = "anxiety"
