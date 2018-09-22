# import logging

from flask import request, jsonify

from codeitsuisse import app

# logger = logging.getLogger(__name__)

import itertools
import numpy as np

@app.route('/two-dinosaurs', methods=['POST'])
def dino2():
    data = request.get_json()
    app.logger.info("data sent for evaluation {}".format(data))
    n = data.get("number_of_types_of_food")
    a = data.get("calories_for_each_type_for_raphael")
    b = data.get("calories_for_each_type_for_leonardo")
    q = data.get("maximum_difference_for_calories")

    a.sort()
    b.sort()

    a_combs = [[0,],]
    b_combs = [[0,],]
    for i in range(1, n+1):
        els = [list(x) for x in itertools.combinations(a, i)]
        a_combs.extend(els)
        els = [list(x) for x in itertools.combinations(b, i)]
        b_combs.extend(els)

    print(a_combs,b_combs)
    a_sums=[]
    b_sums=[]
    for i in range(len(a_combs)):
        a_sums.append(sum(a_combs[i]))
        b_sums.append(sum(b_combs[i]))
    print(a_sums,b_sums)
 
    total = 0
    for num in a_sums:
        # sum += x for x in b_sums if l <= x <= r
        start = np.searchsorted(b_sums, num-q, 'left')
        end = np.searchsorted(b_sums, num+q, 'right')
        total = total + end - start

    result = total % 100000123
    # a = np.array([1, 3, 5, 6, 9, 10, 14, 15, 56])

    # np.where(np.logical_and(a>=6, a<=10))
    # # returns (array([3, 4, 5]),)

    # b = np.array(b_sums)
    # for
    # np.where(np.logical_and(b>=6, b<=10))

    # app.logger.info("My result :{}".format(result))
    return jsonify({"result":int(result)})

