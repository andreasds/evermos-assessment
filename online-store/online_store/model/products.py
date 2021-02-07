from http import HTTPStatus
from online_store.helper.database import Database
from online_store.helper.response import failed_response

class Product(object):

    def __init__(self, id=None, product_name='', stock=0):
        self.id = id
        self.product_name = product_name
        self.stock = stock

class Products(object):

    @staticmethod
    def get_products():
        """ Get all products

        Returns:
            (tuple):
                - (array): query result
                - (flask.Response): failed response
        """
        query = """
            SELECT id, product_name, stock
            FROM products
            ORDER BY product_name ASC
            """
        values = ()

        result, failed = Database().fetchQuery(query, values)
        if failed is not None:
            # failed fetch from database
            return [], failed

        result = [ {
                'id': product[0],
                'product_name': product[1],
                'stock': product[2],
            } for product in result ]

        return result, failed

    @staticmethod
    def add_product(product):
        """ Add new product into database

        Args:
            product (Product): new product

        Returns:
            flask.Response: failed response
        """
        query = """
            INSERT INTO products ( id, product_name, stock )
            VALUES ( %s, %s, %s )
            """
        values = (
            product.id, product.product_name, product.stock,
        )

        result, failed = Database().storeQuery(query, values)
        if failed is not None:
            # failed save to database
            return failed

        id = result['lastrowid']
        if id == 0:
            # something error
            return failed_response(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                'ERROR add new product',
            )

        product.id = id

        return None

    @staticmethod
    def add_stock_product(product):
        """ Add stock with new quantity

        Args:
            product (Product): new product stock

        Returns:
            flask.Response: failed response
        """
        query = """
            UPDATE products
            SET stock = stock + %s
            WHERE id = %s
            """
        values = (
            product.stock, product.id,
        )

        result, failed = Database().storeQuery(query, values)
        if failed is not None:
            # failed update in database
            return failed

        affectedRow = result['rowcount']
        if affectedRow == 0:
            # something error
            return failed_response(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                'ERROR updating stock product',
            )

        return None

    @staticmethod
    def sell_product(product):
        """ Substract stock with ordered quantity

        Args:
            product (Product): ordered product

        Returns:
            flask.Response: failed response
        """
        query = """
            UPDATE products
            SET stock = stock - %s
            WHERE id = %s
            """
        values = (
            product.stock, product.id,
        )

        result, failed = Database().storeQuery(query, values)
        if failed is not None:
            # failed update in database
            return failed

        affectedRow = result['rowcount']
        if affectedRow == 0:
            # something error
            return failed_response(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                'ERROR updating stock product',
            )

        return None
