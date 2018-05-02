# _*_ coding=utf-8 _*_
from Projects.Cyb32.Pages.localMusic import localMusic
import unittest
from Projects.Cyb32.Pages.textSearch import textSearch
from Projects.Cyb32.Pages.pageBase import pageBase

class test_localMusic(unittest.TestCase): 
    '''本地音乐'''       
    localMusic = localMusic()
    textSearch = textSearch()
    pageBase = pageBase()
    
    def setUp(self):
        self.pageBase.ignoreTip()
    
    def tearDown(self):
        self.localMusic.restartApp()
        
    def test_sdMusic(self):
        '''SD卡音乐'''
        self.localMusic.accessLocalMusic()
        self.localMusic.switchTo("SD卡音乐")
        l = self.localMusic.getSDMusic()
        assert l!=[], "获取SD卡音乐失败"
    