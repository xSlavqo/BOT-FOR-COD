# task_manager.py

import queue
import threading
import time
import sys
from datetime import datetime

import gui_utils
from build.auto_build import auto_build
from small_tasks.hospital import check_hospital
from legions_status.rss import rss
from train.train import monitor_trainings
from control_game.window_management import cod_restart, cod_run

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
        self.tasks = [
            Task(check_hospital, 3600, ["heal"]),
            Task(auto_build, 300, ["autobuild"]),
            Task(rss, 300, ["goldmap", "woodmap", "stonemap", "manamap"]),
            Task(monitor_trainings, 60, [])
        ]
        self.task_queue = queue.Queue(maxsize=10)
        self.stop_event = threading.Event()
        self.error_count = 0

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
            current_time = time.time()
            summary = []
            for task in self.tasks:
                if not task.checkboxes or gui_utils.check_task_conditions(task.checkboxes):
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
                print("\n".join(summary))
            time.sleep(2)

    def execute_task(self, task):
        task.mark_as_running()
        if not cod_run():
            self.error_count += 1
            if self.error_count >= 5:
                self.handle_critical_failure()
            return

        result = task.function()
        if not result:
            self.error_count += 1
            if self.error_count >= 5:
                self.handle_critical_failure()

        task.mark_as_completed()

    def reset_tasks(self):
        with self.task_queue.mutex:
            self.task_queue.queue.clear()
        for task in self.tasks:
            task.last_run = 0
            task.queued = False
        self.error_count = 0

    def handle_critical_failure(self):
        if cod_restart():
            self.reset_tasks()
