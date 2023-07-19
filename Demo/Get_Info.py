#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RepkaPi.GPIO as GPIO

# Получаем модель выбранной платы
print (GPIO.getboardmodel())

# Версия библиотеки
print (GPIO.VERSION)

# Версия библиотеки
print (GPIO.RPI_INFO)

