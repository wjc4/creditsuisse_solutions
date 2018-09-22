# import logging
from flask import request, jsonify

from codeitsuisse import app

@app.route('/tally-expense', methods=['POST'])
def evaluate_tally_expense():
    # JSON mode
    data = request.get_json()
    app.logger.info("data sent for evaluation {}".format(data))

    answer = {
        "transactions": []
    }

    N = len(data.get("persons"))
    ppl = data.get("persons")
    table = calculate_amount(data.get("expenses"),data.get("persons"))
    print(table)
    amount = []
    for human in table:
        amount.append(table[human])
    answer = {
        "transactions": []
    }
    result = minCashFlowRec(amount, N, ppl, answer)

    # result = answer

    app.logger.info("My result :{}".format(result))

    return jsonify(result)

def calculate_amount(expenses, people):
    table = {}
    for human in people:
        table[human]=0
    for expense in expenses:
        table[expense["paidBy"]] = table[expense["paidBy"]] + expense['amount']
        tempcopy = people.copy()
        for human in expense['exclude']:
            tempcopy.remove(human)
        div_amt = expense['amount']/len(tempcopy)
        # sum=(div_amt*100-int(div_amt*100))*len(tempcopy)
        # print(sum)
        # div_amt = float(int(div_amt*100))/100
        # print(div_amt)
        for human in tempcopy:
            table[human] = table[human] - div_amt
    return table

# Python3 program to fin maximum
# cash flow among a set of persons
 
# Number of persons(or vertices in graph)
# N = 3
 
# A utility function that returns
# index of minimum value in arr[]
def getMin(arr, N):
     
    minInd = 0
    for i in range(1, N):
        if (arr[i] < arr[minInd]):
            minInd = i
    return minInd
 
# A utility function that returns
# index of maximum value in arr[]
def getMax(arr, N):
 
    maxInd = 0
    for i in range(1, N):
        if (arr[i] > arr[maxInd]):
            maxInd = i
    return maxInd
 
# A utility function to
# return minimum of 2 values
def minOf2(x, y):
 
    return x if x < y else y
 
# amount[p] indicates the net amount to
# be credited/debited to/from person 'p'
# If amount[p] is positive, then i'th 
# person will amount[i]
# If amount[p] is negative, then i'th
# person will give -amount[i]
def minCashFlowRec(amount, N, humans, answer):
 
    # Find the indexes of minimum
    # and maximum values in amount[]
    # amount[mxCredit] indicates the maximum
    # amount to be given(or credited) to any person.
    # And amount[mxDebit] indicates the maximum amount
    # to be taken (or debited) from any person.
    # So if there is a positive value in amount[], 
    # then there must be a negative value
    mxCredit = getMax(amount, N)
    mxDebit = getMin(amount, N)
 
    # If both amounts are 0, 
    # then all amounts are settled
    if (amount[mxCredit] == 0 and amount[mxDebit] == 0):
        return 0
 
    # Find the minimum of two amounts
    min = minOf2(-amount[mxDebit], amount[mxCredit])
    amount[mxCredit] -=min
    amount[mxDebit] += min
 
    if min < 0.01:
        return answer
    if min == 0:
        return answer

    # If minimum is the maximum amount to be
    # print("Person " , mxDebit , " pays " , min
    #     , " to " , "Person " , mxCredit)
    transaction = {
        "from": humans[mxDebit],
        "to": humans[mxCredit],
        "amount": float(normal_round(min*100))/100
    }
    print(transaction)
    answer['transactions'].append(transaction)
    print(answer)
        
    # Recur for the amount array. Note that
    # it is guaranteed that the recursion
    # would terminate as either amount[mxCredit] 
    # or amount[mxDebit] becomes 0
    minCashFlowRec(amount, N, humans, answer)
    return answer
 
import math
def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)

# Given a set of persons as graph[] where
# graph[i][j] indicates the amount that
# person i needs to pay person j, this
# function finds and prints the minimum 
# cash flow to settle all debts.
# def minCashFlow(graph):
 
#     # Create an array amount[],
#     # initialize all value in it as 0.
#     amount = [0 for i in range(N)]
 
#     # Calculate the net amount to be paid
#     # to person 'p', and stores it in amount[p].
#     # The value of amount[p] can be calculated by
#     # subtracting debts of 'p' from credits of 'p'
#     for p in range(N):
#         for i in range(N):
#             amount[p] += (graph[i][p] - graph[p][i])
 
#     minCashFlowRec(amount)
     
# Driver code
 
# graph[i][j] indicates the amount
# that person i needs to pay person j
# graph = [ [0, 1000, 2000],
#           [0, 0, 5000],
#           [0, 0, 0] ]
 
# minCashFlow(graph)
 
# This code is contributed by Anant Agarwal.