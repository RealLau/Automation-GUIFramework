import unittest
import os
import yaml
from Helper.HTMLTestRunner import HTMLTestRunner
import importlib
eutDir = os.path.dirname(__file__)
globalConfFile = os.path.join(eutDir, "Conf", "running.yaml")

with open(globalConfFile, "r") as f:
    globalConf = yaml.load(f)
runningProject = globalConf["project"]
casesDir = os.path.join(eutDir, "Projects", runningProject, "Cases")
logPath = os.path.join(eutDir, "Log", "log.txt")
reportPath = os.path.join(eutDir, "Report", "report.html")
projectConfigPath = os.path.join(eutDir, "Projects", runningProject, "%s.yaml" % runningProject)
with open(projectConfigPath, "r") as f:
    projectConfig = yaml.load(f)

pagesToRun = projectConfig["pagesToRun"]

modules = []
for fileName in os.listdir(casesDir):
    if fileName.startswith("test_") and fileName.endswith(".py"):
        moduleName = fileName[:-3]
        modules.append(moduleName)


class Test:
    def suite(self): #Function stores all the modules to be tested
        su = unittest.TestSuite()
        print(modules)
        if modules:
            for i in modules:
                m = "Projects.%s.Cases.%s" % (runningProject, i)
                s = importlib.import_module(m)
                clss = getattr(s,i)
                className = clss.__name__
                print(pagesToRun)
                if pagesToRun:
                    for j in pagesToRun.split(", "):
                        if j == className:
                            for c in dir(clss):
                                if c.startswith("test_"):
                                    su.addTest(clss(c))
                else:
                    for c in dir(clss):
                        if c.startswith("test_"):
                            su.addTest(clss(c))
        print(su)
        return su


if __name__ == '__main__':
    MyTests = Test()
    with open(reportPath, "wb") as f:
        runner = HTMLTestRunner(stream=f,title='Automation Test Report',description='Project: %s' % runningProject)
        runner.run(MyTests.suite())
    if globalConf["autoSendReport"]:
        emailSender.sendReport(globalConf, reportPath, runningProject)
