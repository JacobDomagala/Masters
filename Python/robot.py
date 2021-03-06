import wiringpi
import connection
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

UPPER_BOUND = 40

class Robot:
    def __init__(self):
        self.m_LeftWheel = 0
        self.m_RightWheel = 0

        self.m_DistLeft = 0.0
        self.m_DistRight = 0.0
        self.m_DistFrontLeft = 0.0
        self.m_DistFrontRight = 0.0
        self.m_DistFront = 0.0

        self.m_TcpClient = connection.TcpClient()

        # Init_RPI
        wiringpi.wiringPiSetup()

        # Init_Motor
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

        # Init_Usonic
        for i in range(len(echo_sensors_pins)):
            wiringpi.pinMode(echo_sensors_pins[i][0], wiringpi.OUTPUT)
            wiringpi.pinMode(echo_sensors_pins[i][1], wiringpi.INPUT)
            wiringpi.digitalWrite(echo_sensors_pins[i][0], wiringpi.LOW)

    def Cycle(self):

        self.SetMove(-self.m_LeftWheel, -self.m_RightWheel, 0)

        self.m_DistFrontLeft = self.UsonicReadCM(
            echo_sensors_pins[0][0], echo_sensors_pins[0][1])

        self.m_DistFrontRight = self.UsonicReadCM(
            echo_sensors_pins[1][0], echo_sensors_pins[1][1])

        self.m_DistRight = self.UsonicReadCM(
            echo_sensors_pins[2][0], echo_sensors_pins[2][1])

        self.m_DistLeft = self.UsonicReadCM(
            echo_sensors_pins[3][0], echo_sensors_pins[3][1])

        self.m_DistFront = self.UsonicReadCM(
            echo_sensors_pins[4][0], echo_sensors_pins[4][1])

    def UsonicReadCM(self, trig, echo):
        wiringpi.digitalWrite(trig, wiringpi.HIGH)
        delayMicroseconds(10)
        wiringpi.digitalWrite(trig, wiringpi.LOW)

        startTime = getTimeInMicros()
        stopTime = getTimeInMicros()
        timer = getTimeInMicros()

        while wiringpi.digitalRead(echo) == wiringpi.LOW:
           startTime = getTimeInMicros()
           if checkForTimeout(timer):
              return 0

        timeout = getTimeInMicros()

        while wiringpi.digitalRead(echo) == wiringpi.HIGH:
           stopTime = getTimeInMicros()
           if checkForTimeout(timer):
              return 0

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

    def Braitenberg(self):
        self.Cycle()

        prox_sensors = [self.m_DistLeft, self.m_DistFrontLeft, self.m_DistFront,
                        self.m_DistFrontRight, self.m_DistRight]

        # normalize and round to 2 digits
        sensors = [round(1-(min(i, 40)/40), 2) for i in prox_sensors]
        wl = [-8, -20, 30, 4, 4]
        wr = [4, 4, -30, -20, -8]
        b = 2
        rightWheel = 0
        leftWheel = 0

        for i in range(len(sensors)):
           leftWheel += wl[i]*sensors[i] + b
           rightWheel += wr[i]*sensors[i] + b

        self.m_LeftWheel = int((clamp(leftWheel, -UPPER_BOUND, UPPER_BOUND)))
        self.m_RightWheel = int((clamp(rightWheel, -UPPER_BOUND, UPPER_BOUND)))
        self.AdjustSpeed()

        print(sensors)
        print([self.m_LeftWheel, self.m_RightWheel])

    def Fuzzy(self):
        self.Cycle()

        sensors = [self.m_DistLeft, min([self.m_DistFrontLeft, self.m_DistFront, self.m_DistFrontRight]), self.m_DistRight]
        intSensors = [int(clamp(i, 10, 40)) for i in sensors]
        bytesSent = self.m_TcpClient.SendData(intSensors)

        print(str(bytesSent) + " bytes sent to Matlab")

        dataReceived = self.m_TcpClient.RecvData()
        
        self.m_LeftWheel = clamp(dataReceived[0], -UPPER_BOUND, UPPER_BOUND)
        self.m_RightWheel = clamp(dataReceived[1], -UPPER_BOUND, UPPER_BOUND)

        print(intSensors)
        print([self.m_LeftWheel, self.m_RightWheel])

    def ConnectTo(self, IP, Port):
        self.m_TcpClient((IP,Port))

    def ShutDown(self):
        self.SetMove(0, 0, 0)
        self.m_TcpClient.Disconnect()

    def AdjustSpeed(self):
       if self.m_LeftWheel > 0 and self.m_LeftWheel < 40:
          self.m_LeftWheel = 40
       if self.m_RightWheel > 0 and self.m_RightWheel < 40:
          self.m_RightWheel = 40

       if self.m_LeftWheel < 0 and self.m_LeftWheel > -40:
          self.m_LeftWheel = -40
       if self.m_RightWheel < 0 and self.m_RightWheel > -40:
          self.m_RightWheel = -40