from webob import Response

from plinx.status_codes import StatusCodes


def handle_404(response: Response) -> None:
    """
    Set the response status code to 404 and return None.
    :param response:
    :return:
    """
    response.status_code = StatusCodes.NOT_FOUND.value
    response.text = StatusCodes.NOT_FOUND.name.replace("_", " ").title()
