import pymongo
from person import *

def get_id_from_document(document):
    return document["main"]["person"]["id"]

def build_connection(server_adress: str, database: str):
    client = pymongo.MongoClient(server_adress)
    return client[database]

def build_users(database: pymongo.collection.Collection):
    users = dict()

    cursor = database.find() # get all documents
    for document in cursor:
        current_user_id = get_id_from_document(document)
        if current_user_id not in users:
            users[current_user_id] = PersonFactory.create(document)
        users[current_user_id].update(document)
    return users.values()
