from BaseDriver.Driver import appiumDriver
from Helper.elementLoader import elementLoader
import datetime
from selenium.common.exceptions import NoSuchElementException

class tabFindMusic(elementLoader):
    driver = appiumDriver() 
        
    def __init__(self):       
        elementLoader.__init__(self, self.__class__.__name__)
    
    def restartApp(self):
        return self.driver.restartAPP()
    
    def loadEditorSuggestion(self):
        '''滑动直到找到"编辑推荐"'''
        self.driver.findElement(self.locator("btnNoLogin"))
        timeOut = 80
        d1 = datetime.datetime.now()
        d2 = datetime.datetime.now()
        while (d2-d1).seconds<timeOut:
            try:
                self.driver.instantFindElement(self.locator("EditorSuggestion"))
                return True
            except NoSuchElementException:
                try:
                    lo = ("id", "com.hongfans.rearview:id/iv_error_load")
                    e = self.driver.instantFindElement(lo)
                    self.driver.click(e)
                except Exception:
                    '''每次滑动100像素，粒度小，精度才高'''
                    self.driver.swipe(300,400,300,300,800)
                    d2 = datetime.datetime.now()
        raise BaseException("80秒内仍未找到编辑推荐")
    
    def accessTabFoundMusic(self):
        tabFoundMusic = self.driver.findElement(self.locator("tabFoundMusic"))
        self.driver.click(tabFoundMusic)