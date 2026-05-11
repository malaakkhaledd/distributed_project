import asyncio
import time

from client.client import generate_requests
from workers.worker import Worker
from master.master import Master
from vector_db.ingest import load_documents
from utils.logger import log
from utils.monitor import monitor   # ✅ FIX: shared monitor instance

NUM_USERS = 1000


async def run_system():

    log("SYSTEM", "Loading vector database...")
    load_documents()

    # =========================
    # ✅ SCALABLE WORKERS SETUP
    # =========================
    workers = []

    # CPU workers
    for i in range(2):
        workers.append(Worker(i, "CPU"))

    # GPU workers (simulated cluster scaling)
    gpu_count = 3
    for i in range(gpu_count):
        workers.append(Worker(i + 2, "GPU"))

    log("SYSTEM", f"Cluster initialized with {len(workers)} workers (CPU + GPU mix)")

    worker_tasks = [asyncio.create_task(w.start()) for w in workers]

    master = Master(workers)

    requests = generate_requests(NUM_USERS)

    start_time = time.time()

    success = 0
    failure = 0

    lock = asyncio.Lock()

    worker_stats = {w.worker_id: 0 for w in workers}

    async def process_request(req):

        nonlocal success, failure

        try:
            result = await master.assign(req)

            async with lock:
                success += 1
                worker_stats[result["worker_id"]] += 1

            log("CLIENT", result["response"], request_id=req.request_id)

        except Exception as e:
            async with lock:
                failure += 1
            log("CLIENT", f"Request {req.request_id} failed: {e}", "ERROR", req.request_id)

    await asyncio.gather(*(process_request(r) for r in requests))

    # shutdown
    for w in workers:
        w.active = False

    for w in workers:
        await w.queue.put(None)

    await asyncio.gather(*worker_tasks, return_exceptions=True)

    total_time = time.time() - start_time

    log("SYSTEM", "===== PERFORMANCE REPORT =====")

    print(f"\nTotal Requests: {len(requests)}")
    print(f"Successful Requests: {success}")
    print(f"Failed Requests: {failure}")
    print(f"Total Execution Time: {round(total_time, 2)}s")
    print(f"Throughput: {round(len(requests)/total_time, 2)} req/sec")

    print("\n===== WORKER UTILIZATION =====")
    for k, v in worker_stats.items():
        print(f"Worker {k}: {v}")

    monitor.report()

    log("SYSTEM", "===== SYSTEM END =====")


if __name__ == "__main__":
    asyncio.run(run_system())