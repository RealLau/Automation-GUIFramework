# _*_ coding=utf-8 _*_
from Projects.Cyb32.Pages.onlineMusic import onlineMusic
from Projects.Cyb32.Pages.pageBase import pageBase
import unittest

class test_onlineMusic(unittest.TestCase):   
    '''在线音乐'''     
    onlineMusic = onlineMusic()
    pageBase = pageBase()
    
    def setUp(self):
        self.pageBase.ignoreTip()
        
    def tearDown(self):
        self.onlineMusic.restartApp()
    
    def test_canAccessRightGedan(self):
        '''进入正确的歌单'''
        self.onlineMusic.accessOnlineMusic()
        self.onlineMusic.accessSubTab("歌单分类")
        detailGedanName = "儿童"
        self.onlineMusic.accessSubCatoryOfGedanfenlei("主题", detailGedanName )
        actualGedanName = self.onlineMusic.getCurrentGedanName()
        assert actualGedanName==detailGedanName, "进入的歌单与预期不一致. 预期: %s, 实际: %s" % (detailGedanName, actualGedanName)