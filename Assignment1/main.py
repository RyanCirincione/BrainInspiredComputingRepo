import time
import random
import math
import matplotlib.pyplot as plt


# Constants
CAPACITANCE = 8
RESISTANCE = 2
THRESHOLD = 5
RESET = 0

VoltageNa = -115
VoltageK = 12
VoltageL = -10.613

maximumConductanceOfNa = 120
maximumConductanceOfK = 36
maximumConductanceOfL = 0.3

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
    spike = 0

    # If membrane potential reaches threshold, fire!
    if potential > THRESHOLD:
        spike = 1
        potential = RESET

    output[0].append(potential)
    return potential, spike

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
    v = potential

    alpha_n = 0.01 * ((10 + v) / (math.exp((10 + v) / 10) - 1))
    beta_n = 0.125 * math.exp(v / 80)

    alpha_m = 0.1 * ((25 + v) / (math.exp((25 + v) / 10) - 1))
    beta_m = 4 * math.exp(v / 18)

    alpha_h = 0.07 * math.exp(v / 20)
    beta_h = 1 / (math.exp((30 + v) / 10) + 1)

    n = alpha_n / (alpha_n + beta_n)
    m = alpha_m / (alpha_m + beta_m)
    h = alpha_h / (alpha_h + beta_h)

    ionConductanceOfNa = maximumConductanceOfNa * m * h
    ionConductanceOfK = maximumConductanceOfK * m
    ionConductanceOfL = maximumConductanceOfL

    sodium = ionConductanceOfNa * (m**3) * h * (v - VoltageNa)
    potassium = ionConductanceOfK * (n**4) * (v - VoltageK)
    leaky = ionConductanceOfL * (v - VoltageL)

    potential += (input - sodium - potassium - leaky) / CAPACITANCE
    n += 0.01 * (alpha_n * (1-n) - beta_n * n)
    m += 0.01 * (alpha_m * (1-m) - beta_m * m)
    h += 0.01 * (alpha_h * (1-h) - beta_h * h)

    output[0].append(potential)
    # potential = 0
    if potential > 1:
        potential = -7
    output[1].append(n)
    output[2].append(m)
    output[3].append(h)

    return potential, n, m, h

# Input structured by (x, y), where
# At time x, change to input probability y
input = [
    (0, 0),
    (250, 1),
    (500, 0),
    (750, 1),
    (1000, 0)
]
output = [[], [], [], []]
spikeGraph = []

tick = 0
spikes = 0
while len(input) > 1:
    # Handle timed input system
    if tick >= input[1][0]:
        input.pop(0)
        # spikeGraph.append(spikes)
        # spikes = 0
    tick += 1


    i = 5 if random.random() < input[0][1] else 0
    # i = input[0][1]

    # potential, s = LIF(i, potential, output)
    # potential, recovery = izhikevich(i, potential, recovery, output)
    potential, n, m, h = hodgkin_huxley(i, potential, n, m, h, output)

    # spikes += s

# plt.plot([0,1,2,3,4,5,6,7,8,9,10,11], spikeGraph)
plt.plot(output[0], label="potential")
plt.plot(output[1], label="n")
plt.plot(output[2], label="m")
plt.plot(output[3], label="h")
plt.xlabel("time")
# plt.ylabel("spikes per 50 ms")
# plt.xlabel("input")
plt.legend()
plt.show()
