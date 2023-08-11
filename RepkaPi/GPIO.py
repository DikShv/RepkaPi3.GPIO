# -*- coding: utf-8 -*-
# Copyright (c) 2018 Richard Hull
# Адаптация и доработка под Repka Pi (c) 2023 Дмитрий Шевцов (@screatorpro)
# Подробности смотрите в README.rst.


import warnings

from RepkaPi.constants import IN, OUT
from RepkaPi.constants import LOW, HIGH                     
from RepkaPi.constants import NONE, RISING, FALLING, BOTH   
from RepkaPi.constants import BCM, BOARD, SUNXI, SOC, SYSFS, DEFAULTBOARD, REPKAPI3
from RepkaPi.constants import PUD_UP, PUD_DOWN, PUD_OFF
from RepkaPi.constants import PA, PC, PD, PE, PF, PG, PL       
from RepkaPi.constants import VERSION, AUTODETECT
from RepkaPi.boards import get_gpio_pin, get_name, get_board, get_info
from RepkaPi.PWM_A import PWM_A
from RepkaPi import event, sysfs


_gpio_warnings = True
_mode = None
_board = DEFAULTBOARD
_exports = {}
_boards = [REPKAPI3]
RPI_INFO = "Не выбранна модель платы. Для выбора модели платы используйте метод setboard()"

if AUTODETECT:
  _board=get_board()

if _board in _boards:
  RPI_INFO = get_info(_board)



def _check_configured(channel, direction=None):
    configured = _exports.get(channel)
    if configured is None:
        raise RuntimeError("Channel {0} is not configured".format(channel))

    if direction is not None and direction != configured:
        descr = "input" if configured == IN else "output"
        raise RuntimeError("Channel {0} is configured for {1}".format(channel, descr))

# Устанавливаем модель платы
def setboard(board):
    global _board
    assert board in _boards
    _board = board

# Получаем установленную модель платы
def getboardmodel():
    global _board
    global _boards
    
    if _board not in _boards:
        raise RuntimeError("Не выбранна модель платы. Для выбора модели платы используйте метод setboard()")

    return get_name(_board)

def getmode():
    """
    To detect which pin numbering system has been set.

    :returns: :py:attr:`GPIO.BOARD`, :py:attr:`GPIO.BCM`, :py:attr:`GPIO.SUNXI`
        or :py:attr:`None` if not set.
    """
    return _mode


def setmode(mode):
    """
    You must call this method prior to using all other calls.

    :param mode: the mode, one of :py:attr:`GPIO.BOARD`, :py:attr:`GPIO.BCM`,
        :py:attr:`GPIO.SUNXI`, or a `dict` or `object` representing a custom
        pin mapping.
    """

    assert mode in [BCM, BOARD, SUNXI, SOC]
    global _mode
    _mode = mode


def setwarnings(enabled):
    global _gpio_warnings
    _gpio_warnings = enabled


def setup(channel, direction, initial=None, pull_up_down=None):
    global _boards
    """
    You need to set up every channel you are using as an input or an output.

    :param channel: the channel based on the numbering system you have specified
        (:py:attr:`GPIO.BOARD`, :py:attr:`GPIO.BCM` or :py:attr:`GPIO.SUNXI`).
    :param direction: whether to treat the GPIO pin as input or output (use only
        :py:attr:`GPIO.IN` or :py:attr:`GPIO.OUT`).
    :param initial: (optional) When supplied and setting up an output pin,
        resets the pin to the value given (can be :py:attr:`0` / :py:attr:`GPIO.LOW` /
        :py:attr:`False` or :py:attr:`1` / :py:attr:`GPIO.HIGH` / :py:attr:`True`).
    :param pull_up_down: (optional) When supplied and setting up an input pin,
        configures the pin to 3.3V (pull-up) or 0V (pull-down) depending on the
        value given (can be :py:attr:`GPIO.PUD_OFF` / :py:attr:`GPIO.PUD_UP` /
        :py:attr:`GPIO.PUD_DOWN`)

    To configure a channel as an input:

    .. code:: python

       GPIO.setup(channel, GPIO.IN)

    To set up a channel as an output:

    .. code:: python

       GPIO.setup(channel, GPIO.OUT)

    You can also specify an initial value for your output channel:

    .. code:: python

       GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)

    **Setup more than one channel:**
    You can set up more than one channel per call. For example:

    .. code:: python

       chan_list = [11,12]    # add as many channels as you want!
                              # you can tuples instead i.e.:
                              #   chan_list = (11,12)
       GPIO.setup(chan_list, GPIO.OUT)
    """
    if _board not in _boards:
        raise RuntimeError("Не выбранна модель платы. Для выбора модели платы используйте метод setboard()")

    if _mode is None:
        raise RuntimeError("Mode has not been set")

    if pull_up_down is not None:
        if _gpio_warnings:
            warnings.warn("Pull up/down пока не поддерживаются, но выполнение продолжается. Используйте GPIO.setwarnings(False) что бы отключить предупреждение.", stacklevel=2)

    if isinstance(channel, list):
        for ch in channel:
            setup(ch, direction, initial)
    else:
        if channel in _exports:
            raise RuntimeError("Channel {0} is already configured".format(channel))
        pin = get_gpio_pin(_board, _mode, channel)
        try:
            sysfs.export(pin)
        except (OSError, IOError) as e:
            if e.errno == 16:   # Device or resource busy
                if _gpio_warnings:
                    warnings.warn("Channel {0} is already in use, continuing anyway. Use GPIO.setwarnings(False) to disable warnings.".format(channel), stacklevel=2)
                sysfs.unexport(pin)
                sysfs.export(pin)
            else:
                raise e

        sysfs.direction(pin, direction)
        _exports[channel] = direction
        if direction == OUT and initial is not None:
            sysfs.output(pin, initial)


