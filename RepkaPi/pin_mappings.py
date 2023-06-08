# -*- coding: utf-8 -*-
# Copyright (c) 2018 Richard Hull
# See LICENSE.md for details.

import functools
from copy import deepcopy
from RepkaPi.constants import BOARD, BCM, SUNXI, CUSTOM, REPKAPI3


class _sunXi(object):

    def __getitem__(self, value):

        offset = ord(value[1]) - 65
        pin = int(value[2:])

        assert value[0] == "P"
        assert 0 <= offset <= 25
        assert 0 <= pin <= 31

        return (offset * 32) + pin


_pin_map = {
    # pin number = (положение буквы в алфавите - 1) * 32 + номер пина
    # Пример, PD14 будет 3 * 32 +14 = 110
    REPKAPI3: {
        BOARD: {
            3:   12,    # PA12/TWI1_SDA/DI_RX/PA_EINT12
            5:   11,    # PA11/TWI1_SCK/DI_TX/PA_EINT11
            7:    7,    # PA7
            8:    4,    # PA4/UART0_TX
            10:   5,    # PA5/UART0_RX
            11:   8,    # PA8
            12:   6,    # PA14
            13:   9,    # PA9
            15:  10,    # PA10
            16: 354,    # PL2/S_UART_TX
            18: 355,    # PL3/S_UART_RX
            19:  64,    # PA15/SPI0_MOSI
            21:  65,    # PA16/SPI0_MISO
            22:   2,    # PA2
            23:  66,    # PA14/SPI0_CLK
            24:  67,    # PA13/SPI0_CS0
            26:   3,    # PA3/SPI0_CS0
            27:  19,    # PA19/TWI2_SDA
            28:  18,    # PA18/TWI2_SCK
            29:   0,    # PA0/UART2_TX
            31:   1,    # PA1/UART2_RX
            32: 363,    # PL11
            33: 362,    # PL10/PWM0
            35:  16,    # PA16/SPI1_MISO
            36:  13,    # PA13/SPI1_CS0
            37:  21,    # PA21
            38:  15,    # PG6/SPI1_MOSI
            40:  14,    # PG7/SPI1_CLK
        },

        # BCM pin to actual GPIO pin
        BCM: {
            3: 2,
            5: 3,
            7: 4,
            8: 14,
            10: 15,
            11: 17,
            12: 18,
            13: 27,
            15: 22,
            16: 23,
            18: 24,
            19: 10,
            21: 9,
            22: 25,
            23: 11,
            24: 8,
            26: 7,
            29: 5,
            31: 6,
            32: 12,
            33: 13,
            35: 19,
            36: 16,
            37: 26,
            38: 20,
            40: 21
        },

        SUNXI: _sunXi(),

        # User defined, initialized as empty
        CUSTOM: {}
    }
}


def set_custom_pin_mappings(mappings):
    _pin_map[CUSTOM] = deepcopy(mappings)


def get_gpio_pin(board, mode, channel):
    assert mode in [BOARD, BCM, SUNXI, CUSTOM]
    assert board in [REPKAPI3]
    return _pin_map[board][mode][channel]


bcm = functools.partial(get_gpio_pin, BCM)
board = functools.partial(get_gpio_pin, BOARD)
sunxi = functools.partial(get_gpio_pin, SUNXI)
custom = functools.partial(get_gpio_pin, CUSTOM)
