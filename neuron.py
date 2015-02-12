import random
import math

from helpers import transpose


def minus(x):
    return -x


def elementsSum(x):
    assert isinstance(x, list)
    if isinstance(x[0], int) or isinstance(x[0], float):
        return sum(x)
    else:
        return sum([elementsSum(i) for i in x])


def matrixSum(x, y):
    assert len(x) == len(y)
    assert all([len(x[i]) == len(y[i]) for i in range(len(x))])

    for i in range(len(x)):
        for j in range(len(x[0])):
            x[i][j] += y[i][j]

    return x


def matrixSubtract(x, y):
    return matrixSum(x, functoMatrix(minus, y))


def starMatrix(x, y):
    """Implements matrix multiplication"""
    assert len(x[0]) == len(y)

    result = [[0 for _ in range(len(y[0]))] for _ in range(len(x))]

    for i in range(len(x)):
        for j in range(len(y[0])):
            summ = 0
            for k, value in enumerate(x[i]):
                summ += value * y[k][j]
            result[i][j] = summ

    return result


def functoMatrix(func, matrix):
    if isinstance(matrix, float) or isinstance(matrix, int):
        return func(matrix)
    else:
        return [functoMatrix(func, i) for i in matrix]


def dotMatrix(x, y):
    assert len(x) == len(y)
    assert all([len(x[i]) == len(y[i]) for i in range(len(x))])

    for i in range(len(x)):
        for j in range(len(x[0])):
            x[i][j] *= y[i][j]
    return x


def outputfunc(x):
    return 1 / (1 + math.exp(-x))


def outputfuncd(x):
    return outputfunc(x) * (1 - outputfunc(x))


class NeuralNetwork(object):
    """Implements a 3-layer neural network
        layers - (# of input nodes, # of hidden nodes, # of output neurons)"""

    def __init__(self, layers, lmbd):
        self.layers = layers
        self.lmbd = lmbd

    def generate_weights(self):
        self.hiddenweights = [[random.random() for _ in range(self.layers[1])] for _ in range(self.layers[0])]
        self.outputweights = [[random.random() for _ in range(self.layers[2])] for _ in range(self.layers[1])]

        beta = 0.7 * (self.layers[1]) ** (1 / self.layers[0])
        n = math.fsum([w ** 2 for i in range(self.layers[0]) for w in self.hiddenweights[i]]) ** 0.5
        for i, weights in enumerate(self.hiddenweights):
            for k, w in enumerate(weights):
                self.hiddenweights[i][k] = beta * w / n

    def input(self, inputvector):
        assert len(inputvector[0]) == self.layers[0]
        self.hiddenoutput = starMatrix(inputvector, self.hiddenweights)
        self.activatedho = functoMatrix(outputfunc, self.hiddenoutput)
        self.output = starMatrix(self.activatedho, self.outputweights)
        self.result = functoMatrix(outputfunc, self.output)
        return self.result

    def cost(self, inputvector, expOutput):
        """ Computes the cost function.
         inputvector - 2-dimentional array as specified in input function,
        expOutput - 1xn array of expected output """
        output = self.input(inputvector)
        j = 0.5 * elementsSum(
            functoMatrix(lambda x: x ** 2, matrixSubtract(expOutput, output)))  # /len(inputvector) + \
        # self.lmbd/2 * elementsSum(functoMatrix(lambda  x: x**2, self.hiddenweights)) + \
        # elementsSum(functoMatrix(lambda x: x**2, self.outputweights))
        return j

    def teach(self, inputvector, resultvector, leariningrate):
        assert len(inputvector) == len(resultvector)
        assert all([len(inputvector[i]) == self.layers[0] for i in range(len(inputvector))])
        assert all([len(resultvector[i]) == self.layers[2] for i in range(len(resultvector))])

        output = self.input(inputvector)

        delta3 = dotMatrix(matrixSubtract(output, resultvector), functoMatrix(outputfuncd, self.output))
        # changerate2 = matrixSum(starMatrix(transpose(self.activatedho), delta3), functoMatrix(lambda x: self.lmbd*x, self.outputweights))

        changerate2 = starMatrix(transpose(self.activatedho), delta3)

        delta2 = dotMatrix(starMatrix(delta3, transpose(self.outputweights)),
                           functoMatrix(outputfuncd, self.hiddenoutput))
        # changerate1 = matrixSum(starMatrix(transpose(inputvector), delta2), functoMatrix(lambda x: self.lmbd*x, self.hiddenweights))

        changerate1 = starMatrix(transpose(inputvector), delta2)

        self.outputweights = matrixSubtract(self.outputweights, functoMatrix(lambda x: leariningrate * x, changerate2))
        self.hiddenweights = matrixSubtract(self.hiddenweights, functoMatrix(lambda x: leariningrate * x, changerate1))
