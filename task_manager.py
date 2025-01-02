# task_manager.py

import queue
import threading
import time
from datetime import datetime

from control_game.window_management import cod_restart, cod_run
from tasks.build.auto_build import auto_build
from tasks.hospital import check_hospital
from tasks.rss import rss
from tasks.train.train import monitor_trainings
import gui_utils

class Task:
    def __init__(self, function, interval, checkboxes):
        self.function = function
        self.interval = interval
        self.last_run = 0
        self.in_queue = False
        self.running = False
        self.checkboxes = checkboxes

    def should_run(self, current_time):
        return (current_time - self.last_run) >= self.interval and not self.in_queue and not self.running


class TaskManager:
    def __init__(self):
        self.tasks = [
            Task(monitor_trainings, 60, []),
            Task(check_hospital, 3600, ["heal"]),
            Task(auto_build, 300, ["autobuild"]),
            Task(rss, 300, ["goldmap", "woodmap", "stonemap", "manamap"]),
        ]
        self.task_queue = queue.Queue(maxsize=10)
        self.stop_event = threading.Event()
        self.error_count = 0

    def handle_task_error(self, task, error_message):
        print(f"Błąd podczas wykonywania zadania {task.function.__name__}: {error_message}")
        self.error_count += 1
        if self.error_count >= 5:
            self.handle_critical_failure()

    def handle_critical_failure(self):
        if cod_restart():
            self.reset_tasks()

    def reset_tasks(self):
        with self.task_queue.mutex:
            self.task_queue.queue.clear()
        for task in self.tasks:
            task.last_run = 0
            task.in_queue = False
            task.running = False
        self.error_count = 0

    def execute_task(self, task):
        task.in_queue = False
        task.running = True
        try:
            if not cod_run():
                self.handle_task_error(task, "Nie udało się uruchomić gry")
                return

            if not task.function():
                self.handle_task_error(task, "Zadanie nie powiodło się")
        except Exception as e:
            self.handle_task_error(task, f"Błąd: {e}")
        finally:
            task.running = False
            task.last_run = time.time()

    def log_task_summary(self):
        summary = []
        current_time = time.time()
        for task in self.tasks:
            if not task.checkboxes or gui_utils.check_task_conditions(task.checkboxes):
                if task.running:
                    summary.append(f"{task.function.__name__}: w trakcie")
                elif task.in_queue:
                    summary.append(f"{task.function.__name__}: w kolejce")
                else:
                    time_to_next_run = task.interval - (current_time - task.last_run)
                    summary.append(f"{task.function.__name__}: czas do następnego wywołania: {int(time_to_next_run)} sekund")
        print("\n".join(summary))

    def update_tasks(self):
        current_time = time.time()
        for task in self.tasks:
            if not task.checkboxes or gui_utils.check_task_conditions(task.checkboxes):
                if task.should_run(current_time):
                    self.task_queue.put(task)
                    task.in_queue = True

    def start(self):
        self.stop_event.clear()
        threading.Thread(target=self.task_worker, daemon=True).start()
        threading.Thread(target=self.monitor_tasks, daemon=True).start()

    def stop(self):
        self.stop_event.set()

    def task_worker(self):
        while not self.stop_event.is_set():
            try:
                task = self.task_queue.get(timeout=1)
                self.execute_task(task)
            except queue.Empty:
                continue

    def monitor_tasks(self):
        while not self.stop_event.is_set():
            self.update_tasks()
            self.log_task_summary()
            time.sleep(2)
