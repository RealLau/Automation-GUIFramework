from BaseDriver.Driver import appiumDriver
from Helper.elementLoader import elementLoader
import time
class myFavorites(elementLoader):
    driver = appiumDriver() 
        
    def __init__(self):       
        elementLoader.__init__(self, self.__class__.__name__)
    
    def restartApp(self):
        return self.driver.restartAPP()
    
    def accessTabMyFavorites(self):
        '''进入我的收藏'''
        tabMyFavorites = self.driver.findElement(self.locator("tabMyFavorites"))
        self.driver.click(tabMyFavorites)
    
    def accessSongsCollection(self):
        '''进入单曲收藏列表'''
        songsCollection = self.driver.findElement(self.locator("songsCollection"))
        self.driver.click(songsCollection)
    
    def getCurrentPlayingItemStatus(self):
        '''获取当前播放的栏目的状态: 已收藏 -> True, 未收藏 -> False'''
        self.driver.findImageElement(self.locator("favorite"))
        s = self.driver.sameAsWithOpenCV("favorite")
        return s
    
    def switchFavoriteOnSong(self):
        '''变换当前正在播放的歌曲的收藏状态: 已收藏->未收藏, 未收藏->已收藏'''
        e = self.driver.findElement(self.locator("favorite"))
        self.driver.click(e)
    
    def getSongsCollection(self):
        '''获取歌曲收藏列表歌曲名称'''
        songNameInSongsCollection = self.driver.findElements(self.locator("songNameInSongsCollection"))
        l = []
        for i in songNameInSongsCollection:
            songname = i.get_attribute("text")
            if "单曲收藏" not in songname:
                l.append(songname)
        return l
    
    def backToHomePage(self):
        '''回到我的收藏主页'''
        backIcon = self.driver.findElement(self.locator("backIcon"))
        self.driver.click(backIcon)
        
    def getItemsCollection(self):
        '''获取收藏的栏目, 单曲除外'''
        time.sleep(20)
        l = []
        collectedItems = self.driver.findElements(self.locator("collectedItems"))
        for i in collectedItems:
            itemName = i.get_attribute("text")
            if itemName!='我的单曲收藏':
                l.append(itemName)
        return l
    
    def refreshMyFavorites(self):
        '''通过切换至在线音乐再切回来,刷新我的收藏'''
        tabOnlineMusic = self.driver.findElement(self.locator("tabOnlineMusic"))
        self.driver.click(tabOnlineMusic)
        self.accessTabMyFavorites()
        self.driver.findElement(self.locator("collectedItems"))
        
    def cancelFavoriteOnItem(self, itemName):
        time.sleep(10)
        '''取消收藏'''
        cancelFavorite = self.driver.findElement(self.locator("cancelFavorite", itemName))
        self.driver.click(cancelFavorite)
        
    def cancelAllFavoriteOnItems(self):
        '''取消收藏的所有节目'''
        time.sleep(10)
        cancelFavorites = self.driver.findElements(self.locator("cancelFavorites"), True)
        for i in cancelFavorites:
            self.driver.click(i)
            time.sleep(2)
    
    def cancelAllFavoriteOnSongs(self, playingSong=False):
        time.sleep(10)
        '''取消收藏所有歌曲'''
        favoriteSongs = self.driver.findElements(self.locator("favorite"), allowNoneList=True)
        if playingSong:
            favoriteSongs = favoriteSongs[:-1]
        while favoriteSongs!=[]:
            for i in favoriteSongs:
                self.driver.click(i)
                time.sleep(2)
            self.backToHomePage()
            self.accessSongsCollection()
            time.sleep(10)
            favoriteSongs = self.driver.findElements(self.locator("favorite"), allowNoneList=True)
            if playingSong:
                favoriteSongs = favoriteSongs[:-1]