RepkaPi.GPIO
========


A drop-in replacement library for `RPi.GPIO <https://sourceforge.net/projects/raspberry-gpio-python/>`_
for the Repka Pi and other SBCs. Only the basic GPIO functions are replicated,
using sysfs: this allows the GPIO pins to be accessed from user space.


Installation
----------

  $ sudo apt-get update

  $ sudo apt-get install python-dev git

  $ git clone https://github.com/DikShv/RepkaPi3.GPIO.git

  $ cd RepkaPi3.GPIO

  $ sudo python setup.py install


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

Non Root Access
---------------
If you want to be able to use the library as a non root user, you will need to setup a `UDEV` rule to grant you permissions first. 
This can be accomplished as follows: 

``$ sudo usermod -aG gpio <current_user>``

``$ sudo nano /etc/udev/rules.d/99-gpio.rules``

That should add your user to the GPIO group, create a new ``UDEV`` rule, and open it in the Nano text editor. 

Enter the following into Nano:

.. code-block:: text

   SUBSYSTEM=="gpio", KERNEL=="gpio*", ACTION=="add", PROGRAM="/bin/sh -c 'chown root:gpio /sys%p/active_low /sys%p/direction /sys%p/edge /sys%p/value ; chmod 660 /sys%p/active_low /sys%p/direction /sys%p/edge /sys%p/value'"
   SUBSYSTEM=="gpio", KERNEL=="gpiochip*", ACTION=="add", PROGRAM="/bin/sh -c 'chown root:gpio /sys/class/gpio/export /sys/class/gpio/unexport ; chmod 220 /sys/class/gpio/export /sys/class/gpio/unexport'" 

Press ``ctrl-x``, ``Y``, and ``ENTER`` to save and close the file. 

Finally, reboot and you should be ready to use ``RepkaPi.GPIO`` as a non root user. 


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
