# -*- coding: utf-8 -*-
# Copyright (c) 2018 Richard Hull
# Адаптация и доработка под Repka Pi (c) 2023 Дмитрий Шевцов (@screatorpro)
# Подробности смотрите в README.rst.

import functools
from copy import deepcopy
from RepkaPi.constants import BOARD, BCM, SUNXI, SOC, REPKAPI3
import os


class _sunXi(object):

    def __getitem__(self, value):

        offset = ord(value[1]) - 65
        pin = int(value[2:])

        assert value[0] == "P"
        assert 0 <= offset <= 25
        assert 0 <= pin <= 31

        return (offset * 32) + pin

class _SOC(object):

    def __getitem__(self, value):

        return value

_board_model = {
    'Repka-Pi3-H5': REPKAPI3
}

_pin_map = {
    # pin number = (положение буквы в алфавите - 1) * 32 + номер пина
    # Пример, PD14 будет 3 * 32 +14 = 110
    REPKAPI3: {
        # Версия платы
        0 : "Repka Pi 3",

        # Информация о плате
        1 : {'P1_REVISION': 3, 'TYPE': 'Repka Pi 3', 'MANUFACTURER': 'ИНТЕЛЛЕКТ', 'RAM': '1024M', 'REVISION': '', 'PROCESSOR': 'Allwinner H5'},

        # Контакт на гребенке к фактическому контакту SUNXI
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

        # Контакт BCM к фактическому контакту SUNXI
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

        SOC: _SOC()
    }
}


def get_gpio_pin(board, mode, channel):
    assert mode in [BOARD, BCM, SUNXI, SOC]
    assert board in [REPKAPI3]
    return _pin_map[board][mode][channel]

def get_name(board):
    assert board in [REPKAPI3]
    return _pin_map[board][0]

def get_info(board):
    if board not in [REPKAPI3]:
        raise RuntimeError("Не выбранна модель платы. Для выбора модели платы используйте метод setboard()")

    info = _pin_map[board][1]
    mem = os.popen("cat /proc/meminfo | grep -i 'memtotal' | grep -o '[[:digit:]]*'").read().strip()

    ram=int(mem)/1024
    if ram > 1024 and ram < 2048:
        info['RAM'] = "2GB"
    else:
        info['RAM'] = "1GB"

    return info

def get_board():
    with open('/proc/device-tree/model', 'r') as f:
            model = f.read().strip().rstrip('\x00')
        
    if model not in _board_model:
        raise RuntimeError("Не выбранна модель платы. Для выбора модели платы используйте метод setboard()")

    return _board_model[model]

