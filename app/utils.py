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
    Validates that the URL has a valid scheme and network location.
    """
    try:
        result = urlparse(url)
        return result.scheme in ('http', 'https') and bool(result.netloc)
    except Exception:
        return False


def build_short_url(code: str) -> str:
    """
    Builds the absolute short URL using the current request host.
    """
    from flask import request
    return request.host_url.rstrip('/') + '/' + code