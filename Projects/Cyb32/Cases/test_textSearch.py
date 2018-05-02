# _*_ coding=utf-8 _*_
from Projects.Cyb32.Pages.textSearch import textSearch
from Projects.Cyb32.Pages.pageBase import pageBase
import unittest

class test_textSearch(unittest.TestCase): 
    '''文本搜索'''       
    textSearch = textSearch()
    pageBase = pageBase()
    
    def setUp(self):
        self.pageBase.ignoreTip()
    
    def tearDown(self):
        self.textSearch.restartApp()
    
    def test_searchSinger(self):
        '''搜索歌手'''
        singerName = '刘德华'
        resultSearchSinger = self.textSearch.doSearch('singer', singerName)
        assert resultSearchSinger==singerName, "搜索结果错误，预期: %s, 实际：%s" % (singerName, resultSearchSinger)
         
    def test_searchSong(self):
        '''搜索歌曲'''
        songName = '冰雨'
        resultSearchSong = self.textSearch.doSearch('song', songName)
        assert resultSearchSong==songName, "搜索结果错误，预期: %s, 实际：%s" % (songName, resultSearchSong)
               
    def test_searchItem(self):
        '''搜索节目'''
        itemName = '盗墓笔记'
        resultSearchItem = self.textSearch.doSearch('item', itemName)
        assert itemName in resultSearchItem, "搜索结果错误，预期: %s, 实际：%s" % (itemName, resultSearchItem)
        
    def test_getSuggestions(self):
        '''换一批功能'''
        self.textSearch.accessSearchPage()
        self.textSearch.waitForBtnSearchAppear()
        beforChange = self.textSearch.getSearchSuggestions()
        assert beforChange!=[], "换一批之前，推荐搜索为空"
        self.textSearch.doChangeSuggestions()
        afterChange = self.textSearch.getSearchSuggestions()
        assert afterChange!=[], "换一批之后，推荐搜索为空"
        for i in afterChange:
            assert i not in beforChange, "重复的搜索推荐: %s" % i
       
    def test_deleteSearchHistory(self):
        '''删除历史搜索记录'''
        self.textSearch.doSearch("song", "一千个伤心的理由")
        self.textSearch.backToHomePage()
        self.textSearch.accessSearchPage()
        records = self.textSearch.getSearchHistory()
        assert records!=[], "搜索记录为空"
        self.textSearch.deleteSearchHistory()
        records = self.textSearch.getSearchHistory()
        assert records==[], "删除搜索记录失败"
   
    def test_researchInSearchRecord(self):
        '''历史搜索触发重新搜索'''
        songName = "冰雨"
        self.textSearch.doSearch("song", songName)
        self.textSearch.backToHomePage()
        resultSearchSong = self.textSearch.doResearch('song', songName)
        assert resultSearchSong==songName, "搜索结果错误，预期: %s, 实际：%s" % (songName, resultSearchSong)