def input(channel):
    """
    Read the value of a GPIO pin.

    :param channel: the channel based on the numbering system you have specified
        (:py:attr:`GPIO.BOARD`, :py:attr:`GPIO.BCM` or :py:attr:`GPIO.SUNXI`).
    :returns: This will return either :py:attr:`0` / :py:attr:`GPIO.LOW` /
        :py:attr:`False` or :py:attr:`1` / :py:attr:`GPIO.HIGH` / :py:attr:`True`).
    """
    _check_configured(channel)  # Can read from a pin configured for output
    pin = get_gpio_pin(_board, _mode, channel)
    return sysfs.input(pin)


def output(channel, state):
    """
    Set the output state of a GPIO pin.

    :param channel: the channel based on the numbering system you have specified
        (:py:attr:`GPIO.BOARD`, :py:attr:`GPIO.BCM` or :py:attr:`GPIO.SUNXI`).
    :param state: can be :py:attr:`0` / :py:attr:`GPIO.LOW` / :py:attr:`False`
        or :py:attr:`1` / :py:attr:`GPIO.HIGH` / :py:attr:`True`.

    **Output to several channels:**
    You can output to many channels in the same call. For example:

    .. code:: python

       chan_list = [11,12]                             # also works with tuples
       GPIO.output(chan_list, GPIO.LOW)                # sets all to GPIO.LOW
       GPIO.output(chan_list, (GPIO.HIGH, GPIO.LOW))   # sets first HIGH and second LOW
    """
    if isinstance(channel, list):
        for ch in channel:
            output(ch, state)
    else:
        _check_configured(channel, direction=OUT)
        pin = get_gpio_pin(_board, _mode, channel)
        return sysfs.output(pin, state)


def wait_for_edge(channel, trigger, timeout=-1):
    """
    This function is designed to block execution of your program until an edge
    is detected.

    :param channel: the channel based on the numbering system you have specified
        (:py:attr:`GPIO.BOARD`, :py:attr:`GPIO.BCM` or :py:attr:`GPIO.SUNXI`).
    :param trigger: The event to detect, one of: :py:attr:`GPIO.RISING`,
        :py:attr:`GPIO.FALLING` or :py:attr:`GPIO.BOTH`.
    :param timeout: (optional) TODO

    In other words, the polling example above that waits for a button press
    could be rewritten as:

    .. code:: python

       GPIO.wait_for_edge(channel, GPIO.RISING)

    Note that you can detect edges of type :py:attr:`GPIO.RISING`,
    :py:attr`GPIO.FALLING` or :py:attr:`GPIO.BOTH`. The advantage of doing it
    this way is that it uses a negligible amount of CPU, so there is plenty left
    for other tasks.

    If you only want to wait for a certain length of time, you can use the
    timeout parameter:

    .. code:: python

       # wait for up to 5 seconds for a rising edge (timeout is in milliseconds)
       channel = GPIO.wait_for_edge(channel, GPIO_RISING, timeout=5000)
       if channel is None:
           print('Timeout occurred')
       else:
           print('Edge detected on channel', channel)
    """
    _check_configured(channel, direction=IN)
    pin = get_gpio_pin(_board, _mode, channel)
    if event.blocking_wait_for_edge(pin, trigger, timeout) is not None:
        return channel


