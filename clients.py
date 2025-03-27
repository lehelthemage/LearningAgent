import weaviate
from config import OPENAI_API_KEY

def get_openai_client():
    """Initialize and return the OpenAI client."""
    from openai import OpenAI
    return OpenAI(api_key=OPENAI_API_KEY)

def get_weaviate_client():
    """Initialize and return the Weaviate client for a local instance."""
    return weaviate.connect_to_local()