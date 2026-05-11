import asyncio


class Master:
    def __init__(self, workers, strategy="least_connections"):
        self.workers = workers
        self.strategy = strategy
        self.index = 0
        self.lock = asyncio.Lock()

    async def assign(self, request):
        worker = self.get_best_worker()

        print(f"[Master] Request {request.request_id} → Worker {worker.worker_id}")

        # push request to worker queue
        await worker.queue.put(request)

        # wait for worker to resolve future
        try:
            result = await request.future
            return result
        except Exception as e:
            return {
                "request_id": request.request_id,
                "worker_id": worker.worker_id,
                "response": f"FAILED: {str(e)}"
            }

    def get_best_worker(self):
        alive = [w for w in self.workers if w.active]

        if not alive:
            raise Exception("No available workers")

        # ROUND ROBIN
        if self.strategy == "round_robin":
            worker = alive[self.index % len(alive)]
            self.index += 1
            return worker

        # LEAST LOADED
        if self.strategy == "least_connections":
            return min(alive, key=lambda w: w.queue.qsize())

        # LOAD AWARE
        if self.strategy == "load_aware":
            return min(
                alive,
                key=lambda w: (
                    w.queue.qsize(),
                    0 if w.worker_type == "GPU" else 1
                )
            )

        return alive[0]