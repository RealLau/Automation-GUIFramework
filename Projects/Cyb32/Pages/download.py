from BaseDriver.Driver import appiumDriver
from Helper.elementLoader import elementLoader
import time
from Projects.Cyb32.Pages.playMusic import playMusic

class download(elementLoader):
    driver = appiumDriver()
    playMusic = playMusic()
    def __init__(self):
        elementLoader.__init__(self, self.__class__.__name__)

    def restartApp(self):
        return self.driver.restartAPP()

    def accessCurrentDownloading(self):
        '''进入正在下载'''
        btnDownload = self.driver.findElement(self.locator("btnsDownLoad"))
        self.driver.click(btnDownload)

    def startAllDownloadTask(self):
        '''开始所有下载任务'''
        btnStartAllDownload = self.driver.findElement(self.locator("btnStartAllDownload"))
        self.driver.click(btnStartAllDownload)

    def pauseAllDownloadTask(self):
        '''暂停所有下载'''
        btnPauseAllDownload = self.driver.findElement(self.locator("btnPauseAllDownload"))
        self.driver.click(btnPauseAllDownload)

    def getCurrentDownloading(self):
        '''获取当前正在下载的列表'''
        currentDownloadingItems = self.driver.instantFindElements(self.locator("currentDownloadingItem"))
        l = []
        for i in currentDownloadingItems:
            l.append(i.get_attribute("text").split("(")[0])
        return l

    def clearAllDownload(self):
        '''清除所有下载'''
        try:
            btnclearDownload = self.driver.findElement(self.locator("btnclearDownload"))
            self.driver.click(btnclearDownload)
            btnConfirmClearAllDownloads = self.driver.findElement(self.locator("btnConfirmClearAllDownloads"))
            self.driver.click(btnConfirmClearAllDownloads)
        except Exception as e:
            print("可能已经下载完成")
            return e

    def downloadSpecifiedSongInSearchResult(self, songName, singerName, timeDur):
        '''下载搜索出来的资源. resourceType: song, item'''
        btnDownLoad = self.driver.findElement(
            self.locator("btnDownloadInSpecifiedSongTimeSingerNameAndSongName", timeDur, singerName, songName))
        self.driver.click(btnDownLoad)

    def downloadSpecifiedItemInAlbum(self, item):
        '''下载专辑中的第几集(从上到下一次为1,2,3,...)'''
        btnsDownload = self.driver.findElements(self.locator("btnsDownLoad"))
        itemName = self.driver.findElements(self.locator("songsTitle"))
        count = 0
        for i in btnsDownload:
            if count == item:
                self.driver.click(btnsDownload[count])
                return itemName[count].get_attribute("text")
            else:
                count += 1

    def downloadFirstSongInWuSunYinYue(self, popBox=False):
        '''在无损音乐里下载第一个歌曲'''
        btnsDownLoad = self.driver.findElements(self.locator("btnsDownLoad"))
        i = 0
        for i in range(20):
            if len(btnsDownLoad) == 1:
                time.sleep(1)
                btnsDownLoad = self.driver.findElements(self.locator("btnsDownLoad"))
                continue
            else:
                break
        if i == 19:
            raise BaseException("未找到下载按钮, 可能由于网络问题页面加载失败")
        else:
            btnFirstDownload = btnsDownLoad[1]
            self.driver.click(btnFirstDownload)
            if popBox:
                self.selectMusicQualityInPopUp("高品质")
            self.driver.findElement(self.locator("downloadCompleted"))
            downloadSong = self.driver.findElements(self.locator("songsTitle"))
            downloadSongName = downloadSong[1].get_attribute("text")
            return downloadSongName

    def downloadFirstSongInFuFeiZhuanQuAndDoNOTWaitComplete(self, popBox=False):
        '''在付费专区里下载第一个歌曲不等待结束直接返回'''
        downloadSong = self.driver.findElements(self.locator("songsTitle"))
        downloadSongName = downloadSong[1].get_attribute("text")
        btnsDownLoad = self.driver.findElements(self.locator("btnsDownLoad"))
        i = 0
        for i in range(20):
            if len(btnsDownLoad) == 1:
                time.sleep(1)
                btnsDownLoad = self.driver.findElements(self.locator("btnsDownLoad"))
                continue
            else:
                break
        if i == 19:
            raise BaseException("未找到下载按钮, 可能由于网络问题页面加载失败")
        else:
            btnFirstDownload = btnsDownLoad[1]
            self.driver.click(btnFirstDownload)
            if popBox:
                self.selectMusicQualityInPopUp("高品质")
            return downloadSongName

    def downloadFirstSongInFuFeiZhuanQu(self, popBox=False):
        '''在付费专区里下载第一个歌曲'''
        downloadSong = self.driver.findElements(self.locator("songsTitle"))
        while len(downloadSong)==1:
            downloadSong = self.driver.findElements(self.locator("songsTitle"))
        downloadSongName = downloadSong[1].get_attribute("text")
        btnsDownLoad = self.driver.findElements(self.locator("btnsDownLoad"))
        i = 0
        for i in range(20):
            if len(btnsDownLoad) == 1:
                time.sleep(1)
                btnsDownLoad = self.driver.findElements(self.locator("btnsDownLoad"))
                continue
            else:
                break
        if i == 19:
            raise BaseException("未找到下载按钮, 可能由于网络问题页面加载失败")
        else:
            btnFirstDownload = btnsDownLoad[1]
            self.driver.click(btnFirstDownload)
            if popBox:
                self.selectMusicQualityInPopUp("高品质")
            return downloadSongName

    def selectMusicQualityInPopUp(self, musicQuality="标准"):
        '''在弹出框中选择音质'''
        btnMusicQuality = self.driver.findElement(self.locator("btnMusicQuality", musicQuality))
        self.driver.click(btnMusicQuality)
        btnConfirm = self.driver.findElement(self.locator("btnConfirm"))
        self.driver.click(btnConfirm)

    def back(self, backFromSearch=False):
        """回退一步"""
        btnBack = None
        if backFromSearch:
            btnBack = self.driver.findElement(self.locator("btnBackFromSearch"))
        else:
            btnBack = self.driver.findElement(self.locator("btnBack"))
        self.driver.click(btnBack)

    def downloadCurrentPlayingSong(self):
        # 下载正在播放的歌曲
        sts = self.playMusic.getPlayStatus()
        if not sts:
            raise BaseException("20秒内未自动播放")
        else:
            donwloadSongName = self.driver.findElement(self.locator("songNameInPlayer")).get_attribute("text").strip()
            downloadBtnInPlayer = self.driver.findElement(self.locator("downloadBtnInPlayer"))
            self.driver.click(downloadBtnInPlayer)
            return donwloadSongName
