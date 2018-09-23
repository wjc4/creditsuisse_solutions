# import logging

from flask import request, jsonify

from codeitsuisse import app

import copy
import operator

# logger = logging.getLogger(__name__)

# # {
#     "tetrominoSequence": "IOJLLLTIOOTIOTZSTTTLLIJSZTIT"
# }

@app.route('/tetris', methods=['POST'])
def tetris_evaluate2():
    data = request.get_json()
    app.logger.info("data sent for evaluation {}".format(data))
    seq = data["tetrominoSequence"]
    actions = []

    n = len(seq)

    # seq[i]

    # setup code
    table = []
    for i in range(10):
        table.append([])
    # table = []
    # for i in range(20):
    #   table.append(row)
    print(table)
    # print([len(col) for col in table])
    res = []
    for i in range(n):
        piece = seq[i]
        score = calc(table,piece)
        print(score)
        move = max(score, key=operator.itemgetter('points'))
        res.append(move['action'])
        table = move['table']
        
        harray = [len(col) for col in table]
        # print(harray)
        # height = sum(harray)
        # lines = 0
        to_pop=[]
        for i in range(max(harray)):
            full = True
            for j in range(10):
                # print(i,j)
                # print(len(table[j]))
                if len(table[j]) <= i or len(table[j]) == 0 or table[j][i] == 0:
                    full = False 
                    break
            if full:
                to_pop.append(i)
        while to_pop:
            index = to_pop.pop()
            for i in range(10):
                if table[i][index] == 0:
                    raise Exception('wtf u doing')
                table[i].pop(index)


    app.logger.info("My result :{}".format(res))
    return jsonify({'actions':res})


def calc(table,piece):
    score = []
    if piece == 'O':
        for i in range(9):
            newtable=copy.deepcopy(table)
            top = max(len(newtable[i]),len(newtable[i+1]))
            while(len(newtable[i])<top):
                newtable[i].append(0)
            while(len(newtable[i+1])<top):
                newtable[i+1].append(0)
            newtable[i].append(1)
            newtable[i].append(1)
            newtable[i+1].append(1)
            newtable[i+1].append(1)
            score.append({
                'points':calc_score(newtable),
                'action':i,
                'table': newtable
            })
    if piece == 'I':
        for i in range(10):
            newtable=copy.deepcopy(table)
            newtable[i].append(1)
            newtable[i].append(1)
            newtable[i].append(1)
            newtable[i].append(1)
            score.append({
                'points':calc_score(newtable),
                'action':i,
                'table': newtable
            })
        for i in range(7):
            newtable=copy.deepcopy(table)
            to_cmp = [len(newtable[i]),len(newtable[i+1]),len(newtable[i+2]),len(newtable[i+3])]
            top = max(to_cmp)
            for j in range(4):
                while(len(newtable[i+j])<top):
                    newtable[i+j].append(0)
                newtable[i+j].append(1)
            score.append({
                'points':calc_score(newtable),
                'action':i,
                'table': newtable
            })


    return score

def calc_score(table):
    a = -0.510066 
    b = 0.760666
    c = -0.35663
    d = -0.184483
    harray = [len(col) for col in table]
    # print(harray)
    height = sum(harray)
    lines = 0
    for i in range(max(harray)):
        full = True
        for j in range(10):
            # print(i,j)
            # print(len(table[j]))
            if len(table[j]) <= i or len(table[j]) == 0 or table[j][i] == 0:
                full = False 
                break
        if full:
            lines += 1
    holes = 0
    for i in range(10):
        if 0 in table[i]:
            holes += 1
    bump = 0
    for i in range(9):
        bump += abs(harray[i]-harray[i+1])
    output = a*height+b*lines+c*holes+d*bump
    return output 