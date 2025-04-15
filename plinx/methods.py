from enum import Enum


class HTTPMethods(Enum):
    """HTTP methods for the API."""

    # Safe methods
    GET = "GET"
    HEAD = "HEAD"

    # Idempotent methods
    PUT = "PUT"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"

    # Non-idempotent methods
    POST = "POST"
    PATCH = "PATCH"