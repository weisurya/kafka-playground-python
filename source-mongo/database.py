from pymongo import MongoClient
import time

import generate_data

DEFAULT_URL = "mongodb+srv://admin:P4ssw0rd@surya-playground-jw0cq.mongodb.net/test?retryWrites=true&w=majority"
DEFAULT_DB = "data"
DEFAULT_COLLECTION = 'user'

class Mongo:
    def __init__(self, url=DEFAULT_URL, database=DEFAULT_DB):
        self.url = url
        self.database = database

    def connect(self):
        return MongoClient(self.url)[self.database]

def insert_new_data():
    user = generate_data.FakeUser().generate()

    mongo = Mongo().connect()
    inserted_data = mongo[DEFAULT_COLLECTION].insert_one(dict(user))
    print(inserted_data.inserted_id)
        
if __name__ == "__main__":
    try:
        while True:
            insert_new_data()
            time.sleep(1)

    except (KeyboardInterrupt, SystemExit) as e:
        print(e)