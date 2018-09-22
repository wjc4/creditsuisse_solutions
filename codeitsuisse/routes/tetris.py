import logging

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tetris', methods=['POST'])
def tetris_evaluate():

    # JSON mode
    data = request.get_json();
    app.logger.info("data sent for evaluation {}".format(data))
    seq = data["tetrominoSequence"]
    actions = []

    n = len(seq)

    # # challenge 1
    # for i in range(n):
    #     shift = (i%5)* 2
    #     actions.append(shift)

    # challenge 2
    # J_count = 0
    # L_count = 0
    # for i in range(n):
    #     rotate = 0
    #     shift = 0
    #     if(seq[i]=="L"):
    #         if(int(L_count/3)%2==0):
    #             shift = L_count%3 * 2
    #         else:
    #             rotate = 2
    #             shift = L_count%3 * 2
    #         L_count += 1
    #     else:
    #         offset = 6
    #         if(int(J_count/2)%2==0):
    #             shift = (J_count%2 * 2) + offset
    #         else:
    #             rotate = 2
    #             shift = (J_count%2 * 2) + offset
    #         J_count+=1
    #
    #     if(rotate!=0):
    #         actions.append(int(str(rotate)+str(shift)))
    #     else:
    #         actions.append(shift)

    #challenge 3
    O_count = 0
    I_count = 0
    for i in range(n):
        rotate = 0
        shift = 0
        if(seq[i]=="O"):
            shift = O_count%3 * 2
            O_count += 1
        else:
            offset = 6
            if(int(I_count/4)%2 ==0):
                shift = (I_count%4 * 1) + offset
            else:
                shift = (I_count%4 * 1) + offset
            I_count+=1

        if(rotate!=0):
            actions.append(int(str(rotate)+str(shift)))
        else:
            actions.append(shift)


    print("Final actions are as follows: ",actions)
    result = {"actions":actions}

    app.logger.info("My result :{}".format(result))

    return jsonify(result);
