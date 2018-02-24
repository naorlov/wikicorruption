from main_server.graph_client import GraphClient
import pymongo
import pymongo.database


class Engine:
    user_comment_weight = 10
    confirmation_weight = 5

    def __init__(self, declarator_data: pymongo.database,
                 edges_data: pymongo.database,
                 graph_connection: GraphClient):
        self.declarator_data = declarator_data
        self.edges_data = edges_data
        self.graph_connection = graph_connection

    """accepts string and returns list of relevant user ids"""

    def get_person_id(self, family_name="", given_name="", patronymic_name=""):
        records = self.declarator_data.declarations.find(
            {
                "$and":
                    [
                        {"main.person.given_name": given_name},
                        {"main.person.family_name": family_name},
                        {"main.person.patronymic_name": patronymic_name}
                    ]

            }
        )
        return list(set([item["main"]["person"]["id"] for item in records]))

    """
    gets person_id and returns summary: incomes, work and other
    format:
    {
        "last_year_income": <number>,
        "max_income": (<year>, <number>),
        "min_income": (<year>, <number>),
        "max_area": <number>,
    }    
    """

    def get_user_summary(self, person_id):
        result = {}
        documents = self.declarator_data.declarations.find({"main.person.id": person_id})
        for item in documents:
            if item["main"]["year"] == 2017:
                result["last_year_income"] = item["incomes"][0]["size"]
            result["max_area"] = max(
                [estate["square"] for estate in item["real_estates"]]
            )
        #result["max_income"] = max([(item["incomes"]["size"] for item in documents)])      # WRONG
        #result["min_income"] = min([(item["incomes"]["size"] for item in documents)])
        return result

    """
    gets person_id and returns full available info
    Person instance
    """

    def get_user_info(self, person_id):
        pass

    """
    gets person_id and returns all neighbourgs
    {
        <uid>: <list of heuristcs>,
        ...
    }
    """

    def get_neighbourgs(self, person_id):
        try:
            connected_persons = self.graph_connection.get_adjacent(person_id)
            return connected_persons['response']
        except:
            return []

    """
    gets two person_ids and returns heuristcs or None, if no connection found
    """

    def get_connection(self, person_id1, person_id2):
        try:
            edge = self.graph_connection.get_edge(person_id1, person_id2)['response']
            eid = int(edge['key'])
            weight = int(edge['weight'])
            return weight, self.edges_data.test_edges.find({"eid": eid})[0]
        except:
            return None, None


    """
    adds heuristic connection between people
    """

    def add_connection(self, person_id1, person_id2, user_coment):
        eid = 0
        weight = 0
        try:
            edge = self.graph_connection.get_edge(person_id1, person_id2)['response']
            eid = int(edge['key'])
            weight = int(edge['weight'])
        except:
            eid = 1 + self.edges_data.test_edges.find().count()
            self.graph_connection.add_edge(person_id1, person_id2, eid)
            self.edges_data.test_edges.insert_one({'eid': eid, 'features': []})
        weight += self.user_comment_weight
        self.graph_connection.update_weight(eid, weight)
        features = self.edges_data.test_edges.find({'eid': eid})[0]['features']
        features.append({'plus_w': self.user_comment_weight, 'minus_w': 0, 'user_comment': user_coment})
        self.edges_data.test_edges.update_one({'eid': eid}, {'$set': {'features': features}})



    """
    confirms connection between people
    """

    def confirm_connection(self, person_id1, person_id2, heuristic):
        try:
            edge = self.graph_connection.get_edge(person_id1, person_id2)['response']
            eid = int(edge['key'])
            weight = int(edge['weight']) + self.confirmation_weight
            self.graph_connection.update_weight(eid, weight)
            self.edges_data.test_edges.update_one({'eid': eid},
                                {'$inc': {'features.' + str(heuristic) + '.plus_w': self.confirmation_weight}})
        except:
            print('WARNING: edge not found')


    def decline_connection(self, person_id1, person_id2, heuristic):
        try:
            edge = self.graph_connection.get_edge(person_id1, person_id2)['response']
            eid = int(edge['key'])
            weight = int(edge['weight']) - self.confirmation_weight
            self.graph_connection.update_weight(eid, weight)
            self.edges_data.test_edges.update_one({'eid': eid},
                                {'$inc': {'features.' + str(heuristic) + '.minus_w': self.confirmation_weight}})
        except:
            print('WARNING: edge not found')



graph_server_credits = {
    "url": "http://35.204.32.159",
    "port": "80"
}
gc = GraphClient(graph_server_credits)
db = pymongo.MongoClient('mongodb://35.229.26.187:2700/declarator').declarator

en = Engine(db, db, gc)
print(en.get_person_id('Путин', 'Владимир', 'Владимирович'))
print(en.get_user_summary(582))
print(en.get_neighbourgs(582))
# print(en.get_connection(8, 182))
# print(en.get_connection(281, 8))
# print(en.get_connection(282, 8))
# #en.add_connection(8, 182, "JUST TEST")
# #en.add_connection(8, 183, "ANOTHER TEST")
# #en.add_connection(0, 0, "TEST")
#
# #en.confirm_connection(8, 182, 0)
# en.decline_connection(8, 182, 1)

