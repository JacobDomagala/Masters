import wiringpi
import socket
import json
from utils import *

BIN2 = 0
BIN1 = 1
AIN2 = 3
AIN1 = 4
MOTOR_MODE = 2

BENBL = BIN2
BPHASE = BIN1
AENBL = AIN2
APHASE = AIN1

GY80_AINT_1 = 5
GY80_M_DRDY = 7

echo_sensors_pins = [[21, 22], [26, 23], [27, 24], [28, 29], [11, 25]]

UPPER_BOUND = 50

class Robot:
    def __init__(self):
        self.m_LeftWheel = 0
        self.m_RightWheel = 0
        self.m_CycleMillis = 0

        self.m_DistLeft = 0.0
        self.m_DistRight = 0.0
        self.m_DistFrontLeft = 0.0
        self.m_DistFrontRight = 0.0
        self.m_DistFront = 0.0

        self.m_CycleNumber = 0

        socket.setdefaulttimeout(1.0)
        self.m_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.m_Conn = 0
        self.m_Addr = 0
        self.bound = False

        # Init_RPI()
        wiringpi.wiringPiSetup()

        # Init_Motor()
        wiringpi.pinMode(BIN2, wiringpi.OUTPUT)
        wiringpi.pinMode(BIN1, wiringpi.OUTPUT)
        wiringpi.pinMode(AIN2, wiringpi.OUTPUT)
        wiringpi.pinMode(AIN1, wiringpi.OUTPUT)
        wiringpi.pinMode(MOTOR_MODE, wiringpi.OUTPUT)
        wiringpi.digitalWrite(MOTOR_MODE, wiringpi.HIGH)

        wiringpi.softPwmCreate(AENBL, 0, 100)
        wiringpi.softPwmCreate(BENBL, 0, 100)
        wiringpi.softPwmWrite(AENBL, 0)
        wiringpi.softPwmWrite(BENBL, 0)

        wiringpi.pinMode(GY80_AINT_1, wiringpi.INPUT)
        wiringpi.pinMode(GY80_M_DRDY, wiringpi.INPUT)

        # Init_Usonic()
        for i in range(len(echo_sensors_pins)):
            wiringpi.pinMode(echo_sensors_pins[i][0], wiringpi.OUTPUT)
            wiringpi.pinMode(echo_sensors_pins[i][1], wiringpi.INPUT)
            wiringpi.digitalWrite(echo_sensors_pins[i][0], wiringpi.LOW)

    def Cycle(self):
        self.m_CycleNumber += 1

        #self.SetMove(self.m_LeftWheel, self.m_RightWheel, 0)

      #   self.m_DistFrontLeft = int(min(self.UsonicReadCM(
      #       echo_sensors_pins[0][0], echo_sensors_pins[0][1]) + 7.7, UPPER_BOUND))

      #   self.m_DistRight = int(min(self.UsonicReadCM(
      #       echo_sensors_pins[2][0], echo_sensors_pins[2][1]) + 5.75, UPPER_BOUND))

      #   self.m_DistFrontRight = int(min(self.UsonicReadCM(
      #       echo_sensors_pins[1][0], echo_sensors_pins[1][1]) + 7.7, UPPER_BOUND))

      #   self.m_DistLeft = int(min(self.UsonicReadCM(
      #       echo_sensors_pins[3][0], echo_sensors_pins[3][1]) + 5.75, UPPER_BOUND))

      #   self.m_DistFront = int(min(self.UsonicReadCM(
      #       echo_sensors_pins[4][0], echo_sensors_pins[4][1]) + 8, UPPER_BOUND))

        self.m_DistFrontLeft = self.UsonicReadCM(
            echo_sensors_pins[0][0], echo_sensors_pins[0][1])

        self.m_DistRight = self.UsonicReadCM(
            echo_sensors_pins[2][0], echo_sensors_pins[2][1])

        self.m_DistFrontRight = self.UsonicReadCM(
            echo_sensors_pins[1][0], echo_sensors_pins[1][1])

        self.m_DistLeft = self.UsonicReadCM(
            echo_sensors_pins[3][0], echo_sensors_pins[3][1])

        self.m_DistFront = self.UsonicReadCM(
            echo_sensors_pins[4][0], echo_sensors_pins[4][1])

        self.m_CycleMillis = millis

    def delayMicroseconds(self, seconds):
        time.sleep(seconds/1000000)

    def UsonicReadCM(self, trig, echo):
        wiringpi.digitalWrite(trig, wiringpi.HIGH)
        self.delayMicroseconds(10)
        wiringpi.digitalWrite(trig, wiringpi.LOW)

        startTime = micros()
        stopTime = micros()

        while wiringpi.digitalRead(echo) == wiringpi.LOW:
           startTime = micros()

        while wiringpi.digitalRead(echo) == wiringpi.HIGH:
           stopTime = micros()

        travelTime = stopTime - startTime

        # divide by 58.0 to get centimeters
        return travelTime / 58.0        

    def SetMove(self, l, r, save_direction):
        wiringpi.softPwmWrite(AENBL, abs(l))
        wiringpi.softPwmWrite(BENBL, abs(r))
        lphase = 0
        rphase = 0
        if not save_direction:
            if l >= 0:
                lphase = 0
            else:
                lphase = 1
            if r >= 0:
                rphase = 0
            else:
                rphase = 1

        wiringpi.digitalWrite(APHASE, lphase)
        wiringpi.digitalWrite(BPHASE, rphase)

    def CheckTimeout(self, start_us, timeout_us):
        res = 0
        curr_us = micros()
        if curr_us <= start_us:
            if curr_us + 0xFFFFFFFF - start_us >= timeout_us:
                res = 1
            else:
                res = 0
        else:
            if curr_us - start_us >= timeout_us:
                res = 1
            else:
                res = 0

        return res

    def Braitenberg(self):
        self.Cycle()

        prox_sensors = [self.m_DistLeft, self.m_DistFrontLeft,
                        self.m_DistFront, self.m_DistFrontRight, self.m_DistRight]

        sensors = [1-(min(i, 40)/40) for i in prox_sensors]
        wl = [8, 10, 50, -30, -9]
        wr = [-9, -30, -50, 10, 8]
        b = 4
        rightWheel = 0
        leftWheel = 0

        for i in range(len(sensors)):
            leftWheel += wl[i]*sensors[i] + b
            rightWheel += wr[i]*sensors[i] + b

        self.m_LeftWheel = int(-(clamp(10*leftWheel, -UPPER_BOUND, UPPER_BOUND)))
        self.m_RightWheel = int(-(clamp(10*rightWheel, -UPPER_BOUND, UPPER_BOUND)))
        self.AdjustSpeed()

        print(sensors)
        print([self.m_LeftWheel, self.m_RightWheel])

    def Fuzzy(self):
        self.Cycle()

        sensors = [self.m_DistLeft, min(min(self.m_DistFrontLeft, self.m_DistFront), self.m_DistFrontRight), self.m_DistRight]
        intSensors = [int(clamp(i, 10, 40)) for i in sensors]
        bytesSent = self.m_Conn.send(json.dumps(intSensors).encode())

        print(json.dumps(intSensors))
        print(str(bytesSent) + " bytes sent to Matlab")

        rawData = self.m_Conn.recv(20).decode()

        if len(rawData) == 0:
            self.m_LeftWheel = 0 
            self.m_RightWheel = 0
        else:     
            #print("Raw data: " + str(rawData))
            decodedData = json.loads(rawData)
            #print("After json.loads: " + str(decodedData))

            self.m_LeftWheel = -(clamp(decodedData[0], -UPPER_BOUND, UPPER_BOUND))
            self.m_RightWheel = -(clamp(decodedData[1], -UPPER_BOUND, UPPER_BOUND))

        print(intSensors)
        print([self.m_LeftWheel, self.m_RightWheel])

    def ConnectTo(self, IP, Port):
        if not self.bound:
            print("Waiting for Matlab to cennect...")
            self.m_Socket.bind((IP, Port))
            self.m_Socket.listen(1)

            self.m_Conn, self.m_Addr = self.m_Socket.accept()
            print("Matlab connected! Address" + str(self.m_Addr))
            self.bound = True

    def Stop(self):
        self.SetMove(0, 0, 0)
        self.m_Socket.close()

    def AdjustSpeed(self):
       if self.m_LeftWheel > 0 and self.m_LeftWheel < 40:
          self.m_LeftWheel = 40
       if self.m_RightWheel > 0 and self.m_RightWheel < 40:
          self.m_RightWheel = 40

       if self.m_LeftWheel < 0 and self.m_LeftWheel > -40:
          self.m_LeftWheel = -40
       if self.m_RightWheel < 0 and self.m_RightWheel > -40:
          self.m_RightWheel = -40