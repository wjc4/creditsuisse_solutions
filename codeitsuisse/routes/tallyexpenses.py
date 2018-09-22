# import logging
from flask import request, jsonify

from codeitsuisse import app

input_data = {}
N = len(input_data['persons'])
ppl = input_data['persons']
answer = {
    "transactions": []
}

def form_table(data):
    expenses = data['expenses']
    people = data['persons']

    table = [[0] * len(people) for i in range(len(people))]

    for expense in expenses:
        index_paidBy = people.index(expense["paidBy"])
        print(index_paidBy)

        if 'exclude' in expense:
            owe_money = people[:]
            for name in expense["exclude"]:
                owe_money.remove(name)

            # owed = float(round(Decimal(expense["amount"]/(len(owe_money))-1),2))
            owed = round(float((expense["amount"]/(len(owe_money))-1)),2)

            for i in range(len(owe_money)):
                if i == index_paidBy:
                    pass
                else:
                    table[i][index_paidBy] += owed


        else:
            # owed = float(round(Decimal(expense["amount"]/(len(people)-1)),2))
            owed = round(float(expense["amount"]/(len(people)-1)),2)

            for i in range(len(people)):
                if i == index_paidBy:
                    pass
                else:
                    table[i][index_paidBy] += owed

    return table

def getMin(arr):
    global N

    minInd = 0
    for i in range(1, N):
        if (arr[i] < arr[minInd]):
            minInd = i
    return minInd

def getMax(arr):
    global N

    maxInd = 0
    for i in range(1, N):
        if (arr[i] > arr[maxInd]):
            maxInd = i
    return maxInd


def minOf2(x, y):
    return x if x < y else y

def minCashFlowRec(amount):
    global answer
    global ppl

    mxCredit = getMax(amount)
    mxDebit = getMin(amount)

    print(mxCredit)
    print(mxDebit)

    # Terminating case
    if (amount[mxCredit] == 0 and amount[mxDebit] == 0):
        return 0

    # Find the minimum of two amounts
    min = minOf2(-amount[mxDebit], amount[mxCredit])
    amount[mxCredit] -=min
    amount[mxDebit] += min

    final_paid = round(min,2)
    # # If minimum is the maximum amount to be
    # print("Person " , mxDebit , " pays " , final_paid
    #     , " to " , "Person " , mxCredit)
    transaction = {
        "from": ppl[mxDebit],
        "to": ppl[mxCredit],
        "amount": final_paid
    }
    answer["transactions"].append(transaction)

    # Recursion
    minCashFlowRec(amount)

def minCashFlow(graph):
    global N

    net_amount = [0 for i in range(N)]

    for p in range(N):
        for i in range(N):
            net_amount[p] += (graph[i][p] - graph[p][i])

    minCashFlowRec(net_amount)


@app.route('/tally-expense', methods=['POST'])
def evaluate_primes():
    global input_data

    # JSON mode
    data = request.get_json();
    app.logger.info("data sent for evaluation {}".format(data))
    input_data = data.get("input");

    table = form_table(input_data)
    minCashFlow(table)

    result = answer

    app.logger.info("My result :{}".format(result))

    return jsonify(result);
#
# data = {
#     "name": "Jan Expense Report",
#     "persons": ["Alice", "Bob", "Claire", "David"],
#     "expenses": [
#         {
#             "category": "Breakfast",
#             "amount": 60,
#             "paidBy": "Bob",
#             "exclude": ["Claire","David"]
#         },
#         {
#             "category": "Phone Bill",
#             "amount": 100,
#             "paidBy": "Claire"
#         },
#         {
#             "category": "Groceries",
#             "amount": 80,
#             "paidBy": "David"
#         },
#         {
#             "category": "Petrol",
#             "amount": 40,
#             "paidBy": "David"
#         }
#     ]
# }




# table = form_table(data)
# print(table)
# minCashFlow(table)
# print(answer)
