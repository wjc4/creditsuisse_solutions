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

logger = logging.getLogger(__name__)

@app.route('/skill-tree', methods=['POST'])
def ST_evaluate():

    # JSON mode
    data = request.get_json();
    app.logger.info("data sent for evaluation {}".format(data))
    boss = data["boss"]
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

    for skill in skills:
        print('Registering a skill...{}'.format(skill["name"]))
        skill = Tree(
                [],
                skill["name"],
                skill["offense"],
                skill["points"],
                skill["require"]
                )
        #do treeSearch
        if(skill.require==None):
            root.children.append(skill)

        else:
            #add skill to branch require
            print("Pre-req skill needed.")
            addSkill(root,skill)

    # root.data = "root"
    # root.left = Tree()
    # root.left.data = "left"
    # root.right = Tree()
    # root.right.data = "right"

    print(len(root.children))

    #build skill Tree

    print('\n\n\n\n\n\n')

    printTree(root)

    result = "done"
    # app.logger.info("My result :{}".format(result))

    return jsonify(result);
