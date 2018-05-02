# _*_ coding=utf-8 _*_
from Projects.Cyb32.Pages.onlineFM import onlineFM
from Projects.Cyb32.Pages.pageBase import pageBase
import unittest

class test_onlineFM(unittest.TestCase):
    '''在线FM'''        
    onlineFM = onlineFM()
    pageBase = pageBase()
    
    def setUp(self):
        self.pageBase.ignoreTip()
    
    def tearDown(self):
        self.onlineFM.restartApp()
    
    def test_orderAfterDrag(self):
        '''拖动排序'''
        self.onlineFM.accessonlineFM()
        self.onlineFM.accessMore()
        item1NameBefore = self.onlineFM.getItemName(1)
        item2Name = self.onlineFM.getItemName(2)
        self.onlineFM.dragItemAToItemB(1, 2)
        item1NameAfter = self.onlineFM.getItemName(1)
        assert item1NameAfter!=item1NameBefore and item1NameAfter==item2Name, "拖动前后栏目顺序未改变"