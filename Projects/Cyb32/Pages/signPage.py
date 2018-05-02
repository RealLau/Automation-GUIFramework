from BaseDriver.Driver import appiumDriver
from Helper.elementLoader import elementLoader
import datetime
from Projects.Cyb32.Pages.profilePage import profilePage


class signPage(elementLoader):
    driver = appiumDriver() 
        
    def __init__(self):       
        elementLoader.__init__(self, self.__class__.__name__)
    
    def restartApp(self):
        return self.driver.restartAPP()
    
    def getLoginStatus(self):
        '''获取登录状态， 已登录为True, 未登录为False'''
        signInterfaceElement =self.driver.findElement(self.locator("signInterface"))
        if signInterfaceElement.get_attribute("text")!="未登录":
            return True
        else:
            return False
        
    def signOutUser(self):
        signInterfaceElement =self.driver.findElement(self.locator("signInterface"))
        self.driver.click(signInterfaceElement)
        btnSignOut = self.driver.findElement(self.locator("btnSignOut"))
        self.driver.click(btnSignOut)
    
    def signIn(self, userId = 2):
        user = self.getUserWithID(userId)
        mobile = user["mobile"]
        pwd = user["pwd"]
        nickname = user["nickname"] 
        alreadySignIn = self.getLoginStatus()
        if alreadySignIn:
            self.signOutUser()
        signInterfaceElement =self.driver.findElement(self.locator("signInterface"))
        self.driver.click(signInterfaceElement)
        editTextUserNameElement = self.driver.findElement(self.locator("editTextMobile"))
        self.driver.sendKeys(editTextUserNameElement, mobile)
        editTextPwdElement = self.driver.findElement(self.locator("editTextPwd"))
        self.driver.sendKeys(editTextPwdElement, pwd, pwdType=True)
        btnSignIn = self.driver.findElement(self.locator("btnSignIn"))
        self.driver.click(btnSignIn)
        timeOut = 60
        d1 = datetime.datetime.now()
        d2 = datetime.datetime.now()
        loginSuccess = False
        while (d2-d1).seconds<timeOut:
            try:
                btnLogin = self.driver.instantFindElement("btnSignIn")
                self.driver.click(btnLogin)
                d2 = datetime.datetime.now()
                continue
            except:
                loginSuccess = True
                break
        if not loginSuccess:
            raise Exception("登录失败，原因：超时")
        else:
            signInterfaceElement =self.driver.findElement(self.locator("signInterface"))
            userNickname = signInterfaceElement.get_attribute("text")
            if userNickname!=nickname:
                print("昵称匹配失败。 预期: %s, 实际: %s, 修改回默认昵称..." % (nickname, userNickname))
                p = profilePage()
                p.setUserNickNameToDefault()