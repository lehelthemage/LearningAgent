import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Weaviate URL
WEAVIATE_URL = "http://localhost:8080"

# Event loop settings
EVENT_LOOP_INTERVAL = 60  # in seconds