import asyncio


class Request:
    def __init__(self, request_id, query, user_id=0):
        self.request_id = request_id
        self.user_id = user_id
        self.query = query
        self.future = asyncio.get_event_loop().create_future()


class Response:
    def __init__(self, request_id, user_id, result):
        self.request_id = request_id
        self.user_id = user_id
        self.result = result