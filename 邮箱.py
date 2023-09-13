import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
# 获取天气数据
def get_weather():
    response = requests.get('https://api.vvhan.com/api/weather?city=%E7%9C%89%E5%B1%B1&type=week')
    content = response.text

    # 解析JSON字符串
    data = json.loads(content)

    # 提取中文内容
    city = data['city']
    week = data['info']['week']
    type = data['info']['type']
    low = data['info']['low']
    high = data['info']['high']
    fengxiang = data['info']['fengxiang']
    fengli = data['info']['fengli']
    night_type = data['info']['night']['type']
    night_fengxiang = data['info']['night']['fengxiang']
    night_fengli = data['info']['night']['fengli']
    tip = data['info']['tip']

    return f'城市: {city}<br>星期：{week}<br>天气类型:{type}<br>最低温度:{low}<br>最高温度:{high}<br>风向:{fengxiang}<br>风力:{fengli}<br>夜间天气类型:{night_type}<br>夜间风向:{night_fengxiang}<br>夜间风力:{night_fengli}<br>提示:{tip}<br>'

def get_hitokoto():
    # 使用一言网站的API获取一言
    url = 'https://v1.hitokoto.cn/'
    response = requests.get(url)
    hitokoto_data = response.json()

    return hitokoto_data['hitokoto']


def get_history_data():
    # 替换为你的API请求URL
    url = 'https://api.oioweb.cn/api/common/history'
    response = requests.get(url)

    # 解析API响应
    data = response.json()

    # 提取所有字段值
    results = data["result"]
    history_list = []
    for result in results:
        year = result["year"]
        title = result["title"]
        history_list.append(f'时间：{year}<br>事件：{title}<br>')  # 使用HTML标签<br>来表示换行

    return ''.join(history_list)

# 发送邮件
def get_api_data():
    url = 'https://api.vvhan.com/api/en'
    response = requests.get(url)
    data = response.json()
    return data

def tp(text):
    api_data = get_api_data()
    zh_text = api_data['data']['zh']
    en_text = api_data['data']['en']
    pic_text = api_data['data']['pic']

    msg = MIMEMultipart()
    html = f"""
        <html>
            <body>
                <p>{text}</p>
                 <h1>今日励志语录</h1>
                <p>中文：{zh_text}</p>
                <p>英文：{en_text}</p>
                <img src="{pic_text}" alt="图片">
                <h1>今日二次元图片</h1>
                <img src="https://api.vvhan.com/api/acgimg" alt="图片">
                <h1>今日风景元图片</h1>
                <img src="https://api.vvhan.com/api/view" alt="图片">
                <h1>60秒读懂世界</h1>
                <img src="https://api.vvhan.com/api/60s" alt="图片">
            </body>
        </html>
        """
    msg.attach(MIMEText(html, 'html'))
    return msg
def send_email():
    sender_email = '3545184062@qq.com'
    sender_password = 'cvgdfvcxtmawdaij'
    receiver_email = ['827737456@qq.com']
    smtp_server = 'smtp.qq.com'
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_email)
    msg['Subject'] = 'FY云自动推送'

    # 获取天气数据
    weather = get_weather()

    # 添加文本内容
    hitokoto = get_hitokoto()
    ls = get_history_data()
    text = f'今日{weather}<br><br>一言：{hitokoto}<br><br>历史上的今天：<br>{ls}<br>'
    msg.attach(MIMEText(text, 'plain'))
    msg.attach(tp(text))

    # 发送邮件
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print('邮件发送成功！')
    except Exception as e:
        print('邮件发送失败！错误信息：', str(e))


send_email()
