import robot
import terminal_functions

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
    print("Wybierz:\n")
    print("c - podlacz Raspberry z Matlabem\n")
    print("f - omijanie przeszkod Fuzzy\n")
    print("b - omijanie przeszkod Braitenberg\n")
    print("s - wyjdz\n")

def main():
    key = 0
    lastKey = 0

    shaggy = robot.Robot()
    terminal_functions.init()
    print_main_menu()

    while key != 'q':
       if terminal_functions.kbhit():
          key = terminal_functions.getch()

       lastKey = key
       if lastKey == 'c':
          shaggy.ConnectTo(("10.42.0.249", 5006))

       if lastKey == 'f':
          shaggy.Fuzzy()

       if lastKey == 'b':
          shaggy.Braitenberg()

       if lastKey == 's':
          shaggy.Stop()
          break

    print("QUIT")

if __name__ == "__main__":
    main()
