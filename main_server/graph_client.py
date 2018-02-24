import requests
import json


class BufferedRequestQueue:
    queue = []

    def __init__(self, url, port):
        self.url = url
        self.port = port

    def add_request(self, request):
        self.queue.append(request)
        if len(self.queue) == 100:
            self.send()
        self.queue = []

    def send(self):
        payload = {"data": (self.queue,)}
        self.queue = []
        r = requests.post(
            self.url + ":" + self.port,
            data=payload
        )
        return r.json()


class GraphClient:
    def __init__(self, graph_server_creds):
        self.url = graph_server_creds["url"]
        self.port = graph_server_creds["port"]
        self.queue = BufferedRequestQueue(self.url, self.port)

    def status(self):
        self.queue.add_request(self.make_request("status"))

    def add_vertex(self, v1):
        self.queue.add_request(self.make_request("add_vertex", v1))

    def add_edge(self, v1, v2, key):
        self.queue.add_request(self.make_request("add_edge", v1, v2, key=key))

    def has_vertex(self, v1):
        return self.make_immideate_request("has_vertex", v1)

    def has_edge(self, key):
        return self.make_immideate_request("has_edge", key=key)

    def remove_vertex(self, v1):
        self.queue.add_request(self.make_request("remove_vertex", v1))

    def remove_edge(self, key):
        self.queue.add_request(self.make_request("remove_edge", key=key))

    def update_weight(self, key, new_weight):
        self.queue.add_request(self.make_request("update_weight", key=key, weight=new_weight))

    def get_weight(self, key):
        return self.make_immideate_request("get_weight", key=key)

    def commit(self):
        self.queue.send()

    def make_request(self, request_type, v1=0, v2=0, key=0, weight=0):
        payload = {"type": request_type,
                   "vertex1": v1,
                   "vertex2": v2,
                   "key": key,
                   "weight": weight}
        return payload
        # r = requests.get(
        #    self.url + ":" + self.port,
        #    params=payload
        # )
        # return r.json()

    def make_immideate_request(self, request_type, v1=0, v2=0, key=0, weight=0):
        self.queue.send()
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