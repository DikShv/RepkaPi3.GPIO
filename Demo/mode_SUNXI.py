#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RepkaPi.GPIO as GPIO
from time import sleep          # this lets us have a time delay

GPIO.setboard(GPIO.REPKAPI3)      # Repka Pi 3
GPIO.setmode(GPIO.SUNXI)          # set up SOC numbering

GPIO.setup("PA7", GPIO.OUT)      # set PA7 as an output (Status led of board)

try:
  while True:
    GPIO.output("PA7", 1)        # set port/pin value to 1/HIGH/True
    sleep(0.1)
    GPIO.output("PA7", 0)        # set port/pin value to 0/LOW/False
    sleep(0.1)
    GPIO.output("PA7", 1)        # set port/pin value to 1/HIGH/True
    sleep(0.1)
    GPIO.output("PA7", 0)        # set port/pin value to 0/LOW/False
    sleep(0.5)

except KeyboardInterrupt:
  GPIO.output(sled, 0)
  GPIO.cleanup()                # clean up after yourself
  print ("Bye.")
