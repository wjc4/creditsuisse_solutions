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

# def bubblecount_up(node, node_to_check):
#     if "from" not in node[node_to_check]:
#         node[node_to_check]["ccount"] += 1
#     else:
#         for parent in node[node_to_check]["from"]:
#             bubblecount_up(node,parent)
#
# def bubblecount_down(node, node_to_check):
#     if "to" not in node[node_to_check]:
#         node[node_to_check]["ccount"] += 1
#     else:
#         for child in node[node_to_check]["to"]:
#             bubblecount_up(node,child)

def most_connections(data):
    node = {}
    for relationships in data:
        rs = relationships.split("->")
        if rs[0] in node:
            # if "to" array already exists
            if "to" in node[rs[0]]:
                node[rs[0]]["to"].append(rs[1])
                # node[rs[0]]["ccount"] += 1
            # if rs[0] alr created but only "from" is filled
            else:
                node[rs[0]]["to"] = [rs[1]]
                # node[rs[0]]["ccount"] = 1
            # bubblecount_up(node, rs[0])
            # bubblecount_down(node, rs[0])
        # if rs[0] is still not in dict
        else:
            node[rs[0]] = {}
            node[rs[0]]["to"] = [rs[1]]
            # node[rs[0]]["ccount"] = 1
        if rs[1] in node:
            if "from" in node[rs[1]]:
                node[rs[1]]["from"].append(rs[0])
            else:
                node[rs[1]]["from"] = [rs[0]]
            # bubblecount_down(node,rs[1])
            # bubblecount_up(node,rs[1])
        else:
            node[rs[1]] = {}
            node[rs[1]]["from"] = [rs[0]]

    print(node)
    # search for roots
    roots = []
    for key in node:
        if "from" not in node[key]:
            roots.append(key)

    answers = []

    for root in roots:
        reset()
        count_children(node,root)
        count = returncount()
        answers.append((root,count))

    sorted_answers = sorted(answers, key=lambda x: x[1], reverse=True)
    final_answers = []

    for i in range(len(sorted_answers)):
        if sorted_answers[i][1]==sorted_answers[0][1]:
            final_answers.append(sorted_answers[i])
     # sort by alphabetical order
    if len(final_answers)==1:
        return final_answers[0][0]
    else:
        sorted_fanswers = sorted(final_answers, key=lambda x: x[0])
        return sorted_fanswers[0][0]

 def count_children(node,node_to_check):
    if "to" in node[node_to_check]:
        for child in node[node_to_check]["to"]:
            plusone()
            count_children(node,child)
    else:
        pass

 def plusone():
    global count
    count += 1
 def reset():
    global count
    count = 0

def returncount():
    global count
    return count
