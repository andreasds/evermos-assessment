from http import HTTPStatus
from online_store.helper.database import Database
from online_store.helper.response import failed_response

class Order(object):

    def __init__(self, id=None, order_number='', customer_id=0,
        issued_date=0, order_status=1):
        self.id = id
        self.order_number = order_number
        self.customer_id = customer_id
        self.issued_date = issued_date
        self.order_status = order_status

class Orders(object):

    @staticmethod
    def add_order(order):
        """ Add new order into database

        Args:
            order (Order): new order

        Returns:
            flask.Response: failed response
        """
        query = """
            INSERT INTO orders ( id, order_number, customer_id,
                issued_date, order_status )
            VALUES ( %s, %s, %s,
                %s, %s )
            """
        values = (
            order.id, order.order_number, order.customer_id,
            order.issued_date, order.order_status
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
                'ERROR add new order',
            )

        order.id = id

        return None
