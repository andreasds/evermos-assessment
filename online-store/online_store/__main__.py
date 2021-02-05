import argparse

from online_store import app

if __name__ == '__main__':
    # creating a parser
    parser = argparse.ArgumentParser(
        description='Online Store available command',
    )

    # adding argument
    parser.add_argument(
        '-c', '--conf',
        required=True,
        help='config file path',
        metavar='file_path',
    )

    # parse arguments
    args = parser.parse_args()

    # run the app
    app.run(args)
