import robot
import terminal_functions
import socket
import sys
import termios
import contextlib
import atexit
import json

def robot_info():
    print("\r\nRobot Kudlaty (2016) oparty o podzespoly\r\n")
    print("- podwozie uniwersalne trzykolowe z dwoma silnikami DC\r\n")
    print("- komputer RaspberryPi 2\r\n")
    print("- modul inercyjny GY-80: ADXL245B, HMC5883L, L3G4200D, BMP085\r\n")
    print("- ultradzwiekowe czujniki odleglosci HC-SR04\r\n")
    print("- dwukanalowy kontroler silnikow DC: DRV8835\r\n")
    print("- czterokanalowy konwerter poziomow logicznych Sparkfun\r\n")
    print("- przetwornica StepUpDown zasilajaca RPI\r\n")
    print("- zasilanie akumulatorowe: 4 x AA NiMh\r\n")


def print_main_menu():
    print("Wybierz:\r\n")
    print("w - omijanie przeszkod Fuzzy\r\n")
    print("h - informacje o robocie\r\n")

TCP_IP = "10.42.0.249"
TCP_PORT = 5006
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

pred_lew = 0
pred_praw = 0

def Wysylanie(conn, robotState):
    global pred_lew
    global pred_praw

    print("Wysylanie() start")

    distLeft = min(int(robotState.distLeft), 40)
    distFront = min(int(robotState.distFront), 40)
    distRight = min(int(robotState.distRight), 40)

    print("Left sensor: " + str(distLeft))
    print("Front sensor: " + str(distFront))
    print("Right sensor: " + str(distRight))

    bytesSent = conn.send(json.dumps([distLeft, distFront, distRight]).encode())

    print(str(bytesSent) + " bytes sent to Matlab")
    rawData = conn.recv(8).decode()
    print("Raw data: " + str(rawData))
    decodedData = json.loads(rawData)
    print("After json.loads: " + str(decodedData))

    pred_lew = decodedData[0]
    pred_praw = decodedData[1]

    print("Lewa: " + str(pred_lew))
    print("Prawa: " + str(pred_praw))

    print("Wysylanie() end")

def main():
    kb = 0
    lastKb = 0

   #  print("Waiting for Matlab to cennect...")
   #  sock.bind((TCP_IP, TCP_PORT))
   #  sock.listen(1)

   #  conn, addr = sock.accept()
   #  print("Matlab connected! Address" + str(addr))

    shaggy = robot.Robot()
    robotState = robot.RobotState()

    shaggy.Cycle()
    shaggy.GetState(robotState)

    atexit.register(terminal_functions.set_normal_term)
    terminal_functions.set_curses_term()

    print_main_menu()

    while kb != 'q':
       shaggy.GetState(robotState)

       if terminal_functions.kbhit():
          kb = terminal_functions.getch()

       lastKb = kb
       if lastKb == 'e':
          print("'e' insertet!")
          Wysylanie(conn, robotState)

          #shaggy.SetWheel(pred_lew,pred_praw)
          shaggy.Cycle()

       if lastKb == 'b':
          #print("Braitenberg")
          shaggy.Braitenberg()
          #shaggy.SetWheel(pred_lew,pred_praw)
          shaggy.Cycle()

       if lastKb == 's':
          print("STOP")
          shaggy.SetWheel(0,0)
          break

    print("QUIT")
    shaggy.Cycle()
    sock.close()

if __name__ == "__main__":
    main()
