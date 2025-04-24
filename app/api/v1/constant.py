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
