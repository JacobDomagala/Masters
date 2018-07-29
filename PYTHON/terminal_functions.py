import termios
import ctypes
import sys

oldt = termios.tcgetattr(sys.stdin.fileno())
newt = termios.tcgetattr(sys.stdin.fileno())

def changemode(dir):
    if dir == 1:
        global oldt
        global newt
        oldt = termios.tcgetattr(sys.stdin.fileno())
        newt = oldt
        newt[3] = newt[3] & ~( termios.ICANON | termios.ECHO )
        termios.tcsetattr( sys.stdin.fileno(), termios.TCSANOW, oldt)
    else:
        termios.tcsetattr( sys.stdin.fileno(), termios.TCSANOW, oldt)

def khbit():
    pass
