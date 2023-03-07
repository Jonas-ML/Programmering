import RPI.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
chan_list = [16,20,26,21]
GPIO.setup(chan_list, GPIO.OUT)

#PWM opsætning
motor1 = GPIO.PWM(16, 100)
motor2 = GPIO.PWM(20, 100)
motor3 = GPIO.PWM(21, 100)
motor4 = GPIO.PWM(26, 100)
a = 100
b = 80
c = 50
stop = 0

def forwards():
	motor1.ChangeDutyCycle(a)
	motor2.ChangeDutyCycle(stop)
	motor3.ChangeDutyCycle(a)
	motor4.ChangeDutyCycle(stop)

def backwards():
	motor1.ChangeDutyCycle(stop)
	motor2.ChangeDutyCycle(a)
	motor3.ChangeDutyCycle(stop)
	motor4.ChangeDutyCycle(a)
def left():
	motor1.ChangeDutyCycle(30)
	motor2.ChangeDutyCycle(stop)
	motor3.ChangeDutyCycle(a)
	motor4.ChangeDutyCycle(stop)
def right():
	motor1.ChangeDutyCycle(a)
	motor2.ChangeDutyCycle(stop)
	motor3.ChangeDutyCycle(30)
	motor4.ChangeDutyCycle(stop)

def halt():
	motor1.ChangeDutyCycle(stop)
	motor2.ChangeDutyCycle(stop)
	motor3.ChangeDutyCycle(stop)
	motor4.ChangeDutyCycle(stop)

def cutl():
	motor1.ChangeDutyCycle(b)

def cutr():
	motor3.ChangeDutyCycle(b)




