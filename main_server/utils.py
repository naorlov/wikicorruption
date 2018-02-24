import pymongo
from person import *
import itertools
import networkx
import heuristic

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

# from internal user representation to MongoDB
def build_users_db(connection: pymongo.collection.Collection, users: list):
    db_result = {}
    graph_result = networkx.Graph()
    cur_edge_num = 0

    for p1, p2 in itertools.combinations(users, 2):
        cur_edge = []
        graph_result.add_edge(p1["id"], p2["id"], key=cur_edge_num)
        
        # for relation in heuristic.find_realations(p1["id"], p2["id"]):
        #     cur_edge.append({
        #         "type": type(relation),
        #         "confidence": relation.confidence
        #     })
        pass


    return db_result, graph_result
