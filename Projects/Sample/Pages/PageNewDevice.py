from BaseDriver.Driver import AutoDriver
from Helper.ElementLoader import ElementLoader
from Projects.Sample.Pages.PageBase import PageBase


class PageNewDevice(PageBase):
    driver = AutoDriver()

    def __init__(self):       
        ElementLoader.__init__(self, self.__class__.__name__)

    def get_title(self):
        title = self.driver.find_element(self.locator("title"))
        return title.text