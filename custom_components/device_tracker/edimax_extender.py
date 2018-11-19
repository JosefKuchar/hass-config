import logging

import urllib.request
import re
import voluptuous as vol
import base64

import homeassistant.helpers.config_validation as cv
from homeassistant.components.device_tracker import (
    DOMAIN, PLATFORM_SCHEMA, DeviceScanner)
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_USERNAME, default='admin'): cv.string,
    vol.Optional(CONF_PASSWORD, default='1234'): cv.string,
})

def get_scanner(hass, config):
    scanner = EdimaxExtenderScanner(config[DOMAIN])
    return scanner

class EdimaxExtenderScanner(DeviceScanner):
    def __init__(self, config):
        self.host = config[CONF_HOST]
        self.username = config[CONF_USERNAME]
        self.password = config[CONF_PASSWORD]

    def scan_devices(self):
        encoded = base64.b64encode(('%s:%s' % (self.username, self.password)).encode())
        url = "http://%s/wlstatblRepeater.asp" % self.host
        hdr = {'Authorization' : 'Basic %s' % encoded.decode("utf-8")}
        req = urllib.request.Request(url, headers=hdr)
        response = urllib.request.urlopen(req)
        macs = re.findall(r'<tr class="table3"><td>(.*?)</td>', str(response.read()))
        return macs[:-1]

    def get_device_name(self, device):
        return None

