import datetime
import threading

lock = threading.Lock()


def log(source, message, level="INFO", request_id=None):
    with lock:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        if request_id is not None:
            print(f"[{timestamp}] [{level}] [{source}] [REQ-{request_id}] {message}")
        else:
            print(f"[{timestamp}] [{level}] [{source}] {message}")