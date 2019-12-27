import json
import requests

KAFKA_BROKER_URL = "localhost:9092"
KAFKA_CONNECT_URL = "http://localhost:8083/connectors"

MONGO_REPLICA_SET = "rs0"
MONGO_URL = "surya-playground-shard-00-00-jw0cq.mongodb.net:27017,surya-playground-shard-00-01-jw0cq.mongodb.net:27017,surya-playground-shard-00-02-jw0cq.mongodb.net:27017"
MONGO_USER = "admin"
MONGO_PASS = "P4ssw0rd"
MONGO_DB = "data"

MONGO_WHITELIST_COLLECTION = "data.user"
MONGO_BLACKLIST_FIELD = "*.*.last_location"

MONGO_CONNECT_PREFIX = "mongo"
MONGO_CONNECT_TOPIC = "database.mongo.user"
MONGO_CONNECT_CONFIG = {
    "name": MONGO_CONNECT_TOPIC,
    "connector.class": "io.debezium.connector.mongodb.MongoDbConnector",
    "tasks.max": "1",
    "mongodb.hosts": MONGO_URL,
    "mongodb.name": MONGO_CONNECT_PREFIX,
    "mongodb.user": MONGO_USER,
    "mongodb.password": MONGO_PASS,
    "mongodb.ssl.enabled": True,
    "database.whitelist": MONGO_DB,
    "database.history.kafka.bootstrap.servers" : KAFKA_BROKER_URL,
    "collection.whitelist": MONGO_WHITELIST_COLLECTION,
    "field.blacklist": MONGO_BLACKLIST_FIELD,
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable": "false",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",
    "transforms": "route",
    "transforms.route.type" : "org.apache.kafka.connect.transforms.RegexRouter",
    "transforms.route.regex" : "([^.]+)\\.([^.]+)\\.([^.]+)",
    "transforms.route.replacement" : "$2.$3"
}


class MongoConnector:
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

        return response.json()

    def __connector_is_exist(self):
        response = requests.get(f"{self.connect_url}/{self.connect_name}")

        if response.status_code == 200:
            return True

        return False

if __name__ == "__main__":
    try:
        mongo_connect = MongoConnector(
            connect_url=KAFKA_CONNECT_URL,
            connect_name=MONGO_CONNECT_TOPIC,
            connect_config=MONGO_CONNECT_CONFIG,
        )

        client = mongo_connect.connect()
        print(client)

    except Exception as e:
        print(e)
