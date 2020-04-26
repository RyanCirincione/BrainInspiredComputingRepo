CAPACITANCE = 2
RESISTANCE = 2
THRESHOLD = 15

class LIFNeuron:
    potential = 0

    def update(self, input):
        potential += (input - potential/RESISTANCE) / CAPACITANCE
        # If membrane potential reaches threshold, fire!
        if potential > THRESHOLD:
            potential = 0

HIDDEN_LAYER_SIZE = 5

x = LIFNeuron()
y = LIFNeuron()
out = LIFNeuron()
hiddenLayer = []
for i in range(0, HIDDEN_LAYER_SIZE):
    hiddenLayer.append(LIFNeuron())
