import unittest
import os
import yaml
from Helper.HTMLTestRunner import HTMLTestRunner
import importlib
from Helper.EmailSender import EmailSender

eutDir = os.path.dirname(__file__)
global_conf_file = os.path.join(eutDir, "Conf", "running.yaml")

with open(global_conf_file, "r") as f:
    global_conf = yaml.load(f)
runningProject = global_conf["project"]
casesDir = os.path.join(eutDir, "Projects", runningProject, "Cases")
logPath = os.path.join(eutDir, "Log", "log.txt")
reportPath = os.path.join(eutDir, "Report", "report.html")
project_config_path = os.path.join(eutDir, "Projects", runningProject, "%s.yaml" % runningProject)
with open(project_config_path, "r") as f:
    project_config = yaml.load(f)

pagesToRun = project_config["pagesToRun"]

modules = []
for fileName in os.listdir(casesDir):
    if fileName.startswith("Test_") and fileName.endswith(".py"):
        moduleName = fileName[:-3]
        modules.append(moduleName)


class Test:

    # 收集测试用例
    def suite(self):
        su = unittest.TestSuite()
        if modules:
            for i in modules:
                m = "Projects.%s.Cases.%s" % (runningProject, i)
                s = importlib.import_module(m)
                clss = getattr(s, i)
                class_name = clss.__name__
                if pagesToRun:
                    for j in pagesToRun.split(", "):
                        if j == class_name:
                            for c in dir(clss):
                                if c.startswith("test_"):
                                    su.addTest(clss(c))
                else:
                    for c in dir(clss):
                        if c.startswith("test_"):
                            su.addTest(clss(c))
        return su


if __name__ == '__main__':
    MyTests = Test()
    with open(reportPath, "wb") as f:
        runner = HTMLTestRunner(stream=f, title='Automation Test Report', description='Project: %s' % runningProject)
        runner.run(MyTests.suite())
    if global_conf["autoSendReport"]:
        EmailSender.send_report(global_conf, reportPath)
