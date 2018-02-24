from main_server.graph_client import GraphClient
import pymongo
import pymongo.database


class Engine:
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
        result["max_income"] = max([(item["incomes"]["size"], item["main"]["year"] for item in documents)])[::-1]
        result["max_income"] = min([(item["incomes"]["size"], item["main"]["year"] for item in documents)])[::-1]
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
        result = {}
        connected_persons = self.graph_connection.get_adjacent(person_id)
        for person in connected_persons:
            eid = self.graph_connection.get_edge(person_id, person)
            '''ANDERY, WRITE THIS PLZ'''
            result[eid] = [self.edges_data.edges.find({""})]
        return result

    """
    gets two person_ids and returns heuristcs or None, if no connection found
    """

    def get_connection(self, person_id1, person_id2):
        result = []
        eid = self.graph_connection.get_edge(person_id1, person_id2)
        '''WRITE THIS TOO'''
        #your code
        return result


    """
    adds heuristic connection between people
    """

    def add_connection(self, person_id1, person_id2, heuristic):
        '''NEED TO WRITE THIS TOO'''
        self.graph_connection.add_edge(person_id1, person_id2, None)


    """
    confirms connection between people
    """

    def confirm_connection(self, person_id1, person_id2, heuristic):
        ''' AND THIS'''
