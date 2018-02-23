import pymongo
import person
def build_connection(server_adress: str, database: str):
    client = pymongo.MongoClient(server_adress)
    return client[database]

def build_users(database: pymongo.collection.Collection):
    user_ids = set()


    # walk through all declarations and collect people
    for item in database.find():
