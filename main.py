# main.py
import queue
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from control_game.window_management import cod_restart, cod_run
import time
from datetime import datetime

task_queue = queue.Queue()
finished_tasks_queue = queue.Queue()

def log_error(task_name, error_type, error_message):
    with open("errors.txt", "a") as error_file:
        error_file.write(f"{datetime.now()} - Task: {task_name} - {error_type}: {error_message}\n")

def execute_task_with_timeout(task, timeout=30):
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(lambda: (cod_run(), task())[1])  # Najpierw wywołuje cod_run, potem task
        try:
            future.result(timeout=timeout)
            # Zadanie zakończone sukcesem
            finished_tasks_queue.put(task)  # Oznaczamy zadanie jako wykonane
        except (TimeoutError, Exception) as e:
            # Obsługa błędu niezależnie od jego rodzaju
            error_type = "Timeout" if isinstance(e, TimeoutError) else "Exception"
            error_message = f"Przekroczono limit czasu {timeout} sekund" if isinstance(e, TimeoutError) else str(e)
            log_error(task.__name__, error_type, error_message)
            
            # Próba anulowania zadania
            future.cancel()
            time.sleep(0.1)  # Krótkie opóźnienie na zakończenie procesu
            
            # Sprawdzamy, czy zadanie zostało skutecznie anulowane lub zakończone
            if future.cancelled() or future.done():
                print(f"Zadanie {task.__name__} zostało skutecznie anulowane lub zakończone.")
                finished_tasks_queue.put(task)  # Oznaczamy zadanie jako zakończone
            else:
                print(f"Nie udało się zakończyć zadania {task.__name__}.")
            
            # Restart gry i odczekanie 5 sekund przed podjęciem kolejnego zadania
            cod_restart()
            time.sleep(5)
        finally:
            if not future.done():
                future.cancel()  # W razie potrzeby anulujemy przyszłe wykonanie

def execute_tasks(stop_event):
    while not stop_event.is_set():
        if not task_queue.empty():
            task = task_queue.get()
            try:
                execute_task_with_timeout(task)
            except Exception as e:
                log_error(task.__name__, "Critical Exception", str(e))
            finally:
                task_queue.task_done()

def start_task_execution(stop_event):
    task_monitoring_thread = threading.Thread(target=execute_tasks, args=(stop_event,))
    task_monitoring_thread.daemon = True
    task_monitoring_thread.start()
