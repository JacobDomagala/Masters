import robot
import terminal_functions
import time

def print_main_menu():
    print("Wybierz:")
    print("c - podlacz Raspberry z Matlabem")
    print("f - omijanie przeszkod Fuzzy")
    print("b - omijanie przeszkod Braitenberg")
    print("s - wyjdz")

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
          shaggy.ConnectTo("10.42.0.249", 5006)

       if lastKey == 'f':
          shaggy.Fuzzy()

       if lastKey == 'b':
          shaggy.Braitenberg()

       if lastKey == 's':
          shaggy.Stop()
          break

       #time.sleep(0.05)

    print("QUIT")

if __name__ == "__main__":
    main()
