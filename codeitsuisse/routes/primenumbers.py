# import logging
import math

from flask import request, jsonify

from codeitsuisse import app

# logger = logging.getLogger(__name__)

@app.route('/prime-sum', methods=['POST'])
def evaluate_primes():
    # JSON mode
    data = request.get_json();
    app.logger.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input");

    # Args Key Mode
    # data = request.args
    # inputValue = int(data.get('input'))

    result = sum_of_primes(inputValue)
    app.logger.info("My result :{}".format(result))

    return jsonify(result);


def prime_sieve(limit):
    prime = [True] * limit
    prime[0] = prime[1] = False

    for i, is_prime in enumerate(prime):
        if is_prime:
            yield i
            for n in range(i * i, limit, i):
                prime[n] = False

def sum_of_primes(n):
    solution = []
    primes = list(prime_sieve(n))
    # for fast `in` lookups:
    primes_set = set(primes)
    for a in primes:
        b = n - a
        if b in primes_set:
            # this is the lexicographically smallest by design
            solution = [a, b]

    if len(solution)==0:
        solution = [n]

    return solution
