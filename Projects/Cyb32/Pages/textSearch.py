from BaseDriver.Driver import appiumDriver
from Helper.elementLoader import elementLoader
import time

class textSearch(elementLoader):
    driver = appiumDriver() 
        
    def __init__(self):       
        elementLoader.__init__(self, self.__class__.__name__)
    
    def restartApp(self):
        return self.driver.restartAPP()
    
    def doSearch(self, searchType, searchContent):
        '''searchType: song=歌曲, singer=歌手，item=节目'''
        self.accessSearchPage()
        searchBox = self.driver.findElement(self.locator("searchBox"))
        self.driver.sendKeys(searchBox, searchContent)
        btnSearch = self.driver.findElement(self.locator("btnSearch"))
        self.driver.click(btnSearch)
        if searchType=="song":
            firstSong = self.driver.findElement(self.locator("firstSongInSearchResult"))
            firstSongName = firstSong.get_attribute("text")
            return firstSongName
        elif searchType=="singer":
            singers = self.driver.findElements(self.locator("singers"))
            firstSingerName = singers[1].get_attribute("text")
            return firstSingerName
        elif searchType == "item":
            itemControl = self.driver.findElement(self.locator("itemControl"))
            self.driver.click(itemControl)
            firstItem = self.driver.findElement(self.locator("firstItemInSearchResult"))
            firstItemName = firstItem.get_attribute("text")
            return firstItemName
        else:
            raise Exception("搜索类型错误:'searchType' should be one of 'song', 'singer', 'item'.")
    
    def accessSpecifiedItemInSearchResult(self, itemName):
        specifiedItemInSearchResult = self.driver.findElement(self.locator("specifiedItemInSearchResult", itemName))
        self.driver.click(specifiedItemInSearchResult)
    
    def playTheFirstSeachoutSong(self, playTimeDur=0):
        '''播放第一首搜索出来的歌, playTimeDur: 播放时长(单位秒)'''
        firstSongInSearchResult = self.driver.findElement(self.locator("firstSongInSearchResult"))
        self.driver.click(firstSongInSearchResult)
        '''延时20秒，保证歌曲广告时间已经跳过'''
        adTime = 10
        d = playTimeDur+adTime
        time.sleep(d)
    
    def accessTheFirstSearchoutItem(self, has_add=False):
        '''播放第一个搜索出来的栏目(专辑或节目), 非单首歌曲'''
        firstItemName = self.driver.findElements(self.locator("itemNameInSearchResult"))[0].get_attribute("text")
        firstItemInSearchResult = self.driver.findElement(self.locator("firstItemInSearchResult"))
        self.driver.click(firstItemInSearchResult)
        if has_add:
            '''延时20秒，保证歌曲广告时间已经跳过'''
            time.sleep(20)
        return firstItemName
        
    def getSearchSuggestions(self):
        '''获取所有推荐的搜索项目'''
        suggesionsElements = self.driver.findElements(self.locator("searchSuggestions"))
        suggestions = []
        for i in suggesionsElements:
            t = i.get_attribute("text")
            suggestions.append(t)
        return suggestions
    
    def accessSearchPage(self):
        '''进入搜索页面'''
        searchBox = self.driver.findElement(self.locator("searchBox"))
        self.driver.click(searchBox)
    
    def waitForBtnSearchAppear(self):
        '''等待换一批按钮出现'''
        self.driver.findElement(self.locator("btnChangeSearchSuggestions"))
        
    def doChangeSuggestions(self):
        '''点击换一批按钮'''
        btnChangeSuggesions = self.driver.findElement(self.locator("btnChangeSearchSuggestions"))
        self.driver.click(btnChangeSuggesions)
    
    def backToHomePage(self):
        '''回到首页'''
        btnBack = self.driver.findElement(self.locator("btnBack"))
        self.driver.click(btnBack)
        self.driver.findElement(self.locator("findSound"))
        
    def getSearchHistory(self):
        '''获取搜索历史列表'''
        historyElements = self.driver.findElements(self.locator("searchHistoryRecord"), allowNoneList=True)
        histories = []
        for i in historyElements:
            histories.append(i.get_attribute("text"))
        return histories
    
    def deleteSearchHistory(self):
        '''删除搜索历史'''
        btnDeleteSearchRecords = self.driver.findElement(self.locator("deleteSearchRecords"))
        self.driver.click(btnDeleteSearchRecords)
    
    def doResearch(self, searchType, searchContent):
        '''搜索. 搜索类型: song->歌曲, singer->歌手, item->栏目/专辑, searchContent->搜索内容'''
        self.accessSearchPage()
        historyElements = self.driver.findElements(self.locator("searchHistoryRecord"))
        for i in historyElements:
            if i.get_attribute("text")==searchContent:
                self.driver.click(i)
                if searchType=="song":
                    firstSong = self.driver.findElement(self.locator("firstSongInSearchResult"))
                    firstSongName = firstSong.get_attribute("text")
                    return firstSongName
                elif searchType=="singer":
                    firstSinger = self.driver.findElement(self.locator("firstSingerInSearchResult"))
                    firstSingerName = firstSinger.get_attribute("text")
                    return firstSingerName
                elif searchType=="item":
                    firstItem = self.driver.findElement(self.locator("firstItemInSearchResult"))
                    firstItemName = firstItem.get_attribute("text")
                    return firstItemName
                else:
                    raise Exception("搜索类型错误:'searchType' should be one of 'song', 'singer', 'item'.")
                break
    
    def setFavoriteOnItem(self, flag):
        '''收藏/取消收藏. flag: True->收藏, False->取消收藏'''
        '''变换当前专辑栏目(非单曲)的收藏状态: flag=True:未收藏->已收藏; flag=False, 已收藏->未收藏'''
        t = None
        if flag:
            t = "点击收藏"
        else:
            t = "已收藏"
        e = self.driver.findElement(self.locator("btnClickToCollection", t))
        self.driver.click(e)
    