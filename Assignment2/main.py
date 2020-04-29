CAPACITANCE = 1
RESISTANCE = 1
THRESHOLD = 2
SPIKE_VALUE = 1

class LIFNeuron:
    potential = 0
    weights = []

    def __init__(self, numInputs):
        self.weights = [5] * numInputs # TODO: change 0.5 to be random, otherwise network is symmetric

    def update(self, inputs):
        for i in range(0, len(inputs)):
            inputs[i] = inputs[i] * self.weights[i]

        for input in inputs:
            self.potential += (input - self.potential/RESISTANCE) / CAPACITANCE
        # If membrane potential reaches threshold, fire!
        if self.potential > THRESHOLD:
            return SPIKE_VALUE
            self.potential = 0

        return 0

HIDDEN_LAYER_SIZE = 5

outNeuron = LIFNeuron(HIDDEN_LAYER_SIZE)
hiddenLayer = []
for i in range(0, HIDDEN_LAYER_SIZE):
    hiddenLayer.append(LIFNeuron(2))

# x and y are simulated input neurons
def updateNetwork(x, y, hiddenLayer, out):
    spikes = []
    for i in range(0, len(hiddenLayer)):
        spikes.append(hiddenLayer[i].update([x, y]))

    return out.update(spikes)

# consider each iteration of this loop 1 milisecond
for i in range(0, 1000):
    # This will alternate every 100 ms between a "high" signal (1 and 0 alternating) and "low" signal(0s, with 1 every 10 ms)
    x = 1 if (i % (2 if int(i / 100) % 2 == 0 else 10)) == 0 else 0
    y = 1 if (i % (2 if int(i / 100) % 2 == 0 else 10)) == 0 else 0

    print(updateNetwork(x, y, hiddenLayer, outNeuron))
