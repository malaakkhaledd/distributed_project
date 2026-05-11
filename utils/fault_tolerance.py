import random

class FaultManager:
    def __init__(self, workers):
        self.workers = workers

    def simulate_failure(self, probability=0.01):
        # randomly kill workers (for demo/testing)
        for w in self.workers:
            if random.random() < probability:
                w.active = False
                print(f"[FAULT] Worker {w.worker_id} FAILED")

    def recover_workers(self):
        # revive workers (simulation of healing)
        for w in self.workers:
            if not w.active and random.random() < 0.5:
                w.active = True
                print(f"[RECOVERY] Worker {w.worker_id} restored")