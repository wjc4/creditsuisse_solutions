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

    # challenge 1
    for i in range(n):
        shift = (i%5)* 2
        actions.append(shift)


    print("Final actions are as follows: ",actions)
    result = {"actions":actions}

    app.logger.info("My result :{}".format(result))

    return jsonify(result);
