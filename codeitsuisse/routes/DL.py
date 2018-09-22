import logging
import numpy as np
import numpy as np
import os
import codeitsuisse.routes.train as train
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
def DL_evaluate():
        # JSON mode
        data = request.get_json();
        app.logger.info("data sent for evaluation {}".format(data))

        trg_data = data["question"]

        # train.train(trainX, trainY)
        # testX = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,100,139,180,250,242,139,96,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,145,245,262,236,281,218,227,196,29,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,187,222,274,286,206,123,176,254,222,108,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,57,214,244,233,34,11,0,5,182,235,155,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,81,236,239,27,0,0,0,115,284,254,74,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,34,15,0,0,0,0,196,263,274,70,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,112,260,256,178,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,71,238,243,256,57,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,110,243,234,124,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,163,274,261,145,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,28,219,237,237,33,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,196,241,275,138,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,70,276,271,215,13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,21,194,231,276,122,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,154,259,274,150,13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,242,279,288,22,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,245,250,225,39,18,23,21,22,5,0,6,23,19,35,168,153,169,145,9,0,0,0,0,0,0,0,0,0,261,277,216,217,279,253,286,249,159,155,160,242,280,251,268,237,288,251,109,0,0,0,0,0,0,0,0,0,167,272,280,279,244,256,248,276,238,274,248,232,260,220,272,153,125,113,64,0,0,0,0,0,0,0,0,0,0,134,124,107,113,184,283,278,229,138,125,138,40,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        # testY = [2]

        testX = np.array(trg_data)
        testX = testX.reshape((len(testX), 28, 28, 1)).astype(np.float)

        labels = train.test(testX)

        print("Predictions:",labels)

        y_predict = labels.tolist()

        result = {"answer":y_predict}
        app.logger.info("My result :{}".format(result))

        return jsonify(result);

def load_mnist():
    #APPEND DATA DIRECTORY
    data_dir = '../data'

    fd = open(os.path.join(data_dir, 'train-images-idx3-ubyte'))
    loaded = np.fromfile(file=fd, dtype=np.uint8)
    trX = loaded[16:].reshape((60000, 28, 28, 1)).astype(np.float)

    fd = open(os.path.join(data_dir, 'train-labels-idx1-ubyte'))
    loaded = np.fromfile(file=fd, dtype=np.uint8)
    trY = loaded[8:].reshape((60000)).astype(np.int)

    fd = open(os.path.join(data_dir, 't10k-images-idx3-ubyte'))
    loaded = np.fromfile(file=fd, dtype=np.uint8)
    teX = loaded[16:].reshape((10000, 28, 28, 1)).astype(np.float)

    fd = open(os.path.join(data_dir, 't10k-labels-idx1-ubyte'))
    loaded = np.fromfile(file=fd, dtype=np.uint8)
    teY = loaded[8:].reshape((10000)).astype(np.int)

    trY = np.asarray(trY)
    teY = np.asarray(teY)

    perm = np.random.permutation(trY.shape[0])
    trX = trX[perm]
    trY = trY[perm]

    perm = np.random.permutation(teY.shape[0])
    teX = teX[perm]
    teY = teY[perm]

    return trX, trY, teX, teY


def print_digit(digit_pixels, label='?'):
    for i in range(28):
        for j in range(28):
            if digit_pixels[i, j] > 128:
                print('#'),
            else:
                print('.'),
        print('')

    print('Label: ', label)
