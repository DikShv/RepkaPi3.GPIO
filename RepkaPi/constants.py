# -*- coding: utf-8 -*-
# Copyright (c) 2018 Richard Hull
# Адаптация и доработка под Repka Pi (c) 2023 Дмитрий Шевцов (@screatorpro)
# Подробности смотрите в README.rst.

import sys


class _const:

    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const(%s)" % name)
        self.__dict__[name] = value


GPIO = _const()

# From: https://sourceforge.net/p/raspberry-gpio-python/code/ci/default/tree/source/c_gpio.h#l42
GPIO.IN = 1
GPIO.OUT = 0
GPIO.ALT0 = 4

GPIO.HIGH = 1
GPIO.LOW = 0

GPIO.PUD_OFF = 0
GPIO.PUD_DOWN = 1
GPIO.PUD_UP = 2

# From: https://sourceforge.net/p/raspberry-gpio-python/code/ci/default/tree/source/common.h
GPIO.BOARD = 10
GPIO.BCM = 11
GPIO.SUNXI = 12  
GPIO.SOC = 13  

GPIO.NONE = 0
GPIO.RISING = 1
GPIO.FALLING = 2
GPIO.BOTH = 3
GPIO.VERSION = '0.1.0'

GPIO.PA = 0
GPIO.PC = 64
GPIO.PD = 96
GPIO.PE = 128
GPIO.PF = 160
GPIO.PG = 192
GPIO.PL = 352

#Поддерживаемые платы
GPIO.REPKAPI3 = 1

#Плата по умолчанию
#GPIO.DEFAULTBOARD = None
GPIO.DEFAULTBOARD = GPIO.REPKAPI3 # Repka Pi 3 выставлена по умолчанию

sys.modules[__name__] = GPIO
