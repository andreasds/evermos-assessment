from http import HTTPStatus
from online_store.helper.database import Database
from online_store.helper.response import failed_response

class Cart(object):

    def __init__(self, customer_id=None, product_id=None, quantity=1):
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity

class Carts(object):

    @staticmethod
    def get_cart(customer_id):
        """ Collect products in customer cart

        Args:
            customer_id (int): customer id

        Returns:
            flask.Response: failed response
        """
        query = """
            SELECT customer_id, product_id, quantity,
                IF ( quantity <= stock, 0, 1 ) AS out_of_stock
            FROM carts
            LEFT JOIN products ON products.id = carts.product_id
            WHERE carts.customer_id = %s
            """
        values = ( customer_id, )

        result, failed = Database().fetchQuery(query, values)
        if failed is not None:
            # failed fetch from database
            return [], failed

        result = [ {
                'customer_id': cart[0],
                'product_id': cart[1],
                'quantity': cart[2],
                'out_of_stock': bool(cart[3]),
            } for cart in result ]

        return result, failed

    @staticmethod
    def add_cart(cart):
        """ Add product into customer cart

        Args:
            cart (Cart): new cart

        Returns:
            flask.Response: failed response
        """
        query = """
            REPLACE INTO carts ( customer_id, product_id, quantity )
            VALUES ( %s, %s, %s )
            """
        values = (
            cart.customer_id, cart.product_id, cart.quantity,
        )

        _, failed = Database().storeQuery(query, values)
        if failed is not None:
            # failed save to database
            return failed

        return None

    @staticmethod
    def remove_cart(cart):
        """ Remove product in customer cart

        Args:
            cart (Cart): removed cart

        Returns:
            flask.Response: failed response
        """
        query = """
            DELETE FROM carts
            WHERE customer_id = %s AND product_id = %s
            """
        values = (
            cart.customer_id, cart.product_id,
        )

        _, failed = Database().storeQuery(query, values)
        if failed is not None:
            # failed save to database
            return failed

        return None
