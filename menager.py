import threading
import queue

class VariableManager:
    def __init__(self):
        self.variables = {}
        self.queue = queue.Queue()

    def process_queue(self):
        while True:
            name, value = self.queue.get()
            if name is None:
                break
            self.variables[name] = value

    def start(self):
        threading.Thread(target=self.process_queue, daemon=True).start()