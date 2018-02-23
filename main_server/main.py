import networkx
import main_server.settings as settings
from pymongo import MongoClient
import main_server.utils as utils
import pprint
import itertools
<<<<<<< HEAD

from graph_client import GraphClient
=======
import main_server.relationship as relationship
from main_server.graph_client import GraphClient
>>>>>>> 6ef6a2432e075c8fc691a07342d2dc5860f77dba


if __name__ == "__main__":
    client = GraphClient(settings.graph_server_credits)
    client.add_vertex(1)
    client.add_vertex(2)
    client.add_edge(1, 2, 10)



# connection = utils.build_connection(settings.server_url, settings.db_name)
# users = utils.build_users(connection.declarations)
#
#  for i in users:
#      print(i.name)
#

#  for pair in itertools.combinations(users, 2):
#      for relation in relationship.find_realations(pair[0], pair[1]):
#         print("person_1: {0}; person_2 {1}; relation {2}".format(pair[0].id,  pair[1].id, relation))
