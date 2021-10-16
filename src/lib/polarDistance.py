import math

def polarDistance(r1, theta1, r2, theta2):
    distance = math.sqrt(r1**2 + r2**2 - 2 * r1 * r2 * math.cos(math.radians(theta1 - theta2)))
    return distance