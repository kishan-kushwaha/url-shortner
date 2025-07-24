# TODO: Implement utility functions here
# Consider functions for:
# - Generating short codes
# - Validating URLs
# - Any other helper functions you need

import random
import string
from urllib.parse import urlparse

def generate_short_code(length: int = 6) -> str:
    """
    Generates a random alphanumeric code of the given length.
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def is_valid_url(url: str) -> bool:
    """
    Returns True if URL has scheme http/https and a network location.
    """
    try:
        result = urlparse(url)
        return result.scheme in ('http', 'https') and bool(result.netloc)
    except Exception:
        return False

def build_short_url(code: str) -> str:
    """
    Constructs the public short URL using the current request host.
    """
    from flask import request
    return request.host_url.rstrip('/') + '/' + code