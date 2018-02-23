import networkx
import pickle


class ServerGraph:
    graph = networkx.Graph()
    edges = dict()

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
        self.graph.add_node(v1)

    def add_edge(self, v1, v2, key, weight):
        self.graph.add_edge(v1, v2, key=key, weight=weight)
        self.edges[key] = (v1, v2)

    def has_vertex(self, v1):
        return self.graph.has_node(v1)

    def has_edge(self, id):
        return id in self.edges

    def remove_vertex(self, v1):
        keys = [self.graph[v1][v2]["key"] for v2 in self.graph[v1]]
        self.graph.remove_node(v1)
        for key in keys:
            self.edges.pop(key)

    def remove_edge(self, key):
        v1, v2 = self.edges[key]
        self.graph.remove_edge(v1, v2)
        self.edges.pop(key)

    def update_weight(self, key, new_weight):
        v1, v2 = self.edges[key]
        self.graph[v1][v2]["weight"] = new_weight

    def get_weight(self, key):
        v1, v2 = self.edges[key]
        return self.graph[v1][v2]["weight"]
