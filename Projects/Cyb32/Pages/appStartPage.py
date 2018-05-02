from BaseDriver.Driver import appiumDriver
from Helper.elementLoader import elementLoader

class appStartPage(elementLoader):
    driver = appiumDriver() 
        
    def __init__(self):       
        elementLoader.__init__(self, self.__class__.__name__)
    
    def restartApp(self):
        return self.driver.restartAPP()
        
    def skipAdd(self):
        """跳过广告"""
        btnSkipAdd = self.driver.findElement(self.locator("btnSkipAdd"))
        self.driver.click(btnSkipAdd)
        self.driver.findElement(self.locator("btnNoLogin"))
        
    def waitForHomePageLoadComplete(self):
        """等待首页加载完成"""
        self.driver.findElement(self.locator("btnNoLogin"))
    

        