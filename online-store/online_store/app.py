import configparser

from online_store.flaskr import FlaskApp
from online_store.flaskr.home import home

def run(args):
    """ Main application

    Args:
        args (ArgumentParser): parsed arguments
    """
    # config file
    config = configparser.ConfigParser()
    config.read_file(open(args.conf))

    # database config
    dbConf = config['database']

    # flask app
    app = FlaskApp()

    # add endpoint
    app.add_endpoint('/', 'home', home, ['GET'])

    # run flask app
    app.run('0.0.0.0', 5000)
