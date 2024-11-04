# main.py
import queue
import threading

task_queue = queue.Queue()

def execute_tasks(stop_event):
    while not stop_event.is_set():
        if not task_queue.empty():
            task = task_queue.get()
            task()
            task_queue.task_done()

def start_task_execution(stop_event):
    task_execution_thread = threading.Thread(target=execute_tasks, args=(stop_event,))
    task_execution_thread.daemon = True
    task_execution_thread.start()
