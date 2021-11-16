import MPU6050
import time
import RPi.GPIO as GPIO

from datetime import datetime
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
buzzerPin = 32 # define buzzerPin


mpu = MPU6050.MPU6050()     # instantiate a MPU6050 class object
accel = [0]*3               # define an arry to store accelerometer data
#gyro = [0]*3                # define an arry to store gyroscope data
def setup():
    mpu.dmp_initialize()    # initialize MPU6050
    GPIO.setmode(GPIO.BOARD) # use PHYSICAL GPIO Numbering
    GPIO.setup(buzzerPin, GPIO.OUT) # set buzzerPin to OUTPUT mode

def loop():
    while(True):
        accel = mpu.get_acceleration()      # get accelerometer data
#        gyro = mpu.get_rotation()           # get gyroscope data
        GPIO.output(buzzerPin,GPIO.LOW)
        print("%.2f g\t%.2f g\t%.2f g\t"%(accel[0]/16384.0,accel[1]/16384.0,accel[2]/16384.0))

        if (accel[1]/16384.0)>0.8 :

            f = open("logfile.txt", "a")
            f.write("tiled left time = {}\n".format(current_time))
            f.close()
            
            print("tilted left")
            GPIO.output(buzzerPin,GPIO.HIGH) # turn on buzzer

        if (accel[1]/16384.0)<-0.8 :

            f = open("logfile.txt", "a")
            f.write("tiled right time = {}\n".format(current_time))
            f.close()

            print("tilted right")
            GPIO.output(buzzerPin,GPIO.HIGH) # turn on buzzer

        if abs(accel[0]/16384.0)>1 :
            
            f = open("logfile.txt", "a")
            f.write("hit time = {}\n".format(current_time))
            f.close()

            print("hit")
            GPIO.output(buzzerPin,GPIO.HIGH) # turn on buzzer


        time.sleep(0.2)

if __name__ == '__main__':     # Program entrance
    print("Program is starting ... ")
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        pass