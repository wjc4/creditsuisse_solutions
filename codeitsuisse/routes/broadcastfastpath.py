# import logging

from flask import request, jsonify
from collections import defaultdict

from codeitsuisse import app

class Graph():
    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        self.edges[from_node].append(to_node)
        self.weights[(from_node, to_node)] = weight

@app.route('/broadcaster/fastest-path', methods=['POST'])
def eval_broadcast_fastpath():
    data = request.get_json()
    # app.logger.info("data sent for evaluation {}".format(data))
    input_data = data.get("data")
    sender = data.get("sender")
    recipient = data.get("recipient")
    result_input = fastpath(input_data,sender,recipient)
    result = {
        "result": result_input
    }
    app.logger.info("My result :{}".format(result))
    return jsonify(result)

def fastpath(data,start,dst):
    graph = Graph()
    for relationships in data:
        rs = relationships.replace("->"," ").replace(","," ").split()
        graph.add_edge(rs[0], rs[1], int(rs[2]))

    path = dijsktra(graph,start,dst)
    return path

def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path
