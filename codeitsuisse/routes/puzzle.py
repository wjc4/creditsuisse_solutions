# import logging

from flask import request, jsonify

from codeitsuisse import app
from .puzzle15 import *

# logger = logging.getLogger(__name__)
"""
{
  "puzzle":[
            [1,2,3],
            [4,8,5],
            [7,6,0] 
          ]
    }
"""


@app.route('/sorting-game', methods=['POST'])
def solvegame():
    data = request.get_json()
    app.logger.info("data sent for evaluation {}".format(data))
    inputValue = data.get("puzzle")
    # tracepuzzle = []
    # for array in inputValue:
    #     for i in range(len(array)):
    #         tracepuzzle.append(array[len(array)-i-1])
    puzzle = []
    for array in inputValue:
        for i in range(len(array)):
            puzzle.append(array[i])
    # print(tracepuzzle)
    puzzle[puzzle.index(0)]=9
    print(puzzle)
    # puzzle = [1,4,7,2,8,6,3,5,9]
    # puzzle = [7, 5, 9, 8, 1, 2, 3, 6, 4]
    # solve the puzzle only if it is solvable
    if is_solvable(puzzle):
        print('solvable')
        steps = solve(puzzle)
    print(steps)
    result = []
    for i in range(len(steps)):
        start = steps[i][0]
        end = steps[i][1]
        result.append(puzzle[start])
        temp = puzzle[start]
        puzzle[start]=puzzle[end]
        puzzle[end]=temp

    app.logger.info("My result :{}".format(result))
    return jsonify({"result":result})

