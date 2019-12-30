import json
import requests
import os

KAFKA_BROKER_URL = "localhost:9092"
KAFKA_CONNECT_URL = "http://localhost:8083/connectors"
KAFKA_REPLICATION_FACTOR = "1"

DEFAULT_AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
DEFAULT_AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')

KINESIS_REGION = "US_EAST_1"
KINESIS_TOPIC = "kinesis-topic"

KINESIS_CONNECT_TOPIC = "stream.kinesis.log"
KINESIS_CONNECT_CONFIG = {
    "name": KINESIS_CONNECT_TOPIC,
    "connector.class": "io.confluent.connect.kinesis.KinesisSourceConnector",
    "tasks.max": "1",
    "kinesis.region": KINESIS_REGION,
    "kinesis.stream": KINESIS_TOPIC,
    # "confluent.license": "",
    "kafka.topic": KINESIS_CONNECT_TOPIC,
    "confluent.topic.bootstrap.servers": KAFKA_BROKER_URL,
    "confluent.topic.replication.factor": KAFKA_REPLICATION_FACTOR,
    "aws.access.key.id": DEFAULT_AWS_ACCESS_KEY_ID,
    "aws.secret.key.id": DEFAULT_AWS_SECRET_ACCESS_KEY,
}


class KinesisConnector:
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

        print(response.json())

        response.raise_for_status()

        return response.json()

    def __connector_is_exist(self):
        response = requests.get(f"{self.connect_url}/{self.connect_name}")

        if response.status_code == 200:
            return True

        return False

if __name__ == "__main__":
    try:
        mongo_connect = KinesisConnector(
            connect_url=KAFKA_CONNECT_URL,
            connect_name=KINESIS_CONNECT_TOPIC,
            connect_config=KINESIS_CONNECT_CONFIG,
        )

        client = mongo_connect.connect()
        print(client)

    except Exception as e:
        print(e)
