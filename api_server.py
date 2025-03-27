from flask import Flask, request, jsonify
from clients import get_openai_client, get_weaviate_client
from task_storage import store_task, find_similar_task
from event_loop import queue_task

app = Flask(__name__)

# Initialize clients
openai_client = get_openai_client()
weaviate_client = get_weaviate_client()

@app.route("/learn_task", methods=["POST"])
def learn_task():
    """Receives new task definitions from user input."""
    data = request.json
    description = data["description"]
    steps = data["steps"]
    context = data.get("context", "General")

    store_task(weaviate_client, openai_client, description, steps, context)
    return jsonify({"status": "Task learned!"})


@app.route("/store_task", methods=["POST"])
def store_task_endpoint():
    """API endpoint to store a task."""
    data = request.json
    description = data.get("description")
    steps = data.get("steps")
    context = data.get("context", "General")

    if not description or not steps:
        return jsonify({"error": "Missing required fields"}), 400

    store_task(weaviate_client, openai_client, description, steps, context)
    return jsonify({"message": "Task stored successfully"}), 200


@app.route("/find_task", methods=["POST"])
def find_task_endpoint():
    """API endpoint to find a similar task."""
    data = request.json
    query = data.get("query")

    if not query:
        return jsonify({"error": "Missing query"}), 400

    task = find_similar_task(weaviate_client, openai_client, query)
    if task:
        return jsonify(task), 200
    else:
        return jsonify({"message": "No similar task found"}), 404


@app.route("/queue_task", methods=["POST"])
def queue_task_endpoint():
    """API endpoint to queue a task."""
    data = request.json
    task = data.get("task")

    if not task:
        return jsonify({"error": "Missing task data"}), 400

    queue_task(task)
    return jsonify({"message": "Task queued successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
