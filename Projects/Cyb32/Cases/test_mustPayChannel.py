# _*_ coding=utf-8 _*_

from Projects.Cyb32.Pages.mustPayChannel import mustPayChannel
from Projects.Cyb32.Pages.pageBase import pageBase
from Projects.Cyb32.Pages.signPage import signPage
from Projects.Cyb32.Pages.playMusic import playMusic
from Projects.Cyb32.Pages.download import download
from Projects.Cyb32.Pages.localMusic import localMusic
from Projects.Cyb32.Pages.tabFindMusic import tabFindMusic
from Projects.Cyb32.Pages.textSearch import textSearch
from Projects.Cyb32.Pages.onlineFM import onlineFM
import unittest


class test_mustPayChannel(unittest.TestCase):        
    '''付费专区'''
    mustPayChannel = mustPayChannel()
    pageBase = pageBase()
    signPage = signPage()
    playMusic = playMusic()
    download = download()
    localMusic = localMusic()
    tabFindMusic = tabFindMusic()
    textSearch = textSearch()
    onlineFM = onlineFM()

    def setUp(self):
        self.pageBase.ignoreTip()
    
    def tearDown(self):
        self.mustPayChannel.restartApp()
    
    def test_buyAllInItem(self):
        '''专辑整个购买'''
        self.signPage.signIn(2)
        self.onlineFM.accessonlineFM()
        self.onlineFM.accessTopMenu("付费节目")
        self.pageBase.accessFirstItemInFuFeiJingPin()
        self.mustPayChannel.buy()
        assert self.pageBase.hasWebView()
        self.mustPayChannel.back()

    def test_buyOneItem(self):
        '''节目专辑单集购买'''
        self.signPage.signIn(2)
        itemName = "麻衣神算子"
        self.textSearch.doSearch("item", searchContent = itemName)
        self.textSearch.accessTheFirstSearchoutItem(has_add=False)
        self.mustPayChannel.buy(item_type=1)
        assert self.pageBase.hasWebView()
        self.mustPayChannel.back()

    def test_trailPlay(self):
        '''试听节目可以直接播放'''
        self.signPage.signIn(1)
        itemName = "麻衣神算子"
        self.textSearch.doSearch("item", searchContent=itemName)
        self.textSearch.accessTheFirstSearchoutItem(has_add=False)
        sts = self.playMusic.getPlayStatus(timeDelay=10)
        assert sts==True, "10秒内自动播放试听歌曲/节目失败, 可能因为网络原因"

    def test_trialCanDirectlyDownload(self):
        '''试听节目可以直接下载'''
        self.signPage.signIn(1)
        self.localMusic.accessLocalMusic()
        self.localMusic.switchTo("已下载节目")
        self.localMusic.clearDownloadedMusic()
        self.onlineFM.accessonlineFM()
        self.onlineFM.accessTopMenu("付费节目")
        self.pageBase.accessFirstItemInFuFeiJingPin()
        downloadSongName = self.download.downloadFirstSongInFuFeiZhuanQu()
        self.download.accessCurrentDownloading()
        self.download.pauseAllDownloadTask()
        l = self.download.getCurrentDownloading()
        if l == []:
            self.download.back()
            self.download.back()
            self.localMusic.accessLocalMusic()
            l = self.localMusic.getDownloadedMusic()
            assert downloadSongName in l, "下载失败"

        else:
            assert l == [downloadSongName], "正在下载: %s" % l
            sts = self.download.clearAllDownload()
            if isinstance(sts, BaseException):
                self.download.back()
                self.download.back()
                self.localMusic.accessLocalMusic()
                self.localMusic.clearDownloadedMusic()