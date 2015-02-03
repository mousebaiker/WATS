import random
import math


class Neuron(object):
    def __init__(self, function):
        self.inputvector = []
        self.evalfunction = function

    def input(self, x, w):
        self.inputvector.append([x, w])

    def output(self):
        self.outputsum = sum([x * w for x, w in self.inputvector])
        self.inputvector = []
        return self.evalfunction(self.outputsum)

    def get_raw(self):
        return self.outputsum


def outputfunc(x):
    return x


def outputfuncd(x):
    return 1


class NeuralNetwork(object):
    """Implements a 3-layer neural network
        layers - (# of input nodes, # of hidden nodes, # of output neurons)"""

    def __init__(self, layers):
        self.layers = layers


    def generate_nodes(self):
        self.nodes = [[Neuron(outputfunc) for k in range(self.layers[i + 1])] for i in range(2)]

    def generate_weights(self):
        self.hiddenweights = [[random.random() for _ in range(self.layers[0])] for _ in range(self.layers[1])]
        self.outputweights = [[random.random() for _ in range(self.layers[1])] for _ in range(self.layers[2])]

        beta = 0.7 * (self.layers[1]) ** (1 / self.layers[0])
        n = math.fsum([w ** 2 for i in range(self.layers[1]) for w in self.hiddenweights[i]]) ** 0.5
        for i, weights in enumerate(self.hiddenweights):
            for k, w in enumerate(weights):
                self.hiddenweights[i][k] = beta * w / n

    def input(self, inputvector, verbose=False):
        assert len(inputvector) == self.layers[0]
        if not verbose:
            return self.insert(1, self.insert(0, inputvector))
        else:
            hiddenoutput = self.insert(0, inputvector)
            output = self.insert(1, hiddenoutput)
            return (output, hiddenoutput)

    def insert(self, layer, inputvec):
        output = []
        for k, node in enumerate(self.nodes[layer]):
            for i, value in enumerate(inputvec):
                node.input(value, self.hiddenweights[k][i])
            output.append(node.output())
        return output

    def teach(self, inputvector, resultvector):
        assert len(inputvector) == self.layers[0]
        assert len(resultvector) == self.layers[2]

        result, hiddenoutputvalues = self.input(inputvector, verbose=True)
        errors = [(resultvector[i] - result[i]) * outputfuncd(self.nodes[1][i].get_raw()) for i in
                  range(self.layers[2])]
        learningstep = 0.5

        dwoutput = [[learningstep * errors[i] * hiddenoutputvalues[k]
                     for k in range(self.layers[1])] for i in range(self.layers[2])]

        hiddenerrors = [sum([self.outputweights[i][k] * errors[i] for i in range(self.layers[2])]) *
                        outputfuncd(self.nodes[0][k].get_raw())
                        for k in range(self.layers[1])]
        dwhidden = [[learningstep * hiddenerrors[i] * inputvector[k]
                     for k in range(self.layers[0])] for i in range(self.layers[1])]

        for i in range(self.layers[1]):
            for k in range(self.layers[0]):
                self.hiddenweights[i][k] += dwhidden[i][k]

        for i in range(self.layers[2]):
            for k in range(self.layers[1]):
                self.outputweights[i][k] += dwoutput[i][k]
