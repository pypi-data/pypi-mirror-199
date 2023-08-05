import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from CarH.ProxyConfig import *
import socket

class CPUtils:
    #发送邮件功能
    def send_email(self,email_content):
        # 发件人邮箱账号
        my_sender = My_sender
        # 发件人邮箱密码（授权码）
        my_pass = My_pass
        # 收件人邮箱账号
        my_user = My_user

        # 创建一个MIMEText对象，包含email_content作为邮件正文
        msg = MIMEText(email_content, 'plain', 'utf-8')
        # 设置发件人和收件人地址
        msg['From'] = formataddr(["From Test User", my_sender])
        msg['To'] = formataddr(["Recipient", my_user])
        # 设置邮件主题
        msg['Subject'] = "爬虫问题"

        try:
            # 创建一个SMTP对象，连接QQ邮箱的SMTP服务器
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            # 登录QQ邮箱
            server.login(my_sender, my_pass)
            # 发送邮件
            server.sendmail(my_sender, [my_user], msg.as_string())
            # 关闭SMTP连接
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print("Failed to send email:", e)

    # 传输socket信息，控制ip池的定时任务结束
    def shutdown(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost',Socket_port))
        sock.sendall(b'shutdown')
        sock.close()
