from main_server.graph_client import GraphClient, BufferedRequestQueue
from main_server.person import PersonFactory
import pymongo
import itertools
import main_server.settings
import main_server.heuristic as heuristic

def get_id_from_document(document):
    return document["main"]["person"]["id"]

def build_connection(server_adress: str, database: str):
    client = pymongo.MongoClient(server_adress)
    return client[database]

def build_users(database: pymongo.collection.Collection):
    users = dict()

    cursor = database.find() # get all documents
    counter = 0
    for document in cursor:
        current_user_id = get_id_from_document(document)
        if current_user_id not in users:
            users[current_user_id] = PersonFactory.create(document)
        users[current_user_id].update(document)
        counter += 1
        if counter % 1000 == 0:
            print(counter)
        if counter == 10000:
            break
    return users.values()

# from internal user representation to MongoDB
def build_graph(users: list, edges: pymongo.collection.Collection):
    # client = GraphClient(settings.graph_server_credits)
    # for user in users:
    #    client.add_vertex(user.id)

    curr_edge = 0
    counter = 0
    for p1, p2 in itertools.combinations(users, 2):
        #client.add_edge(p1.id, p2.id, key=curr_edge)
        features = heuristic.find_relations(p1, p2, deep=False)
        if len(features) != 0:
            print(features)
            print(p1.surname, p1.name)
            print(p1.real_estates)
            print(p2.surname, p2.name)
            print(p2.real_estates)
            break
            # edges.insert_one({'eid': curr_edge,
            #                  'features': features})
            curr_edge += 1
        counter += 1
        if counter % 10000 == 0:
            print(counter)
    return curr_edge
