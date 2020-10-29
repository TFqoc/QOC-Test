# -*- coding: utf-8 -*-

from odoo.addons.hw_drivers.driver import Driver
import serial
import time

class Arduino(Driver):
    connection_type = 'serial'

    def __init__(self, identifier, device):
        super(ArduinoDriver, self).__init__(identifier, device)
        self._device_type = 'Arduino'
        self._device_connection = 'serial'
        self._device_name = 'Arduino'
        self.priority = 10
        self.ser = serial.Serial(identifier, 9600, timeout=1)#device['identifier']
        #identifier gives me Adams Scale, device['identifier'] makes me not show up at all
        self.ser.flush()

    def __del__(self):
        try:
            self.ser.close()
        except Exception:
            pass

    def connection_test(self):
        try:
            self.ser.write(b"S\n")
            time.sleep(0.2)
            answer = self.ser.readline().decode('utf-8').rstrip()#connection.read(8)
            if answer == "H":
                return True
        except serial.serialutil.SerialTimeoutException:
            pass
        except Exception:
            pass
        return False

    @classmethod
    def supported(cls, device):
        return self.connection_test() or self.connection_test()