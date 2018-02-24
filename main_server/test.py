import main_server.settings as settings
import main_server.utils as utils

db = utils.build_connection(settings.server_url, settings.db_name)
print('Building users.')
users = utils.build_users(db['declarations'])
print('Users built.')
utils.build_graph(users, db['test_edges'])