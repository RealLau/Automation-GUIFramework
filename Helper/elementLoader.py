# _*_ coding:utf-8 _*_
import os
import yaml
import configparser
import time


class elementLoader:
    
    def __init__(self, pageName):
        cDir = os.getcwd()
        globalConfFile = os.path.join(cDir, "Conf", "running.yaml")
        with open(globalConfFile, "rb") as f:
            globalConf = yaml.load(f)
        runningProject = globalConf["project"]
        
        pageDir = os.path.join(cDir, "Projects",runningProject,"Pages",'Elements',pageName+".conf")
        self.data = {}
        cf = configparser.ConfigParser()
        cf.read(pageDir, encoding="utf-8")
        secs = cf.sections()
        for i in secs:
            temp = {}
            for j in cf[i]:
                temp[j] = cf[i][j]
            self.data[i] = temp
        projectConfigPath = os.path.join(cDir, "Projects",runningProject,"%s.yaml" % runningProject)
        with open(projectConfigPath, "rb") as f:
            projectConf = yaml.load(f)
        self.users = projectConf["users"]

    def get_time_stamp(self):
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s:%03d" % (data_head, data_secs)
        return time_stamp

    def logger(self, info):
        now = self.get_time_stamp()
        os.system("echo %s - [USER DEBUG INFO] - %s" % (now, info))

    def locator(self, elementName, *args):
        byAndValue = self.data[elementName]
        by = list(byAndValue.keys())[0]
        value = byAndValue[by]
        ind = 0
        for i in args:
            value = value.replace('{%d}' % ind, i)
            ind+=1
        print(value)
        return by, value

    def getUserWithID(self, user_id):
        k = "user"+str(user_id)
        return self.users[k]