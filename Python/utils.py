import time

def clamp(val, low, high):
    return min(max(val, low), high)

def millis():
    return int(round(time.time() * 1000))

def micros():
    return int(round(time.time() * 1000000))