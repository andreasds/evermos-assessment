from http import HTTPStatus
from online_store.helper.database import Database
from online_store.helper.response import failed_response

class Customer(object):

    def __init__(self, id=None, username=''):
        self.id = id
        self.username = username

class Customers(object):

    @staticmethod
    def addCustomer(customer):
        query = """
            INSERT INTO customers ( id, username )
            SELECT * FROM ( SELECT %s, %s ) AS tmp
            WHERE NOT EXISTS (
                SELECT username FROM customers
                WHERE username = %s LIMIT 1
            ) LIMIT 1
            """
        values = (
            customer.id, customer.username,
            customer.username,
        )

        result, failed = Database().storeQuery(query, values)
        if failed is not None:
            # failed save to database
            return failed

        id = result['lastrowid']
        if id == 0:
            # error customer already exists
            return failed_response(
                HTTPStatus.CONFLICT,
                'ERROR customer already exist',
            )

        customer.id = id

        return None
