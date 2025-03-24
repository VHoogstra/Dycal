import threading
import time


class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        task= self.queue.get()
        data = task()
        self.queue.task_done()
