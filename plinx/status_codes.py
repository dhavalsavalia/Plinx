from enum import Enum


class StatusCodes(Enum):
    """
    Enumeration of HTTP status codes supported by the Plinx framework.

    This enum defines standard HTTP status codes as defined in RFC 7231,
    organized by their categories (2xx for success, 3xx for redirection, etc.).

    Each status code has a name that reflects its standard description,
    and a numeric value that is sent in HTTP responses.

    Usage:
        ```python
        from plinx.status_codes import StatusCodes

        # Set a 404 status code
        response.status_code = StatusCodes.NOT_FOUND.value  # 404

        # Get the name of a status code for display
        status_name = StatusCodes.NOT_FOUND.name  # "NOT_FOUND"
        # Can be formatted for human display:
        human_readable = StatusCodes.NOT_FOUND.name.replace("_", " ").title()  # "Not Found"
        ```
    """

    # 2XX - Success
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204

    # 3XX - Redirection
    NOT_MODIFIED = 304

    # 4XX - Client Error
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    CONFLICT = 409
    GONE = 410
    PRECONDITION_FAILED = 412
    UNSUPPORTED_MEDIA_TYPE = 415
    TOO_MANY_REQUESTS = 429
    UNAVAILABLE_FOR_LEGAL_REASONS = 451

    # 5XX - Server Error
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    HTTP_VERSION_NOT_SUPPORTED = 505
