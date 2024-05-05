import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class DB:
    """Class handles postgres db interactions
        Currently only connection initialization and insertion is needed
    """

    def __init__(self):

        # load db values from .env file
        db_name = os.environ.get('POSTGRES_DB')
        username = os.environ.get('POSTGRES_USER')
        password = os.environ.get('POSTGRES_PASSWORD')
        host = os.environ.get('POSTGRES_HOST')
        port = os.environ.get('POSTGRES_PORT')

        # initalize connection to postgres database
        try:
            self.conn = psycopg2.connect(
                dbname=db_name, user=username, password=password, host=host, port=port)
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor = self.conn.cursor()

        except Exception as e:
            print("Error connecting to database. Exiting program...")
            exit(0)

    def insert(self, item, table):
        """Inserts given item into given table in postgres database

        :param item: dictionary item representing narcotic product
        :param table: name of the postgres table to insert item

        """
        try:
            print(f"\nInserting {item.get('title')} into database...")
            self.cursor.execute(f"insert into {table} (%s) values (%s)" % (
                ','.join(item), ','.join('%%(%s)s' % k for k in item)), item)

            return item

        except:
            print("Error inserting item into database, continuing...")
