# -*- coding: utf-8 -*-
# Copyright (c) 2018 Richard Hull
# Адаптация и доработка под Repka Pi (c) 2023 Дмитрий Шевцов (@screatorpro)
# Подробности смотрите в README.rst.

from RepkaPi import sysfs

class PWM_A:

    # To Do:
    # 1. Start tracking pwm cases to  list like _exports say _exports_pwm
    # 2. find way to check _exports against _exports_pwm to make sure there is no overlap.
    # 3. Create map of pwm pins to various boards.

    def __init__(self, chip, pin, frequency, duty_cycle_percent, invert_polarity=False):  # (pwm pin, frequency in KHz)

        """
        Setup the PWM object to control.

        :param chip: the pwm chip number you wish to use.
        :param pin: the pwm pin number you wish to use.
        :param frequency: the frequency of the pwm signal in hertz.
        :param duty_cycle_percent: the duty cycle percentage.
        :param invert_polarity: invert the duty cycle.
            (:py:attr:`True` or :py:attr:`False`).
        """

        self.chip = chip
        self.pin = pin
        self.frequency = frequency
        self.duty_cycle_percent = duty_cycle_percent
        self.invert_polarity = invert_polarity

        try:
            sysfs.PWM_Export(chip, pin)  # creates the pwm sysfs object
            if invert_polarity is True:
                sysfs.PWM_Polarity(chip, pin, invert=True)  # invert pwm i.e the duty cycle tells you how long the cycle is off
            else:
                sysfs.PWM_Polarity(chip, pin, invert=False)  # don't invert the pwm signal. This is the normal way its used.
            sysfs.PWM_Enable(chip, pin)
            return sysfs.PWM_Frequency(chip, pin, frequency)

        except (OSError, IOError) as e:
            if e.errno == 16:   # Device or resource busy
                warnings.warn("Pin {0} is already in use, continuing anyway.".format(pin), stacklevel=2)
                sysfs.PWM_Unexport(chip, pin)
                sysfs.PWM_Export(chip, pin)
            else:
                raise e

    def start_pwm(self):  # turn on pwm by setting the duty cycle to what the user specified
        """
        Start PWM Signal.
        """
        return sysfs.PWM_Duty_Cycle_Percent(self.chip, self.pin, self.duty_cycle_percent)  # duty cycle controls the on-off

    def stop_pwm(self):  # turn on pwm by setting the duty cycle to 0
        """
        Stop PWM Signal.
        """
        return sysfs.PWM_Duty_Cycle_Percent(self.chip, self.pin, 0)  # duty cycle at 0 is the equivilant of off

    def change_frequency(self, new_frequency):
        # Order of opperations:
        # 1. convert to period
        # 2. check if period is increasing or decreasing
        # 3. If increasing update pwm period and then update the duty cycle period
        # 4. If decreasing update the duty cycle period and then the pwm period
        # Why:
        # The sysfs rule for PWM is that PWM Period >= duty cycle period (in nanosecs)

        """
        Change the frequency of the signal.

        :param new_frequency: the new PWM frequency.
        """

        pwm_period = (1 / new_frequency) * 1e9
        pwm_period = int(round(pwm_period, 0))
        duty_cycle = (self.duty_cycle_percent / 100) * pwm_period
        duty_cycle = int(round(duty_cycle, 0))

        old_pwm_period = int(round((1 / self.frequency) * 1e9, 0))

        if (pwm_period > old_pwm_period):  # if increasing
            sysfs.PWM_Period(self.chip, self.pin, pwm_period)  # update the pwm period
            sysfs.PWM_Duty_Cycle(self.chip, self.pin, duty_cycle)  # update duty cycle

        else:
            sysfs.PWM_Duty_Cycle(self.chip, self.pin, duty_cycle)  # update duty cycle
            sysfs.PWM_Period(self.chip, self.pin, pwm_period)  # update pwm freq

        self.frequency = new_frequency  # update the frequency

    def duty_cycle(self, duty_cycle_percent):  # in percentage (0-100)
        """
        Change the duty cycle of the signal.

        :param duty_cycle_percent: the new PWM duty cycle as a percentage.
        """

        if (0 <= duty_cycle_percent <= 100):
            self.duty_cycle_percent = duty_cycle_percent
            return sysfs.PWM_Duty_Cycle_Percent(self.chip, self.pin, self.duty_cycle_percent)
        else:
            raise Exception("Duty cycle must br between 0 and 100. Current value: {0} is out of bounds".format(duty_cycle_percent))

    def pwm_polarity(self):  # invert the polarity of the pwm
        """
        Invert the signal.
        """
        sysfs.PWM_Disable(self.chip, self.pin)
        sysfs.PWM_Polarity(self.chip, self.pin, invert=not(self.invert_polarity))
        sysfs.PWM_Enable(self.chip, self.pin)

    def pwm_close(self):
        """
        remove the object from the system.
        """
        sysfs.PWM_Unexport(self.chip, self.pin)