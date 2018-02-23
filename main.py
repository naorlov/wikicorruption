import networkx
import settings
from pymongo import MongoClient
import utils
import pprint
import itertools
import relationship

if __name__ == "__main__":
    connection = utils.build_connection(settings.server_url, settings.db_name)
    users = utils.build_users(connection.declarations)

    for i in users:
        print(i.name)


    for pair in itertools.combinations(users, 2):
        for relation in relationship.find_realations(pair[0], pair[1]):
            print("person_1: {0}; person_2 {1}; relation {2}".format(pair[0].id,  pair[1].id, relation))
