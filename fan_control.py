import time

import RPi.GPIO as IO
from gpiozero import CPUTemperature

GPIO_PIN = 14  # the pin for controlling the fan
PWM_FREQUENCY = 64  # (Hertz)

ON_THRESHOLD = 60  # (degrees Celsius) when the fan is started
OFF_THRESHOLD = 45  # (degress Celsius) when the fan is turned off
MAX_TEMP = 80  # (temperature) when the fan should be set to max speed

MIN_SPEED = 40  # [0:100] minimum speed for the fan to run
MAX_SPEED = 100  # [0:100] maximum speed for the fan to run

UPDATE_INTERVAL = 5  # (seconds) how often the temperature is checked

ABS_TEMP_DELTA = MAX_TEMP - OFF_THRESHOLD


def determine_best_speed(temperature):
    if temperature < ON_THRESHOLD:
        return MIN_SPEED
    else:
        temp_delta = MAX_TEMP - temperature
        temp_percentage = 1 - temp_delta / ABS_TEMP_DELTA
        calculated_speed = temp_percentage * 100
        print("temp delta " + str(temp_delta) + ", temp speed " + str(calculated_speed))
        if calculated_speed > MAX_SPEED:
            return MAX_SPEED
        elif calculated_speed < MIN_SPEED:
            return MIN_SPEED
        else:
            return calculated_speed


if __name__ == '__main__':
    IO.setwarnings(True)
    IO.setmode(IO.BCM)
    IO.setup(GPIO_PIN, IO.OUT)

    cpu = CPUTemperature()
    fan = IO.PWM(GPIO_PIN, PWM_FREQUENCY)
    fan.start(0)

    while True:
        temp = cpu.temperature
        if temp > ON_THRESHOLD:
            fan.start(100)
            time.sleep(2)
            while temp > OFF_THRESHOLD:
                speed = determine_best_speed(temp)
                print("temp: " + str(temp) + "C -> cooling " + str(speed) + "%")
                fan.ChangeDutyCycle(speed)
                time.sleep(UPDATE_INTERVAL)
                temp = cpu.temperature
            fan.ChangeDutyCycle(0)
        else:
            print("temp: " + str(temp))
            time.sleep(UPDATE_INTERVAL)

    # IO.cleanup()
    # print("done")
