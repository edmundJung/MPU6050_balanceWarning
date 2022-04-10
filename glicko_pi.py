import MPU6050
import time
import RPi.GPIO as GPIO
import requests
from uuid import uuid4


import MFRC522
import asyncio
import aiohttp

# current_time = now.strftime("%H:%M:%S")
# buzzerPin = 32  # define buzzerPin

trigPin = 8
echoPin = 10
MAX_DISTANCE = 5000  # define the maximum measuring distance, unit: cm
timeOut = (
    MAX_DISTANCE * 60
)  # calculate timeout according to the maximum measuring distance
buzzerPin = 32  # define buzzerPin

mpu = MPU6050.MPU6050()  # instantiate a MPU6050 class object
accel = [0] * 3  # define an arry to store accelerometer data
gyro = [0] * 3  # define an arry to store gyroscope data


def setup():
    mpu.dmp_initialize()  # initialize MPU6050
    GPIO.setmode(GPIO.BOARD)  # use PHYSICAL GPIO Numbering

    GPIO.setup(trigPin, GPIO.OUT)  # set trigPin to OUTPUT mode
    GPIO.setup(echoPin, GPIO.IN)  # set echoPin to INPUT mode
    GPIO.setup(buzzerPin, GPIO.OUT)  # set buzzerPin to OUTPUT mode


def pulseIn(pin, level, timeOut):  # obtain pulse time of a pin under timeOut
    t0 = time.time()
    while GPIO.input(pin) != level:
        if (time.time() - t0) > timeOut * 0.000001:
            return 0
    t0 = time.time()
    while GPIO.input(pin) == level:
        if (time.time() - t0) > timeOut * 0.000001:
            return 0
    pulseTime = (time.time() - t0) * 1000000
    return pulseTime


def getSonar():  # get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin, GPIO.HIGH)  # make trigPin output 10us HIGH level
    time.sleep(0.1)  # 1ms
    GPIO.output(trigPin, GPIO.LOW)  # make trigPin output LOW level
    pingTime = pulseIn(echoPin, GPIO.HIGH, timeOut)  # read plus time of echoPin
    distance = (
        pingTime * 340.0 / 2.0 / 10000.0
    )  # calculate distance with sound speed 340m/s
    return distance


async def make_account(trip_id, ax, ay, az, distance):
    url = "http://glicko-ui.herokuapp.com/api/data-create/"
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            data={
                "accel_x": ax,
                "accel_y": ay,
                "accel_z": az,
                "distance": distance,
                "user_id": "375a156f-1a18-454f-9234-cf11e16085af",
                "trip_id": trip_id,
            },
        ):
            pass


def loop():
    sending = False
    current_trip = ""
    card_reader = MFRC522.MFRC522()
    loop = asyncio.get_event_loop()
    while True:
        (status, TagType) = card_reader.MFRC522_Request(card_reader.PICC_REQIDL)
        (status, uid) = card_reader.MFRC522_Anticoll()
        if status == card_reader.MI_OK and uid == [19, 103, 173, 26, 195]:
            sending = not sending
            trip_id = uuid4()
            if sending:
                requests.post(
                    url="http://glicko-ui.herokuapp.com/api/trip-create/",
                    data={
                        "publisher": "375a156f-1a18-454f-9234-cf11e16085af",
                        "id": trip_id,
                        "scooter_id": "b46dd6c8-487e-4c7e-a9555-1eeee31558ca",
                    },
                )
                current_trip = trip_id
                GPIO.output(buzzerPin, GPIO.HIGH)  # turn on buzzer
                time.sleep(0.1)
                GPIO.output(buzzerPin, GPIO.LOW)  # turn on buzzer
                time.sleep(0.5)
            else:
                if current_trip != "":
                    requests.post(
                        url=f"http://glicko-ui.herokuapp.com/api/trip-update/{current_trip}/",
                        data={
                            "publisher": "375a156f-1a18-454f-9234-cf11e16085af",
                            "id": current_trip,
                            "scooter_id": "b46dd6c8-487e-4c7e-a9555-1eeee31558ca",
                            "trip_status": "Finished",
                        },
                    )
                    GPIO.output(buzzerPin, GPIO.HIGH)  # turn on buzzer
                    time.sleep(0.5)
                    GPIO.output(buzzerPin, GPIO.LOW)  # turn on buzzer
                    time.sleep(0.5)

        print(f"we are sending or not: {sending}")
        if sending:
            accel = mpu.get_acceleration()  # get accelerometer data

            distance = getSonar()  # get distance
            print("The distance is : %.2f cm" % (distance))
            print(
                "%.2f g\t%.2f g\t%.2f g\t"
                % (accel[0] / 16384.0, accel[1] / 16384.0, accel[2] / 16384.0)
            )

            loop.run_until_complete(
                make_account(
                    trip_id,
                    accel[0] / 16384.0,
                    accel[1] / 16384.0,
                    accel[2] / 16384.0,
                    distance,
                )
            )


if __name__ == "__main__":  # Program entrance
    print("Program is starting ... ")
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        pass
