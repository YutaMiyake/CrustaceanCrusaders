#Yuta Miyake

def clamp(val, min, max):
    if val <= min:
        return min
    elif val >= max:
        return max

    return val

import math

twopi  = 2.0 * math.pi
pi     = math.pi
halfpi = math.pi/2.0

def fixAngle(angle):
    while angle > pi:
        angle -= twopi
    while angle < -pi:
        angle += twopi

    return angle

def diffAngle(angle1, angle2):
    return fixAngle(angle1 - angle2)

