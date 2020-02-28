import time
import random
import matplotlib.pyplot as plt


# Constants
CAPACITANCE = 10
RESISTANCE = 25
THRESHOLD = 2

A = 0.02
B = 0.02
C = -65 #mV
D = 2

# Transient variables
potential = 0
recovery = 0
n = 0
m = 0
h = 0

def LIF(input, potential, output):
    # LIF formula
    potential += (input - potential/RESISTANCE) / CAPACITANCE

    # If membrane potential reaches threshold, fire!
    if potential > THRESHOLD:
        potential = 0

    output[0].append(potential)
    return potential

def izhikevich(input, potential, recovery, output):
    # Izhikevich formula
    v = potential
    potential += 0.04 * v ** 2 + 5 * v + 140 - recovery + input
    recovery += A * (B * v - recovery)

    # When the voltage reaches the threshold,
    # reset potential to C and adjust recovery by D
    if potential > 30: #mV
        potential = C
        recovery += D

    output[0].append(potential)
    output[1].append(recovery)
    return potential, recovery

def hodgkin_huxley(input, potential, n, m, h, output):
    potential += 0
    n += 0
    m += 0
    h += 0

    output[0].append(potential)
    output[1].append(n)
    output[2].append(m)
    output[3].append(h)

    return potential, n, m, h

# Input structured by (x, y), where
# At time x, change to input probability y
input = [
    (0, 0),
    (50, 1),
    (100, 0),
    (150, 1),
    (200, 0)
]
output = [[], [], [], []]

tick = 0
while len(input) > 1:
    # Handle timed input system
    if tick >= input[1][0]:
        input.pop(0)
    tick += 1

    i = 111 if random.random() < input[0][1] else 0

    # potential = LIF(i, potential, output)
    # potential, recovery = izhikevich(i, potential, recovery, output)
    potential, n, m, h = hodgkin_huxley(i, potential, n, m, h, output)

plt.plot(output[0], label="potential")
plt.plot(output[1], label="recovery")
plt.plot(output[2])
plt.plot(output[3])
plt.legend()
plt.show()
