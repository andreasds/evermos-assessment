from flask import Flask
from online_store.helper.singleton import Singleton

class FlaskApp(metaclass=Singleton):

    def __init__(self):
        """ Main Flask application
        """
        self.app = Flask('Online Store Application')

    def run(self, host, port):
        """ Start Flask application server

        Args:
            host (string): host ip
            port (int): port address
        """
        self.app.run(host=host, port=port)

    def add_endpoint(self, endpoint, endpoint_name, handler, methods):
        """ Add new endpoint

        Args:
            endpoint (string): endpoint url
            endpoint_name (string): unique name for endpoint
            handler (func): handler function
            methods (array): list http method supported
        """
        self.app.add_url_rule(
            endpoint,
            endpoint_name,
            handler,
            methods=methods,
        )
