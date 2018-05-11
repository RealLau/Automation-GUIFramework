# _*_ coding=utf-8 _*_
from Projects.Sample.Pages.PageNewDevice import PageNewDevice
from Projects.Sample.Pages.PageBase import PageBase
import unittest


class Test_PageNewDevice(unittest.TestCase):
    PageNewDevice = PageNewDevice()
    PageBase = PageBase()
    
    def setUp(self):
        self.PageBase.login("liushuangshuang@sunseagroup.com", "12369874")
        self.PageBase.access_Page("注册新设备")
    
    def tearDown(self):
        self.PageBase.logout()

    def test_verify_title(self):
        expected_title = "设备注册"
        actual_title = self.PageNewDevice.get_title()
        assert actual_title == expected_title, "注册新设备页面title校验失败, 期望: %s, 实际: %s" % (expected_title, actual_title)
