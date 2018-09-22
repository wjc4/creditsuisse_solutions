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