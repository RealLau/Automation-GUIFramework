# _*_ coding=utf-8 _*_
from Projects.Sample.Pages.PageBase import PageBase
import unittest


class Test_PageBase(unittest.TestCase):
    PageBase = PageBase()
    config_user_2 = PageBase.get_config_user_info(2)
    email = config_user_2["email"]
    pwd = config_user_2["pwd"]

    def setUp(self):
        self.PageBase.login(self.email, self.pwd)

    def tearDown(self):
        self.PageBase.logout()

    def test_verify_nickname(self):
        expected_nickname = self.PageBase.get_config_user_info(1)["nickname"]
        actual_nickname = self.PageBase.get_current_user_nickname()
        assert expected_nickname == actual_nickname, "注册新设备页面title校验失败, 期望: %s, 实际: %s" % (expected_nickname,
                                                                                           actual_nickname)

