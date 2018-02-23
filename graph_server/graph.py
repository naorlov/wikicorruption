import networkx
import pickle


class ServerGraph:
    graph = networkx.Graph
    def __init__(self, path):
        self.path = path
        try:
            self.graph = pickle.load(open(path, "rb"))
        except:
            print("no pickle file found, creating one")
            with open(path, "wb") as file:
                pickle.dump(self.graph, file)
        self.file = open(path, "wb")

    def save(self):
        pickle.dump(self.graph, self.path)

    def add_vertex(self, v1):
        pass

    def add_edge(self, v1, v2, key):
        pass

    def has_vertex(self, v1):
        pass

    def has_edge(self, v1, v2):
        pass

    def remove_vertex(self, v1):
        pass

    def remove_edge(self, v1, v2):
        pass

    def update_weight(self, v1, v2, new_weight):
        pass

    def get_weight(self, v1, v2):
        pass

