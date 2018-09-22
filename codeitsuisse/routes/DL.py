import logging
import numpy as np
from scipy.optimize import curve_fit

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/machine-learning/question-1', methods=['POST'])
def ML_evaluate():

    # JSON mode
    data = request.get_json();
    app.logger.info("data sent for evaluation {}".format(data))

    xdata = np.array(data["input"])
    n,m = np.shape(xdata)
    X0 = np.ones((n,1))
    xdata = np.hstack((X0,xdata))
    n,m = np.shape(xdata)
    X0 = xdata[:,0]
    X1 = xdata[:,1]
    X2 = xdata[:,2]
    X3 = xdata[:,3]

    ydata = np.array(data["output"])
    q = np.array(data["question"])

    print(np.shape(X0))
    print(np.shape(ydata))

    # Args Key Mode
    # data = request.args
    # inputValue = int(data.get('input'))

    #calculate optimal values & cov
    p0 = 0.,0.,0.
    popt, pcov = curve_fit(func, (X1,X2,X3), ydata, p0)

    result = popt.dot(q)

    result = {"answer":result}

    app.logger.info("My result :{}".format(result))

    return jsonify(result);

def func(X, b, c, d):
    X1,X2,X3 = X
    return b*X1 + c*X2 + d*X3

@app.route('/machine-learning/question-2', methods=['POST'])
def DL_evaluate(): {}
