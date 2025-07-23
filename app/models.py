# TODO: Implement your data models here
# Consider what data structures you'll need for:
# - Storing URL mappings
# - Tracking click counts
# - Managing URL metadata


import threading
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class URLMap:
    code: str
    original_url: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    click_count: int = 0


# In-memory store for URL mappings\_store = {}
_store_lock = threading.Lock()


def save_mapping(code: str, original_url: str) -> None:
    """
    Saves a new URLMap to the store.
    """
    with _store_lock:
        _store[code] = URLMap(code=code, original_url=original_url)


def get_mapping(code: str) -> URLMap:
    """
    Retrieves a URLMap by its code, or None if not found.
    """
    return _store.get(code)


def increment_clicks(code: str) -> None:
    """
    Atomically increments the click count for a given code.
    """
    with _store_lock:
        if code in _store:
            _store[code].click_count += 1