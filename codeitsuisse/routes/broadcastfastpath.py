# import logging

from flask import request, jsonify

from codeitsuisse import app

all_paths = []

@app.route('/broadcaster/fastest-path', methods=['POST'])
def eval_broadcast_fastpath():
    data = request.get_json()
    # app.logger.info("data sent for evaluation {}".format(data))
    input_data = data.get("data")
    sender = data.get("sender")
    recipient = data.get("recipient")
    result = fastpath(input_data,sender,recipient)
    app.logger.info("My result :{}".format(result))
    return jsonify(result)

def fastpath(data,start,dst):
    global all_paths

    node = {}
    for relationships in data:
        rs = relationships.replace("->"," ").replace(","," ").split()
        # print(rs)
        if rs[0] in node:
            node[rs[0]]["to"].append((rs[1],rs[2]))
        else:
            node[rs[0]] = {}
            node[rs[0]]["to"] = [(rs[1],rs[2])]

    # print(node)
    res_paths = printAllPaths(node,start,dst)
    print(res_paths)

def printAllPathsUtil(node_to_visit, dst, visited, path, node, res_paths):
    # Mark the current node as visited and store in path
    visited[node_to_visit]= True
    path.append(node_to_visit)

    # If current vertex is same as destination, then print
    # current path[]
    if node_to_visit == dst:
        print("correct path is",path)
        res_paths.append(path)
        print(all_paths)
        # print(all_paths)
    elif node_to_visit not in node:
        print(path)
    else:
        # If current vertex is not destination
        #Recur for all the vertices adjacent to this vertex
        for child in node[node_to_visit]["to"]:
            if visited[child[0]]==False:
                printAllPathsUtil(child[0], dst, visited, path, node, res_paths)

    # Remove current vertex from path[] and mark it as unvisited
    path.pop()
    visited[node_to_visit]= False

    return res_paths


# Prints all paths from 's' to 'd'
def printAllPaths(node, start, dst):
    visited = set()
    for key in node:
        visited.add(key)
        if "to" in node[key]:
            for child in node[key]["to"]:
                visited.add(child[0])

    visited_dict = {}
    for val in visited:
        visited_dict[val] = False


    # Create an array to store paths
    path = []
    res_paths = []
    # Call the recursive helper function to print all paths
    return printAllPathsUtil(start, dst,visited_dict, path, node, res_paths)




    # answer = []
    #
    # while visited:
    #     mother_node = find_mother(node, visited[0])
    #     answer.append(mother_node)
    #     # print(answer)
    #     remove_children(node,mother_node,visited)

    # result_string = {
    #     "result":
    # }

    return

def appendpath(path):
    global all_paths
    all_paths.append(path)

def resetpath():
    global all_paths
    all_paths = []

# def find_mother(node, node_to_check):
#     if "from" in node[node_to_check]:
#         # print("finding parent of",node_to_check)
#         parent_node = node[node_to_check]["from"][0]
#         return find_mother(node, parent_node)
#     else:
#         # print("parent found! parent is:",node_to_check)
#         return node_to_check
#
# def remove_children(node, node_to_check, visited):
#     if "to" in node[node_to_check]:
#         for children_node in node[node_to_check]["to"]:
#             # print("visiting children:", children_node)
#             if children_node not in visited:
#                 pass
#             else:
#                 remove_children(node, children_node, visited)
#         # print("popping",node_to_check)
#         visited.pop(visited.index(node_to_check))
#     else:
#         # print("this is the node to check",node_to_check)
#         # print("this is visited: ",visited)
#         if node_to_check in visited:
#             # print("popping",node_to_check)
#             visited.pop(visited.index(node_to_check))
#         else:
#             # print(node_to_check,"not in loop")
#             pass
