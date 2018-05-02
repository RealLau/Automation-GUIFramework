# _*_ coding=utf-8 _*_
from Projects.Cyb32.Pages.tabFindMusic import tabFindMusic
from Projects.Cyb32.Pages.pageBase import pageBase
import unittest

class test_tabFindMusic(unittest.TestCase):    
    '''发现音乐'''    
    tabFindMusic = tabFindMusic()
    pageBase = pageBase()
    
    def setUp(self):
        self.pageBase.ignoreTip()
        
    def tearDown(self):
        self.tabFindMusic.restartApp()
        
    # def test_loadHomePage(self):
    #     '''标签：发现音乐'''
    #     resultFindEditorSuggestion = self.tabFindMusic.loadEditorSuggestion()
    #     assert resultFindEditorSuggestion, "发现音乐标签下，查找'编辑推荐'失败"