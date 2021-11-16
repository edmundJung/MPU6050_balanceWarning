import MPU6050
import time
import RPi.GPIO as GPIO
#import urllib.request
from urllib.request import urlopen

from datetime import datetime
now = datetime.now()

current_time = now.strftime("%H:%M:%S")

GPIO.setmode(GPIO.BOARD)
BUZZER= 32
GPIO.setup(BUZZER, GPIO.OUT)


mpu = MPU6050.MPU6050()     # instantiate a MPU6050 class object
accel = [0]*3               # define an arry to store accelerometer data
#gyro = [0]*3                # define an arry to store gyroscope data

write_api = "4JFAFWEM2I4Y9NTH"
base_url = "https://api.thingspeak.com/update?api_key={}".format(write_api)


def setup():
    mpu.dmp_initialize()    # initialize MPU6050
    GPIO.setmode(GPIO.BOARD) # use PHYSICAL GPIO Numbering



def loop():
    while(True):
        accel = mpu.get_acceleration()      # get accelerometer data
#        gyro = mpu.get_rotation()           # get gyroscope data

        print("%.2f g\t%.2f g\t%.2f g\t"%(accel[0]/16384.0,accel[1]/16384.0,accel[2]/16384.0))
        thingspeakHttp = base_url + "&field1={:.2f}&field2={:.2f}&field3={:.2f}".format(accel[0]/16384.0, accel[1]/16384.0,accel[2]/16384.0)
       
        conn = urlopen(thingspeakHttp)
        print("Response: {}".format(conn.read()))
        conn.close()

        if (accel[1]/16384.0)>0.8 :

            f = open("logfile.txt", "a")
            f.write("tiled left time = {}\n".format(current_time))
            f.close()
            
            print("tilted left")
            
            GPIO.output(BUZZER,1)
            time.sleep(1)#turn on buzzer

        if (accel[1]/16384.0)<-0.8 :

            f = open("logfile.txt", "a")
            f.write("tiled right time = {}\n".format(current_time))
            f.close()

            print("tilted right")
            
            GPIO.output(BUZZER,1)
            time.sleep(1)#turn on buzzer

        if abs(accel[0]/16384.0)>1 :
            
            f = open("logfile.txt", "a")
            f.write("hit time = {}\n".format(current_time))
            f.close()

            print("hit")
            
            GPIO.output(BUZZER,1)
            time.sleep(1)#turn on buzzer


        time.sleep(0.2)
        GPIO.output(BUZZER,0)

if __name__ == '__main__':     # Program entrance
    print("Program is starting ... ")
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        pass