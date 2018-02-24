import main_server.settings as settings
import main_server.utils as utils
import main_server.graph_client as gc

if __name__ == '__main__':
    client = gc.GraphClient(settings.graph_server_credits)
    client.add_edge(1, 2, 3)
    print(client.get_edge(1, 2))
