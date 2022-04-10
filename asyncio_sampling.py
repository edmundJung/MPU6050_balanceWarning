from sense_hat import SenseHat
import time
import serial
import asyncio
import json
import redis

sense = SenseHat()

elapsed_time = time.time()
send_interval = 5
message = ""

# ser = serial.Serial(
#     port="/dev/ttyUSB0",
#     baudrate = 9600,
#     parity = serial.PARITY_NONE,
#     stopbits=serial.STOPBITS_ONE,
#     bytesize=serial.EIGHTBITS,
#     timeout=1
# )

# redis = redis.Redis(
#     host = "redis-13884.c275.us-east-1-4.ec2.cloud.redislabs.com",
#     port= "13884",
#     password= "JhW0tL0cBzJQihh57TTnblPdE9LlaP5J",
# )

async def get_data(gather_data):
    try:
        # x = ser.readline().decode("utf-8").rsplit(";")
        # x =[str(_) for _ in x] 
        # x[-1] = x[-1][:-2] 
        gather_data["Time"] = time.time()
        # gather_data["distance"] = int(x[0])
        # gather_data["right_pressure"] = int(x[1])
        # gather_data["left_pressure"] = int(x[2])
        gather_data["accelerometer"] = sense.accelerometer
        gather_data["gyroscope"] = sense.gyroscope
        gather_data["temperature"] = sense.temperature
    except UnicodeDecodeError:
        pass

async def save_data(gather_data):
    if gather_data !={}: 
        with open("save1.json", "a") as outfile:
            outfile.write(json.dumps(gather_data))
            outfile.write(",")
            outfile.close()
    
    
# async def send_data(message, elapsed_time):  
#     redis.append("user", message)
#     message= ""
#     elapsed_time = time.time()


async def main():
    gather_data = {}
    await get_data(gather_data)
    await save_data(gather_data)
    # if time.time() - elapsed_time > send_interval:
    #     await send_data(message, elapsed_time)

while 1:
    loop = asyncio.get_event_loop()
    runner = loop.run_until_complete(main())
