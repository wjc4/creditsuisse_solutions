# import logging

from flask import request, jsonify
from collections import defaultdict

from codeitsuisse import app


@app.route('/broadcaster/most-connected-node', methods=['POST'])
def eval_broadcast_connected():
    data = request.get_json()
    app.logger.info("CONNECTED NODES TEST CASE {}".format(data))
    input_data = data.get("data")
    result_input = most_connections(input_data)
    result = {
        "result": result_input
    }
    app.logger.info("-----------\n\nMy result ISSSS:{}".format(result))
    return jsonify(result)

def bubblecount_up(node, node_to_check):
    if "from" not in node[node_to_check]:
        node[node_to_check]["ccount"] += 1
    else:
        for parent in node[node_to_check]["from"]:
            bubblecount_up(node,parent)

def most_connections(data):
    node = {}
    for relationships in data:
        rs = relationships.split("->")
        if rs[0] in node:
            # if "to" array already exists
            if "to" in node[rs[0]]:
                node[rs[0]]["to"].append(rs[1])
                node[rs[0]]["ccount"] += 1
            # if rs[0] alr created but only "from" is filled
            else:
                node[rs[0]]["to"] = [rs[1]]
                node[rs[0]]["ccount"] = 1
            bubblecount_up(node, rs[0])
        # if rs[0] is still not in dict
        else:
            node[rs[0]] = {}
            node[rs[0]]["to"] = [rs[1]]
            node[rs[0]]["ccount"] = 1
        if rs[1] in node:
            if "from" in node[rs[1]]:
                node[rs[1]]["from"].append(rs[0])
            else:
                node[rs[1]]["from"] = [rs[0]]
        else:
            node[rs[1]] = {}
            node[rs[1]]["from"] = [rs[0]]

    # search for roots
    roots = []
    maxcount = 0
    maxkey = ""
    for key in node:
        if "from" not in node[key]:
            num_child = node[key]["ccount"]
            if num_child>maxcount:
                maxcount = num_child
                maxkey = key

    return maxkey
