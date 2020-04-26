CAPACITANCE = 2
RESISTANCE = 2
THRESHOLD = 15
SPIKE_VALUE = 1

class LIFNeuron:
    potential = 0
    weights = []

    def __init__(self, numInputs):
        self.weights = [0.5] * numInputs # TODO: change 0.5 to be random, otherwise network is symmetric

    def update(self, inputs):
        for i in range(0, len(inputs)):
            inputs[i] = inputs[i] * self.weights[i]

        for input in inputs:
            potential += (input - potential/RESISTANCE) / CAPACITANCE
        # If membrane potential reaches threshold, fire!
        if potential > THRESHOLD:
            return SPIKE_VALUE
            potential = 0

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

    outNeuron.update(spikes)
