from BaseDriver.Driver import appiumDriver
from Helper.elementLoader import elementLoader
import time
import datetime
from selenium.common.exceptions import NoSuchElementException

class playMusic(elementLoader):
    driver = appiumDriver() 
        
    def __init__(self):       
        elementLoader.__init__(self, self.__class__.__name__)
    
    def restartApp(self):
        return self.driver.restartAPP()
        
    def accessFirstItemInEditorSuggestion(self):
        '''进入编辑推荐的第一个栏目'''
        timeOut = 20
        d1 = datetime.datetime.now()
        d2 = datetime.datetime.now()
        while (d2-d1).seconds<timeOut:
            try:
                firstItemInEditorSuggestion = self.driver.instantFindElement(self.locator("firstItemInEditorSuggestion"))
                self.driver.click(firstItemInEditorSuggestion)
                break
            except NoSuchElementException:
                try:
                    lo = ("id", "com.hongfans.rearview:id/tv_autoTest")
                    self.driver.instantFindElement(lo)
                    raise BaseException("网络加载超时, 请人工验证此条用例")
                except Exception:
                    '''每次滑动100像素，粒度小，精度越高'''
                    self.driver.swipe(300,400,300,300,800)
                    d2 = datetime.datetime.now()
        
    def getPlayStatus(self, timeDelay=20):
        '''播放状态返回True， 暂停状态返回False'''
        time.sleep(timeDelay)
        e = self.driver.findElement(self.locator("btnPlayOrPause"))
        sts = e.get_attribute("name")
        print("当前播放状态为:%s" % sts)
        if sts=="播放":
            return True
        else:
            return False
            
    def switchPlayStatus(self):
        '''切换播放状态: 播放->暂停, 暂停->播放'''
        btnplayOrPause = self.driver.findElement(self.locator("btnPlayOrPause"))
        self.driver.click(btnplayOrPause)
    
    def getCurrentPlayingItemName(self):
        '''获取当前正在播放的曲目名称'''
        time.sleep(5)
        currentPlayingItem = self.driver.findElement(self.locator("currentPlayingItem"))
        currentPlayingItemName = currentPlayingItem.get_attribute("text")
        for i in range(20):
            if currentPlayingItemName.strip()=="听你想听":
                try:
                    lo = ("id", "com.hongfans.rearview:id/tv_autoTest")
                    self.driver.instantFindElement(lo)
                    raise BaseException("网络加载超时, 请人工验证此条用例")
                except Exception:
                    time.sleep(1)
                    currentPlayingItem = self.driver.findElement(self.locator("currentPlayingItem"))
                    currentPlayingItemName = currentPlayingItem.get_attribute("text")
            else:
                return currentPlayingItemName
            
        raise BaseException("20秒内自动播放失败")
    
    def playNextItem(self):
        '''下一曲'''
        btnNextItem = self.driver.findElement(self.locator("btnNextItem"))
        self.driver.click(btnNextItem)
    
    def playPreItem(self):
        '''上一曲'''
        btnPreItem = self.driver.findElement(self.locator("btnPreItem"))
        self.driver.click(btnPreItem)
        
    def getPlayList(self):
        '''获取播放列表的全部歌曲名'''
        playL = []
        playList = self.driver.findElements(self.locator("playList"))
        for i in playList:
            if i.get_attribute("text")!='专辑详情':
                playItemName = i.get_attribute("text")
                playL.append(playItemName)
        return playL
    
    def getPlayHistoryInPop(self):
        '''获取播放历史列表'''
        playHistory = []
        itemsInPlayHistoryInPop = self.driver.findElements(self.locator("itemsInPlayHistoryInPop"), allowNoneList=True)
        for i in itemsInPlayHistoryInPop:
            itemName = i.get_attribute("text")
            playHistory.append(itemName)
        return playHistory
    
    def accessPopPlayList(self):
        '''打开弹出框以获得播放列表和播放历史'''
        btnPlayList = self.driver.findElement(self.locator("btnPlayList"))
        self.driver.click(btnPlayList)
    
    def accessPopPlayHistory(self):
        '''进入历史收听列表'''
        self.accessPopPlayList()
        playHistoryInPop = self.driver.findElement(self.locator("tabPlayHistoryInPop"))
        self.driver.click(playHistoryInPop)
        
    def getPlayListInPop(self):
        '''在弹出框中获取播放列表的全部歌曲名'''
        self.accessPopPlayList()
        playL = []
        playList = self.driver.findElements(self.locator("playListInPop"))
        for i in playList:
            playItemName = i.get_attribute("text")
            playL.append(playItemName)
        return playL
    
    def deleteHistory(self):
        '''删除历史歌曲'''
        btnDeleteHistory = self.driver.findElement(self.locator("btnDeleteHistory"))
        self.driver.click(btnDeleteHistory)
        
    def getPlayHistoryCount(self):
        '''获取历史歌曲数量'''
        playHistoryCount = self.driver.findElement(self.locator("playHistoryCount"))
        return int(playHistoryCount.get_attribute("text").replace("共", "").replace("首", ""))

    def switch_play_quality(self, quality, isMembership = False):
        musicQuality = self.driver.findElement(self.locator("musicQuality"))
        self.driver.click(musicQuality)
        musicQualityDetail = self.driver.findElement(self.locator("musicQualityDetail", quality))
        self.driver.click(musicQualityDetail)
        if isMembership:
            confirmMusicQualitySetting = self.driver.findElement(self.locator("confirmMusicQualitySetting"))
            self.driver.click(confirmMusicQualitySetting)
            musicQuality = self.driver.findElement(self.locator("musicQuality"))
            currentQuality = musicQuality.get_attribute("text")
            assert currentQuality ==quality, "设置播放音质失败, 期望:%s, 当前: %s" %(quality, currentQuality)