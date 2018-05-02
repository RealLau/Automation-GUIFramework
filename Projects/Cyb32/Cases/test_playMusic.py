# _*_ coding=utf-8 _*_
from Projects.Cyb32.Pages.playMusic import playMusic
from Projects.Cyb32.Pages.onlineMusic import onlineMusic
import unittest
from Projects.Cyb32.Pages.tabFindMusic import tabFindMusic
from Projects.Cyb32.Pages.pageBase import pageBase

class test_playMusic(unittest.TestCase):
    '''音乐播放'''        
    playMusic = playMusic()
    tabFindMusic = tabFindMusic()
    pageBase = pageBase()
    onlineMusic = onlineMusic()

    def setUp(self):
        self.pageBase.ignoreTip()
        
    def tearDown(self):
        self.playMusic.restartApp()
    
    def test_autoPlay(self):
        '''自动播放'''
        self.onlineMusic.accessOnlineMusic()
        self.onlineMusic.accessFirstSongSet()
        playStatus = self.playMusic.getPlayStatus()
        assert playStatus, "进入编辑推荐第一个栏目等待指定时间后，依然未自动播放"

    def test_deleteHistory(self):
        '''删除历史播放记录'''
        self.onlineMusic.accessOnlineMusic()
        self.onlineMusic.accessFirstSongSet()
        #先切换至暂停状态
        playStatus = self.playMusic.getPlayStatus()
        if playStatus:
            self.playMusic.switchPlayStatus()
            playStatus = self.playMusic.getPlayStatus()
            assert not playStatus, "暂停15秒之后依然在播放"
            self.playMusic.accessPopPlayHistory()
            histories = self.playMusic.getPlayHistoryInPop()
            assert histories!=[], "历史收听列表为空"
            self.playMusic.deleteHistory()
            histories = self.playMusic.getPlayHistoryInPop()
            assert histories==[], "历史收听列表不为空"
            historyCountAfterDelete = self.playMusic.getPlayHistoryCount()
            assert historyCountAfterDelete==0, "删除历史歌曲后, 历史歌曲数量不为零: %d" % historyCountAfterDelete

    def test_nextItem(self):
        '''下一曲功能'''
        self.onlineMusic.accessOnlineMusic()
        self.onlineMusic.accessFirstSongSet()
        beforeNexPlayingItemName = self.playMusic.getCurrentPlayingItemName()
        playStatus = self.playMusic.getPlayStatus()
        if playStatus:
            self.playMusic.playNextItem()
            afterNextPlayingItemName = self.playMusic.getCurrentPlayingItemName()
            assert beforeNexPlayingItemName!=afterNextPlayingItemName, "下一曲功能测试失败. 原因: 切换前后播放栏目一致: %s" % (afterNextPlayingItemName)
        else:
            raise Exception("下一曲功能测试失败. 原因: 进入编辑推荐第一个栏目后自动播放失败")

    def test_pause(self):
        '''暂停功能'''
        self.onlineMusic.accessOnlineMusic()
        self.onlineMusic.accessFirstSongSet()
        playStatus = self.playMusic.getPlayStatus()
        if playStatus:
            self.playMusic.switchPlayStatus()
            playStatus = self.playMusic.getPlayStatus()
            assert not playStatus, "暂停15秒之后依然在播放"
        else:
            raise Exception("暂停功能测试失败. 原因: 进入编辑推荐第一个栏目后自动播放失败")

    def test_playList(self):
        '''点播列表(弹出框-数据正确性)'''
        self.onlineMusic.accessOnlineMusic()
        self.onlineMusic.accessFirstSongSet()
        #先切换至暂停状态
        playStatus = self.playMusic.getPlayStatus()
        if playStatus:
            self.playMusic.switchPlayStatus()
            playStatus = self.playMusic.getPlayStatus()
            assert not playStatus, "暂停15秒之后依然在播放"
            #再获取两个播放列表
            p1 = self.playMusic.getPlayList()
            p2 = self.playMusic.getPlayListInPop()
            assert p1!=[], "底部播放列表为空"
            for i in p1:
                assert i in p2, "弹出框列表加载错误. 底部栏目%s不在弹出框列表 %s里" % (i, p2)
        else:
            raise Exception("暂停功能测试失败. 原因: 进入编辑推荐第一个栏目后自动播放失败")

    def test_preItem(self):
        '''上一曲功能'''
        self.onlineMusic.accessOnlineMusic()
        self.onlineMusic.accessFirstSongSet()
        beforeNexPlayingItemName = self.playMusic.getCurrentPlayingItemName()
        playStatus = self.playMusic.getPlayStatus()
        if playStatus:
            self.playMusic.playNextItem()
            afterNextPlayingItemName = self.playMusic.getCurrentPlayingItemName()
            assert beforeNexPlayingItemName!=afterNextPlayingItemName, "下一曲功能测试失败. 原因: 切换前后播放栏目一致: %s" % (afterNextPlayingItemName)
            self.playMusic.playPreItem()
            nowPlayItemName = self.playMusic.getCurrentPlayingItemName()
            assert nowPlayItemName==beforeNexPlayingItemName, "上一曲功能测试失败. 预期: %s, 实际: %s" % (beforeNexPlayingItemName, nowPlayItemName)
        else:
            raise Exception("下一曲功能测试失败. 原因: 进入编辑推荐第一个栏目后自动播放失败")



