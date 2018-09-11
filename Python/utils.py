import time

def clamp(val, low, high):
    return min(max(val, low), high)

def getTimeInMicros():
    return int(round(time.time() * 1000000))

def delayMicroseconds(seconds):
    time.sleep(seconds/1000000)

def checkForTimeout(timeStarted, timeoutInMicros = 1000000):
    if (getTimeInMicros() - timeStarted) >= timeoutInSeconds:
        print("TIMEOUT!")
        return True
    else:
        return False