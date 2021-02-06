import configparser

from online_store.flaskr import FlaskApp
from online_store.flaskr.cart import add_cart, get_cart
from online_store.flaskr.customer import add_customer
from online_store.flaskr.home import home
from online_store.flaskr.product import add_product, get_all_product
from online_store.helper.database import Database

def run(args):
    """ Main application

    Args:
        args (ArgumentParser): parsed arguments
    """
    # config file
    config = configparser.ConfigParser()
    config.read_file(open(args.conf))

    # setup database
    dbConf = config['database']
    db = Database()
    db.setConfig(dbConf)

    # flask app
    app = FlaskApp()

    # add endpoint
    app.add_endpoint('/', 'home', home, ['GET'])

    app.add_endpoint('/customer/add', 'addCustomer', add_customer, ['POST'])

    app.add_endpoint('/product/all', 'getProducts', get_all_product, ['GET'])
    app.add_endpoint('/product/add', 'addProduct', add_product, ['POST'])

    app.add_endpoint('/cart/<int:customer_id>', 'getCart', get_cart, ['GET'])
    app.add_endpoint('/cart/add', 'addCart', add_cart, ['POST'])

    # run flask app
    app.run('0.0.0.0', 5000)
