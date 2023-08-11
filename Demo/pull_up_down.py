#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pull_up_down пока не поддерживается

import RepkaPi.GPIO as GPIO

from time import sleep          # позволяет выставить задержку на время

GPIO.setboard(GPIO.REPKAPI3)    # Repka Pi 3
GPIO.setmode(GPIO.BOARD)        # выбираем тип обращения к GPIO по номеру PIN (BOARD)
button = 15                     # устанавливаем pin 15 для кнопки
led = 11                        # устанавливаем pin 11 для диода
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # устанавливаем кновка как input
GPIO.setup(led, GPIO.OUT)       # устанавливаем диод (LED) как output

try:
    while True:                 # цикл будет выполняться пока не нажмем CTRL+C
        if GPIO.input(button) == 1:      # if button == 1
            print (f'PIN {button} равен 1/HIGH/True - LED ON')
            GPIO.output(led, 1) # выставляем pin led 1/HIGH/True
        else:
            print (f'PIN {button} равен 0/LOW/False - LED OFF')
            GPIO.output(led, 0) # выставляем pin led 0/LOW/False
        sleep(0.1)              # задержка 0.1 секунда

finally:                        # выполняет блок инструкций в любом случае, было ли исключение, или нет
    print("Завершение.")
    GPIO.output(led, 0)         # выставляем pin led 0/LOW/False
    GPIO.cleanup()              # убираем все настойки по GPIO
