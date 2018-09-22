# import logging

from flask import request, jsonify

from codeitsuisse import app

# logger = logging.getLogger(__name__)

@app.route('/customers-and-hotel/minimum-distance', methods=['POST'])
def part1mindist():
    data = request.get_json()
    app.logger.info("data sent for evaluation {}".format(data))
    result = findMinDiff(data, len(data))
    app.logger.info("My result :{}".format(result))
    return jsonify({'answer':result})

@app.route('/customers-and-hotel/minimum-camps', methods=['POST'])
def mincamp():
    data = request.get_json()
    app.logger.info("data sent for evaluation {}".format(data))
    ranges=[]
    for hooman in data:
        ranges.append((hooman['pos']-hooman['distance'],hooman['pos']+hooman['distance']))
    result = findMinCamps(ranges)
    app.logger.info("My result :{}".format(result))
    return jsonify({'answer':result})

# Returns minimum difference between any pair
def findMinDiff(arr, n):
 
    # Sort array in non-decreasing order
    arr = sorted(arr)
 
    # Initialize difference as infinite
    diff = 10**20
 
    # Find the min diff by comparing adjacent
    # pairs in sorted array
    for i in range(n-1):
        if arr[i+1] - arr[i] < diff:
            diff = arr[i+1] - arr[i]
        if diff == 0:
            break
 
    # Return min diff
    return diff

def findMinCamps(ranges):
    # sort by the end points
    # ranges=[(1,5),(2,4),(4,6),(3,7),(5,9),(6,6)]

    ranges.sort(key=lambda p:p[1])

    #generate required points
    out=[]
    last = None
    ans = 0
    for r in ranges:
        if last == None or last < r[0]:
            last = r[1]
            ans = ans + 1
            out.append(last)
    return ans
    #print answer
    # print(out)