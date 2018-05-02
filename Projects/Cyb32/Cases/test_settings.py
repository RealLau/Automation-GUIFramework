# _*_ coding=utf-8 _*_
from Projects.Cyb32.Pages.signPage import signPage
from Projects.Cyb32.Pages.settings import settings
from Projects.Cyb32.Pages.download import download
from Projects.Cyb32.Pages.textSearch import textSearch
from Projects.Cyb32.Pages.localMusic import localMusic
from Projects.Cyb32.Pages.pageBase import pageBase
from Projects.Cyb32.Pages.tabFindMusic import tabFindMusic
from Projects.Cyb32.Pages.onlineMusic import onlineMusic

import unittest


class test_settings(unittest.TestCase):  
    '''设置相关'''      
    signPage = signPage()
    settings = settings()
    download = download()
    textSearch = textSearch()
    localMusic = localMusic()
    pageBase = pageBase()
    tabFindMusic = tabFindMusic()
    onlineMusic = onlineMusic()
    def setUp(self):
        self.pageBase.ignoreTip()
    
    def tearDown(self):
        self.settings.restartApp()
 
    def test_memberAndmusicQualitySettingNotAlwaysAskMe(self):
        '''会员且音质下载设置为非每次都询问我当下载时无弹框'''
        self.signPage.signIn(2)
        self.localMusic.accessLocalMusic()
        self.localMusic.switchTo("已下载音乐")
        self.localMusic.clearDownloadedMusic()
        self.settings.accessSetting("音质设置")
        self.settings.setMusicQualitySettingTo(detailSetting="标准")
        self.settings.backToHome()
        self.onlineMusic.accessOnlineMusic()
        self.onlineMusic.accessFirstSongSet()
        downloadSongName = self.download.downloadCurrentPlayingSong()
        self.download.accessCurrentDownloading()
        self.download.pauseAllDownloadTask()
        downloadingSongs = self.download.getCurrentDownloading()
        if downloadingSongs==[]:
            self.download.back()
            self.download.back()
            self.localMusic.accessLocalMusic()
            downloadingSongs = self.localMusic.getDownloadedMusic()
            self.localMusic.clearDownloadedMusic()
        else:
            self.download.clearAllDownload()
        assert downloadSongName in downloadingSongs, "校验失败: 期望歌曲: %s, 实际歌曲: %s" % (downloadSongName, downloadingSongs)

    def test_memberAndmusicQualitySettingAlwaysAskMe(self):
        '''会员且音质下载设置为每次都询问我当下载时有弹框'''
        self.signPage.signIn(2)
        self.localMusic.accessLocalMusic()
        self.localMusic.switchTo("已下载音乐")
        self.localMusic.clearDownloadedMusic()
        self.settings.accessSetting("音质设置")
        self.settings.setMusicQualitySettingTo(detailSetting="每次都询问我")
        self.settings.backToHome()
        self.onlineMusic.accessOnlineMusic()
        self.onlineMusic.accessFirstSongSet()
        self.download.downloadCurrentPlayingSong()
        self.download.selectMusicQualityInPopUp("标准")

    def test_memberInDownloadMusicQualitySettingsNoPopUp(self):
        '''会员在音质下载设置里任何选项均无弹框'''
        self.signPage.signIn(2)
        self.settings.accessSetting("音质设置")
        self.settings.setMusicQualitySettingTo(detailSetting="高品质")
        #如果能点到返回按钮说明没有弹框
        self.settings.backToHome()

    def test_notMemberInDownloadMusicQualitySettingsYesPopUp(self):
        '''非会员在音质下载设置里如果是高品质则有弹框'''
        self.signPage.signIn(1)
        self.settings.accessSetting("音质设置")
        self.settings.setMusicQualitySettingTo(detailSetting="高品质")
        #有弹框则点击取消
        self.settings.dealWithBuyVipPop(False)