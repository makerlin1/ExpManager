# _*_ coding: utf-8 _*_
"""
Time:     2022-05-22 14:51
Author:   Haolin Yan(XiDian University)
File:     utils.py
"""
import os
import smtplib
from email.mime.text import MIMEText
from pyecharts.components import Table
import pandas as pd


# from bs4 import BeautifulSoup


def visualize(df):
    table = Table()
    headers = df.columns.tolist()
    rows = []
    for index, row in df.iterrows():
        rows.append(row.values.tolist())
    table.add(headers, rows)
    html_path = "leaderboard.html"
    table.render(path=html_path)
    with open(html_path, "r") as f:
        html = f.read()
    return html


def send_email(info="", **profile):
    mail_host = 'smtp.163.com'
    # 163用户名
    mail_user = profile["mail_user"]
    mail_pass = profile["secret"]
    sender = profile["sender"]
    receivers = [profile["receiver"]]
    # 邮件内容设置
    message = MIMEText(info, 'html')
    # 邮件主题
    message['Subject'] = profile["theme"]
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = receivers[0]

    # 登录并发送邮件
    smtpObj = smtplib.SMTP()
    # 连接到服务器
    smtpObj.connect(mail_host, 25)
    # 登录到服务器
    smtpObj.login(mail_user, mail_pass)
    # 发送
    smtpObj.sendmail(
        sender, receivers, message.as_string())
    # 退出
    smtpObj.quit()
