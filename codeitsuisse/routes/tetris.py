import logging

from flask import request, jsonify

from codeitsuisse import app
from codeitsuisse.routes.tetris_field import *

logger = logging.getLogger(__name__)

@app.route('/tetris', methods=['POST'])
def tetris_evaluate():

    # JSON mode
    data = request.get_json();
    app.logger.info("data sent for evaluation {}".format(data))
    seq = data["tetrominoSequence"]
    actions = []

    n = len(seq)

    # if('I' not in seq and 'J' not in seq):
    #     # # challenge 1
    #     for i in range(n):
    #         shift = (i%5)* 2
    #         actions.append(shift)
    #
    # elif('I' not in seq and 'O' not in seq):
    #     # challenge 2
    #     J_count = 0
    #     L_count = 0
    #     for i in range(n):
    #         rotate = 0
    #         shift = 0
    #         if(seq[i]=="L"):
    #             if(int(L_count/3)%2==0):
    #                 shift = L_count%3 * 2
    #             else:
    #                 rotate = 2
    #                 shift = L_count%3 * 2
    #             L_count += 1
    #         else:
    #             offset = 6
    #             if(int(J_count/2)%2==0):
    #                 shift = (J_count%2 * 2) + offset
    #             else:
    #                 rotate = 2
    #                 shift = (J_count%2 * 2) + offset
    #             J_count+=1
    #
    #         if(rotate!=0):
    #             actions.append(int(str(rotate)+str(shift)))
    #         else:
    #             actions.append(shift)
    #
    # elif('J' not in seq and 'L' not in seq):
    #     #challenge 3
    #     O_count = 0
    #     I_count = 0
    #     for i in range(n):
    #         rotate = 0
    #         shift = 0
    #         if(seq[i]=="O"):
    #             shift = O_count%3 * 2
    #             O_count += 1
    #         else:
    #             offset = 6
    #             if(int(I_count/4)%2 ==0):
    #                 shift = (I_count%4 * 1) + offset
    #             else:
    #                 shift = (I_count%4 * 1) + offset
    #             I_count+=1
    #
    #         if(rotate!=0):
    #             actions.append(int(str(rotate)+str(shift)))
    #         else:
    #             actions.append(shift)

    ####################################

    # Initialise matrix
    # Floor is made of blocks as well
    w, h = 10, 21;
    M = [[0 for x in range(w)] for y in range(h)]
    M[-1][:] = [1]*w  #populate floor

    M = clearLines(M)
    # addPiece(M,'O',0,0)
    # addPiece(M,'O',0,1)
    # addPiece(M,'T',0,3)
    # addPiece(M,'L',0,3)

    for i in range(n):

        M = clearLines(M)
        printMatrix(M)

        # Get best action
        (pos,rot) = rankRot(M,seq[i])
        # convert into json output
        shift = pos #movements start from leftmost 0th blk
        if(rot!=0):
            actions.append(int(str(rot)+str(shift)))
        else:
            actions.append(shift)

        print('Updating...')
        print("Piece: ",seq[i])
        M = addPiece(M,seq[i],rot,pos)

        input("\nPress Enter to continue...")


    ####################################
    print("Final actions are as follows: ",actions)
    result = {"actions":actions}

    app.logger.info("My result :{}".format(result))

    return jsonify(result);
