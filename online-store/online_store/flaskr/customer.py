from flask import request
from http import HTTPStatus
from online_store.model.customers import Customer, Customers
from online_store.helper.request import is_request_data_exists
from online_store.helper.response import failed_response, success_response

def addCustomer():
    """ Add new customer

    Returns:
        flask.Response: success or failed response
    """
    data = request.json

    if (failed := is_request_data_exists(
        data,
        [ 'username' ],
    )) is not None:
        # request data is null
        return failed

    # create new customer
    customer = Customer(
        username = data['username'],
    )

    # add to database
    if (failed := Customers.addCustomer(customer)) is not None:
        # failed save to database
        return failed

    return success_response(
        'Customer has been successfully created',
        None,
    )
