#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RepkaPi.GPIO as GPIO
from time import sleep          # this lets us have a time delay

GPIO.setboard(GPIO.REPKAPI3)      # Repka Pi 3
GPIO.setmode(GPIO.BCM)          # set up BCM numbering
GPIO.setup(4, GPIO.OUT)      # set BCM4 as an output (LED)

try:
  while True:
    GPIO.output(4, 1)        # set port/pin value to 1/HIGH/True
    sleep(0.1)
    GPIO.output(4, 0)        # set port/pin value to 0/LOW/False
    sleep(0.1)
    GPIO.output(4, 1)        # set port/pin value to 1/HIGH/True
    sleep(0.1)
    GPIO.output(4, 0)        # set port/pin value to 0/LOW/False
    sleep(0.5)

except KeyboardInterrupt:
  GPIO.output(sled, 0)
  GPIO.cleanup()                # clean up after yourself
  print ("Bye.")
