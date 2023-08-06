# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`isl29125`
================================================================================

CircuitPython driver for the ISL29125 Sensor


* Author(s): Jose D. Montoya

Implementation Notes
--------------------


* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register

"""

from micropython import const
from adafruit_bus_device import i2c_device
from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct

try:
    from busio import I2C
except ImportError:
    pass

__version__ = "0.1.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_isl29125.git"

_I2C_ADDR = const(0x44)
_REG_WHOAMI = const(0x00)
_CONFIG_1 = const(0x01)


class ISL29125:
    """Driver for the ISL29125 Light Sensor connected over I2C.

    :param ~busio.I2C i2c_bus: The I2C bus the ISL29125 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x44`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`ISL29125` class.
    First you will need to import the libraries to use the sensor

        .. code-block:: python

            import board
            import circuitpython_isl29125.isl29125 as isl29125

    Once this is done you can define your `board.I2C` object and define your sensor object

        .. code-block:: python

            i2c = board.I2C()  # uses board.SCL and board.SDA
            isl = isl29125.ISL29125(i2c)

    Now you have access to the :attr:`colors` attribute

        .. code-block:: python

            red, green, blue = isl.colors


    """

    _device_id = ROUnaryStruct(_REG_WHOAMI, "B")
    _device_config = UnaryStruct(_CONFIG_1, "B")

    _g_LSB = ROUnaryStruct(0x09, "B")
    _g_MSB = ROUnaryStruct(0x0A, "B")
    _r_LSB = ROUnaryStruct(0x0B, "B")
    _r_MSB = ROUnaryStruct(0x0C, "B")
    _b_LSB = ROUnaryStruct(0x0D, "B")
    _b_MSB = ROUnaryStruct(0x0E, "B")

    def __init__(self, i2c_bus: I2C, address: int = _I2C_ADDR) -> None:
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)

        if self._device_id != 0x7D:
            raise RuntimeError("Failed to find ISL29125")

        self._device_config = 0x0D

    @property
    def green(self):
        """Green property"""

        return self._g_MSB * 256 + self._g_LSB

    @property
    def red(self):
        """red property"""

        return self._r_MSB * 256 + self._r_LSB

    @property
    def blue(self):
        """blue property"""

        return self._b_MSB * 256 + self._b_LSB

    @property
    def colors(self):
        """colors property"""

        return self.red, self.green, self.blue
