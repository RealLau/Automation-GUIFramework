from appium import webdriver as adriver
from selenium import webdriver as sdriver
import time
import datetime
import os
import yaml
import subprocess
import requests
from selenium.common.exceptions import NoSuchElementException
from PIL import Image
import math
import operator
from functools import reduce


class Singleton(object):  
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Singleton, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance


class AutoDriver(Singleton):
    driver = None
    currentFileDir = os.path.dirname(__file__)
    eutDir = os.path.abspath(currentFileDir+os.path.sep+"..")
    p = os.path.join(os.path.abspath(currentFileDir+os.path.sep+".."), "Conf", "running.yaml")
    with open(p, 'r') as f:
        data = yaml.load(f)
    timeOut = data["timeOut"]
    logLevel = data["logLevel"]
    projectName = data['project']
    projectDir = os.path.join(eutDir, "Projects", "%s" % projectName)
    unicodeKeyboard = data["unicodeKeyBoard"]
    soundResourceDir = os.path.join(eutDir, "Projects", projectName, "SoundResource")
    c = os.path.join(projectDir, "%s.yaml" % projectName)
    with open(c, 'r') as f:
        dataProject = yaml.load(f)
    projectType = dataProject["projectType"]
    desired_caps = {}
    if projectType == 'APP':
        fullReset = dataProject["fullReset"]
        dc = dataProject["dc"]
        display = dataProject["display"]
        mac = dataProject["mac"]
        model = dataProject["model"]
        uuid = dataProject["uuid"]
        desired_caps["platformName"] = dataProject["platformName"]
        desired_caps["platformVersion"] = dataProject["platformVersion"]
        desired_caps["deviceName"] = dataProject["deviceName"]
        desired_caps["appPackage"] = dataProject["appPackage"]
        desired_caps["appActivity"] = dataProject["appActivity"]
        desired_caps["udid"] = dataProject["udid"]
        desired_caps["app"] = dataProject["app"]
        # Need specify from config file
        desired_caps['newCommandTimeout'] = timeOut
        desired_caps["clearSystemFiles"] = True
        desired_caps["recreateChromeDriverSessions"] = True
        desired_caps["fullReset"] = fullReset
        desired_caps["unicodeKeyboard"] = unicodeKeyboard
        desired_caps["resetKeyboard"] = True
        desired_caps["androidInstallTimeout"] = 90000*2
        # desired_caps["automationName"] = "uiautomator2"
        subprocess.Popen("appium --log-level %s --log-timestamp --local-timezone" % logLevel, shell=True)
        while 1:
            time.sleep(1)
            try:
                response = requests.get('http://127.0.0.1:4723/wd/hub/status').status_code
                if response==200:
                    break
            except Exception:
                pass
        driver = adriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    elif projectType == "Web":
        browser = dataProject["Browser"]
        startPage = dataProject["startPage"]
        if not driver:
            driver = eval("sdriver.%s()" % browser)
            driver.get("%s" % startPage)
    else:
        print("projectType must be APP or Web ")
        raise BaseException("projectType must be APP or Web")

    @classmethod
    def instant_find_element(self, locator):
        # 单次查找一个元素
        return self.driver.find_element(locator[0], locator[1])

    @classmethod
    def instant_find_elements(self, locator):
        # 单次查找多个元素
        return self.driver.find_elements(locator[0], locator[1])

    @classmethod
    def get_all_contexts(self):
        # 获取所有上下文
        ctx = self.driver.contexts
        print(ctx)
        return ctx
    
    @classmethod
    def get_current_context(self):
        # 获取所有上下文
        return self.driver.context
       
    @classmethod
    def find_element(self, locator):
        # 超时时间内循环查找元素，直至找到为止
        d1 = datetime.datetime.now()
        d2 = datetime.datetime.now()
        passed_time = (d2-d1).seconds
        while passed_time < self.timeOut:
            try:
                ele = self.driver.find_element(locator[0], locator[1])
                return ele
            except NoSuchElementException:
                try:
                    # 如果遇到网络不好的情况，开发应在此定义一个页面加载超时出现的元素，点击后触发重新加载
                    time_out_element = self.driver.find_element_by_id("com.hongfans.rearview:id/iv_error_load")
                    time_out_element.click()
                    continue
                except NoSuchElementException:
                    print("Retrying to find element by %s: %s" % (locator[0], locator[1]))
                    time.sleep(0.5)
                    d2 = datetime.datetime.now()
                    passed_time = (d2-d1).seconds
        print("Can not find element specified -> ", locator)
        raise NoSuchElementException
    
    @classmethod
    def find_elements(self, locator, allow_none_list=False):
        # 超时时间内循环查找元素集，直至找到为止
        # allow_none_list: 是否允许返回空的结果集
        d1 = datetime.datetime.now()
        d2 = datetime.datetime.now()
        passed_time = (d2-d1).seconds
        while passed_time < self.timeOut:
            try:
                elements = self.driver.find_elements(locator[0], locator[1])
                if allow_none_list:
                    return elements
                else:
                    if not elements:
                        try:
                            # 如果遇到网络不好的情况，开发应在此定义一个页面加载超时出现的元素，点击后触发重新加载
                            time_out_element = self.driver.find_element_by_id("com.hongfans.rearview:id/iv_error_load")
                            time_out_element.click()
                        except NoSuchElementException:
                            d2 = datetime.datetime.now()
                            passed_time = (d2-d1).seconds
                            continue
                    else:
                        return elements
            except NoSuchElementException:
                print("Retrying to find element by %s: %s" % (locator[0], locator[1]))
                time.sleep(0.5)
                d2 = datetime.datetime.now()
                passed_time = (d2-d1).seconds
        print("Can not find elements specified ->", locator)
        raise NoSuchElementException

    @classmethod
    def set_input_method(self, keyboard_name):
        # 安卓可用，设置输入法
        dic = {"fly": "com.iflytek.inputmethod.pad/.FlyIME", "appium": "io.appium.android.ime/.UnicodeIME", "adb":"com.android.adbkeyboard/.AdbIME"}
        os.system("adb shell ime set %s" % dic[keyboard_name])

    @classmethod
    def clear(self, element):
        # 清除输入框内容
        return element.clear()
        
    @classmethod
    def click(self, element):
        # 点击
        return element.click()

    @classmethod
    def send_keys(self, element, content):
        # 输入，不替换原有内容
        return element.send_keys(content)
        
    @classmethod
    def set_value(self, element, content):
        # 输入，将会替换掉原有内容
        return self.driver.set_value(element, content)
    
    @classmethod
    def assert_true(self, p, error_info):
        # 断言真: 表达式p若为假, 则抛错, 并显示error_info
        try:
            assert p, error_info
        except AssertionError:
            raise
         
    @classmethod
    def page_should_contains_text(self, expected_text):
        # 5秒内，检查页面是否出现指定文本
        d1 = datetime.datetime.now()
        d2 = datetime.datetime.now()
        passed_time = (d2 - d1).seconds
        while passed_time < 5:
            try:
                page_source = self.driver.page_source
                self.assert_true(expected_text in page_source, "%s is NOT in current Page, retrying" % expected_text)
                return
            except AssertionError:
                time.sleep(0.5)
                d2 = datetime.datetime.now()
                passed_time = (d2 - d1).seconds
                continue
        raise Exception("5秒内校验页面包含文本 %s 失败。" % expected_text)

    @classmethod
    def switch_to_context(self, context_name):
        # 切换上下文
        return self.driver.switch_to.context(context_name)
     
    @classmethod
    def get_page_source(self):
        # web及app的webview页面可用，用于返回页面源码
        return self.driver.page_source
    
    @classmethod
    def get_android_display_resolution(self):
        # 安卓可用，获取安卓屏幕分辨率
        r = os.popen("adb shell dumpsys display | findstr PhysicalDisplayInfo").read()
        if "not found" in r or not r:
            r = os.popen("adb shell wm size").read()
            resolution = r.replace("\n", "").replace("\r", "").split(": ")[1].split("x")
        else:
            resolution = r.split('{')[1].split(',')[0].replace(' ', '').split("x")
        width = resolution[0]
        height = resolution[1]
        print("获取到分辨率：%sx%s" % (width, height))
        return int(width), int(height)
     
    @classmethod
    def swipe(self, start_x, start_y, end_x, end_y, dur=800):
        # start_x: 滑动起始点横坐标
        # start_y: 滑动起始点纵坐标
        # end_x：滑动终点横坐标
        # end_y：滑动终点纵坐标
        # dur：在多少时间内完成滑动动作（单位：ms毫秒）
        return self.driver.swipe(start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y, duration=dur)

    @classmethod
    def restart_app(self):
        # 安卓可用，重启app
        self.driver.close_app()
        self.driver.launch_app()

    @classmethod
    def restart(self):
        self.driver.quit()
        self.driver = sdriver.Chrome()
        self.driver.get(self.dataProject["startPage"])

    @classmethod
    def restart_browser(self, func):
        # web可用，重启浏览器
        def wraper(*arg, **kwargs):
            self.restart()
            return func(*arg, **kwargs)
        return wraper

    @classmethod
    def access_new_tab_by_click_link(self, locator):
        # 仅Web测试可用: 通过点击链接进入新页签
        try:
            windows_before = self.driver.window_handles
            el = self.find_element(locator)
            self.click(el)
            windows_after = self.driver.window_handles
            while windows_before == windows_after:
                time.sleep(1)
                windows_after = self.driver.window_handles
            for newWindow in windows_after:
                if newWindow not in windows_before:
                    self.driver.switch_to.window(newWindow)
                    print("Switched to new window")
        except Exception:
            raise
    
    @classmethod
    def hide_app_to_backend(self):
        # 按Home键隐藏app到后台
        return self.driver.press_keycode(3)

    @classmethod
    def compare_image_the_same_use_pil(self, source_image_element_path_original, source_image_element_path_current):
        # Deprecated, PIL对比图片相似度
        image1 = Image.open(source_image_element_path_original)
        image2 = Image.open(source_image_element_path_current)
        histogram1 = image1.histogram()
        histogram2 = image2.histogram()
        differ = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a-b)**2, histogram1, histogram2))))
        print("差异度:", differ)
        if differ <= 100:
            return True
        else:
            return False
    
    @classmethod
    def drag_from_to(self, locator_original, locator_destination):
        e1 = self.find_element(locator_original)
        e2 = self.find_element(locator_destination)
        return self.driver.drag_and_drop(e1, e2)

    @classmethod
    def execute_script(self, script):
        return self.driver.execute_script(script)
