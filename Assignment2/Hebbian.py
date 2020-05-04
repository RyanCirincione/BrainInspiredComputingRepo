import random
CAPACITANCE = 1
RESISTANCE = 30
THRESHOLD = 3
SPIKE_VALUE = 1

class LIFNeuron:
    potential = 0
    weights = []
    name = ""

    def __init__(self, numInputs, newName):
        self.weights = [5] * numInputs # TODO: change 0.5 to be random, otherwise network is symmetric
        self.post = [1] * numInputs
        self.prev = [1] * numInputs
        self.a2 = [1] * numInputs
        self.name = newName

    def update(self, inputs):

        for i in range(0, len(inputs)):
            inputs[i] = inputs[i] * self.weights[i]

            if inputs[i] > 0:
                self.post[i] = 1
                self.prev[i] = 1
                self.a2[i] = 1
            else:
                self.post[i] += 1
                self.prev[i] += 1
                self.a2[i] += 1
        counter = -1
        for input in inputs:
            self.potential += (input - self.potential/RESISTANCE) / CAPACITANCE
            counter = counter + 1
        # If membrane potential reaches threshold, fire!
        print("OUT POTENTIAL: ", self.potential)
        if self.potential > THRESHOLD:
            self.post[counter] = self.potential
            self.updateWeights(inputs)

            print("OUT FIRED")
            self.potential = 0
            return SPIKE_VALUE
        else:
            self.prev[counter] = self.potential


        return 0
    #Used to update the weights of nodes based on prespike timing.
    def updateWeights (self,inputs):
        counter = 0
        gamma = 5
        for input in inputs:
            self.a2[counter] = gamma * (1 - self.weights[counter])
            self.weights[counter] += self.post[counter] * self.prev[counter] * self.a2[counter]
            print("Node ", counter, "Current Weight ", self.weights[counter])
            counter += 1


class HiddenNeuron:
    potential = 0
    weights = []
    name = ""

    def __init__(self, numInputs, newName):
        self.weights = [random.random()]*numInputs
        self.name = newName
        self.post = [random.random()]*numInputs
        self.prev = [random.random()]*numInputs
        self.a2 = [random.random()]*numInputs

    def update(self, inputs):
        for i in range(0, len(inputs)):
            inputs[i] = inputs[i] * self.weights[i]


        for input in inputs:
            self.potential += (input - self.potential/RESISTANCE) / CAPACITANCE
        # If membrane potential reaches threshold, fire!
        # print(self.name, " POTENTIAL: ", self.potential)
        if self.potential > THRESHOLD:
            #print ("Node ",self.name, " fired")
            self.potential = 0
            return SPIKE_VALUE

        return 0

HIDDEN_LAYER_SIZE = 5

outNeuron = LIFNeuron(HIDDEN_LAYER_SIZE, "out")
hiddenLayer = []
for i in range(0, HIDDEN_LAYER_SIZE):
    hiddenLayer.append(HiddenNeuron(2,i))

# x and y are simulated input neurons
def updateNetwork(x, y, hiddenLayer, out):
    spikes = []
    for i in range(0, len(hiddenLayer)):
        spikes.append(hiddenLayer[i].update([x, y]))

    return out.update(spikes)

# consider each iteration of this loop 1 milisecond
failures = 0
for i in range(0, 1000):
    # This will alternate every 100 ms between a "high" signal (1 and 0 alternating) and "low" signal(0s, with 1 every 10 ms)
    x = 1 if (i % (2 if int(i / 100) % 2 == 0 else 10)) == 0 else 0
    y = 1 if (i % (2 if int(i / 100) % 2 == 0 else 10)) == 0 else 0
    updateNetwork(x, y, hiddenLayer, outNeuron)
    if y == 1:
        print ("Fireing")
largest = 0
for i in range(0,len(hiddenLayer)):
    print("Neuron ", i, "Weight with XY ", hiddenLayer[i].weights[0], " ", hiddenLayer[i].weights[1])
    if outNeuron.weights[i] > outNeuron.weights[largest]:
        largest = i
print("OutPut Node had highest weight with Node ", largest, " With weight of ", outNeuron.weights[largest])
