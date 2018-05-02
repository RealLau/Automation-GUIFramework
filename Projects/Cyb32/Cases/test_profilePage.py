# _*_ coding=utf-8 _*_
from Projects.Cyb32.Pages.profilePage import profilePage
import unittest
from Projects.Cyb32.Pages.signPage import signPage
from Projects.Cyb32.Pages.pageBase import pageBase
from Projects.Cyb32.Pages.settings import settings
from unittest.case import skip

class test_profilePage(unittest.TestCase):
    '''个人中心'''        
    profilePage = profilePage()
    signPage = signPage()
    pageBase = pageBase()
    settings = settings()
    
    def setUp(self):
        self.pageBase.ignoreTip()
    
    def tearDown(self):
        self.profilePage.restartApp()

    def test_clearCache(self):
        '''清除缓存'''
        self.signPage.signIn()
        self.settings.accessSetting("缓存信息")
        self.profilePage.accessCacheInfo()
        self.profilePage.clearCache()

    def test_editNickName(self):
        '''编辑用户昵称'''
        afterChangeName = 'Change'
        self.signPage.signIn()
        self.profilePage.accessProfileEditPage()
        self.profilePage.editUserNick(afterChangeName)
        newNickName = self.profilePage.getUserNickName()
        assert newNickName==afterChangeName, "修改昵称失败. 期望: %s, 实际: %s" % (afterChangeName, newNickName)
        self.profilePage.setUserNickNameToDefault()

    def test_signOut(self):
        '''退出登录'''
        self.signPage.signIn()
        self.profilePage.openProfile()
        self.profilePage.exitLogin()
        status = self.signPage.getLoginStatus()
        assert not status, "退出登录失败"

