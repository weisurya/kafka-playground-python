import psycopg2
import time

import generate_data

DEFAULT_USER = "postgres"
DEFAULT_PASS = "password"
DEFAULT_HOST = "localhost"
DEFAULT_PORT = "5433"
DEFAULT_DATABASE = "postgres"

# DEFAULT ERROR
DB_CONNECTION_ERROR = "DB_CONNECTION_ERROR"

class Postgres:
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT,
                 database=DEFAULT_DATABASE, user=DEFAULT_USER,
                 password=DEFAULT_PASS):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        
    def connect(self):
        self.connection = psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )

        return self.connection

def insert_new_data(connection=None):
    card = generate_data.FakeCard().generate()

    cursor = connection.cursor()

    query = "insert into card \
            (card_number, exp_month, exp_year, cvn) \
            values(%s, %s, %s, %s) \
            returning id"

    cursor.execute(query, (
        card['card_number'],
        card['exp_month'],
        card['exp_year'],
        card['cvn'],
    ))

    connection.commit()

    print(cursor.fetchone()[0])
    

if __name__ == "__main__":
    try:
        while True:
            connection = Postgres().connect()

            insert_new_data(connection)
            time.sleep(1)

    except (KeyboardInterrupt, SystemExit) as e:
        print(e)