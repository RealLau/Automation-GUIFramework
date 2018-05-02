from BaseDriver.Driver import appiumDriver
from Helper.elementLoader import elementLoader

class onlineFM(elementLoader):
    driver = appiumDriver() 
        
    def __init__(self):       
        elementLoader.__init__(self, self.__class__.__name__)
    
    def restartApp(self):
        return self.driver.restartAPP()
    
    def accessonlineFM(self):
        '''进入在线FM'''
        tabOnlineFM = self.driver.findElement(self.locator("tabOnlineFM"))
        self.driver.click(tabOnlineFM)

    def accessTopMenu(self, menu_name):
        menu_name = self.driver.findElement(self.locator("TopMenu", menu_name))
        self.driver.click(menu_name)

    def accessMore(self):
        '''进入更多'''
        more = self.driver.findElement(self.locator("more"))
        self.driver.click(more)
    
    def dragItemAToItemB(self, itemAindex, itemBIndex):
        '''把两个索引位置不同的栏目通过拖动调换位置'''
        '''因为appium的get_attribute(index)有BUG:https://testerhome.com/topics/2606, 所以这里尽量不采用通过获取元素的索引的方法来校验'''
        itemAindex = str(itemAindex)
        itemBIndex = str(itemBIndex)
        self.driver.dragFromAToB(self.locator("itemInMore", itemAindex), self.locator("itemInMore", itemBIndex))
    
    def getItemName(self, itemIndex):
        '''获取在index位置的栏目名称'''
        itemIndex = str(itemIndex)
        item = self.driver.findElement(self.locator("itemInMore", itemIndex))
        return item.get_attribute("text")