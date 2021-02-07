import json

from flask import request
from http import HTTPStatus
from online_store.model.products import Product, Products
from online_store.helper.request import is_request_data_exists
from online_store.helper.response import failed_response, success_response

def get_all_product():
    """ Collect all products

    Returns:
        flask.Response: success or failed response
    """
    # fetch all products from database
    result, failed = Products.get_products()
    if failed is not None:
        # failed to fetch from database
        return failed

    return success_response(
        'Product has been successfully fetched',
        result,
    )

def get_product(product_id):
    """ Collect product detail

    Returns:
        flask.Response: success or failed response
    """
    # fetch all products from database
    result, failed = Products.get_product(product_id)
    if failed is not None:
        # failed to fetch from database
        return failed

    return success_response(
        'Product has been successfully fetched',
        result,
    )

def add_product():
    """ Add new product

    Returns:
        flask.Response: success or failed response
    """
    data = request.json

    if (failed := is_request_data_exists(
        data,
        [ 'product_name', 'stock' ],
    )) is not None:
        # request data is null
        return failed

    # create new product
    product = Product(
        product_name = data['product_name'],
        stock = data['stock'],
    )

    # add to database
    if (failed := Products.add_product(product)) is not None:
        # failed save to database
        return failed

    return success_response(
        'Product has been successfully created',
        json.dumps(product.__dict__),
    )

def add_stock_product():
    """ Add stock product

    Returns:
        flask.Response: success or failed response
    """
    data = request.json

    if (failed := is_request_data_exists(
        data,
        [ 'product_id', 'stock' ],
    )) is not None:
        # request data is null
        return failed

    # update product stock
    product = Product(
        id = data['product_id'],
        stock = data['stock'],
    )

    # update database
    if (failed := Products.add_stock_product(product)) is not None:
        # failed to update database
        return failed

    return success_response(
        'Product stock has been successfully updated',
        None,
    )
