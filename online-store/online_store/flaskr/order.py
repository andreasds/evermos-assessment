import hashlib
import time

from datetime import datetime
from flask import request
from http import HTTPStatus
from online_store.model.carts import Cart, Carts
from online_store.model.order_products import OrderProduct, OrderProducts
from online_store.model.orders import Order, Orders
from online_store.model.products import Product, Products
from online_store.helper.database import Database
from online_store.helper.request import is_request_data_exists
from online_store.helper.response import failed_response, success_response

def order_step(data):
    # TODO: handle rollback if failed in the middle of process
    customer_id = data['customer_id']

    # check available product stock in cart
    carts, failed = Carts.get_cart(customer_id)
    if failed is not None:
        # failed to fetch from database
        return failed

    if len(carts) == 0:
        # empty cart
        return failed_response(
            HTTPStatus.PRECONDITION_FAILED,
            "ERROR cart is empty",
        )

    for product in carts:
        if product['out_of_stock']:
            # there is out of stock product
            return failed_response(
                HTTPStatus.PRECONDITION_FAILED,
                "ERROR some product is out of stock",
            )

    # create new order
    order_number = ''.join([
        str(customer_id), '_', str(time.time_ns())
    ])
    hash_order_number = hashlib.sha1(
        bytes(order_number, 'utf-8'),
    ).hexdigest()
    order = Order(
        order_number = hash_order_number,
        customer_id = customer_id,
        issued_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    )

    # add to database
    if (failed := Orders.add_order(order)) is not None:
        # failed save to database
        return failed

    # add ordered product to database
    for cart in carts:
        product_id = cart['product_id']
        quantity = cart['quantity']

        order_product = OrderProduct(
            order_id = order.id,
            product_id = product_id,
            quantity = quantity,
        )

        # add ordered product to database
        if (failed := OrderProducts.add_order_product(order_product)) is not None:
            # failed save to database
            return failed

        product = Product(
            id = product_id,
            stock = quantity,
        )

        # updating stock product in database
        if (failed := Products.sell_product(product)) is not None:
            # failed update database
            return failed

        cart = Cart(
            customer_id = customer_id,
            product_id = product_id,
        )

        # remove ordered product from cart
        if (failed := Carts.remove_cart(cart)) is not None:
            # failed remove in database
            return failed

    return None

def add_order():
    """ Create new order

    Returns:
        flask.Response: success or failed response
    """
    data = request.json

    if (failed := is_request_data_exists(
        data,
        [ 'customer_id' ],
    )) is not None:
        # request data is null
        return failed

    with_lock = True if 'with_lock' not in data else data['with_lock']
    if with_lock:
        # get stock mutex
        with Database().stock_lock:
            if (failed := order_step(data)) is not None:
                # something failed when create order
                return failed
    else:
        if (failed := order_step(data)) is not None:
            # something failed when create order
            return failed

    return success_response(
        'Order has been successfully updated',
        None,
    )
