from odoo.addons.hw_drivers.tools.helpers import load_iot_handlers
from importlib import util
import os
from pathlib import Path

from odoo.modules.module import get_resource_path

def load_iot_handlers():
    """
    This method loads local files: 'odoo/addons/hw_drivers/iot_handlers/drivers' and
    'odoo/addons/hw_drivers/iot_handlers/interfaces' and also
    'user/drivers_module/drivers'
    And execute these python drivers and interfaces
    """
    for directory in ['interfaces', 'drivers']:
        path = get_resource_path('hw_drivers', 'iot_handlers', directory)
        filesList = os.listdir(path)
        for file in filesList:
            path_file = os.path.join(path, file)
            spec = util.spec_from_file_location(file, path_file)
            if spec:
                module = util.module_from_spec(spec)
                spec.loader.exec_module(module)
    ## Now look in this module
    """
    path = get_resource_path('my_module', 'drivers')
    filesList = os.listdir(path)
    for file in filesList:
            path_file = os.path.join(path, file)
            spec = util.spec_from_file_location(file, path_file)
            if spec:
                module = util.module_from_spec(spec)
                spec.loader.exec_module(module)
    """
    ##
    http.addons_manifest = {}
    http.root = http.Root()