#!/usr/bin/env python3

from sys import argv
import RPi.GPIO as GPIO
import time

import smtplib
server=smtplib.SMTP('smtp.gmail.com',587)


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#buzzer
buzzer = 17 
GPIO.setup(buzzer, GPIO.OUT)
buzzerNoise = GPIO.PWM(buzzer, 1000)
buzzerNoise.start(10)


server.starttls()
server.login("proiectsm22","PrjSM2022!")
msg="IMPORTANT!!!\nExponat ID2589 in pericol!!!"

# leduri
led_red = 26
led_green = 13
led_yellow = 19

GPIO.setup(led_red, GPIO.OUT)
GPIO.setup(led_green, GPIO.OUT)
GPIO.setup(led_yellow, GPIO.OUT)


def distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.0001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance


if __name__ == '__main__':
    try:
        while True:
            GPIO.output(led_green, GPIO.HIGH)
            dist = distance()
            if dist < 10:
                buzzerNoise.ChangeFrequency(20000)
                GPIO.output(buzzer, GPIO.HIGH)
                GPIO.output(led_red, GPIO.HIGH)
                GPIO.output(led_yellow, GPIO.LOW)
                time.sleep(0.1)
                
                server.sendmail("proiectsm22@gmail.com", ["bordeabianca2000@gmail.com", "dumbravapetronela111@gmail.com"],msg)
            elif dist >= 10 and dist < 25:
                buzzerNoise.ChangeFrequency(1)
                GPIO.output(buzzer,GPIO.LOW)
                GPIO.output(led_red, GPIO.LOW)
                GPIO.output(led_yellow, GPIO.HIGH)
                time.sleep(0.1)
            else:
                buzzerNoise.ChangeFrequency(1)
                GPIO.output(buzzer,GPIO.LOW)
                GPIO.output(led_red, GPIO.LOW)
                GPIO.output(led_yellow, GPIO.LOW)
                time.sleep(0.1)
    finally:
        buzzerNoise.stop()
        GPIO.cleanup()
        server.quit()
