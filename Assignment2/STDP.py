import random
CAPACITANCE = 1
RESISTANCE = 20
THRESHOLD = 7
SPIKE_VALUE = 1
POST_SPIKE = 14

class LIFNeuron:
    potential = 0
    weights = []
    times = []
    name = ""
    lastSpike = 0

    def __init__(self, numInputs, newName):
        self.weights = []
        for i in range(numInputs):
            self.weights.append(10 * (random.random() - 0.45))
        self.times = [0] * numInputs
        self.name = newName

    def update(self, inputs):
        for i in range(0, len(inputs)):
            inputs[i] = inputs[i] * self.weights[i]
            if inputs[i] > 0:
                self.times[i] = 1
            elif self.times[i] > 0:
                self.times[i] += 1

        for input in inputs:
            self.potential += (input - self.potential/RESISTANCE) / CAPACITANCE
        # If membrane potential reaches threshold, fire!
        #print("OUT POTENTIAL: ",self.potential)
        self.updateWeights(inputs)
        if self.potential > THRESHOLD:
            self.potential = 0
            self.lastSpike = POST_SPIKE
            return SPIKE_VALUE
        if self.lastSpike > 0:
            self.lastSpike -= 1
        return 0
    #Used to update the weights of nodes based on prespike timing.
    def updateWeights (self,inputs):
        counter = 0
        for i in range (0,len(inputs)):
            if self.potential > THRESHOLD and self.times[counter] != 0:
                self.weights[counter] = self.weights[counter] + (((self.times[counter])**-1)/5)
                if self.weights[counter] >= 6:
                    self.weights[counter] = 6
            elif self.times[i] > 0 and self.lastSpike > 0:
                self.weights[counter] = self.weights[counter] - ((self.lastSpike**(1/2))/100)
                if self.weights[counter] <= -6:
                    self.weights[counter] = -6
            counter +=1


HIDDEN_LAYER_SIZE = 5

outNeuron = LIFNeuron(HIDDEN_LAYER_SIZE, "out")
hiddenLayer = []
for i in range(0, HIDDEN_LAYER_SIZE):
    hiddenLayer.append(LIFNeuron(2,i))

# x and y are simulated input neurons
def updateNetwork(x, y, hiddenLayer, out):
    numSpikes = 0
    for time in range(500):
        spikes = []
        inX = 0
        inY = 0
        if x == 1:
            inX = 1 if (time % 2 == 0) else 0
        else:
            inX = 1 if (time % 10 == 0) else 0
        if y == 1:
            inY = 1 if (time % 2 == 0) else 0
        else:
            inY = 1 if (time % 10 == 0) else 0

        for i in range(0, len(hiddenLayer)):
            spikes.append(hiddenLayer[i].update([inX, inY]))
        if x != y:
            out.potential = THRESHOLD * 100 if (time % 2 == 0) else out.potential
        else:
            out.potential = THRESHOLD * 100 if (time % 10 == 0) else out.potential
        numSpikes += out.update(spikes)

    return numSpikes

# consider each iteration of this loop 1 milisecond
failures = 0
for j in  range(0,1):
    for i in range(0, 100):
        # 50/50 of x or y being 1 or 0
       # x = 1 if random.random() > 0.5 else 0
       # y = 1 if random.random() > 0.5 else 0
        if i % 4 == 0:
           x = 0
           y = 0
        elif i % 4 == 1:
          x = 1
          y = 1
        elif i % 4 == 2:
          x = 1
          y = 0
        elif i % 4 == 3:
          x = 0
          y = 1
        outSpike = updateNetwork(x, y, hiddenLayer, outNeuron)

    for i in range  (0,len(outNeuron.weights)):
        print("Weight of Neuron ", i, ": ", outNeuron.weights[i])
        print("Neuron ", i, "'s weights: ",  hiddenLayer[i].weights[0], " ",  hiddenLayer[i].weights[1])
        print("")
x = 0
y = 0
print("x = 0, y = 0. Result: ", (updateNetwork(x, y, hiddenLayer, outNeuron)))

x = 1
y = 0
print("x = 1, y = 0. Result: ", (updateNetwork(x, y, hiddenLayer, outNeuron)))

x = 0
y = 1
print("x = 0, y = 1. Result: ", (updateNetwork(x, y, hiddenLayer, outNeuron)))

x = 1
y = 1
print("x = 1, y = 1. Result: ", (updateNetwork(x, y, hiddenLayer, outNeuron)))
