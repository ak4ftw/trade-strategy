import time
import hashlib
import math
import vndb
import pmodel
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# 时间处理
def get_now_time():
    return time.time()
    
def get_now_date_format(format = '%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, time.localtime(time.time()))

def get_date_format(format, input_time):
    return time.strftime(format, time.localtime(input_time))
    
def str_md5(s):
    md5_hash = hashlib.md5()
    md5_hash.update(s.encode('utf-8'))
    return md5_hash.hexdigest()
    
# 获取鸡蛋手续费 会自动向上取整2位小数 默认万分之1.5 保值万分之0.75
def get_jd_charge(price):
    charge = price * 10 * 0.00015
    charge_ceil = math.ceil(charge * 100) / 100
    return charge_ceil
    
# 获取鸡蛋手续费
def get_jd_charge_total(price, num):
    charge = get_jd_charge(price) * num
    return charge

# 获取kv
def kv_get(key):
    get = pmodel.KV.select(pmodel.KV.value).where(pmodel.KV.key == key).first()
    if get == None:
        return ''
    return get.value

# 获取账户下持仓的所有code
def kv_account_open_code(account):
    select = pmodel.Slice.select(pmodel.Slice.code).where((pmodel.Slice.account == account) & (pmodel.Slice.is_close == 0)).group_by(pmodel.Slice.code)
    account_open_code = []
    for v in select:
        account_open_code.append(v.code)
    return account_open_code

# 获取账户
def get_account():
    get = pmodel.Account.select(pmodel.Account.account).first()
    if get == None:
        return ''
    return get.account

# 获取今日是否下单 True 今日已经下过单; False 今日未下过单;
def is_today_open():
    now_date_form = time.strftime("%Y-%m-%d", time.localtime())
    slice_model = vndb.SliceModel()
    where = f"`create_date` >= '{now_date_form} 00:00:00' AND create_date <= '{now_date_form} 23:59:59'"
    count = slice_model.Count(where)
    if count > 0:
        return True
    return False


# 发送文本邮件
def send_email_text(toEmail, title, text):
    # 邮件信息
    from_email = kv_get("send_email_username")
    to_email = toEmail
    subject = title
    body = text

    # 设置SMTP服务器及端口
    smtp_server = kv_get("send_email_smtp_server")
    smtp_port = kv_get("send_email_smtp_port")
    password = kv_get("send_email_password")

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
