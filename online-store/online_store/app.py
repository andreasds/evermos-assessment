import configparser

from online_store.flaskr import FlaskApp
from online_store.flaskr.customer import addCustomer
from online_store.flaskr.home import home
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

    app.add_endpoint('/customer/add', 'addCustomer', addCustomer, ['POST'])

    # run flask app
    app.run('0.0.0.0', 5000)
