# _*_ coding=utf-8 _*_
from Projects.Cyb32.Pages.speakSearch import speakSearch
from Projects.Cyb32.Pages.pageBase import pageBase
import unittest
import datetime
from unittest.case import skip

class test_speakSearch(unittest.TestCase): 
    '''语音搜索'''       
    speakSearch = speakSearch()
    pageBase = pageBase()
    
    def setUp(self):
        self.pageBase.ignoreTip()
    
    def tearDown(self):
        self.speakSearch.restartApp()

    # @skip
    # def test_searchSinger(self):
    #     '''搜索歌手'''
    #     singer = "刘德华"
    #     defaultSong = "一起走过的日子"
    #     self.speakSearch.accessSpeakSearch()
    #     willSearch = self.speakSearch.speakWorlds(singer)
    #     print("即将搜索: %s" % willSearch)
    #     currentPlayingSong = self.speakSearch.getCurrentPlayingSong()
    #     timeOut = 10
    #     d1 = datetime.datetime.now()
    #     d2 = datetime.datetime.now()
    #     while (d2-d1).seconds<timeOut:
    #         if currentPlayingSong!=defaultSong:
    #             currentPlayingSong = self.speakSearch.getCurrentPlayingSong()
    #         else:
    #             return
    #         d2 = datetime.datetime.now()
    #     raise Exception("语音搜索失败: 10s内未发现歌手%s的默认歌曲: %s" % (singer, defaultSong))
    #
    # @skip
    # def test_searchSong(self):
    #     '''搜索歌曲'''
    #     songName = "一千个伤心的理由"
    #     self.speakSearch.accessSpeakSearch()
    #     willSearch = self.speakSearch.speakWorlds(songName)
    #     print("即将搜索: %s" % willSearch)
    #     currentPlayingSong = self.speakSearch.getCurrentPlayingSong()
    #     timeOut = 10
    #     d1 = datetime.datetime.now()
    #     d2 = datetime.datetime.now()
    #     while (d2-d1).seconds<timeOut:
    #         if currentPlayingSong!=songName:
    #             currentPlayingSong = self.speakSearch.getCurrentPlayingSong()
    #         else:
    #             return
    #         d2 = datetime.datetime.now()
    #     raise Exception("语音搜索失败: 10s内未发现播放目标歌曲: %s" % songName)
    #
    # @skip
    # def test_searchItem(self):
    #     '''搜索节目'''
    #     itemName = "盗墓笔记"
    #     defaultSearchItem = "牵绊"
    #     self.speakSearch.accessSpeakSearch()
    #     willSearch = self.speakSearch.speakWorlds(itemName)
    #     print("即将搜索: %s" % willSearch)
    #     currentPlayingSong = self.speakSearch.getCurrentPlayingSong()
    #     timeOut = 10
    #     d1 = datetime.datetime.now()
    #     d2 = datetime.datetime.now()
    #     while (d2-d1).seconds<timeOut:
    #         if defaultSearchItem not in currentPlayingSong:
    #             currentPlayingSong = self.speakSearch.getCurrentPlayingSong()
    #         else:
    #             return
    #         d2 = datetime.datetime.now()
    #     raise Exception("语音搜索失败: 10s内未发现播放目标节目(语音识别失败或网络错误): %s。 当前正在播放: %s" % (defaultSearchItem, currentPlayingSong))
