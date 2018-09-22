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
    count = [0]
    ans = outer_sum(q,count,a,b)
    # ans = highmem(n,a,b,q)
    # a = np.array([1, 3, 5, 6, 9, 10, 14, 15, 56])

    # np.where(np.logical_and(a>=6, a<=10))
    # # returns (array([3, 4, 5]),)

    # b = np.array(b_sums)
    # for
    # np.where(np.logical_and(b>=6, b<=10))

    # app.logger.info("My result :{}".format(result))
    ans = ans % 100000123
    return jsonify({"result":int(ans)})

def outer_sum(q,count,numbers, b, partial=[]):
    s = sum(partial)
    # print(q,count,b.copy(),s,[])
    subset_sum(q,count,b,s,[])

    # # check if the partial sum is equals to target
    # if s == target:
    #     print("sum(%s)=%s" % (partial, target))
    # if s >= target:
    #     return  # if we reach the number why bother to continue

    for i in range(len(numbers)):
        n = numbers[i]
        remaining = numbers[i + 1:]
        outer_sum(q,count,remaining,b,partial + [n])
    
    return count[0]

def subset_sum(q,count, numbers, target, partial=[]):
    s = sum(partial)
    # print(s)
    # check if the partial sum is equals to target
    # if target == 0 or s == 0:
    #     print(target,s, count)
    if s >= target-q and s <= target+q:
        count[0] += 1
    if s >= target+q:
        return  # if we reach the number why bother to continue
    # print(numbers)
    for i in range(len(numbers)):
        n = numbers[i]
        # print(n,numbers,"target: ",target)
        remaining = numbers[i + 1:]
        subset_sum(q,count,remaining, target, partial + [n])
    # print(count[0])

def highmem(n,a,b,q):
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

    return result