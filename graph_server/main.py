import tornado
import tornado.web
import tornado.ioloop
import settings
import json
from graph import ServerGraph

graph = ServerGraph(settings.pickle_path)


def extract_parameters(handler: tornado.web.RequestHandler):
    vertex1 = handler.get_query_argument("vertex1", default=None)
    vertex2 = handler.get_query_argument("vertex2", default=None)
    key = handler.get_query_argument("key", default=None)
    weight = handler.get_query_argument("weight", default=None)
    return vertex1, vertex2, key, weight


def perform_action(request_type, v1, v2, key, weight):
    print("got request: type {} v1 {} v2 {} key {} weight {}".format(
        request_type, v1, v2, key, weight
    ))
    result = {"response": "OK"}
    if request_type == "status":
        pass
    elif request_type == "add_vertex":
        graph.add_vertex(v1)
    elif request_type == "add_edge":
        graph.add_edge(v1, v2, key, 0)
    elif request_type == "has_vertex":
        result["response"] = graph.has_vertex(v1)
    elif request_type == "has_edge":
        result["response"] = graph.has_edge(key)
    elif request_type == "remove_vertex":
        graph.remove_vertex(v1)
    elif request_type == "remove_edge":
        graph.remove_edge(key)
    elif request_type == "update_weight":
        graph.update_weight(key, weight)
    elif request_type == "get_weight":
        result["response"] = graph.get_weight(key)
    elif request_type == "get_adjacent":
        result["response"] = graph.get_adjacent(v1)
    return result


class GraphHandler(tornado.web.RequestHandler):
    def get(self):
        request_type = self.get_query_argument("type")
        result = {"response": "OK"}
        if graph.count == settings.treshhold:
            graph.save()
            graph.count = 0

        result = perform_action(request_type, *extract_parameters(self))
        self.write(result)
        self.flush()
        graph.count += 1

    def post(self):
        data = map(
            lambda x: json.loads(x),
            map(
                lambda x: x.replace('\'', '\"'),
                self.get_body_arguments("data")
            )
        )
        for item in list(data):
            perform_action(request_type=item["type"],
                           v1=item["vertex1"],
                           v2=item["vertex2"],
                           key=item["key"],
                           weight=item["weight"])

        result = {"response": "OK"}
        self.write(result)
        self.flush()


def startTornado():
    tornado_app = tornado.web.Application(
        [
            (r"/", GraphHandler)
        ]
    )
    tornado_app.listen(settings.port, settings.ip)
    tornado.ioloop.IOLoop.instance().start()


def stopTornado():
    graph.save()
    tornado.ioloop.IOLoop.instance().stop()


if __name__ == '__main__':
    import threading

    threading.Thread(target=startTornado).start()
    command = input()
    if command == "exit":
        stopTornado()
