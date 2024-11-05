# task_monitoring.py
import os
import threading
import time
import main
import gui_utils
from datetime import datetime

from build.auto_build import auto_build
from small_tasks.hospital import check_hospital
from legions_status.rss import rss

tasks = [
    {"function": check_hospital, "interval": 10000, "last_run": 0, "checkboxes": ["heal"], "queued": False},
    {"function": auto_build, "interval": 120, "last_run": 0, "checkboxes": ["autobuild"], "queued": False},
    {"function": rss, "interval": 120, "last_run": 0, "checkboxes": ["goldmap", "woodmap", "stonemap", "manamap"], "queued": False}
]

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def monitor_tasks(stop_event):
    while not stop_event.is_set():
        #clear_console()  

        current_time = time.time()
        
        for task in tasks:
            if gui_utils.check_task_conditions(task["checkboxes"]):
                if task["queued"]:
                    print(f"{task['function'].__name__}: w kolejce")
                else:
                    time_since_last_run = current_time - task["last_run"]
                    time_to_next_run = task["interval"] - time_since_last_run
                    last_run_time = datetime.fromtimestamp(task["last_run"]).strftime('%H:%M') if task["last_run"] != 0 else "Nigdy"

                    if time_to_next_run <= 0:
                        main.task_queue.put(task["function"])
                        task["last_run"] = current_time
                        task["queued"] = True
                        print(f"Uruchomiono zadanie: {task['function'].__name__}")
                    else:
                        print(f"{task['function'].__name__}: Ostatnie wykonanie o {last_run_time}, czas do następnego wywołania: {int(time_to_next_run)} sekund")
            else:
                print(f"{task['function'].__name__}: off")

        time.sleep(1)

        # Monitorowanie zakończenia zadań
        while not main.finished_tasks_queue.empty():
            finished_task = main.finished_tasks_queue.get()
            for task in tasks:
                if task["function"] == finished_task:
                    task["queued"] = False  # Resetujemy status queued
                    task["last_run"] = time.time()  # Ustawia czas startowy do następnego odliczania

def start_task_monitoring(stop_event):
    task_monitoring_thread = threading.Thread(target=monitor_tasks, args=(stop_event,))
    task_monitoring_thread.daemon = True
    task_monitoring_thread.start()
