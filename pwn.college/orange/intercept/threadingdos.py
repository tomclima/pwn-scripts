import threading
import socket
import time

def overload():
    TARGET = ("10.0.0.2", 31337)
    try:
        s = socket.create_connection(TARGET, timeout=5)
        time.sleep(1)
        s.close()
    except Exception:
        pass

threads = [threading.Thread(target=overload) for _ in range(10000)]  # reduced from 1M
for t in threads:
    t.start()
for t in threads:
    t.join()
