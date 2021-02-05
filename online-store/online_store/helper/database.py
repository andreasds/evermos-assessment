import mysql.connector as mysql

from mysql.connector import Error
from online_store.helper.singleton import Singleton

class Database(metaclass=Singleton):

    def __init__(self):
        """ Database singleton class
        """
        self.__ready = False

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
        """
        if not self.__ready:
            raise SystemError('Database is not configured yet.')

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
                db.commit()
            else:
                print('Failed connect to database.')
        except Error as e:
            print('Error connection to database:', e)
        finally:
            if db.is_connected():
                cursor.close()
                db.close()

    def fetchQuery(self, query, values):
        """ Fetch query result

        Args:
            query (string): query script
            values (tuple): value query

        Raises:
            SystemError: error when database is not configured yet

        Returns:
            array: query result
        """
        if not self.__ready:
            raise SystemError('Database is not configured yet.')

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
        except Error as e:
            print('Error connection to database:', e)
        finally:
            if db.is_connected():
                cursor.close()
                db.close()

        return result
