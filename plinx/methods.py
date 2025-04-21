from enum import Enum


class HTTPMethods(Enum):
    """
    Enumeration of HTTP methods supported by the Plinx framework.

    This enum defines the standard HTTP methods as defined in RFC 7231 and RFC 5789,
    categorized by their safety and idempotency properties.

    Safe methods (should not modify resources):
    - GET: Retrieve a representation of a resource
    - HEAD: Same as GET but returns only headers, no body

    Idempotent methods (multiple identical requests have same effect as single request):
    - PUT: Replace a resource with the request payload
    - DELETE: Remove the specified resource
    - OPTIONS: Describe the communication options for the target resource

    Non-idempotent methods (multiple identical requests may have different effects):
    - POST: Submit data to be processed, typically creating a new resource
    - PATCH: Apply partial modifications to a resource

    Usage:
        ```python
        from plinx.methods import HTTPMethods

        # Check if a method is GET
        if method == HTTPMethods.GET:
            # handle GET request

        # Get the string value of a method
        method_str = HTTPMethods.POST.value  # "POST"
        ```
    """

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


def is_valid_method(method: str) -> bool:
    """
    Check if the given method is a valid HTTP method.

    Args:
        method: The HTTP method to check

    Returns:
        bool: True if the method is valid, False otherwise
    """
    return method in HTTPMethods.__members__.values()


def get_handler_name_for_method(method: str) -> str:
    """
    Get the handler name for a given HTTP method.

    Args:
        method: The HTTP method to get the handler name for

    Returns:
        str: The handler name corresponding to the HTTP method
    """
    if not is_valid_method(method):
        raise ValueError(f"Invalid HTTP method: {method}")

    return method.lower()
