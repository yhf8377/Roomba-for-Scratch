# Roomba for Scratch provides an easy-to-use extension to the Scratch
# project (https://scratch.mit.edu) for controlling the Roomba  robots.
# Copyright (C) 2018  Frank Ye

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from serial import Serial

def __worker(uart, data):
    uart.write(data)

class UARTDevice:
    """
    Defines the UART Device on Raspberry Pi
    """

    def __init__(self):
        self.uart = Serial('/dev/ttyAMA0', baudrate=115200,
                           timeout=0, write_timeout=0)

    def send(self, data):
        self.uart.write(data)
