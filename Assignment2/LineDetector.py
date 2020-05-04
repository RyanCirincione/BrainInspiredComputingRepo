import math

def createLine(degrees):
    angle = degrees * math.pi / 180
    matrix = []
    for i in range(11):
        matrix.append([0] * 11)
    x = 0.0
    y = 0.0

    while x < 6 and y < 6 and x > -6 and y > -6:
        matrix[5 + int(y)][5 + int(x)] = 1
        matrix[5 - int(y)][5 - int(x)] = 1
        x += math.cos(angle)
        y += math.sin(angle)

    return matrix
