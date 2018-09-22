# # import logging
# import math
#
# from flask import request, jsonify
#
# from codeitsuisse import app
#
# # logger = logging.getLogger(__name__)
#
# @app.route('/prime-sum', methods=['POST'])
# def evaluate_primes():
#     # JSON mode
#     data = request.get_json();
#     app.logger.info("data sent for evaluation {}".format(data))
#     inputValue = data.get("input");
#
#     # Args Key Mode
#     # data = request.args
#     # inputValue = int(data.get('input'))
#
#     result = sum_of_primes(inputValue)
#     app.logger.info("My result :{}".format(result))
#
#     return jsonify(result);
#
#
# def prime_sieve(limit):
#     prime = [True] * limit
#     prime[0] = prime[1] = False
#
#     for i, is_prime in enumerate(prime):
#         if is_prime:
#             yield i
#             for n in range(i * i, limit, i):
#                 prime[n] = False
#
# def sum_of_primes(n):
#     solution = []
#     primes = list(prime_sieve(n))
#     # for fast `in` lookups:
#     primes_set = set(primes)
#     for a in primes:
#         b = n - a
#         if b in primes_set:
#             # this is the lexicographically smallest by design
#             solution = [b, a]
#
#     if len(solution)==0:
#         return [n]
#     else:
#         return solution
#
# # # Python Program to print
# # # all N primes after prime
# # # P whose sum equals S
# # import math
# #
# # # vector to store prime
# # # and N primes whose
# # # sum equals given S
# # set = []
# # prime = []
# #
# # def prime_sieve(limit):
# #     prime = [True] * limit
# #     prime[0] = prime[1] = False
# #
# #     for i, is_prime in enumerate(prime):
# #         if is_prime:
# #             yield i
# #             for n in range(i * i, limit, i):
# #                 prime[n] = False
# #
# # # function to display N primes whose sum equals S
# # def display():
# #
# #     global set, prime
# #     length = len(set)
# #     for i in range(0, length):
# #         print (set[i], end = " ")
# #     print ()
# #
# # # function to evaluate all possible N primes whose sum equals S
# # def primeSum(total, N, sum, index):
# #
# #     global set, prime
# #
# #     # if total equals sum and total is reached using N primes
# #     if (total == sum and len(set) == N):
# #
# #         # display the N primes
# #         display()
# #         return
# #
# #     # if total is greater than S or if index has reached last element
# #     if (total > sum or index == len(prime)):
# #         return
# #
# #     # add prime[index] to set vector
# #     set.append(prime[index])
# #
# #     # include the (index)th prime to total
# #     primeSum(total + prime[index], N, sum, index + 1)
# #
# #     # remove element from set vector
# #     set.pop()
# #
# #     # exclude (index)th prime
# #     primeSum(total, N, sum, index + 1)
# #
# # # function to generate all primes
# # def allPrime(sum):
# #
# #     global set, prime
# #
# #     # all primes less than sum
# #     primes = prime_sieve(sum)
# #
# #     # if primes are less than N
# #     if (len(prime) < 4):
# #         return primeSum(0, 4, sum, 0)
# #
# # @app.route('/prime-sum', methods=['POST'])
# # def evaluate_primes():
# #     # JSON mode
# #     data = request.get_json();
# #     app.logger.info("data sent for evaluation {}".format(data))
# #     inputValue = data.get("input");
# #
# #     # Args Key Mode
# #     # data = request.args
# #     # inputValue = int(data.get('input'))
# #
# #     result = allPrime(inputValue)
# #     app.logger.info("My result :{}".format(result))
# #
# #     return jsonify(result);



# import logging
import math

from itertools import combinations as cmb
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
    end=False
    i=1
    n=inputValue
    while(i<=10):
        cnt = i
        ci = iter(cmb(genP(n), cnt))
        while True:
            try:
                c = next(ci)
                if sum(c)==n:
                    print(n, ',', cnt , "->", '+'.join(str(s) for s in c))
                    result = c
                    break
            except:
                print(n, ',', cnt, " -> Not possible")

                break
        i=i+1

    app.logger.info("My result :{}".format(result))

    return jsonify(result);


def isP(n):
    if n==2:
        return True
    if n%2==0:
        return False
    return all(n%x>0 for x in range(3, int(n**0.5)+1, 2))

def genP(n):
    p = [2]
    p.extend([x for x in range(3, n+1, 2) if isP(x)])
    return p
