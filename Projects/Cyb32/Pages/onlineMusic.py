from BaseDriver.Driver import appiumDriver
from Helper.elementLoader import elementLoader

class onlineMusic(elementLoader):
    driver = appiumDriver() 
        
    def __init__(self):       
        elementLoader.__init__(self, self.__class__.__name__)
    
    def restartApp(self):
        return self.driver.restartAPP()
    
    def accessOnlineMusic(self):
        '''进入在线音乐'''
        tabOnlineMusic = self.driver.findElement(self.locator("tabOnlineMusic"))
        self.driver.click(tabOnlineMusic)
    
    def accessSubTab(self, subTabName):
        '''进入页签. subTabName: 精选歌单, 歌曲排行, 歌单分类'''
        subTabName = self.driver.findElement(self.locator("subTabName", subTabName))
        self.driver.click(subTabName)
    
    def accessSubCatoryOfGedanfenlei(self, subCatoryName, subSubCatoryName):
        '''进入歌单分类下的某个子标签. 示例: subCatoryName='主题', subSubCatoryName='儿童'. '''
        subCatoryName = self.driver.findElement(self.locator("subTabName", subCatoryName))
        self.driver.click(subCatoryName)
        subSubCatoryName = self.driver.findElement(self.locator("subTabName", subSubCatoryName))
        self.driver.click(subSubCatoryName)
    
    def getCurrentGedanName(self):
        '''获取当前所处的歌单页面名'''
        currentGedan = self.driver.findElement(self.locator("currentGedan"))
        currentGedanName = currentGedan.get_attribute("text")
        return currentGedanName.replace("歌单", "")

    def accessFirstSongSet(self):
        songName = self.driver.findElements(self.locator("songName"))[0]
        self.driver.click(songName)