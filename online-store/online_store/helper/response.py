from flask import make_response
from http import HTTPStatus

def success_response(message, data):
    """ Success response template

    Args:
        message (string): success message
        data (any): response data

    Returns:
        flask.Response: template success response with data
    """
    return make_response(
        {
            'Status': 'success',
            'Message': message,
            'Data': data,
        },
        HTTPStatus.OK,
        {
            'Content-Type': 'application/json',
        },
    )

def failed_response(status_code, message):
    """ Failed response template

    Args:
        status_code (int): http error code
        message (string): error message

    Returns:
        flask.Response: template error response
    """
    return make_response(
        {
            'Status': 'failed',
            'Message': message,
        },
        status_code,
        {
            'Content-Type': 'application/json',
        },
    )
