# _*_ coding=utf-8 _*_
from Projects.Cyb32.Pages.signPage import signPage
from Projects.Cyb32.Pages.pageBase import pageBase
import unittest
    
class test_signPage(unittest.TestCase):
    '''登录'''        
    signPage = signPage()
    pageBase = pageBase()
    
    def setUp(self):
        self.pageBase.ignoreTip()
    
    def tearDown(self):
            self.signPage.restartApp()
        
    def test_signIn(self):
        '''登录'''
        self.signPage.signIn()

