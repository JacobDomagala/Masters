import DB
import robot
import terminal_functions
import socket

robotState = robot.RobotState()
robot = robot.Robot()

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
    print("m - sterowanie reczne\r\n")
    print("t - wczytaj trajektorie z pliku\r\n")
    print("e - tryb ucieczki od przeszkody\r\n")
    print("k - kalibracja magnetometru (kompasu)\r\n")
    print("w - regulacja kata\r\n")
    print("o - regulacja odleglosci\r\n")
    print("d - kat i odleglosc\r\n")
    print("? - informacje o robocie\r\n")


mtmState = 0
mtmCount = 0


def MakeTerrainMap(robot, state, db):
    if mtmState == 1:
        db.clearTerrainMap()
        mtmState = 2
    elif mtmState == 2:
        robot.SetWheel(-33, 33)
        mtmCount += 1
        if mtmCount > 400:
            mtmState = 0
            mtmCount = 0
            robot.SetWheel(0, 0)
        db.WriteStateAsMap(state)
    elif mtmState == 0:
        pass
    else:
        mtmState = 0


def ProcessCommand(cmd, robot, state, db):
    if cmd == "mm":
        mtmState = 1
    elif cmd == "cm":
        db.clearTerrainMap()
    MakeTerrainMap(robot, state, db)


def Rozmywanie(a, b, c, z):
    parametr1 = (z-a)/(b-a)
    parametr2 = (c-z)/(c-b)
    return min(parametr1, parametr2)


def Dopasowanie(x):
    wynsm = rozmywanie(1, 2, 35, x)
    wynbi = rozmywanie(2, 35, 36, x)
    return wynsm < wynbi


cz_l = 0.0
cz_p = 0.0
cz_s = 0.0

cz_l_pop = 0.0
cz_p_pop = 0.0
cz_s_pop = 0.0

cz_l_akt = 0.0
cz_p_akt = 0.0
cz_s_akt = 0.0

a = 0.2

lewa = 0
srodek = 0
prawa = 0
lewa_p = 0
prawa_p = 0
lewa_predkosc = 0
prawa_predkosc = 0


def sterowanie():
    cz_l = robotState.distLeft
    cz_s = robotState.distFront
    cz_p = robotState.distRight

    if cz_l > 35:
        cz_l = 35
    if cz_s > 35:
        cz_s = 35
    if cz_p > 35:
        cz_p = 35

    if cz_l < 2:
        cz_l = 2
    if cz_s < 2:
        cz_s = 2
    if cz_p < 2:
        cz_p = 2

    cz_l_akt = cz_l * a + (cz_l_pop*(1-a))
    cz_s_akt = cz_s * a + (cz_s_pop*(1-a))
    cz_p_akt = cz_p * a + (cz_p_pop*(1-a))

    print("Lewa: %f Srodek: %f Prawa: %f\n\n", cz_l_akt, cz_s_akt, cz_p_akt)

    lewa = dopasowanie(cz_l_akt)
    srodek = dopasowanie(cz_s_akt)
    prawa = dopasowanie(cz_p_akt)

    if lewa == 0 and srodek == 0 and prawa == 0:
        lewa_predkosc = 40
        prawa_predkosc = 40
        if lewa_p != lewa_predkosc or prawa_p != prawa_predkosc:
            robot.SetWheel(40, 40)
    if lewa == 0 and srodek == 0 and prawa == 1:
        lewa_predkosc = -40
        prawa_predkosc = 40
        if lewa_p != lewa_predkosc or prawa_p != prawa_predkosc:
            robot.SetWheel(-40, 40)
    if lewa == 0 and srodek == 1 and prawa == 0:
        lewa_predkosc = -40
        prawa_predkosc = 40
        if lewa_p != lewa_predkosc or prawa_p != prawa_predkosc:
            robot.SetWheel(-40, 40)
    if lewa == 0 and srodek == 1 and prawa == 1:
        lewa_predkosc = -40
        prawa_predkosc = 40
        if lewa_p != lewa_predkosc or prawa_p != prawa_predkosc:
            robot.SetWheel(-40, 40)
    if lewa == 1 and srodek == 0 and prawa == 0:
        lewa_predkosc = 40
        prawa_predkosc = -40
        if lewa_p != lewa_predkosc or prawa_p != prawa_predkosc:
            robot.SetWheel(40, -40)
    if lewa == 1 and srodek == 0 and prawa == 1:
        lewa_predkosc = 40
        prawa_predkosc = 40
        if lewa_p != lewa_predkosc or prawa_p != prawa_predkosc:
            robot.SetWheel(40, 40)
    if lewa == 1 and srodek == 1 and prawa == 0:
        lewa_predkosc = 40
        prawa_predkosc = -40
        if lewa_p != lewa_predkosc or prawa_p != prawa_predkosc:
            robot.SetWheel(40, -40)
    if lewa == 1 and srodek == 1 and prawa == 1:
        lewa_predkosc = -40
        prawa_predkosc = 40
        if lewa_p != lewa_predkosc or prawa_p != prawa_predkosc:
            robot.SetWheel(-40, 40)

    lewa_p = lewa_predkosc
    prawa_p = prawa_predkosc
    cz_l_pop = cz_l_akt
    cz_s_pop = cz_s_akt
    cz_p_pop = cz_p_akt


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_odb = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip_odb = "10.10.20.82"
port_odb = 4012


def Wysylanie():
    dataSize = 4

    liczba = robotState.distLeft
    liczba1 = robotState.distFront
    liczba2 = robotState.distRight

    if liczba > 40:
        liczba = 40
    if liczba1 > 40:
        liczba1 = 40
    if liczba2 > 40:
        liczba2 = 40

    data = "%.0f" % liczba
    data1 = "%.0f" % liczba1
    data2 = "%.0f" % liczba2

    print("lewy: " + data)
    print("srodek: " + data1)
    print("prawy: " + data2)

    ipAddress = "10.10.20.82"

    port1 = 3533
    port2 = 3534
    port3 = 3535

    try:
        sock.sendto(data.encode(), (ipAddress, port1))
        sock.sendto(data.encode(), (ipAddress, port2))
        sock.sendto(data.encode(), (ipAddress, port3))
    except:
        print("nie mozna wysylac danych")
        exit()


pred_lew = 0
pred_praw = 0


def Odbieranie():
    dataSize = 4
    data = ""
    senderport_odb = 3536

    for i in range(2):
        try:
            data, server = sock_odb.recvfrom(dataSize)
        except Exception as e:
            print(e)
            exit()

        print("Data: " + data)

        sum = int(data)

        print("Predkosc: " + sum)

        if sum >= 40:
            sum = 40
        if sum <= -40:
            sum = -40

        if i == 0:
            pred_lew = sum
        if i == 1:
            pred_praw = sum

    print("Lewa: " + pred_lew)
    print("Prawa: " + pred_praw)


def main():
    # changemode(1) // zmiana trybu terminala na nieblokujacy

    priority = 70
    kb = 0
    lastKb = 0

    sock_odb.bind((ip_odb, port_odb))

    #robot.Cycle()
    #robot.GetState(robotState)
    while 1:
       robot.SetMove(20,20, True)
   #  while kb != 'q':
   #     robot.GetState(robotState)

   #     if kbhit():
   #        kb = input()

   #     lastKb = kb
   #     if lastKb == 'w':
   #        Wysylanie()
   #        Odbieranie()

   #        robot.SetWheel(pred_lew,pred_praw)

   #        break

   #     if lastKb == 's':
   #        robot.SetWheel(0,0)
   #        break

    #robot.Cycle()
    #robot.StopLog()

if __name__ == "__main__":
    main()
