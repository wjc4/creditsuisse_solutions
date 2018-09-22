# import logging
from flask import request, jsonify

from codeitsuisse import app

from decimal import *

answer = {
    "transactions": []
}

@app.route('/tally-expense', methods=['POST'])
def evaluate_tally_expense():
    # JSON mode
    data = request.get_json();
    app.logger.info("data sent for evaluation {}".format(data))
    input_data = data.get("input");

    N = len(data.get("persons"))
    ppl = data.get("persons")
    table = form_table(data.get("expenses"),data.get("persons"))
    print(table)
    minCashFlow(table,ppl,N)

    result = answer

    app.logger.info("My result :{}".format(result))

    return jsonify(result);

def form_table(expenses, people):
    table = [[0] * len(people) for i in range(len(people))]

    for expense in expenses:
        index_paidBy = people.index(expense["paidBy"])
        print(index_paidBy)

        if 'exclude' in expense:
            owe_money = people[:]
            for name in expense["exclude"]:
                owe_money.remove(name)

            # owed = float(round(Decimal(expense["amount"]/(len(owe_money))-1),2))
            owed = round(Decimal((expense["amount"]/(len(owe_money))-1)),2)

            for i in range(len(owe_money)):
                if i == index_paidBy:
                    pass
                else:
                    table[i][index_paidBy] += owed


        else:
            # owed = float(round(Decimal(expense["amount"]/(len(people)-1)),2))
            owed = round(Decimal(expense["amount"]/(len(people)-1)),2)

            for i in range(len(people)):
                if i == index_paidBy:
                    pass
                else:
                    table[i][index_paidBy] += owed

    return table

def getMin(arr,N):

    minInd = 0
    for i in range(1, N):
        if (arr[i] < arr[minInd]):
            minInd = i
    return minInd

def getMax(arr,N):

    maxInd = 0
    for i in range(1, N):
        if (arr[i] > arr[maxInd]):
            maxInd = i
    return maxInd


def minOf2(x, y):
    return x if x < y else y

def minCashFlowRec(amount,ppl,N):
    global answer

    mxCredit = getMax(amount,N)
    mxDebit = getMin(amount,N)

    print('Amount is:',amount)
    # Terminating case
    if (amount[mxCredit] == 0.0 and amount[mxDebit] == 0.0):
        return 0

    # Find the minimum of two amounts
    min = minOf2(-amount[mxDebit], amount[mxCredit])
    amount[mxCredit] -= round(min,2)
    amount[mxDebit] += round(min,2)

    print(min)
    final_paid = round(min,2)
    # # If minimum is the maximum amount to be
    print("Person " , mxDebit , " pays " , final_paid
        , " to " , "Person " , mxCredit)
    transaction = {
        "from": ppl[mxDebit],
        "to": ppl[mxCredit],
        "amount": float(final_paid)
    }
    answer["transactions"].append(transaction)

    # Recursion
    minCashFlowRec(amount,ppl,N)

def minCashFlow(graph,ppl,N):
    net_amount = [0 for i in range(N)]

    for p in range(N):
        for i in range(N):
            net_amount[p] += (graph[i][p] - graph[p][i])

    for i in range(len(net_amount)):
        net_amount[i] = round(net_amount[i],2)

    print("net amount is",net_amount)
    minCashFlowRec(net_amount,ppl,N)


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
