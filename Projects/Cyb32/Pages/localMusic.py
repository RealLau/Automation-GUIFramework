from BaseDriver.Driver import appiumDriver
from Helper.elementLoader import elementLoader

class localMusic(elementLoader):
    driver = appiumDriver() 
        
    def __init__(self):       
        elementLoader.__init__(self, self.__class__.__name__)
    
    def restartApp(self):
        return self.driver.restartAPP()
    
    def accessLocalMusic(self):
        '''进入本地音乐'''
        tabLocalMusic = self.driver.findElement(self.locator("tabLocalMusic"))
        self.driver.click(tabLocalMusic)
    
    def clearDownloadedMusic(self):
        '''清除下载的音乐'''
        downloadedSongs = self.getDownloadedMusic()
        if downloadedSongs!=[]:
            btnsClearAll = self.driver.findElements(self.locator("btnClear"))
            for i in btnsClearAll:
                self.driver.click(i)
                btnConfirmClear = self.driver.findElement(self.locator("confirmClear"))
                self.driver.click(btnConfirmClear)
            btnPlayAll = self.driver.findElement(self.locator("btnPlayAll"))
            btnPlayAllText = btnPlayAll.get_attribute("text")
            assert btnPlayAllText=="播放全部", "删除所有歌曲失败"
        else:
            print("当前无已下载歌曲,无需清空")
        
    def refreshLocalMusic(self):
        '''通过切换至在线音乐再切回来,刷新本地音乐'''
        tabOnlineMusic = self.driver.findElement(self.locator("tabOnlineMusic"))
        self.driver.click(tabOnlineMusic)
        self.accessLocalMusic()
    
    def switchTo(self, tabName):
        '''切换已下载音乐/已下载界面/SD卡音乐'''
        tabName = self.driver.findElement(self.locator("tabName", tabName))
        self.driver.click(tabName)
    
    def getSDMusic(self):
        '''获取所有已缓存的SD卡歌曲名称, 先等待20秒，保证如果是sd卡页签下音乐能够加载成功'''
        import time
        time.sleep(20)
        
        l = []
        SDMusicTitles = self.driver.findElements(self.locator("SDMusicTitle"))
        for i in SDMusicTitles:
            titleName = i.get_attribute("text")
            if titleName!="歌曲名称":
                l.append(titleName)
        return l    
    
    def getDownloadedMusic(self):
        '''获取所有已经下载好的歌曲/节目'''
        songs = self.driver.findElements(self.locator("downloadedMusicTitle"))
        l = []
        for i in songs:
            '''防止多次下载歌曲, 自动重命名带来的歌曲名不匹配'''
            songName = i.get_attribute("text").split("(")[0]
            if songName!="歌曲名称" and songName!="名称":
                l.append(songName)
        return l
