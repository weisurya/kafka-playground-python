import boto3
import json
import time
import os

import generate_data

DEFAULT_REGION = "us-east-1"
DEFAULT_AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
DEFAULT_AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
DEFAULT_TOPIC = "kinesis-topic"

class Kinesis:
    def __init__(self, region=DEFAULT_REGION):
        self.region = region

    def connect(self):
        session = boto3.Session(
            region_name=self.region
        )

        client = session.client('kinesis',
            aws_access_key_id=DEFAULT_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=DEFAULT_AWS_SECRET_ACCESS_KEY,
        )

        return client

    def list_streams(self, client=None):
        return client.list_streams()

    def create_stream(self, client=None, topic=None, replica=1):
        if topic not in self.list_streams(client)['StreamNames']:
            return client.create_stream(
                StreamName=topic,
                ShardCount=replica,
            )

        print(f"Stream of {topic} is exist.. Skip new stream creation.\n")

    def send_data(self, client=None, topic=None, 
                  key=None, value=None):
        return client.put_record(
            StreamName=topic,
            PartitionKey=key,
            Data=json.dumps(value),
        )

def stream_new_data(client=None, topic=None):
    data = generate_data.FakeLog().generate()

    response = Kinesis().send_data(
        client=client,
        topic=topic,
        key="test",
        value=data,
    )

    print(response)

def get_data(client=None, topic=None):
    response = client.get_shard_iterator(
        StreamName=DEFAULT_TOPIC,
        ShardId="shardId-000000000000",
        ShardIteratorType="TRIM_HORIZON",
    )

    print(response)

if __name__ == "__main__":
    try:
        client = Kinesis().connect()

        Kinesis().create_stream(client, DEFAULT_TOPIC, 1)

        print(Kinesis().list_streams(client))

        while True:
            stream_new_data(client, DEFAULT_TOPIC)
            time.sleep(1)

            


    except (KeyboardInterrupt, SystemExit) as e:
        print(e)