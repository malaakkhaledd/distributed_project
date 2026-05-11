import asyncio
from llm.llm import generate_response
from rag.rag import retrieve
from utils.logger import log
from utils.monitor import monitor


class Worker:
    def __init__(self, worker_id, worker_type="CPU"):
        self.worker_id = worker_id
        self.worker_type = worker_type
        self.queue = asyncio.Queue()
        self.active = True

    async def start(self):
        print(f"[Worker {self.worker_id}] Started")

        while True:
            request = await self.queue.get()

            if request is None:
                self.queue.task_done()
                break

            try:
                await self.process(request)

            except Exception as e:
                if not request.future.done():
                    request.future.set_exception(e)

            finally:
                self.queue.task_done()

    async def process(self, request):

        log("WORKER", f"Processing", request_id=request.request_id)

        monitor.start_request(request.request_id)

        # simulate GPU vs CPU speed
        if self.worker_type == "GPU":
            await asyncio.sleep(0.02)
        else:
            await asyncio.sleep(0.08)

        loop = asyncio.get_running_loop()

        # =========================
        # ✅ RAG FIX (VISIBLE)
        # =========================
        context = retrieve(request.query)

        log("RAG", f"Query: {request.query}", request_id=request.request_id)
        log("RAG", f"Retrieved: {context}", request_id=request.request_id)

        try:
            result = await loop.run_in_executor(
                None,
                generate_response,
                request.query,
                context if isinstance(context, str) else " ".join([c["text"] for c in context])
            )

            monitor.end_request(request.request_id, self.worker_id)

            if not request.future.done():
                request.future.set_result({
                    "request_id": request.request_id,
                    "worker_id": self.worker_id,
                    "response": result
                })

        except Exception as e:
            monitor.end_request(request.request_id, self.worker_id)

            if not request.future.done():
                request.future.set_exception(e)