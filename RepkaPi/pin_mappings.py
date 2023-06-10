# -*- coding: utf-8 -*-
# Copyright (c) 2018 Richard Hull
# Адаптация и доработка по Repka Pi (c) 2023 Дмитрий Шевцов (@screatorpro)
# Подробности смотрите в LICENSE.md.

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
            24:  67,    # PC3/SPI0_CS0
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

        # Контакт BCM к фактическому контакту GPIO
        BCM: {
            2: 12,
            3: 11,
            4: 7,
            14: 4,
            15: 5,
            17: 8,
            18: 6,
            27: 9,
            22: 10,
            23: 354,
            24: 355,
            10: 64,
            9: 65,
            25: 2,
            11: 66,
            8: 67,
            7: 3,
            5: 0,
            6: 1,
            12: 363,
            13: 362,
            19: 16,
            16: 13,
            26: 21,
            20: 15,
            21: 14
        },

        SUNXI: _sunXi(),

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
