RepkaPi.GPIO
========


A drop-in replacement library for `RPi.GPIO <https://sourceforge.net/projects/raspberry-gpio-python/>`_
for the Repka Pi and other SBCs. Only the basic GPIO functions are replicated,
using sysfs: this allows the GPIO pins to be accessed from user space.


Installation
----------

    sudo apt-get update
    sudo apt-get install python-dev git
    git clone https://github.com/DikShv/RepkaPi3.GPIO.git
    cd RepkaPi3.GPIO
    sudo python setup.py install


Supported Boards
----------

* Repka Pi 3

Usage
----------

Same as RPi.GPIO but with a new function to choose Repka Pi Board.


    import RepkaPi.GPIO as GPIO
    GPIO.setboard(GPIO.REPKAPI3)
    GPIO.setmode(GPIO.BOARD)
    GPIO.output(5, 1)



Many demo is on the Demo folder


References
----------
* https://www.kernel.org/doc/Documentation/gpio/sysfs.txt
* http://linux-sunxi.org/GPIO

License
-------
The MIT License

Copyright (c) 2018 Richard Hull

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
