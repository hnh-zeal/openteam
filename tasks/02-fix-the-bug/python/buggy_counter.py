# buggy_counter.py

import threading
import time

# Race condition occurred because multiple threads could read and modify
# the shared `_current` variable at the same time.
# This resulted in duplicate IDs being returned under concurrent load.
# We fix the race by using `threading.Lock()` to ensure that only one
# thread can access and increment `_current` at a time.
_current = 0
_lock = threading.Lock()

def next_id():
    """Returns a unique ID, incrementing the global counter."""
    global _current
    with _lock:
        value = _current
        time.sleep(0)
        _current += 1
    return value
    