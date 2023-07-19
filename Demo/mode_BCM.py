#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RepkaPi.GPIO as GPIO
from time import sleep          # позволяет выставить задержку на время

GPIO.setboard(GPIO.REPKAPI3)    # Repka Pi 3
GPIO.setmode(GPIO.BCM)          # выбираем тип обращения к GPIO по номеру BCM
led = 4                         # устанавливаем GPIO04 для диода
GPIO.setup(led, GPIO.OUT)       # устанавливаем диод (LED) как output

try:
    print ("Нажмите CTRL+C для завершения")
    while True:
        GPIO.output(led, 1)     # выставляем pin led 1/HIGH/True
        sleep(0.1)              # задержка 0.1 секунда
        GPIO.output(led, 0)     # выставляем pin led 0/LOW/False
        sleep(0.1)              # задержка 0.1 секунда

        GPIO.output(led, 1)     # выставляем pin led 1/HIGH/True
        sleep(0.1)              # задержка 0.1 секунда
        GPIO.output(led, 0)     # выставляем pin led 0/LOW/False
        sleep(0.5)              # задержка 0.5 секунда

except KeyboardInterrupt:
    GPIO.output(led, 0)         # выставляем pin led 0/LOW/False
    GPIO.cleanup()              # убираем все настойки по GPIO
    print ("Завершено")