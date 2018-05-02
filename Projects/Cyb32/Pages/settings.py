from BaseDriver.Driver import appiumDriver
from Helper.elementLoader import elementLoader

class settings(elementLoader):
    driver = appiumDriver() 
        
    def __init__(self):       
        elementLoader.__init__(self, self.__class__.__name__)
        
    def restartApp(self):
        return self.driver.restartAPP()
    
    def accessSetting(self, settingName):
        setting = self.driver.findElement(self.locator("settingInterface"))
        self.driver.click(setting)
        subsetting = self.driver.findElement(self.locator("subSetting", settingName))
        self.driver.click(subsetting)
    
    def setMusicQualitySettingTo(self, subsubSetting='下载音质选择', detailSetting='每次都询问我'):
        musicsettingdict = {"流畅": "Smooth", "每次都询问我":"Smooth", "标准": "NormalQuality", "高品质":"HighQuality", "无损音质":"LosslessQuality"}
        settingPrefix = {'下载音质选择':'download', '播放音质选择':'play'}
        elementName = settingPrefix[subsubSetting]+musicsettingdict[detailSetting]
        detailsettingOption = self.driver.findElement(self.locator(elementName))
        self.driver.click(detailsettingOption)
        
    def backToHome(self):
        back = self.driver.findElement(self.locator("back"))
        self.driver.click(back)
    
    def dealWithBuyVipPop(self, buyVip=False):
        di = {True:"ok", False:"cancel"}
        btnCancelOrOk = self.driver.findElement(self.locator("btnCancelOrOk", di[buyVip]))
        self.driver.click(btnCancelOrOk)