import time
import json
from task_execution import execute_task

task_queue = []

def queue_task(task):
    """Add a task to the queue."""
    task_queue.append(task)
    print(f"Task queued: {task['description']}")

def event_loop():
    """Continuously process tasks in the queue."""
    while True:
        if task_queue:
            task = task_queue.pop(0)
            print(f"⏳ Executing: {task['description']}")
            execute_task(task)
            log_operations(task)
        time.sleep(1)  # Adjust interval as needed

def log_operations(task):
    """Logs executed operations."""
    with open("task_log.json", "a") as f:
        json.dump(task, f, indent=4)
        f.write("\n")
    print(f"📝 Logged: {task['description']}")
