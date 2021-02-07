import mysql.connector as mysql

from http import HTTPStatus
from mysql.connector import Error
from online_store.helper.response import failed_response
from online_store.helper.singleton import Singleton
from threading import Lock

class Database(metaclass=Singleton):

    def __init__(self):
        """ Database singleton class
        """
        self.__ready = False
        self.stock_lock = Lock()

    def setConfig(self, dbConf):
        """ Config database

        Args:
            dbConf (dict): database config
        """
        self.__host = dbConf['dbHost']
        self.__port = dbConf['dbPort']
        self.__db = dbConf['db']
        self.__user = dbConf['dbUser']
        self.__pwd = dbConf['dbPwd']
        self.__ready = True

    def storeQuery(self, query, values):
        """ Store query and commit

        Args:
            query (string): query script
            values (tuple): value query

        Raises:
            SystemError: error when database is not configured yet

        Returns:
            (tuple):
                - (dict): query result, lastrowid and rowcount
                - (flask.Response): failed response
        """
        if not self.__ready:
            raise SystemError('Database is not configured yet.')

        failed = None
        db = None
        cursor = None
        result = None
        try:
            # connect to database
            db = mysql.connect(
                user=self.__user,
                password=self.__pwd,
                database=self.__db,
                host=self.__host,
                port=self.__port,
            )

            if db.is_connected():
                cursor = db.cursor()
                cursor.execute(query, values)

                # get insert id or affected row
                result = {
                    'lastrowid': cursor.lastrowid,
                    'rowcount': cursor.rowcount,
                }

                db.commit()
            else:
                print('Failed connect to database.')
                failed = failed_response(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    'ERROR failed connect to database',
                )
        except Error as e:
            print('Error connection to database:', e)
            failed = failed_response(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                ' '.join([ 'ERROR connection to database.', str(e) ]),
            )
        finally:
            if db is not None and \
                db.is_connected():
                if cursor is not None:
                    cursor.close()

                db.close()

        return result, failed

    def fetchQuery(self, query, values):
        """ Fetch query result

        Args:
            query (string): query script
            values (tuple): value query

        Raises:
            SystemError: error when database is not configured yet

        Returns:
            (tuple):
                - (array): query result
                - (flask.Response): failed response
        """
        if not self.__ready:
            raise SystemError('Database is not configured yet.')

        failed = None
        db = None
        cursor = None
        result = None
        try:
            # connect to database
            db = mysql.connect(
                user=self.__user,
                password=self.__pwd,
                database=self.__db,
                host=self.__host,
                port=self.__port,
            )

            if db.is_connected():
                cursor = db.cursor()
                cursor.execute(query, values)
                result = cursor.fetchall()
            else:
                print('Failed connect to database.')
                failed = failed_response(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    'ERROR failed connect to database',
                )
        except Error as e:
            print('Error connection to database:', e)
            failed = failed_response(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                ' '.join([ 'ERROR connection to database.', str(e) ]),
            )
        finally:
            if db is not None and \
                db.is_connected():
                if cursor is not None:
                    cursor.close()

                db.close()

        return result, failed
