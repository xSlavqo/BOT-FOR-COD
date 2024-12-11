# task_manager.py

import queue
import threading
import time
from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal
import gui_utils
from build.auto_build import auto_build
from small_tasks.hospital import check_hospital
from legions_status.rss import rss
from train.train import create_training_buildings, check_train_end_time
from control_game.window_management import cod_restart, cod_run
import logging
from train.train_utils import read_config
from logging.handlers import RotatingFileHandler

# Konfiguracja loggera
logger = logging.getLogger("TaskManager")
logger.setLevel(logging.ERROR)
handler = RotatingFileHandler("errors.txt", maxBytes=1024*1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class TaskLogger(QObject):
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()


task_logger = TaskLogger()


class Task:
    def __init__(self, function, interval, checkboxes):
        self.function = function
        self.interval = interval
        self.last_run = 0
        self.queued = False
        self.is_running = False
        self.checkboxes = checkboxes

    def should_run(self, current_time):
        return (current_time - self.last_run) >= self.interval and not self.queued and not self.is_running

    def mark_as_queued(self):
        self.queued = True

    def mark_as_running(self):
        self.is_running = True
        self.queued = False

    def mark_as_completed(self):
        self.is_running = False
        self.last_run = time.time()


class TaskManager:
    def __init__(self):
        self.buildings = create_training_buildings()  # Tworzenie budynków podczas startu TaskManagera
        self.tasks = [
            Task(check_hospital, 3600, ["heal"]),
            Task(auto_build, 10, ["autobuild"]),
            Task(rss, 60, ["goldmap", "woodmap", "stonemap", "manamap"]),
        ]
        self.task_queue = queue.Queue(maxsize=10)
        self.stop_event = threading.Event()
        self.error_count = 0
        self.last_training_check = 0
        self.training_check_interval = 5  # Interwał sprawdzania budynków

    def monitor_trainings(self):
        """Monitoruje budynki szkoleniowe i aktualizuje ich stan."""
        current_time = time.time()
        if current_time - self.last_training_check < self.training_check_interval:
            return  # Ominięcie sprawdzania, jeśli interwał nie minął

        self.last_training_check = current_time

        # Aktualizacja statusu budynków (active) na podstawie konfiguracji
        config = read_config()
        for building in self.buildings:
            building.active = config.get(f"comboBox_{building.name}", 0) > 0

            if building.active:
                if not building.train_end_time or building.train_end_time <= datetime.now():
                    if not cod_run():
                        logger.error("Gra nie jest uruchomiona. Pomijanie budynku.")
                        continue
                    if not check_train_end_time(building):
                        logger.error(f"Błąd podczas aktualizacji budynku: {building.name}")
                    else:
                        logger.info(f"Zaktualizowano czas dla budynku: {building.name}")

    def execute_task(self, task):
        try:
            task.mark_as_running()
            if not cod_run():
                self.log_error(task.function.__name__, "Game Not Running", "Gra nie jest uruchomiona. Pomijanie zadania.")
                return
            result = task.function()
            if result:
                task.mark_as_completed()
            else:
                self.log_error(task.function.__name__, "Task Failure", f"Task {task.function.__name__} failed.")  # Zwiększenie licznika tutaj
        except Exception as e:
            self.log_error(task.function.__name__, "Critical Error", str(e))  # Tutaj też zwiększany licznik
        finally:
            task.mark_as_completed()


    def reset_tasks(self):
        with self.task_queue.mutex:
            self.task_queue.queue.clear()
        for task in self.tasks:
            task.last_run = 0
            task.queued = False
        self.error_count = 0

    def log_error(self, task_name, error_type, error_message):
        logger.error(f"{task_name} - {error_type}: {error_message}")
        if error_type != "Task Failure":
            logger.error(f"Traceback:\n{error_message}")
        self.error_count += 1
        task_logger.log_signal.emit(f"ERROR: {task_name} - {error_type}. Licznik błędów: {self.error_count}")
        if self.error_count >= 5:
            self.handle_critical_failure()

    def handle_critical_failure(self):
        task_logger.log_signal.emit("Przekroczono limit błędów. Restartowanie gry...")
        if cod_restart():
            self.reset_tasks()
            task_logger.log_signal.emit("Gra zrestartowana. Wznawianie zadań.")
        else:
            task_logger.log_signal.emit("Nie udało się zrestartować gry.")

    def task_worker(self):
        while not self.stop_event.is_set():
            self.monitor_trainings()
            try:
                task = self.task_queue.get(timeout=1)
                self.execute_task(task)
            except queue.Empty:
                continue

    def monitor_tasks(self):
        while not self.stop_event.is_set():
            current_time = time.time()
            summary = []
            for task in self.tasks:
                if gui_utils.check_task_conditions(task.checkboxes):
                    if task.should_run(current_time):
                        self.task_queue.put(task)
                        task.mark_as_queued()
                        summary.append(f"Uruchomiono zadanie: {task.function.__name__}")
                    elif task.is_running:
                        summary.append(f"{task.function.__name__}: w trakcie")
                    elif task.queued:
                        summary.append(f"{task.function.__name__}: w kolejce")
                    else:
                        last_run_time = datetime.fromtimestamp(task.last_run).strftime('%H:%M') if task.last_run else "Nigdy"
                        time_to_next_run = task.interval - (current_time - task.last_run)
                        summary.append(f"{task.function.__name__}: Ostatnie wykonanie o {last_run_time}, czas do następnego wywołania: {int(time_to_next_run)} sekund")
                else:
                    summary.append(f"{task.function.__name__}: off")
            summary.append(f"Licznik błędów: {self.error_count}")
            if summary:
                task_logger.log_signal.emit("\n".join(summary))
            time.sleep(2)

    def start(self):
        self.stop_event.clear()
        threading.Thread(target=self.task_worker, daemon=True).start()
        threading.Thread(target=self.monitor_tasks, daemon=True).start()

    def stop(self):
        self.stop_event.set()
