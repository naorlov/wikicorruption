import requests
import json


class GraphClient:
    def __init__(self, graph_server_creds):
        self.url = graph_server_creds["url"]
        self.port = graph_server_creds["port"]

    def status(self):
        return self.make_request("status")

    def add_vertex(self, v1):
        return self.make_request("add_vertex", v1)

    def add_edge(self, v1, v2, key):
        return self.make_request("add_edge", v1, v2, key=key)

    def has_vertex(self, v1):
        return self.make_request("has_vertex", v1)

    def has_edge(self, key):
        return self.make_request("has_edge", key=key)

    def remove_vertex(self, v1):
        return self.make_request("remove_vertex", v1)

    def remove_edge(self, key):
        return self.make_request("remove_edge", key=key)

    def update_weight(self, key, new_weight):
        return self.make_request("update_weight", key=key, weight=new_weight)

    def get_weight(self, key):
        return self.make_request("get_weight", key=key)

    def make_request(self, request_type, v1=0, v2=0, key=0, weight=0):
        payload = {"type": request_type,
                   "vertex1": v1,
                   "vertex2": v2,
                   "key": key,
                   "weight": weight}
        r = requests.get(
            self.url + ":" + self.port,
            params=payload
        )
        return r.json()
