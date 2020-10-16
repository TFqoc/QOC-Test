#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 12:02:08 2020

@author: tristanfullmer
"""
import logging
import serial
import time

from odoo.addons.hw_drivers.controllers.driver import Driver
from odoo.addons.hw_drivers.iot_handlers.drivers import SerialDriver, SerialProtocol, serial_connection
from odoo.addons.hw_drivers.controllers.driver import event_manager

_logger = logging.getLogger(__name__)

class ArduinoDriver(SerialDriver):
    connection_type = 'usb'

    def __init__(self, device):
        super(ArduinoDriver, self).__init__(device)
        self._device_type = 'Arduino'
        self._device_connection = 'serial'
        self._device_name = 'Arduino'

    @classmethod
    def supported(cls, device):
        """Checks whether the device at `device` is supported by the driver.
    
        :param device: path to the device
        :type device: str
        :return: whether the device is supported by the driver
        :rtype: bool
        """
    
        protocol = cls._protocol
    
        try:
            with serial_connection(device['identifier'], protocol, is_probing=True) as connection:
                connection.write(b'S' + protocol.commandTerminator)
                time.sleep(protocol.commandDelay)
                answer = connection.read(8)
                if answer == b'H':
                    #connection.write(b'F' + protocol.commandTerminator)
                    return True
        except serial.serialutil.SerialTimeoutException:
            pass
        except Exception:
            _logger.exception('Error while probing %s with protocol %s' % (device, protocol.name))
        return False
    
    def _take_measure(self):
        self._connection.write(b'I' + protocal.commandTerminator)
        time.sleep(protocol.commandDelay)
        answer = connection.read(8)
        self.data['value'] = chr(int(answer))
        event_manager.device_changed(self)
