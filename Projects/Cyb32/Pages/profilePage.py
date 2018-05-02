from BaseDriver.Driver import appiumDriver
from Helper.elementLoader import elementLoader
import os
import time


class profilePage(elementLoader):
    driver = appiumDriver() 
        
    def __init__(self):       
        elementLoader.__init__(self, self.__class__.__name__)
    
    def restartApp(self):
        return self.driver.restartAPP()

    def openProfile(self):
        signInterface = self.driver.findElement(self.locator("signInterface"))
        self.driver.click(signInterface)

    def accessProfileEditPage(self):
        '''进入个人信息页面'''
        self.openProfile()
        udid = self.driver.desired_caps["udid"]
        if not udid in ["20080411", "0123456789ABCDEF"]:
            btnEditProfile = self.driver.findElement(self.locator("btnEditProfile"))
            self.driver.click(btnEditProfile)
        else:
            time.sleep(2)
            os.system("adb shell input tap 737 150")

    def editUserNick(self, newNick):
        '''编辑用户昵称'''
        self.driver.set_input_method("adb")
        editTextUserNickName = self.driver.findElement(self.locator("editTextUserNickName"))
        self.driver.clear(editTextUserNickName)
        self.driver.setValue(editTextUserNickName, newNick)
        btnSaveEditUserInfo = self.driver.findElement(self.locator("btnSaveEditUserInfo"))
        self.driver.click(btnSaveEditUserInfo)
        self.driver.set_input_method("appium")

    def getUserNickName(self):
        '''获取用户昵称'''
        userNickNameOnProfilePage = self.driver.findElement(self.locator("userNickNameOnProfilePage"))
        nickName = userNickNameOnProfilePage.get_attribute("text")
        return nickName.replace("昵称: ", "")

    def setUserNickNameToDefault(self):
        self.accessProfileEditPage()
        '''设置用户昵称为project.yaml的默认配置'''
        user = self.getUserWithID(2)
        defaultNickName = user["nickname"]
        self.editUserNick(defaultNickName)
        result = self.getUserNickName()
        assert result==defaultNickName, "重置用户昵称失败，当前昵称为: %s" % result

    def exitLogin(self):
        '''退出登录'''
        udid = self.driver.desired_caps["udid"]
        if not udid in ["20080411", "0123456789ABCDEF"]:
            btnExitLogin = self.driver.findElement(self.locator("btnExitLogin"))
            self.driver.click(btnExitLogin)
        else:
            time.sleep(2)
            os.system("adb shell input tap 737 268")

    def accessCacheInfo(self):
        cacheInfo = self.driver.findElement(self.locator("cacheInfo"))
        self.driver.click(cacheInfo)
    
    def clearCache(self):
        '''清除缓存'''
        cachedDataElement = self.driver.findElement(self.locator("cachedDataElement"))
        cachedDataBeforeClear = cachedDataElement.get_attribute("text").replace("已缓存数据:", "")
        if "MB" in cachedDataBeforeClear:
            cachedDataBeforeClear = float(cachedDataBeforeClear.replace("MB",""))*1024
        elif "GB" in cachedDataBeforeClear:
            cachedDataBeforeClear = float(cachedDataBeforeClear.replace("GB", "")) * 1024 * 1024
        else:
            cachedDataBeforeClear = float(cachedDataBeforeClear.replace("B", ""))
        btnClearCache = self.driver.findElement(self.locator("btnClearCache"))
        self.driver.click(btnClearCache)
        btnConfirmClearCache = self.driver.findElement(self.locator("btnConfirmClearCache"))
        self.driver.click(btnConfirmClearCache)
        cachedDataElement = self.driver.findElement(self.locator("cachedDataElement"))
        cachedDataAfterClear = cachedDataElement.get_attribute("text").replace("已缓存数据:", "")
        if "MB" in cachedDataAfterClear:
            cachedDataAfterClear = float(cachedDataAfterClear.replace("MB",""))*1024
        elif "GB" in cachedDataAfterClear:
            cachedDataAfterClear = float(cachedDataAfterClear.replace("GB", "")) * 1024 * 1024
        else:
            cachedDataAfterClear = float(cachedDataAfterClear.replace("B", ""))
        assert cachedDataAfterClear <= cachedDataBeforeClear, "清除缓存失败， 清除前:%d, 清除后: %d" % (cachedDataBeforeClear,cachedDataAfterClear)
        print("清除前:%d, 清除后: %d" % (cachedDataBeforeClear,cachedDataAfterClear))