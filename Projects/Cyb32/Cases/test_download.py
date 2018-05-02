# _*_ coding=utf-8 _*_
from Projects.Cyb32.Pages.download import download
from Projects.Cyb32.Pages.pageBase import pageBase
from Projects.Cyb32.Pages.textSearch import textSearch
from Projects.Cyb32.Pages.localMusic import localMusic
import unittest


class test_download(unittest.TestCase):
    '''下载'''
    download = download()
    pageBase = pageBase()
    textSearch = textSearch()
    localMusic = localMusic()

    def setUp(self):
        self.pageBase.ignoreTip()

    def tearDown(self):
        self.download.restartApp()

    def test_download_song(self):
        '''下载歌曲'''
        DOWNLOAD_SONG = "叶衣佛母心咒"
        self.localMusic.accessLocalMusic()
        self.localMusic.clearDownloadedMusic()
        self.textSearch.accessSearchPage()
        self.textSearch.doSearch("song", "母画眉")
        self.download.downloadSpecifiedSongInSearchResult(DOWNLOAD_SONG, "贝玛千贝仁波切", "08:03")
        self.download.back(True)
        self.download.accessCurrentDownloading()
        self.download.pauseAllDownloadTask()
        l = self.download.getCurrentDownloading()
        if l == []:
            self.download.back()
            self.localMusic.accessLocalMusic()
            l = self.localMusic.getDownloadedMusic()
            assert DOWNLOAD_SONG in l, "下载失败"

        else:
            assert l == [DOWNLOAD_SONG], "正在下载: %s" % l
            sts = self.download.clearAllDownload()
            if isinstance(sts, BaseException):
                self.download.back()
                self.localMusic.accessLocalMusic()
                self.localMusic.clearDownloadedMusic()

    def test_download_item(self):
        '''下载节目'''
        DOWNLOAD_ITEM = "摸金天师"
        self.localMusic.accessLocalMusic()
        self.localMusic.switchTo("已下载节目")
        self.localMusic.clearDownloadedMusic()
        self.textSearch.accessSearchPage()
        self.textSearch.doSearch("item", DOWNLOAD_ITEM)
        self.textSearch.accessSpecifiedItemInSearchResult("摸金天师（盗墓小说）：紫襟故事")
        ITEM_NAME = self.download.downloadSpecifiedItemInAlbum(1)
        self.download.back(False)
        self.download.back(True)
        self.download.accessCurrentDownloading()
        self.download.pauseAllDownloadTask()
        l = self.download.getCurrentDownloading()
        if l == []:
            self.download.back()
            self.localMusic.accessLocalMusic()
            self.localMusic.switchTo("已下载节目")
            l = self.localMusic.getDownloadedMusic()
            assert ITEM_NAME in l, "下载失败, 下载节目名:%s, 已下载节目名:%s" % (ITEM_NAME, l)
        else:
            assert l == [ITEM_NAME], "正在下载: %s, 期望: %s" % (l, ITEM_NAME)
            sts = self.download.clearAllDownload()
            if isinstance(sts, BaseException):
                self.download.back()
                self.localMusic.accessLocalMusic()
                self.localMusic.clearDownloadedMusic()