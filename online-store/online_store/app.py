from online_store.flaskr import FlaskApp
from online_store.flaskr.home import home

def run():
    """ Main application
    """
    app = FlaskApp()

    app.add_endpoint('/', 'home', home, ['GET'])

    app.run('0.0.0.0', 5000)