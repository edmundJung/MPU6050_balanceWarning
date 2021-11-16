#!/usr/bin/env python3
########################################################################
# Filename    : MPU6050RAW.py
# Description : Read data of MPU6050.
# auther      : www.freenove.com
# modification: 2021/1/1
########################################################################
import MPU6050
import time


mpu = MPU6050.MPU6050()     # instantiate a MPU6050 class object
accel = [0]*3               # define an arry to store accelerometer data
#gyro = [0]*3                # define an arry to store gyroscope data
def setup():
    mpu.dmp_initialize()    # initialize MPU6050


def loop():
    while(True):
        accel = mpu.get_acceleration()      # get accelerometer data
#        gyro = mpu.get_rotation()           # get gyroscope data
        print("%.2f g\t%.2f g\t%.2f g\t"%(accel[0]/16384.0,accel[1]/16384.0,accel[2]/16384.0))
        if (accel[1]/16384.0)>0.8 :
            print("tilted left")
        if (accel[1]/16384.0)<-0.8 :
            print("tilted right")
        if abs(accel[0]/16384.0)>1 :
            print("hit")


        time.sleep(0.5)

if __name__ == '__main__':     # Program entrance
    print("Program is starting ... ")
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        pass
