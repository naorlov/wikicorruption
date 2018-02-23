import requests
import json


class GraphClient:
    def __init__(self, graph_server_creds):
        self.url = graph_server_creds["url"]
        self.port = graph_server_creds["port"]

    def status(self):
        return self.make_request("status")

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
