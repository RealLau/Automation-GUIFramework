from BaseDriver.Driver import appiumDriver
from Helper.elementLoader import elementLoader
import time

class mustPayChannel(elementLoader):
    driver = appiumDriver() 
        
    def __init__(self):       
        elementLoader.__init__(self, self.__class__.__name__)
    
    def restartApp(self):
        return self.driver.restartAPP()

    def currentPageIsBuyItems(self, pageTitleExpected = "购买专辑"):
        time.sleep(5)
        pageTitle = self.driver.findElement(self.locator("title"))
        pageTitleActual = pageTitle.get_attribute("text")
        assert pageTitleActual==pageTitleExpected, "当前页面不是%s, 而是%s" % (pageTitleExpected, pageTitleActual)
        timeOut = 20
        import datetime
        t1 = datetime.datetime.now()
        t2 = datetime.datetime.now()
        allContexts = self.driver.getContexts()
        while (t2-t1).seconds<timeOut :
            if "WEBVIEW_com.hongfans.rearview:web" in allContexts:
                break
            else:
                time.sleep(1)
                t2 = datetime.datetime.now()
                allContexts = self.driver.getContexts()
        if not (t2-t1).seconds<timeOut:
            raise BaseException("购买专辑页面加载失败")
        else:
            self.driver.switchToContext("WEBVIEW_com.hongfans.rearview:web")
            self.driver.pageShouldContainsText("请用手机扫码支付") 
        self.driver.switchToContext("NATIVE_APP")
        
    def back(self):
        backBtn = self.driver.findElement(self.locator("back"))
        self.driver.click(backBtn)
    
    def playSelectedItem(self, trialPlay=False, restoreDefaultOrder = True):
        '''从专辑里选择一首歌/节目来播放. trialPlay: 是否选择试听类型的'''
        if restoreDefaultOrder:
            self.setItemsToDefault()
        trialItems = self.driver.findElements(self.locator("trialPlay"))
        if trialPlay:
            if trialItems==[]:
                raise BaseException("当前专辑无试听音乐")
            else:
                self.driver.click(trialItems[0])
        else:
            firstNoneTrialPlayItem = self.driver.findElement(self.locator("firstNoneTrialPlayItem",str(len(trialItems)+1)))
            self.driver.click(firstNoneTrialPlayItem)
    
    def setItemsToDefault(self):
        btnSort = self.driver.findElement(self.locator("btnSort"))
        self.driver.click(btnSort)
        time.sleep(3)
        btnSort = self.driver.findElement(self.locator("btnSort"))
        self.driver.click(btnSort)
        time.sleep(3)

    def buy(self, item_type="all"):
        # count: 一次性购买的(点击购买后直接跳转到付费页面的)传all, 默认值; 否则为可单集购买的, 传1
        btnBuyAll = self.driver.findElement(self.locator("btnBuyAll"))
        self.driver.click(btnBuyAll)
        if item_type == 1:
            rounds = self.driver.findElements(self.locator("rounds"))
            self.driver.click(rounds[0])
            btnCofirmBuySelectedItems = self.driver.findElement(self.locator("btnCofirmBuySelectedItems"))
            self.driver.click(btnCofirmBuySelectedItems)



