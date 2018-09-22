# import logging
import math

from flask import request, jsonify

from codeitsuisse import app

# logger = logging.getLogger(__name__)

# Function to create a list of all prime numbers uptil given number
def list_prime(A):
    primes = []  # initialise an empty list of primes
    bool_a = [True for i in range(2,A+3)]  # creates boolean list of index
    for  i in range(2, int(math.sqrt(A))+1):
        if bool_a[i]:
            for j in range( i * i, A +1 , i):  # eliminate all multiples of i*i+i, i*i+2i and so on uptil A+1
                if bool_a[j]:
                    bool_a[j] = False;

    for i in range(2,A):  # the index of reamaining bools are prime numbers
        if bool_a[i]:
            primes.append(i)

    return primes

#Function that returns two prime numbers whose sum is equal to the given number
def prime_sum(A):
    solution_set = []

    for i in (list_prime(A)):
        for j in (list_prime(A)[::-1]):
            if i + j == A:
                solution_set.append((i,j))
                break

    return min(solution_set)

@app.route('/prime-sum', methods=['POST'])
def prime_sum_eval():
    data = request.get_json()
    app.logger.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input")
    result = prime_sum(inputValue)
    app.logger.info("My result :{}".format(result))
    return jsonify(result)
