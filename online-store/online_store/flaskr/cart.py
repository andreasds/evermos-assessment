from flask import request
from http import HTTPStatus
from online_store.model.carts import Cart, Carts
from online_store.helper.request import is_request_data_exists
from online_store.helper.response import failed_response, success_response

def get_cart(customer_id):
    """ Collect all products in cart

    Returns:
        flask.Response: success or failed response
    """
    # fetch all products in cart
    result, failed = Carts.get_cart(customer_id)
    if failed is not None:
        # failed to fetch from database
        return failed

    return success_response(
        'Cart has been successfully fetched',
        result,
    )

def add_cart():
    """ Add product into customer cart

    Returns:
        flask.Response: success or failed response
    """
    data = request.json

    if (failed := is_request_data_exists(
        data,
        [ 'customer_id', 'product_id', 'quantity' ],
    )) is not None:
        # request data is null
        return failed

    # create new cart
    cart = Cart(
        customer_id = data['customer_id'],
        product_id = data['product_id'],
        quantity = data['quantity'],
    )

    # add to database
    if (failed := Carts.add_cart(cart)) is not None:
        # failed save to database
        return failed

    return success_response(
        'Cart has been successfully updated',
        None,
    )

def remove_cart():
    """ Remove product in customer cart

    Returns:
        flask.Response: success or failed response
    """
    data = request.json

    if (failed := is_request_data_exists(
        data,
        [ 'customer_id', 'product_id' ],
    )) is not None:
        # request data is null
        return failed

    # removed cart
    cart = Cart(
        customer_id = data['customer_id'],
        product_id = data['product_id'],
    )

    # remove product in cart
    if (failed := Carts.remove_cart(cart)) is not None:
        # failed to remove
        return failed

    return success_response(
        'Product in cart has been successfully removed',
        None,
    )
