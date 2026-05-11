class LoadBalancer:
    def __init__(self, master):
        self.master = master

    async def handle_request(self, request):
        result = await self.master.assign(request)
        return result, result.get("worker_id", -1), "success"