from sense_hat import SenseHat
import time
import serial
import redis
import json

sense = SenseHat()

elapsed_time = time.time()
send_interval = 2
data = {} 
message = ''

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

redis = redis.Redis(
    host = "redis-13884.c275.us-east-1-4.ec2.cloud.redislabs.com",
    port= "13884",
    password= "JhW0tL0cBzJQihh57TTnblPdE9LlaP5J",
)

while 1:
    try:
        x = ser.readline().decode("utf-8").rsplit(";")
        x =[str(_) for _ in x] 
        x[-1] = x[-1][:-2] 
        data["Time"] = time.time()
        data["distance"] = int(x[0])
        data["right_pressure"] = int(x[1])
        data["left_pressure"] = int(x[2])
        data["accelerometer"] = sense.accelerometer
        data["gyroscope"] = sense.gyroscope
        data["temperature"] = sense.temperature
        message += json.dumps(data) + ';'
        data = {} 
        if time.time() - elapsed_time > send_interval:
            redis.append("user",message)
            message = ""
            elapsed_time = time.time()
    except UnicodeDecodeError:
        pass