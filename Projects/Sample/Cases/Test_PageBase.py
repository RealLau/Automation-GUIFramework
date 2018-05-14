# _*_ coding=utf-8 _*_
from Projects.Sample.Pages.PageBase import PageBase
import unittest
from BaseDriver.Driver import AutoDriver


class Test_PageBase(unittest.TestCase):
    PageBase = PageBase()
    config_user_2 = PageBase.get_config_user_info(2)
    email = config_user_2["email"]
    pwd = config_user_2["pwd"]

    def setUp(self):
        self.PageBase.login(self.email, self.pwd)

    @AutoDriver.restart_browser
    def tearDown(self):
        pass

    def test_verify_nickname(self):
        expected_nickname = self.PageBase.get_config_user_info(2)["nickname"]
        actual_nickname = self.PageBase.get_current_user_nickname()
        assert expected_nickname == actual_nickname, "登录后用户昵称校验失败, 期望: %s, 实际: %s" % (expected_nickname, actual_nickname)