def add_event_detect(channel, trigger, callback=None, bouncetime=None):
    """
    This function is designed to be used in a loop with other things, but unlike
    polling it is not going to miss the change in state of an input while the
    CPU is busy working on other things. This could be useful when using
    something like Pygame or PyQt where there is a main loop listening and
    responding to GUI events in a timely basis.

    :param channel: the channel based on the numbering system you have specified
        (:py:attr:`GPIO.BOARD`, :py:attr:`GPIO.BCM` or :py:attr:`GPIO.SUNXI`).
    :param trigger: The event to detect, one of: :py:attr:`GPIO.RISING`,
        :py:attr:`GPIO.FALLING` or :py:attr:`GPIO.BOTH`.
    :param callback: (optional) TODO
    :param bouncetime: (optional) TODO

    .. code: python

       GPIO.add_event_detect(channel, GPIO.RISING)  # add rising edge detection on a channel
       do_something()
       if GPIO.event_detected(channel):
           print('Button pressed')
    """
    _check_configured(channel, direction=IN)

    if bouncetime is not None:
        if _gpio_warnings:
            warnings.warn("bouncetime is not (yet) fully supported, continuing anyway. Use GPIO.setwarnings(False) to disable warnings.", stacklevel=2)

    pin = get_gpio_pin(_board, _mode, channel)
    event.add_edge_detect(pin, trigger, __wrap(callback, channel))


def remove_event_detect(channel):
    """
    :param channel: the channel based on the numbering system you have specified
        (:py:attr:`GPIO.BOARD`, :py:attr:`GPIO.BCM` or :py:attr:`GPIO.SUNXI`).
    """
    _check_configured(channel, direction=IN)
    pin = get_gpio_pin(_board, _mode, channel)
    event.remove_edge_detect(pin)


def add_event_callback(channel, callback, bouncetime=None):
    """
    :param channel: the channel based on the numbering system you have specified
        (:py:attr:`GPIO.BOARD`, :py:attr:`GPIO.BCM` or :py:attr:`GPIO.SUNXI`).
    :param callback: TODO
    :param bouncetime: (optional) TODO
    """
    _check_configured(channel, direction=IN)

    if bouncetime is not None:
        if _gpio_warnings:
            warnings.warn("bouncetime is not (yet) fully supported, continuing anyway. Use GPIO.setwarnings(False) to disable warnings.", stacklevel=2)

    pin = get_gpio_pin(_board, _mode, channel)
    event.add_edge_callback(pin, __wrap(callback, channel))


def event_detected(channel):
    """
    This function is designed to be used in a loop with other things, but unlike
    polling it is not going to miss the change in state of an input while the
    CPU is busy working on other things. This could be useful when using
    something like Pygame or PyQt where there is a main loop listening and
    responding to GUI events in a timely basis.

    .. code:: python

       GPIO.add_event_detect(channel, GPIO.RISING)  # add rising edge detection on a channel
       do_something()
       if GPIO.event_detected(channel):
           print('Button pressed')

    Note that you can detect events for :py:attr:`GPIO.RISING`,
    :py:attr:`GPIO.FALLING` or :py:attr:`GPIO.BOTH`.

    :param channel: the channel based on the numbering system you have specified
        (:py:attr:`GPIO.BOARD`, :py:attr:`GPIO.BCM` or :py:attr:`GPIO.SUNXI`).
    :returns: :py:attr:`True` if an edge event was detected, else :py:attr:`False`.
    """
    _check_configured(channel, direction=IN)
    pin = get_gpio_pin(_board, _mode, channel)
    return event.edge_detected(pin)


def __wrap(callback, channel):
    if callback is not None:
        return lambda _: callback(channel)


def cleanup(channel=None):
    """
    At the end any program, it is good practice to clean up any resources you
    might have used. This is no different with RepkaPi.GPIO. By returning all
    channels you have used back to inputs with no pull up/down, you can avoid
    accidental damage to your Repka Pi by shorting out the pins. Note that
    this will only clean up GPIO channels that your script has used. Note that
    GPIO.cleanup() also clears the pin numbering system in use.

    To clean up at the end of your script:

    .. code:: python

       GPIO.cleanup()

    It is possible that don't want to clean up every channel leaving some set
    up when your program exits. You can clean up individual channels, a list or
    a tuple of channels:

    .. code:: python

       GPIO.cleanup(channel)
       GPIO.cleanup( (channel1, channel2) )
       GPIO.cleanup( [channel1, channel2] )
    """
    if channel is None:
        cleanup(list(_exports.keys()))
        setwarnings(True)
        global _mode
        _mode = None
    elif isinstance(channel, list):
        for ch in channel:
            cleanup(ch)
    else:
        _check_configured(channel)
        pin = get_gpio_pin(_board, _mode, channel)
        event.cleanup(pin)
        sysfs.unexport(pin)
        del _exports[channel]



