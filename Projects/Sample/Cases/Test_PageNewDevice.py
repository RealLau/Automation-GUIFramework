# _*_ coding=utf-8 _*_
from Projects.Sample.Pages.PageNewDevice import PageNewDevice
from Projects.Sample.Pages.PageBase import PageBase
import unittest
from BaseDriver.Driver import AutoDriver


class Test_PageNewDevice(unittest.TestCase):
    PageNewDevice = PageNewDevice()
    PageBase = PageBase()

    def setUp(self):
        self.PageBase.login("ltest", "123456")
        self.PageBase.access_Page("注册新设备")

    @AutoDriver.restart_browser
    def tearDown(self):
        pass

    def test_verify_title(self):
        expected_title = "设备注册"
        actual_title = self.PageNewDevice.get_title()
        assert actual_title == expected_title, "注册新设备页面title校验失败, 期望: %s, 实际: %s" % (expected_title, actual_title)
