# task_manager.py
import queue
import threading
from concurrent.futures import ThreadPoolExecutor
from control_game.window_management import cod_restart, cod_run
import time
from datetime import datetime
import gui_utils

from build.auto_build import auto_build
from small_tasks.hospital import check_hospital
from legions_status.rss import rss

# Zadania do monitorowania
tasks = [
    {"function": check_hospital, "interval": 10000, "last_run": 0, "checkboxes": ["heal"], "queued": False},
    {"function": auto_build, "interval": 120, "last_run": 0, "checkboxes": ["autobuild"], "queued": False},
    {"function": rss, "interval": 120, "last_run": 0, "checkboxes": ["goldmap", "woodmap", "stonemap", "manamap"], "queued": False}
]

task_queue = queue.Queue()

def log_error(task_name, error_type, error_message):
    with open("errors.txt", "a") as error_file:
        error_file.write(f"{datetime.now()} - Task: {task_name} - {error_type}: {error_message}\n")

def execute_task(task):
    cod_run()  # Uruchamiamy grę
    result = task()  # Wykonanie taska
    return result

def execute_tasks(stop_event):
    while not stop_event.is_set():
        if not task_queue.empty():
            task = task_queue.get()
            try:
                result = execute_task(task)
                if result:
                    # Aktualizacja last_run i ustawienie `queued` na False po zakończeniu taska
                    for t in tasks:
                        if t["function"] == task:
                            t["last_run"] = time.time()
                            t["queued"] = False
                else:
                    print(f"Błąd w zadaniu: {task.__name__}. Wstrzymanie przetwarzania.")
                    # Wywołanie funkcji kontrolnej (zastąp printem do czasu implementacji funkcji)
                    print("Kontrolna funkcja sprawdzająca błędy zadania...")
                    for t in tasks:
                        if t["function"] == task:
                            t["last_run"] = 0  # Ustawienie last_run na 0 po zwróceniu False
                            t["queued"] = False
                    log_error(task.__name__, "Task Failure", "Task zwrócił False")
            except Exception as e:
                log_error(task.__name__, "Critical Exception", str(e))
            finally:
                task_queue.task_done()

def monitor_tasks(stop_event):
    while not stop_event.is_set():
        current_time = time.time()
        
        for task in tasks:
            if gui_utils.check_task_conditions(task["checkboxes"]):
                if task["queued"]:
                    print(f"{task['function'].__name__}: w kolejce")
                else:
                    time_since_last_run = current_time - task["last_run"]
                    time_to_next_run = task["interval"] - time_since_last_run
                    if time_to_next_run <= 0:
                        task_queue.put(task["function"])
                        task["queued"] = True
                        print(f"Uruchomiono zadanie: {task['function'].__name__}")
                    else:
                        last_run_time = datetime.fromtimestamp(task["last_run"]).strftime('%H:%M') if task["last_run"] != 0 else "Nigdy"
                        print(f"{task['function'].__name__}: Ostatnie wykonanie o {last_run_time}, czas do następnego wywołania: {int(time_to_next_run)} sekund")
            else:
                print(f"{task['function'].__name__}: off")

        time.sleep(1)

def start_task_execution(stop_event):
    task_monitoring_thread = threading.Thread(target=execute_tasks, args=(stop_event,))
    task_monitoring_thread.daemon = True
    task_monitoring_thread.start()
    
    task_monitor_thread = threading.Thread(target=monitor_tasks, args=(stop_event,))
    task_monitor_thread.daemon = True
    task_monitor_thread.start()
