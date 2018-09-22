# import logging

from flask import request, jsonify

from codeitsuisse import app


@app.route('/broadcaster/message-broadcast', methods=['POST'])
def eval_broadcaster():
    data = request.get_json()
    app.logger.info("data sent for evaluation {}".format(data))
    input_data = data.get("data")
    result = leastnodes(input_data)
    app.logger.info("My result :{}".format(result))
    return jsonify(result)

def leastnodes(data):
    node = {}
    for rs in data:
        print(rs)
        if rs[0] in node:
            if "to" in node[rs[0]]:
                node[rs[0]]["to"].append(rs[3])
            else:
                print('to is not in rs[0]')
                node[rs[0]]["to"] = [rs[3]]
        else:
            node[rs[0]] = {}
            node[rs[0]]["to"] = [rs[3]]
        if rs[3] in node:
            if "from" in node[rs[3]]:
                node[rs[3]]["from"].append(rs[0])
            else:
                node[rs[3]]["from"] = [rs[0]]
        else:
            node[rs[3]] = {}
            node[rs[3]]["from"] = [rs[0]]

    print(node)

    visited = []
    for key in node:
        visited.append(key)

    print(visited)

    answer = []

    while visited:
        mother_node = find_mother(node, visited[0])
        print(mother_node)
        answer.append(mother_node)
        print(answer)
        remove_children(node,mother_node,visited)

    result_string = {
        "result": answer
    }

    return result_string


def find_mother(node, node_to_check):
    if "from" in node[node_to_check]:
        print("finding parent of",node_to_check)
        parent_node = node[node_to_check]["from"][0]
        return find_mother(node, parent_node)
    else:
        print("parent found! parent is:",node_to_check)
        return node_to_check

def remove_children(node, node_to_check, visited):
    if "to" in node[node_to_check]:
        for children_node in node[node_to_check]["to"]:
            print("visiting children:", children_node)
            remove_children(node, children_node, visited)
        print("popping",node_to_check)
        visited.pop(visited.index(node_to_check))
    else:
        print("popping",node_to_check)
        visited.pop(visited.index(node_to_check))
