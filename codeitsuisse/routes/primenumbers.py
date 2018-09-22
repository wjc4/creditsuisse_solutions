# import logging
import math

from flask import request, jsonify

from codeitsuisse import app

# logger = logging.getLogger(__name__)

# Creates a list of prime numbers up to given number
def prime_list(A):
    primes = []
    bool_a = [True for i in range(2,A+3)]
    for i in range(2, int(math.sqrt(A))+1):
        if bool_a[i]:
            for j in range( i * i, A +1 , i):
                if bool_a[j]:
                    bool_a[j] = False;

    for i in range(2,A):
        if bool_a[i]:
            primes.append(i)

    return primes

#Returns two prime numbers whose sum is equal to the given number
def prime_sum(A):
    answers = []

    for i in (prime_list(A)):
        for j in (prime_list(A)[::-1]):
            if i + j == A:
                answers.append((i,j))
                break

    return min(answers)

@app.route('/prime-sum', methods=['POST'])
def prime_sum_eval():
    data = request.get_json()
    app.logger.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input")
    result = prime_sum(inputValue)
    app.logger.info("My result :{}".format(result))
    return jsonify(result)
