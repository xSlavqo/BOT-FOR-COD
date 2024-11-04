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
    {"function": check_hospital, "interval": 10000, "last_run": 0, "checkboxes": ["heal"]},
    {"function": auto_build, "interval": 120, "last_run": 0, "checkboxes": ["autobuild"]},
    {"function": rss, "interval": 120, "last_run": 0, "checkboxes": ["goldmap", "woodmap", "stonemap", "manamap"]}
]

def clear_console():
    # Czyści konsolę zależnie od systemu operacyjnego
    os.system('cls' if os.name == 'nt' else 'clear')

def monitor_tasks(stop_event):
    while not stop_event.is_set():
        clear_console()  # Czyści konsolę przed każdym wywołaniem

        current_time = time.time()
        
        for task in tasks:
            # Sprawdź stan checkboxa dla zadania
            if gui_utils.check_task_conditions(task["checkboxes"]):
                # Oblicz czas od ostatniego uruchomienia i do następnego uruchomienia
                time_since_last_run = current_time - task["last_run"]
                time_to_next_run = task["interval"] - time_since_last_run
                last_run_time = datetime.fromtimestamp(task["last_run"]).strftime('%H:%M') if task["last_run"] != 0 else "Nigdy"

                if time_to_next_run <= 0:
                    # Dodaj zadanie do kolejki i aktualizuj czas ostatniego uruchomienia
                    main.task_queue.put(task["function"])
                    task["last_run"] = current_time
                    print(f"Uruchomiono zadanie: {task['function'].__name__}")
                else:
                    # Wyświetl informacje o zadaniu
                    print(f"{task['function'].__name__}: Ostatnie wykonanie o {last_run_time}, czas do następnego wywołania: {int(time_to_next_run)} sekund")

            else:
                # Jeśli checkbox nie jest zaznaczony, wyświetl "off"
                print(f"{task['function'].__name__}: off")

        # Poczekaj sekundę przed następną iteracją
        time.sleep(1)

def start_task_monitoring(stop_event):
    task_monitoring_thread = threading.Thread(target=monitor_tasks, args=(stop_event,))
    task_monitoring_thread.daemon = True
    task_monitoring_thread.start()
