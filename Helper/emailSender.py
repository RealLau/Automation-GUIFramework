import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
class emailSender:
    #Send report to receivers
    @classmethod
    def sendReport(self, data, resultFileABSPath, projectName):
        print ("Sending report...")
        resultFileName = resultFileABSPath.split("\\")[-1]
        conf = data["emailServer"]
        sender = conf["sender"]
        receivers = conf["receivers"]
        subject = conf["subject"]
        smtpserver = conf["smtpserver"]
        username = conf["username"]
        password = conf["password"]
        msgRoot = MIMEMultipart('related')    
        msgRoot['Subject'] = subject + resultFileName.replace(".html", "")
        f = open(resultFileABSPath, "rb")
        content = f.read()
        f.close()
        msgContentHtml = MIMEText(content,'html','utf-8')
        msgAttach = MIMEText(content, 'base64', 'utf-8')
        msgAttach["Content-Type"] = 'application/octet-stream'    
        msgAttach["Content-Disposition"] = 'attachment; filename=%s' % resultFileName
        msgRoot.attach(msgContentHtml)
        msgRoot.attach(msgAttach)    
        smtp = smtplib.SMTP()    
        smtp.connect(smtpserver)    
        smtp.login(username, password)    
        smtp.sendmail(sender, receivers, msgRoot.as_string())    
        smtp.quit()
        print ("Email report has been sent.")