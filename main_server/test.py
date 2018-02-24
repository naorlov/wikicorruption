from main_server.graph_client import GraphClient
from main_server.engine import Engine
import main_server.settings as settings
import main_server.utils as utils
import main_server.graph_client as gc
import pymongo


def test():
    db = utils.build_connection(settings.server_url, settings.db_name)
    print('Building users.')
    users = utils.build_users(db['declarations'])
    print('Users built.')
    utils.build_graph(users, db['test_edges'], db['declarations'])


if __name__ == '__main__':
    test()

    graph_server_credits = {
        "url": "http://35.204.32.159",
        "port": "80"
    }
    gc = GraphClient(graph_server_credits)
    db = pymongo.MongoClient('mongodb://35.229.26.187:2700/declarator').declarator
    en = Engine(db, db, gc)
    print(en.get_person_id('Зюганов', 'Геннадий', 'Андреевич'))
    print(en.get_user_summary(8))
    print(en.get_neighbourgs(8))
    print(en.get_connection(8, 182))
    print(en.get_connection(281, 8))
    print(en.get_connection(282, 8))
    en.add_connection(8, 182, "JUST TEST")
    en.add_connection(8, 183, "ANOTHER TEST")
    en.add_connection(0, 0, "TEST")
    en.confirm_connection(8, 182, 0)
    en.decline_connection(8, 182, 1)
