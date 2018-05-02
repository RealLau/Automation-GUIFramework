# _*_ coding=utf-8 _*_
from Projects.Cyb32.Pages.myFavorites import myFavorites
import unittest
from Projects.Cyb32.Pages.textSearch import textSearch
from Projects.Cyb32.Pages.signPage import signPage
from Projects.Cyb32.Pages.pageBase import pageBase

class test_myFavorites(unittest.TestCase): 
    '''我的收藏'''       
    myFavorites = myFavorites()
    textSearch = textSearch()
    signPage = signPage()
    pageBase = pageBase()
    
    def setUp(self):
        self.pageBase.ignoreTip()
    
    def tearDown(self):
        self.myFavorites.restartApp()

    def test_favoriteAlbum(self):
        '''专辑收藏'''
        itemName = "盗墓笔记"
        self.myFavorites.accessTabMyFavorites()
        self.myFavorites.cancelAllFavoriteOnItems()
        self.myFavorites.refreshMyFavorites()
        before = self.myFavorites.getItemsCollection()
        assert itemName not in before, "取消收藏的歌曲失败"
        self.textSearch.accessSearchPage()
        self.textSearch.doSearch("item", itemName)
        firstResultInSearch = self.textSearch.accessTheFirstSearchoutItem()
        self.textSearch.setFavoriteOnItem(True)
        self.myFavorites.backToHomePage()
        self.textSearch.backToHomePage()
        self.myFavorites.refreshMyFavorites()
        after = self.myFavorites.getItemsCollection()
        assert firstResultInSearch in after, "收藏专辑失败, 当前已收藏的专辑为: %s" % after
        self.myFavorites.cancelFavoriteOnItem(firstResultInSearch)
        self.myFavorites.refreshMyFavorites()
        now = self.myFavorites.getItemsCollection()
        assert now == [], "清理环境失败. 当前还有已收藏的专辑: %s" % now

    def test_favoriteSong(self):
        '''单曲收藏'''
        song = "一千个伤心的理由"
        self.myFavorites.accessTabMyFavorites()
        self.myFavorites.accessSongsCollection()
        self.myFavorites.cancelAllFavoriteOnSongs()
        self.myFavorites.backToHomePage()
        self.textSearch.accessSearchPage()
        self.textSearch.doSearch("song", song)
        self.textSearch.playTheFirstSeachoutSong()
        self.myFavorites.switchFavoriteOnSong()
        self.pageBase.back()
        self.myFavorites.accessSongsCollection()
        songsColletions = self.myFavorites.getSongsCollection()
        assert [song] == songsColletions, "验证失败: 当前已收藏歌曲为%s" % songsColletions
        self.myFavorites.cancelAllFavoriteOnSongs(True)


