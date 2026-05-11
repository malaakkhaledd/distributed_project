import time


class Monitor:
    def __init__(self):
        self.latencies = []
        self.worker_latencies = {}
        self.start_times = {}

    def start_request(self, request_id):
        self.start_times[request_id] = time.time()

    def end_request(self, request_id, worker_id=None):
        if request_id in self.start_times:
            latency = time.time() - self.start_times[request_id]
            self.latencies.append(latency)

            if worker_id is not None:
                if worker_id not in self.worker_latencies:
                    self.worker_latencies[worker_id] = []
                self.worker_latencies[worker_id].append(latency)

    def report(self):
        if not self.latencies:
            return

        avg = sum(self.latencies) / len(self.latencies)

        print("\n===== MONITORING =====")
        print(f"Avg Latency: {round(avg, 3)}s")
        print(f"Max Latency: {round(max(self.latencies), 3)}s")
        print(f"Min Latency: {round(min(self.latencies), 3)}s")

        print("\n===== WORKER LATENCY =====")
        for w, vals in self.worker_latencies.items():
            print(f"Worker {w}: avg={round(sum(vals)/len(vals), 3)}s")


# ✅ IMPORTANT FIX: SINGLE GLOBAL INSTANCE
monitor = Monitor()