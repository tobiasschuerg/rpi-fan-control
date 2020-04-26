import time

import RPi.GPIO as IO
from gpiozero import CPUTemperature

FAN_PIN = 14  # the pin for controlling the fan
PWM_FREQUENCY = 32  # (Hertz)
SPEED = 40

UPDATE_INTERVAL = 2  # (seconds) how often the temperature is checked

if __name__ == '__main__':
    IO.setwarnings(True)
    IO.setmode(IO.BCM)
    IO.setup(FAN_PIN, IO.OUT)

    cpu = CPUTemperature()
    fan = IO.PWM(FAN_PIN, PWM_FREQUENCY)
    fan.start(0)

    speed = SPEED

    freq = PWM_FREQUENCY

    while True:
        temp = cpu.temperature
        print("temp: " + str(temp) + "C freq " + str(freq) + " -> cooling " + str(speed) + "%")
        fan.ChangeDutyCycle(speed)
        freq = int(input('frequency'))
        fan.ChangeDutyCycle(100)
        fan.ChangeFrequency(freq)
        time.sleep(1)

