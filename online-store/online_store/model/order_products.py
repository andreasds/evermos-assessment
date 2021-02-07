from http import HTTPStatus
from online_store.helper.database import Database
from online_store.helper.response import failed_response

class OrderProduct(object):

    def __init__(self, order_id=None, product_id=None, quantity=1):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity

class OrderProducts(object):

    @staticmethod
    def add_order_product(order_product):
        """ Add new order product into database

        Args:
            order_product (OrderProduct): new order product

        Returns:
            flask.Response: failed response
        """
        query = """
            INSERT INTO order_products ( order_id, product_id, quantity )
            VALUES ( %s, %s, %s )
            """
        values = (
            order_product.order_id, order_product.product_id,
            order_product.quantity,
        )

        _, failed = Database().storeQuery(query, values)
        if failed is not None:
            # failed save to database
            return failed

        return None

    @staticmethod
    def get_product_ordered(product_id):
        """ Get total product ordered

        Args:
            order_product (OrderProduct): product id

        Returns:
            flask.Response: failed response
        """
        query = """
            SELECT SUM(quantity) AS total
            FROM order_products
            WHERE product_id = %s
            GROUP BY product_id
            """
        values = ( product_id, )

        result, failed = Database().fetchQuery(query, values)
        if failed is not None:
            # failed fetch from database
            return [], failed

        if len(result) == 0:
            return 0, failed_response(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                'ERROR product not found in order',
            )

        return int(result[0][0]), failed
