import unittest
from BubotObj.OcfDevice.subtype.WebServer.WebServer import WebServer as Device
import logging
from Bubot.Core.TestHelper import async_test, wait_run_device, get_config_path


class TestBasic(unittest.TestCase):
    @async_test
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.device = Device.init_from_config()

    @async_test
    def test_init_without_config(self):
        a = 1
        pass
