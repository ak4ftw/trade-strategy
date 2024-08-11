import smtplib
import tools
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# 发送文本邮件
def send_email_text(toEmail, title, text):
    # 邮件信息
    from_email = tools.kv_get("send_email_username")
    to_email = toEmail
    subject = title
    body = text

    # 设置SMTP服务器及端口
    smtp_server = tools.kv_get("send_email_smtp_server")
    smtp_port = tools.kv_get("send_email_smtp_port")
    password = tools.kv_get("send_email_password")

    # 创建MIMEMultipart对象
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    # 将邮件正文添加到MIMEMultipart对象中
    msg.attach(MIMEText(body, "plain"))

    # 发送邮件
    try:
        # 连接到SMTP服务器
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 启用安全传输模式
        server.login(from_email, password)

        # 发送邮件
        server.sendmail(from_email, to_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # 关闭服务器连接
        server.quit()

    pass
