# _*_ coding:utf-8 _*_
import os
import yaml
import configparser
import time


class ElementLoader:
    
    def __init__(self, page_name):
        current_dir = os.getcwd()
        global_conf_file = os.path.join(current_dir, "Conf", "running.yaml")
        with open(global_conf_file, "rb") as f:
            global_conf = yaml.load(f)
        running_project = global_conf["project"]
        
        page_dir = os.path.join(current_dir, "Projects", running_project, "Pages", 'Elements', page_name+".conf")
        self.data = {}
        cf = configparser.ConfigParser()
        cf.read(page_dir, encoding="utf-8")
        secs = cf.sections()
        for i in secs:
            temp = {}
            for j in cf[i]:
                temp[j] = cf[i][j]
            self.data[i] = temp
        project_config_path = os.path.join(current_dir, "Projects", running_project, "%s.yaml" % running_project)
        with open(project_config_path, "rb") as f:
            project_conf = yaml.load(f)
        self.users = project_conf["users"]

    @classmethod
    def get_time_stamp(self):
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s:%03d" % (data_head, data_secs)
        return time_stamp

    def logger(self, info):
        # 日志器
        now = self.get_time_stamp()
        os.system("echo %s - [USER DEBUG INFO] - %s" % (now, info))

    def locator(self, element_name, *args):
        by_and_value = self.data[element_name]
        by = list(by_and_value.keys())[0]
        value = by_and_value[by]
        ind = 0
        for i in args:
            value = value.replace('{%d}' % ind, i)
            ind += 1
        return by, value

    def get_config_user_info(self, user_id):
        # 获取项目级的自动化专用信息，比如登陆所用的账号密码等
        k = "automation_test_user" + str(user_id)
        return self.users[k]
