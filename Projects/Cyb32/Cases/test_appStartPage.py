# _*_ coding=utf-8 _*_
from Projects.Cyb32.Pages.appStartPage import appStartPage
from Projects.Cyb32.Pages.pageBase import pageBase
import unittest
import datetime
from unittest.case import skip


class test_appStartPage(unittest.TestCase): 
    '''app启动'''       
    appStartPage = appStartPage()
    pageBase = pageBase()
    
    def tearDown(self):
        self.appStartPage.restartApp()

    @skip
    def test_skipAdd(self):
        '''跳过广告 '''
        self.appStartPage.skipAdd()

    def test_accessHomePageWithin6Seconds(self):
        '''6秒内进入首页'''
        t1 = datetime.datetime.now()
        self.pageBase.ignoreTip()
        t2 = datetime.datetime.now()
        dur = (t2-t1).seconds
        assert dur<=6, "进入首页时间超过6秒，实际为%d秒" % dur
