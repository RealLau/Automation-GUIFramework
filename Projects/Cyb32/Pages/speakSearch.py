from BaseDriver.Driver import appiumDriver
from Helper.elementLoader import elementLoader
import time
from unittest.case import skip

class speakSearch(elementLoader):
    driver = appiumDriver() 
        
    def __init__(self):       
        elementLoader.__init__(self, self.__class__.__name__)
    
    def restartApp(self):
        return self.driver.restartAPP()


    def accessSpeakSearch(self):
        '''进入语音搜索'''
        speakInterface = self.driver.findElement(self.locator("speakInterface"))
        self.driver.click(speakInterface)
        self.driver.findElement(self.locator("listener"))
        time.sleep(2)

    def speakWorlds(self, worlds):
        '''说话'''
        self.driver.speakWords(worlds)
        willSearch = self.driver.findElement(self.locator("willSearch"))
        return willSearch.get_attribute("text")


    def getCurrentPlayingSong(self):
        '''获取当前正在播放的歌曲/节目'''
        currentPlayingSong = self.driver.findElement(self.locator("currentPlayingSong"))
        return currentPlayingSong.get_attribute("text").strip()