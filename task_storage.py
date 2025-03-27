import logging
from clients import get_weaviate_client
from openai import OpenAI

logger = logging.getLogger(__name__)

def generate_embedding(openai_client, text):
    """Generate a vector embedding for a task description."""
    logger.debug(f"Generating embedding for text: {text}")
    response = openai_client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    embedding = response["data"][0]["embedding"]
    logger.debug(f"Generated embedding: {embedding}")
    return embedding

def store_task(openai_client, description, steps, context):
    """Stores a task in the vector database."""
    logger.info(f"Storing task: {description}")
    embedding = generate_embedding(openai_client, description)

    task_data = {
        "description": description,
        "steps": steps,
        "context": context,
    }

    # Use get_weaviate_client to initialize the client
    with get_weaviate_client() as weaviate_client:
        weaviate_client.data_object.create(
            data_object=task_data,
            class_name="Task",
            vector=embedding
        )
    logger.info(f"Task stored successfully: {description}")

def find_similar_task(openai_client, query):
    """Finds the most similar task in the vector database."""
    logger.info(f"Finding similar task for query: {query}")
    embedding = generate_embedding(openai_client, query)

    # Use get_weaviate_client to initialize the client
    with get_weaviate_client() as weaviate_client:
        response = weaviate_client.query.get(
            class_name="Task",
            properties=["description", "steps", "context"]
        ).with_near_vector({"vector": embedding}).with_limit(1).do()

    tasks = response.get("data", {}).get("Get", {}).get("Task", [])
    if tasks:
        logger.info(f"Found similar task: {tasks[0]['description']}")
    else:
        logger.warning("No similar task found.")
    return tasks[0] if tasks else None
