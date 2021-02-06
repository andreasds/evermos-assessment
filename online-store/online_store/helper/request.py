from http import HTTPStatus
from online_store.helper.response import failed_response

def is_request_data_exists(request_data, params):
    """ Check request data existance

    Args:
        request_data (dict): json request data
        params (array): list param need to check

    Returns:
        flask.Response: failed response data is null
    """
    for param in params:
        if param not in request_data:
            return failed_response(
                HTTPStatus.BAD_REQUEST,
                ' '.join([ 'ERROR data', param, 'is null' ]),
            )

    return None
