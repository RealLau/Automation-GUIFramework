from appium import webdriver
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
from pygame import mixer
# import cv2

class Singleton(object):  
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Singleton, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance
    
class appiumDriver(Singleton):
    driver = None
    currentFileDir = os.path.dirname(__file__)
    eutDir = os.path.abspath(currentFileDir+os.path.sep+"..")
    p = os.path.abspath(currentFileDir+os.path.sep+"..")+r"\Conf\running.yaml"
    f = open(p, 'r')
    data = yaml.load(f)
    f.close()
    timeOut = data["timeOut"]
    logLevel = data["logLevel"]
    projectName = data['project']
    projectDir = eutDir+"\\Projects\\%s" % projectName
    unicodeKeyboard = data["unicodeKeyBoard"]
    soundResourceDir = os.path.join(eutDir, "Projects", projectName, "SoundResource")
    c = projectDir+"\\%s.yaml" % projectName
    f = open(c, 'r')
    dataProject = yaml.load(f)
    f.close()
    projectType = dataProject["projectType"]
    fullReset = dataProject["fullReset"]
    dc = dataProject["dc"]
    display = dataProject["display"]
    imei = dataProject["imei"]
    mac = dataProject["mac"]
    model = dataProject["model"]
    os_ver = dataProject['os_ver']
    uuid = dataProject["uuid"]
    imsi = dataProject["imsi"]
    app_key = dataProject["app_key"]
    app_ver = dataProject["app_ver"]
    if projectType == 'APP':
        desired_caps = {}
        desired_caps["platformName"] = dataProject["platformName"]
        desired_caps["platformVersion"] =dataProject["platformVersion"]
        desired_caps["deviceName"] =dataProject["deviceName"]
        desired_caps["appPackage"] =dataProject["appPackage"]
        desired_caps["appActivity"] =dataProject["appActivity"]
        desired_caps["udid"] =dataProject["udid"]
        desired_caps["app"] =dataProject["app"]
        #Need specify from config file
        desired_caps['newCommandTimeout'] = timeOut
        desired_caps["clearSystemFiles"] = True
        desired_caps["recreateChromeDriverSessions"] = True
        desired_caps["fullReset"] = fullReset
        desired_caps["unicodeKeyboard"] = unicodeKeyboard
        desired_caps["resetKeyboard"] = True
        desired_caps["androidInstallTimeout"] = 90000*2
        
        subprocess.Popen(r"appium --log-level %s --log-timestamp --local-timezone" % logLevel, shell=True)
        while 1:
            time.sleep(1)
            try:
                response = requests.get('http://127.0.0.1:4723/wd/hub/status').status_code
                if response==200:
                    break
            except Exception:
                pass
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    elif projectType == "Web":
        browser = dataProject["Browser"]
        startPage = dataProject["startPage"]
        #log_path定义geckodriver的日志文件位置， os.devnull表示不记录到任何地方
        driver = eval("sdriver.%s(log_path=os.devnull)" % browser)
        driver.get("%s" % startPage)
    else:
        print("projectType must be APP or Web ")
        raise BaseException("projectType must be APP or Web")
    
    @classmethod
    def instantFindElement(self, locator):
        return self.driver.find_element(locator[0], locator[1])

    @classmethod
    def instantFindElements(self, locator):
        return self.driver.find_elements(locator[0], locator[1])

    @classmethod
    def getContexts(self):
        ctx = self.driver.contexts
        print(ctx)
        return ctx
    
    @classmethod
    def getContext(self):
        return self.driver.context
       
    @classmethod
    def findElement(self,locator):
        '''格式化查找元素'''    
        d1 = datetime.datetime.now()
        d2 = datetime.datetime.now()
        passedTime = (d2-d1).seconds
        while passedTime<self.timeOut:
            try:
                ele = self.driver.find_element(locator[0], locator[1])
                return ele
            except Exception as e:
                try:
                    timeOutElement = self.driver.find_element_by_id("com.hongfans.rearview:id/iv_error_load")
                    timeOutElement.click()
                    continue
                except Exception:
                    print (str(e))
                    print ("Retrying to find element by %s: %s" % (locator[0], locator[1]))
                    time.sleep(0.5)
                    d2 = datetime.datetime.now()
                    passedTime = (d2-d1).seconds
        print("CAN NOT FIND ELEMENT SPEFICIED")
        raise NoSuchElementException
    
    @classmethod
    def findElements(self, locator, allowNoneList=False):
        '''格式化查找元素'''  
        d1 = datetime.datetime.now()
        d2 = datetime.datetime.now()
        passedTime = (d2-d1).seconds
        while passedTime<self.timeOut:
            try:
                eles = self.driver.find_elements(locator[0], locator[1])
                if allowNoneList:
                    return eles
                else:
                    if eles==[]:
                        try:
                            timeOutElement = self.driver.find_element_by_id("com.hongfans.rearview:id/iv_error_load")
                            timeOutElement.click()
                        except:
                            d2 = datetime.datetime.now()
                            passedTime = (d2-d1).seconds
                            continue
                    else:
                        return eles
            except Exception as e:
                print (str(e))
                print ("Retrying to find element by %s: %s" % (locator[0], locator[1]))
                time.sleep(0.5)
                d2 = datetime.datetime.now()
                passedTime = (d2-d1).seconds
        print("CAN NOT FIND ELEMENT SPEFICIED")
        raise NoSuchElementException

    # 设置输入法
    @classmethod
    def set_input_method(self, keyboard_name):
        dic = {"fly": "com.iflytek.inputmethod/.FlyIME", "appium": "io.appium.android.ime/.UnicodeIME", "adb":"com.android.adbkeyboard/.AdbIME"}
        os.system("adb shell ime set %s" % dic[keyboard_name])

    @classmethod
    def clear(self, element):
        element.click()
        l = element.get_attribute("text")
        self.click(element)
        cmd = "adb shell am broadcast -a ADB_INPUT_CODE --ei code 67"
        for i in range(len(l)):
            os.system(cmd)
            time.sleep(2)
        os.system("adb shell am broadcast -a ADB_EDITOR_CODE --ei code 2")
        
        
    @classmethod
    def click(self,element):
        '''点击'''
        return element.click()
     
    '''输入'''  
    @classmethod
    def sendKeys(self, element, content, pwdType=False):
        if self.unicodeKeyboard:
            print("当前使用appium keyboard输入法")
            return element.send_keys(content)
        else:
            print("当前使用AdbKeyboard输入法")
            element.click()
            cmd = "adb shell am broadcast -a ADB_INPUT_TEXT --es msg '%s'" % content
            os.system(cmd)
            os.system("adb shell am broadcast -a ADB_EDITOR_CODE --ei code 2")
            nowText = element.get_attribute("text")
            content = str(content)
            if not pwdType:
                if nowText == content:
                    pass
                else:
                    raise Exception("输入内容%s失败" % content)
        
    @classmethod
    def setValue(self, element, content):
        return self.driver.set_value(element, content)
    
    @classmethod
    def assertTrue(self, p, errorInfo):
        #断言真: 表达式p若为假, 则抛错, 并显示errorInfo
        try:
            assert p, errorInfo
        except AssertionError:
            raise
         
    @classmethod
    def pageShouldContainsText(self, expectedText):
        '''检查页面是否出现指定文本'''
        time.sleep(3)
        pageSource = self.driver.page_source
        self.assertTrue(expectedText in pageSource, "%s is NOT in current Page." % expectedText)
    
    @classmethod
    def switchToContext(self, contextName):
        return self.driver.switch_to.context(contextName)
     
    @classmethod
    def getPageSource(self):
        '''webview专用:返回页面源码html'''
        return self.driver.page_source
    
    @classmethod
    def getAndroidDisplayResolution(self):
        '''获取安卓屏幕分辨率'''
        r =  os.popen("adb shell dumpsys display | findstr PhysicalDisplayInfo").read()
        Resolu = None
        if "not found" in r or r=="":
            r = os.popen("adb shell wm size").read()
            Resolu = r.replace("\n","").replace("\r","").split(": ")[1].split("x")
        else:
            Resolu = r.split('{')[1].split(',')[0].replace(' ','').split("x")
        
        width = Resolu[0]
        height = Resolu[1]
        print("获取到分辨率：%sx%s" %(width, height))
        return int(width), int(height)
     
    @classmethod
    def swipe(self, startx, starty, endx, endy, dur=800):
        '''startx:滑动起始点横坐标，starty:滑动起始点纵坐标，endx：滑动终点横坐标，endy：滑动终点纵坐标，dur：在多少时间内完成滑动动作（单位：ms毫秒）'''
        return self.driver.swipe(start_x=startx, start_y=starty, end_x=endx, end_y=endy, duration=dur)
    
    @classmethod
    def restartAPP(self):
        '''重启app'''
        self.driver.close_app()
        self.driver.launch_app()
   
    @classmethod
    def close(self):
        '''关闭appium webdriver'''
        self.driver.quit()
    
    @classmethod
    def accessNewTabByClickLink(self, locator):
        ''''仅Web测试可用: 通过点击链接进入新页签'''
        try:
            windowsBefore = self.driver.window_handles
            el = self.findElement(locator)
            self.click(el)
            windowsAfter = self.driver.window_handles
            while windowsBefore==windowsAfter:
                time.sleep(1)
                windowsAfter = self.driver.window_handles
            for newWindow in windowsAfter:
                if newWindow not in windowsBefore:
                    self.driver.switch_to_window(newWindow)
                    print ("Switched to new window")
        except Exception:
            raise
    
    @classmethod
    def hideAppToBackend(self):
        return self.driver.press_keycode(3)
    
    @classmethod
    def findImageElement(self, locator):
        e = self.findElement(locator=locator)
        location = e.location
        size = e.size
        box = (location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"])
        f = os.path.join(self.projectImagesDir,"screenshot.png")
        self.driver.get_screenshot_as_file(f)
        im = Image.open(f)
        region = im.crop(box)
        region.save(os.path.join(self.projectImagesDir,"temp.png"))
        return e
    
    @classmethod
    def saveImageElementAs(self, imgEl, stringName="temp"):
        location = imgEl.location
        size = imgEl.size
        box = (location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"])
        f = os.path.join(self.projectImagesDir,"screenshot.png")
        self.driver.get_screenshot_as_file(f)
        im = Image.open(f)
        region = im.crop(box)
        region.save(os.path.join(self.projectImagesDir,"%s.png" % stringName))
        
    @classmethod
    def findImageElements(self, locator, listTosaveTo):
        els = self.findElements(locator=locator)
        ind = 0
        for i in els:
            location = i.location
            size = i.size
            box = (location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"])
            f = os.path.join(self.projectImagesDir,"screenshot.png")
            self.driver.get_screenshot_as_file(f)
            im = Image.open(f)
            region = im.crop(box)
            region.save(os.path.join(self.projectImagesDir,listTosaveTo[ind]+".png"))
            ind+=1
        
    #PIL对比图片相似度
    @classmethod
    def sameAsWithPIL(self, sourceImageElementPath, percent =  0.1):
        image1 = Image.open(os.path.join(self.projectImagesDir,"temp.png"))
        sourceImageElementPath = os.path.join(self.projectImagesDir, sourceImageElementPath+".png")
        image2 = Image.open(sourceImageElementPath)
        histogram1 = image1.histogram()
        histogram2 = image2.histogram()
        differ = math.sqrt( reduce(operator.add, list(map(lambda a,b: (a-b)**2, histogram1, histogram2))))
        print("差异度:", differ)
        if differ <= 100:
            return True
        else:
            return False
    
    #openCV对比图片相似度
#     @classmethod
#     def sameAsWithOpenCV(self, sourceImagePath,size = (256,256)):  
#         # 先计算直方图  
#         # 几个参数必须用方括号括起来  
#         # 这里直接用灰度图计算直方图，所以是使用第一个通道，  
#         # 也可以进行通道分离后，得到多个通道的直方图  
#         # bins 取为16
#         # 相似度>0.8则认为一样  
#         img1 = cv2.imread(os.path.join(self.projectImagesDir,"temp.png"))
#         img2 = cv2.imread(os.path.join(self.projectImagesDir,sourceImagePath+".png"))
#         image1 = cv2.resize(img1,size)  
#         image2 = cv2.resize(img2,size)  
#         hist1 = cv2.calcHist([image1],[0],None,[256],[0.0,255.0])  
#         hist2 = cv2.calcHist([image2],[0],None,[256],[0.0,255.0])   
        # 计算直方图的重合度  
#         degree = 0  
#         for i in range(len(hist1)):  
#             if hist1[i] != hist2[i]:  
#                 degree = degree + (1 - abs(hist1[i]-hist2[i])/max(hist1[i],hist2[i]))  
#             else:  
#                 degree = degree + 1  
#         degree = degree/len(hist1) 
#         if isinstance(degree, float):
#             return degree>0.9
#         else:   
#             return degree.tolist()[0]>0.9
    
    @classmethod
    def dragFromAToB(self, locatorA, locatorB):
        e1 = self.findElement(locatorA)
        e2 = self.findElement(locatorB)
        return self.driver.drag_and_drop(e1, e2)
    
    @classmethod
    def speakWords(self, worlds):
        mixer.init()
        rFile = os.path.join(self.soundResourceDir, worlds+".mp3")
        mixer.music.load(rFile)
        mixer.music.play()
        time.sleep(len(worlds))
