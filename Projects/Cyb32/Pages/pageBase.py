from BaseDriver.Driver import appiumDriver
from Helper.elementLoader import elementLoader
import time
from collections import OrderedDict
import hashlib
import requests
import json
from bs4 import BeautifulSoup


class pageBase(elementLoader):
    driver = appiumDriver() 
        
    def __init__(self):       
        elementLoader.__init__(self, self.__class__.__name__)
    
    def restartApp(self):
        return self.driver.restartAPP()
    
    def hasWebView(self):
        time.sleep(5)
        webView = "WEBVIEW"
        allContexts = self.driver.getContexts()
        for i in allContexts:
            if (webView in i) or (webView.lower() in i):
                print("发现webview")
                return True
        print("未发现webview")
        return False
    
    def back(self):
        b = self.driver.findElement(self.locator("backBtn"))
        self.driver.click(b)

    def accessHomePageTopMenu(self, menuName="排行榜"):
        menuname = self.driver.findElement(self.locator("homePageTopMenu", menuName))
        self.driver.click(menuname)
  
    def ignoreTip(self):
        btnIgnoreTip = self.driver.findElement(self.locator("btnIgnoreTip"))
        self.driver.click(btnIgnoreTip)
    
    def accessFirstItemInWuSunYinYue(self):
        '''进入无损音乐的第一个专辑'''
        firstItemInWuSunYinYue = self.driver.findElement(self.locator("firstItemInWuSunYinYue"))
        self.driver.click(firstItemInWuSunYinYue)
    
    def accessFirstItemInFuFeiJingPin(self):
        '''进入付费精品的第一个专辑'''
        firstItemInFuFeiJingPin = self.driver.findElement(self.locator("firstItemInFuFeiJingPin"))
        self.driver.click(firstItemInFuFeiJingPin)
    
    def dealWithBuyItemOrNot(self, buy=False):
        '''处理弹框: 是否购买'''
        di = {True:"ok", False:"cancel"}
        btnCancelOrOk = self.driver.findElement(self.locator("btnCancelOrOk", di[buy]))
        self.driver.click(btnCancelOrOk)

    def         format_url_and_header_to_get_token(self):
        t = str(time.time())[0:-3]
        d = {
            "app_key": self.driver.app_key,
            "app_ver": self.driver.app_ver,
            "dc": self.driver.dc,
            "display": self.driver.display,
            "imei": self.driver.imei,
            "mac": self.driver.mac,
            "model": self.driver.model,
            "net_type": "Wi-Fi",
            "os_ver": self.driver.os_ver,
            "password": "8a410024663b6951a483f3d96e666804",
            "timestamp": str(t),
            "username": "18615756926"
        }
        if self.driver.desired_caps["udid"] not in ["GMPNCUEQSSJVSGW8", "0123456789ABCDEF"]:
            d["imsi"] = self.driver.imsi
        od = OrderedDict()
        for k in sorted(d):
            od[k] = d[k]
        s = ""
        for okey in od:
            kAndV = okey + od[okey]
            s += kAndV
        secret = "hf06304bd93ec0e003e41fa056efd80a60"
        salt = "fd36GFPdIU96f8ln99bf16P889rQOP8e"
        targetS = secret + s + t + salt
        codedS = hashlib.sha1(targetS.encode("utf8"))
        sign = codedS.hexdigest()
        h = {
            "sign": sign.upper()
        }
        url = "http://res.hongfans.cn/v1/login"
        return url, h, d

    def get_user_token_via_login(self):
        url_and_header = self.format_url_and_header_to_get_token()
        r = requests.post(url=url_and_header[0], data=url_and_header[2], headers=url_and_header[1])
        try:
            token = json.loads(r.text.encode("latin-1").decode("unicode-escape"))["data"]["token"]
            print("token: %s" % token)
            return token
        except Exception as e:
            return e

    def get_vip_page_source_code(self, token):
        t = str(time.time())[0:-3]
        timestamp=str(t)
        app_key=self.driver.app_key
        dc=self.driver.dc
        app_ver=self.driver.app_ver
        uuid= self.driver.uuid
        r = requests.get(url="http://res.hongfans.cn/buy_vip?timestamp=%s&app_key=%s&dc=%s&app_ver=%s&uuid=%s&token=%s" % (timestamp, app_key, dc, app_ver,uuid, token))
        r.encoding = "utf-8"
        return r.text

    def verify_membership_page(self, page_source):
        soup = BeautifulSoup(page_source, "html.parser")
        dic = {}
        title = soup.title.string
        original_prices = [i.string.replace(" ","") for i in soup.select(".original")]
        pay_ways = [i.string for i in soup.select("label")]
        membership_out_date = soup.select("h4 span")[0].string
        member_nick_name = soup.select(".usernick")[0].string
        dic["title"] = title
        dic["original_prices"] = original_prices
        dic["pay_ways"] = pay_ways
        dic["membership_out_date"] = membership_out_date
        dic["member_nick_name"] = member_nick_name
        return dic
