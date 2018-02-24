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
                result["last_year_income"] = item["incomes"]["size"]
            result["max_area"] = max(
                [estate["square"] for estate in item["real_estates"]] + result["max_area"]
            )
        #result["max_income"] = max([(item["incomes"]["size"], item["main"]["year"] for item in documents)])[::-1]
        #result["max_income"] = min([(item["incomes"]["size"], item["main"]["year"] for item in documents)])[::-1]
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
        connected_persons = self.graph_connection.get_adjacent(person_id)
        return connected_persons['response']

    """
    gets two person_ids and returns heuristcs or None, if no connection found
    """

    def get_connection(self, person_id1, person_id2):
        try:
            edge = self.graph_connection.get_edge(person_id1, person_id2)['response']
            eid = edge['key']
            weight = edge['weight']
            return weight, self.edges_data.edges.find({"eid": eid})[0]
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
            eid = edge['key']
            weight = edge['weight']
        except:
            eid = 1 + self.edges_data.find().count()
            self.graph_connection.add_edge(person_id1, person_id2, eid)
            self.edges_data.edges.insert_one({'eid': eid, 'features': []})
        weight += self.user_comment_weight
        self.graph_connection.update_weight(eid, weight)
        features = self.edges_data.edges.find({'eid': eid})[0]['features']
        features.append({'plus_w': self.user_comment_weight, 'minus_w': 0, 'user_comment': user_coment})
        self.edges_data.edges.update_one({'eid': eid}, {'$set': {'features': features}})



    """
    confirms connection between people
    """

    def confirm_connection(self, person_id1, person_id2, heuristic):
        try:
            edge = self.graph_connection.get_edge(person_id1, person_id2)['response']
            eid = edge['key']
            weight = edge['weight'] + self.confirmation_weight
            self.graph_connection.update_weight(eid, weight)
            self.edges_data.edges.update_one({'eid': eid},
                                {'$inc': {'features.' + str(heuristic) + '.plus_w': self.confirmation_weight}})
        except:
            print('WARNING: edge not found')


    def decline_connection(self, person_id1, person_id2, heuristic):
        try:
            edge = self.graph_connection.get_edge(person_id1, person_id2)['response']
            eid = edge['key']
            weight = edge['weight'] - self.confirmation_weight
            self.graph_connection.update_weight(eid, weight)
            self.edges_data.edges.update_one({'eid': eid},
                                {'$inc': {'features.' + str(heuristic) + '.minus_w': self.confirmation_weight}})
        except:
            print('WARNING: edge not found')

