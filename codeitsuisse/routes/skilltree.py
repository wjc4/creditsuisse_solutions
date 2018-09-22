class Tree(object):
    def __init__(self,a=[],b=None,c=None,d=None,e=None):
        self.children = a
        self.name = b
        self.offense = c
        self.points = d
        self.require = e
    def add_child(self,child):
        self.children.append(child)

def treeSearch(base,name):
    if(len(base.children)==0):
        if(base.name == name):
            return True
    else:
        for child in base.children:
            treeSearch(child,name)

def addSkill(base,skill):
    print(base.name,skill.require,len(base.children))
    if(base.name == skill.require):
        base.children.append(skill)
        print("children",base.children)

    if(len(base.children)==0): {}
    else:
        for child in base.children:
            addSkill(child,skill)

def printTree(base):
    if(len(base.children)==0):
            print(base.name)
    else:
        for child in base.children:
            print(base.name,"->")
            printTree(child)

import logging

from flask import request, jsonify

from codeitsuisse import app

import operator

logger = logging.getLogger(__name__)

@app.route('/skill-tree', methods=['POST'])
def ST_evaluate():

    # JSON mode
    data = request.get_json()
    app.logger.info("data sent for evaluation {}".format(data))
    hp = data["boss"]["offense"]
    skills = data["skills"]

    # Args Key Mode
    # data = request.args
    # inputValue = int(data.get('input'))

    root = Tree(
            [],
            "root",
            0,
            0,
            None
            )

    skill_list={}
    for skill in skills:
        print('Registering a skill...{}'.format(skill["name"]))
        # print(skill)
        temp = Tree(
                [],
                skill["name"],
                skill["offense"],
                skill["points"],
                skill["require"]
                )
        #do treeSearch
        if(skill["require"]==None):
            root.children.append(temp)
        skill_list[skill["name"]]=temp
    # print(skill_list)
    for skill in skill_list:
        if skill_list[skill].require:
            skill_list[skill_list[skill].require].children.append(skill_list[skill])
    
    print(skill_list)
    


        # else:
        #     #add skill to branch require
        #     print("Pre-req skill needed.")
        #     addSkill(root,skill)

    # root.data = "root"
    # root.left = Tree()
    # root.left.data = "left"
    # root.right = Tree()
    # root.right.data = "right"

    print([node.name for node in root.children])

    available = []
    for node in root.children:
        available.append(node)

    # available.sort(key=operator.attrgetter('points'))

    # print([node.name for node in available])
    possible = {}
    findMinPath(available,skill_list,0,hp,[],possible)
    print(possible)
    res = min(possible.items(), key=operator.itemgetter(1))[0].split(',')
    res.pop(0)
    # app.logger.info("My result :{}".format(result))
    return jsonify(res)


import itertools

def findMinPath(available,skill_list,dmg,hp,path,res):

    combs = []

    for i in range(1, len(available)+1):
        els = [list(x) for x in itertools.combinations(available, i)]
        combs.extend(els)
    for array in combs:
        # calculate damage
        new_dmg = dmg
        # if dmg>=hp, stop and return path and points/costs

        # else carry on searching
        available = []
        new_path=path.copy()
        for obj in array:
            new_dmg = new_dmg + obj.offense
            new_path.append(obj)
            if obj.children:
                for child in obj.children:
                    available.append(child)
        # print(new_path, new_dmg)
        if new_dmg >= hp:
            key = "root"
            cost = 0
            for node in new_path:
                key = key + "," + node.name
                cost = cost + node.points
            res[key]= cost
        elif available:
            findMinPath(available,skill_list,new_dmg,hp,new_path,res)

# def findMaxPath(mat):
 
#     # To find max val in first row
#     res = -1
#     for i in range(M):
#         res = max(res, mat[0][i])
  
#     for i in range(1, N):
  
#         res = -1
#         for j in range(M):
  
#             # When all paths are possible
#             if (j > 0 and j < M - 1):
#                 mat[i][j] += max(mat[i - 1][j],
#                                  max(mat[i - 1][j - 1], 
#                                      mat[i - 1][j + 1]))
  
#             # When diagonal right is not possible
#             elif (j > 0):
#                 mat[i][j] += max(mat[i - 1][j],
#                                  mat[i - 1][j - 1])
  
#             # When diagonal left is not possible
#             elif (j < M - 1):
#                 mat[i][j] += max(mat[i - 1][j],
#                                  mat[i - 1][j + 1])
  
#             # Store max path sum
#             res = max(mat[i][j], res)
#     return res