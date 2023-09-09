import requests
from datetime import date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 获取当前日期
today = date.today().strftime("%Y-%m-%d")

# GitHub API的URL
url = f"https://api.github.com/search/repositories?q=created:{today}&sort=stars&order=desc"

# 发送GET请求获取数据
response = requests.get(url)

# 邮件内容
mail_content = ""

if response.status_code == 200:
    data = response.json()
    # 获取前100个星星最多的项目
    top_projects = data["items"][:100]

    # 创建分类字典
    categories = {}

    # 打印项目信息
    for project in top_projects:
        name = project["name"]
        stars = project["stargazers_count"]
        url = project["html_url"]
        language = project["language"]

        # 将项目按照语言分类
        if language in categories:
            categories[language].append((name, url))
        else:
            categories[language] = [(name, url)]

    # 打印10个分类
    count = 0
    for language, projects in categories.items():
        if count >= 10:
            break
        mail_content += f"<h2>语言分类：{language}</h2>"
        mail_content += "<p>类似的项目：</p>"
        for project in projects:
            mail_content += f"<p>项目名称：{project[0]}，地址：<a href='{project[1]}'>{project[1]}</a></p>"
        count += 1

    # 打印10个不同的项目
    mail_content += "<h2>其他项目：</h2>"
    unique_projects = set()
    for project in top_projects:
        name = project["name"]
        url = project["html_url"]
        if name not in unique_projects:
            mail_content += f"<p>项目名称：{name}，地址：<a href='{url}'>{url}</a></p>"
            unique_projects.add(name)

else:
    mail_content = "无法获取数据"

# QQ 邮箱 SMTP 服务器地址
mail_host = "smtp.qq.com"

# 发件人邮箱
mail_sender = "3545184062@qq.com"

# 邮箱授权码，不是邮箱密码
mail_license = "cvgdfvcxtmawdaij"

# 收件人邮箱
mail_receivers = ["827737456@qq.com"]

# 邮件标题
mail_title = "GitHub 项目信息"

# 创建一个 MIMEMultipart 对象，包含邮件内容和标题
msg = MIMEMultipart('alternative')
msg['From'] = mail_sender
msg['From'] = mail_sender
msg['To'] = mail_receivers[0]
msg['Subject'] = mail_title

# 添加邮件正文（HTML 格式）
mail_content = mail_content.replace('\n', '<br>')  # 将换行符替换为HTML换行标签
html_content = f"<html><body>{mail_content}</body></html>"
msg.attach(MIMEText(html_content, 'html'))

try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用 SSL，端口号为 465
    smtpObj.login(mail_sender, mail_license)  # 登录 QQ 邮箱
    smtpObj.sendmail(mail_sender, mail_receivers, msg.as_string())  # 发送邮件
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")
