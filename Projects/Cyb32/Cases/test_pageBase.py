# _*_ coding=utf-8 _*_

from Projects.Cyb32.Pages.pageBase import pageBase
import unittest

class test_pageBase(unittest.TestCase):        
    pageBase = pageBase()
    
    def tearDown(self):
        self.pageBase.restartApp()
        