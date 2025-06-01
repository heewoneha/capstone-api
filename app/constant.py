"""Constants for the application"""

import os
from dotenv import load_dotenv

load_dotenv()

FRONT_END_IP = os.getenv("FRONT_END_IP")
FRONT_END_PORT = os.getenv("FRONT_END_PORT")
