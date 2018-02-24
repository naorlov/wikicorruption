import main_server.settings as settings
import main_server.utils as utils
import main_server.graph_client as gc


def test():
    db = utils.build_connection(settings.server_url, settings.db_name)
    print('Building users.')
    users = utils.build_users(db['declarations'])
    print('Users built.')
    utils.build_graph(users, db['test_edges'], db['declarations'])
