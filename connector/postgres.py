import json
import requests

KAFKA_BROKER_URL = "localhost:9092"
KAFKA_CONNECT_URL = "http://localhost:8083/connectors"

PG_HOST = "postgres"
PG_PORT = "5432"
PG_USER = "admin"
PG_PASS = "password"
PG_DB = "postgres"
PG_NAME = "fake-card"

PG_WHITELIST_TABLE = "public.data"

PG_CONNECT_TOPIC = "database.postgres.card"
PG_CONNECT_CONFIG = {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "tasks.max": "1",
    "database.hostname": PG_HOST,
    "database.port": PG_PORT,
    "database.user": PG_USER,
    "database.password": PG_PASS,
    "database.server.name": PG_NAME,
    "database.dbname": PG_DB,
    "database.whitelist": PG_WHITELIST_TABLE,
    "database.history.kafka.bootstrap.servers": KAFKA_BROKER_URL,
    "database.history.kafka.topic": PG_CONNECT_TOPIC,
}

class PostgresConnector:
    def __init__(self, connect_url=None, connect_name=None,
                 connect_config=None):
        self.connect_url = connect_url
        self.connect_name = connect_name
        self.connect_config = connect_config

        if self.__connector_is_exist() is not True:
            print(f"Connector {self.connect_name} is not exist. Please create a new connector.")
        else:
            raise ValueError(f"Connector {self.connect_name} is exist! Please delete it first.")

    def connect(self):
        response = requests.post(
            self.connect_url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            data=json.dumps({
                "name": self.connect_name,
                "config": self.connect_config,
            })
        )

        response.raise_for_status()

    def __connector_is_exist(self):
        response = requests.get(f"{self.connect_url}/{self.connect_name}")

        if response.status_code == 200:
            return True

        return False

if __name__ == "__main__":
    try:
        print(PG_CONNECT_CONFIG)
        pg_connect = PostgresConnector(
            connect_url=KAFKA_CONNECT_URL,
            connect_name=PG_CONNECT_TOPIC,
            connect_config=PG_CONNECT_CONFIG,
        )

        client = pg_connect.connect()
        print(client)

    except Exception as e:
        print(e)
