import math
def curves():
    return 0
def easeOutQuint(t):
    return (1- math.pow(1 - t, 5))
def inverseEaseOutQuint(t):
    return (1- math.pow(t, 5))

def easeInQuint(t):
    return (math.pow(t, 5))
def inverseEaseInQuint(t):
    return (math.pow(1-t, 5))