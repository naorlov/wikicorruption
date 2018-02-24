import pymongo
import main_server.api_settings as settings
from main_server.engine import Engine
from main_server.graph_client import GraphClient
import tornado
import tornado.web
import tornado.ioloop
from main_server.engine import Engine

graph_server_credits = {
    "url": "http://35.204.32.159",
    "port": "80"
}
gc = GraphClient(graph_server_credits)
db = pymongo.MongoClient('mongodb://35.229.26.187:2700/declarator').declarator
en = Engine(db, db, gc)


def build_connection(server_adress: str, database: str):
    client = pymongo.MongoClient(server_adress)
    return client[database]


def extract_parameters(handler: tornado.web.RequestHandler):
    arg1 = handler.get_query_argument("arg1", default="")
    arg2 = handler.get_query_argument("arg2", default="")
    arg3 = handler.get_query_argument("arg3", default="")
    return arg1, arg2, arg3


def perform_action(request_type, arg1, arg2, arg3):
    print("got request", request_type, arg1, arg2, arg3)
    result = {'response': 'OK'}
    if request_type == "get_person_id":
        result['response'] = en.get_person_id(arg1, arg2, arg3)
    elif request_type == "get_user_summary":
        result['response'] = en.get_user_summary(int(arg1))
    elif request_type == "get_neighbourgs":
        result['response'] = en.get_neighbourgs(int(arg1))
    elif request_type == "get_connection":
        result['response'] = en.get_connection(int(arg1), int(arg2))
    elif request_type == "add_connection":
        en.add_connection(int(arg1), int(arg2), arg3)
    elif request_type == "confirm_connection":
        en.confirm_connection(int(arg1), int(arg2), int(arg3))
    elif request_type == "decline_connection":
        en.decline_connection(int(arg1), int(arg2), int(arg3))
    else:
        result['response'] = 'ERROR'
    return result


class ApiHandler(tornado.web.RequestHandler):
    def get(self):
        request_method = self.get_query_argument("method")
        result = perform_action(request_method, *extract_parameters(self))
        self.write(result)
        self.flush()


def start_tornado():
    tornado_app = tornado.web.Application(
        [
            (r"/", ApiHandler)
        ]
    )
    tornado_app.listen(settings.port, settings.ip)
    tornado.ioloop.IOLoop.instance().start()

def stop_tornado():
    tornado.ioloop.IOLoop.instance().stop()

if __name__ == '__main__':
    client = gc # GraphClient(settings.graph_server_credits)
    # declarator = build_connection(settings.server_url, settings.declarator_db_name)
    # other_shit = build_connection(settings.server_url, settings.declarator_db_name)

    # engine = Engine(declarator, other_shit, client)
    import threading

    threading.Thread(target=start_tornado).start()
    command = input()
    if command == "exit":
        stop_tornado()
