#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RepkaPi.GPIO as GPIO

# Получаем модель выбранной платы
print (GPIO.getboardmodel())

# Версия библиотеки
print (GPIO.VERSION)