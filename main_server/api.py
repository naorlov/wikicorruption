import pymongo
import main_server.settings as settings
from main_server.engine import Engine
from main_server.graph_client import GraphClient


def build_connection(server_adress: str, database: str):
    client = pymongo.MongoClient(server_adress)
    return client[database]


if __name__ == '__main__':
    client = GraphClient(settings.graph_server_credits)
    declarator = build_connection(settings.server_url, settings.declarator_db_name)
    other_shit = build_connection(settings.server_url, settings.declarator_db_name)

    engine = Engine(declarator, other_shit, client)
    result = engine.get_person_id("Кузьминов", "Ярослав", "Иванович")
    print(*result)

