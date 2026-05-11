from common.models import Request

def generate_requests(num_users=1000):
    return [
        Request(
            request_id=i,
            user_id=i,   # FIXED
            query=f"Explain distributed systems concept {i}"
        )
        for i in range(num_users)
    ]