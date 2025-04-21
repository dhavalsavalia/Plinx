from webob import Response

from plinx.status_codes import StatusCodes


def handle_404(response: Response) -> None:
    """
    Set up a standardized 404 Not Found response.

    This utility function is used internally by the framework when no route
    matches the requested URL path. It sets the status code to 404 and
    the response text to "Not Found".

    Args:
        response: The Response object to configure with 404 status

    Returns:
        None

    Example:
        ```python
        response = Response()
        handle_404(response)
        # response now has status_code=404 and text="Not Found"
        ```
    """
    response.status_code = StatusCodes.NOT_FOUND.value
    response.text = StatusCodes.NOT_FOUND.name.replace("_", " ").title()
