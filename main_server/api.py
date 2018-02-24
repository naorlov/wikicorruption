import pymongo
import main_server.api_settings as settings
from main_server.engine import Engine
from main_server.graph_client import GraphClient
import tornado
import tornado.web


def build_connection(server_adress: str, database: str):
    client = pymongo.MongoClient(server_adress)
    return client[database]


def extract_parameters(handler: tornado.web.RequestHandler):
    person_id = handler.get_query_argument("person_id", default="0")
    family_name = handler.get_query_argument("family_name", default="")
    given_name = handler.get_query_argument("given_name", default="")
    patronymic_name = handler.get_query_argument("patronymic_name", default="")
    other_person_id = handler.get_query_argument("other_person_id", default="")
    heuristic = handler.get_query_argument("heuristic", default="")
    return person_id, family_name, given_name, patronymic_name, other_person_id, heuristic


def perform_action(request_type, v1, v2, key, weight):
    print("got request", self)

class ApiHandler(tornado.web.RequestHandler):
    def get(self):
        request_method = self.get_query_argument("method")
        result = perform_action(request_method, *extract_parameters(self))


def start_tornado():
    tornado_app = tornado.web.Application(
        [
            (r"/", ApiHandler)
        ]
    )
    tornado_app.listen(settings.port, settings.ip)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    client = GraphClient(settings.graph_server_credits)
    declarator = build_connection(settings.server_url, settings.declarator_db_name)
    other_shit = build_connection(settings.server_url, settings.declarator_db_name)

    engine = Engine(declarator, other_shit, client)
    import threading

    threading.Thread(target=startTornado).start()
    command = input()
    if command == "exit":
        stopTornado()
