from online_store.helper.response import success_response

def home():
    """ Home handler

    Returns:
        flask.Response: return status application is online
    """
    return success_response(
        'Online Store application is online',
        None,
    )