import wiringpi
import time

def clamp(val, low, high):
   return min(max(val, low), high)

def millis():
   return int(round(time.time() * 1000))

def micros():
   return int(round(time.time() * 1000000))


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


class RobotState:
    def __init__(self):
        # acceletations in 3 dimensions xyz [m/s2]
        self.ax = 0.0
        self.ay = 0.0
        self.az = 0.0

        # flat orientation angle 0 - 360 deg [degreese]
        self.angle = 0.0

        # distances from Ultra Sonic sensors, [cm]
        self.distLeft = 0.0
        self.distRight = 0.0
        self.distFrontLeft = 0.0
        self.distFrontRight = 0.0
        self.distFront = 0.0

        # PWM power set to wheels, 0 - 100 [%]
        self.wheelRightPWM = 0
        self.wheelLeftPWM = 0

        # real cycle time [ms]
        self.cycleMillis = 0

        # cycle number
        self.cycleNumber = 0

        # timestamp in microseconds, approximately wrap after 71 minutes [us]
        self.microsTimestamp = 0

        # timestamp in milliseconds, wrap after 49 days [ms]
        self.millisTimestamp = 0

        # system timestamp in seconds [s]
        self.sysTimestamp = 0


class Robot:
    def __init__(self):
        self.m_LogFilename = ""
        self.m_LogStream = ""
        self.m_LeftWheel = 0
        self.m_RightWheel = 0
        self.m_CycleMillis = 0

        self.m_DistLeft = 0.0
        self.m_DistRight = 0.0
        self.m_DistFrontLeft = 0.0
        self.m_DistFrontRight = 0.0
        self.m_DistFront = 0.0

        self.m_AccelX = 0.0
        self.m_AccelY = 0.0
        self.m_AccelZ = 0.0
        self.m_Angle = 0.0
        self.m_SilenceInit = True
        self.m_CycleNumber = 0

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

    def SetWheel(self, left, right):
        self.m_LeftWheel = left
        self.m_RightWheel = right

    def Cycle(self):
        self.m_CycleNumber += 1

        self.SetMove(self.m_LeftWheel, self.m_RightWheel, 0)

        # prosto lewy
        # self.m_DistFront
        self.m_DistFrontLeft = self.UsonicReadCM(
            echo_sensors_pins[0][0], echo_sensors_pins[0][1]) + 7.7

        # teraz to jest prawy
        # self.m_DistLeft
        self.m_DistRight = self.UsonicReadCM(
            echo_sensors_pins[2][0], echo_sensors_pins[2][1]) + 5.75

        # prosto prawy
        # self.m_DistBack
        self.m_DistFrontRight = self.UsonicReadCM(
            echo_sensors_pins[1][0], echo_sensors_pins[1][1]) + 7.7

        # terato to jest lewy
        # self.m_DistRight
        self.m_DistLeft = self.UsonicReadCM(
            echo_sensors_pins[3][0], echo_sensors_pins[3][1]) + 5.75

        self.m_DistFront = self.UsonicReadCM(
            echo_sensors_pins[4][0], echo_sensors_pins[4][1]) + 8

        self.m_CycleMillis = millis

    def delayMicroseconds(self, seconds):
        time.sleep(seconds/1000000)

    def UsonicReadCM(self, trig, echo):
        wiringpi.digitalWrite(trig, wiringpi.HIGH)
        self.delayMicroseconds(10)
        wiringpi.digitalWrite(trig, wiringpi.LOW)
        self.delayMicroseconds(240)

        timeout = micros()
        tim = 0

        while wiringpi.digitalRead(echo) == wiringpi.LOW and not tim:
            tim = self.CheckTimeout(timeout, 3000)

        if tim:
            self.delayMicroseconds(100)
            return 0

        startTime = micros()
        tim = 0

        self.delayMicroseconds(60)

        while wiringpi.digitalRead(echo) == wiringpi.HIGH and not tim:
            tim = self.CheckTimeout(startTime, 7000)

        if tim:
            self.delayMicroseconds(10)
            return 120

        travelTime = micros() - startTime

        distance = travelTime / 58.0

        self.delayMicroseconds(10)

        return distance

    def GetState(self, state):
        state.ax = self.m_AccelX
        state.ay = self.m_AccelY
        state.angle = self.m_Angle

        state.distLeft = self.m_DistLeft
        state.distRight = self.m_DistRight
        state.distFrontLeft = self.m_DistFrontLeft
        state.distFrontRight = self.m_DistFrontRight
        state.distFront = self.m_DistFront

        state.cycleMillis = self.m_CycleMillis
        state.wheelLeftPWM = self.m_LeftWheel
        state.wheelRightPWM = self.m_RightWheel
        state.cycleNumber = self.m_CycleNumber
        state.microsTimestamp = micros()
        state.millisTimestamp = millis()
        state.sysTimestamp = time.time()

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
        #         left    front-left, front, front-right, right

        self.Cycle()

        prox_sensors = [self.m_DistLeft, self.m_DistFrontLeft,
                        self.m_DistFront, self.m_DistFrontRight, self.m_DistRight]

        sensors = [min(i, 40)/40 for i in prox_sensors]
        wl = [4, 4, -15, -4, -4]
        wr = [-5, -15, -15, 15, 5]

        b = 4
        rightWheel = 0
        leftWheel = 0

        for i in range(len(prox_sensors)):
            leftWheel += wl[i]*sensors[i] + b
            rightWheel += wr[i]*sensors[i] + b

        leftWheel = clamp(leftWheel, -40, 40)
        rightWheel = clamp(rightWheel, -40, 40)

        print(sensors)
        print([leftWheel, rightWheel])
