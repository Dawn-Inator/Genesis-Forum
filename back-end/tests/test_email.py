import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 邮件发送方的地址和登录凭证
sender_email = "your_email@gmail.com"
sender_password = "your_password"

# 邮件接收方的地址
receiver_email = "receiver_email@example.com"

# SMTP 服务器配置
smtp_server = "smtp.gmail.com"
smtp_port = 465  # 对于 SSL 加密的 SMTP 端口通常是 465

# 创建 MIME 多部分消息对象
message = MIMEMultipart("alternative")
message["Subject"] = "Test Email from Docker Container"
message["From"] = sender_email
message["To"] = receiver_email

# 邮件正文（纯文本和 HTML 版本）
text = """\
Hi,
This is a test email sent from a Docker container."""
html = """\
<html>
  <body>
    <p>Hi,<br>
       This is a <b>test email</b> sent from a <i>Docker container</i>.</p>
  </body>
</html>
"""

# 将文本和 HTML 添加到 MIME 消息中
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")
message.attach(part1)
message.attach(part2)

# 发送邮件
try:
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
