# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from odoo.addons.hw_drivers.driver import Driver
import serial
import time

class Arduino(Driver):
    connection_type = 'serial'

    def __init__(self, identifier, device):
        super(Arduino, self).__init__(identifier, device)
        self._device_type = 'Arduino'
        self._device_connection = 'serial'
        self._device_name = 'Arduino'
        self.priority = 100
        self.ser = serial.Serial(identifier, 9600, timeout=1)#device['identifier']
        #identifier gives me Adams Scale, device['identifier'] makes me not show up at all
        self.ser.flush()

    def __del__(self):
        try:
            self.ser.close()
        except Exception:
            pass

    def connection_test(self):
        return True
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
        ser = serial.Serial(device['identifier'], 9600, timeout=1)#device['identifier']

        # Test connection Twice
        for x in range(0, 2):
            try:
                ser.write(b"S\n")
                time.sleep(0.2)
                answer = sser.readline().decode('utf-8').rstrip()#connection.read(8)
                if answer == "H":
                    ser.close()
                    return True
            except serial.serialutil.SerialTimeoutException:
                pass
            except Exception:
                pass
        ser.close()
        return True#False
        #return cls.connection_test() or cls.connection_test()