from BaseDriver.Driver import AutoDriver
from Helper.ElementLoader import ElementLoader
import unittest


class PageBase(ElementLoader, unittest.TestCase):
    driver = AutoDriver()
        
    def __init__(self):       
        ElementLoader.__init__(self, self.__class__.__name__)

    def login(self, email, pwd):
        email_field = self.driver.find_element(self.locator("email_field"))
        self.driver.send_keys(email_field, email)
        pwd_field = self.driver.find_element(self.locator("pwd_field"))
        self.driver.send_keys(pwd_field, pwd)
        btn_login = self.driver.find_element(self.locator("btn_login"))
        self.driver.click(btn_login)

    def access_Page(self, page_name):
        if page_name == "注册新设备":
            link_register_new_device = self.driver.find_element(self.locator("link_register_new_device"))
            self.driver.click(link_register_new_device)

    def get_user_with_id(self, user_id):
        return self.get_config_user_info(user_id)

    def get_current_user_nickname(self):
        nickname = self.driver.find_element(self.locator("nickname"))
        return nickname.text

    def logout(self):
        script = "document.querySelector('body > div > div.main-wrapper.ng-scope > div:nth-child(1) > div > header > div:nth-child(2) > nav > div > ul').setAttribute('class','');"
        self.driver.execute_script(script)
        link_logout = self.driver.find_element(self.locator("link_logout"))
        self.driver.click(link_logout)

