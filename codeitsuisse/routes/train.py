import numpy   as np
def softmax(x):
    return np.exp(x)/(np.sum(np.exp(x),axis=1,keepdims=True))
def cross_entropy(target,predicted):
        #print(np.log(y1))
        return -np.sum(target*np.log(predicted))/60000
def train(trainX, trainY):
    tx=trainX.reshape(60000,784)
    w=np.zeros((784,10))
    b=np.zeros((1,10))
    y=np.dot(tx,w)+b
    ty=np.zeros((60000,10))
    ty[np.arange(60000),trainY] = 1
    #ty=ty.reshape((60000,1,10))
    #z=softmax(y)
    #error=cross_entropy(ty,z)
    for i in range(1000):
        #print tx.shape,w.shape
        y=np.dot(tx,w)+b
        print(y[0])
        soft=softmax(y)
        loss=cross_entropy(ty,soft)
        print ("In %d iteration loss is %d",i,loss)
        eta=0.00001/60000
        #print eta
        w=w-eta*(tx.T.dot(soft-ty))
        #print w[1:200]
        b=b-np.around((np.sum(soft-ty)),4)
        #print b
    np.savetxt("weights.csv",w,delimiter=",")


def test(testX):
    #Read stored weights
    w=np.genfromtxt("codeitsuisse/routes/weights.csv",delimiter=",")
    print(w.shape,w)
    newy=testX.reshape(len(testX),784).dot(w)
    print(newy.shape)
    newys=softmax(newy)
    output=newys.argmax(axis=1)
    #acc=np.sum(out==testY)
    #print acc
    return output
