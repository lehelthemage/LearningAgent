import logging
from clients import get_openai_client, get_weaviate_client
from task_storage import store_task, find_similar_task
from task_execution import execute_task
from event_loop import queue_task, event_loop
from threading import Thread
from api_server import app

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize clients
logger.info("Initializing OpenAI and Weaviate clients...")
openai_client = get_openai_client()
weaviate_client = get_weaviate_client()

# Store a task
logger.info("Storing a task: 'Read LinkedIn messages'")
store_task(
    weaviate_client,
    openai_client,
    description="Read LinkedIn messages",
    steps=[
        {"action": "load_page", "parameters": {"url": "https://www.linkedin.com"}},
        {"action": "login", "parameters": {"username": "myemail", "password": "mypassword"}},
        {"action": "load_page", "parameters": {"url": "https://www.linkedin.com/messaging/"}},
        {"action": "read_elements", "parameters": {"selector": ".message"}}
    ],
    context="LinkedIn"
)

# Retrieve a task
logger.info("Retrieving a similar task for: 'Check LinkedIn messages'")
task = find_similar_task(weaviate_client, openai_client, "Check LinkedIn messages")

# Queue and execute the task
logger.info(f"Queuing the task: {task['description']}")
queue_task(task)

# Start the event loop in a background thread
def start_event_loop():
    logger.info("Starting the event loop...")
    event_loop()

if __name__ == "__main__":
    # Start the event loop in a separate thread
    Thread(target=start_event_loop, daemon=True).start()

    # Start the Flask web server
    logger.info("Starting the Flask web server...")
    app.run(debug=True, host="0.0.0.0", port=5000)

    # Execute immediately for testing (optional)
    logger.info(f"Executing the task: {task['description']}")
    execute_task(task)
