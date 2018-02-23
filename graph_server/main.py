import tornado
import tornado.web
import tornado.ioloop
import graph_server.settings as settings
from graph_server.graph import ServerGraph

graph = ServerGraph(settings.pickle_path)


def extract_parameters(handler: tornado.web.RequestHandler):
    vertex1 = handler.get_query_argument("vertex1", default=None)
    vertex2 = handler.get_query_argument("vertex2", default=None)
    key = handler.get_query_argument("key", default=None)
    weight = handler.get_query_argument("weight", default=None)
    return vertex1, vertex2, key, weight


class GraphHandler(tornado.web.RequestHandler):
    def get(self):
        request_type = self.get_query_argument("type")
        v1, v2, key, weight = extract_parameters(self)
        print("got request: type {} v1 {} v2 {} key {} weight {}".format(
            request_type, v1, v2, key, weight
        ))
        result = {"response": "OK"}

        if request_type == "status":
            pass
        elif request_type == "add_vertex":
            graph.add_vertex(v1)
        elif request_type == "add_edge":
            graph.add_edge(v1, v2, key)
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
        self.write(result)
        self.flush()


if __name__ == '__main__':
    tornado_app = tornado.web.Application(
        [
            (r"/", GraphHandler)
        ]
    )
    tornado_app.listen(settings.port)
    tornado.ioloop.IOLoop.current().start()
