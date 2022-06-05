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


class AverageMeter(object):
    """
    Computes and stores the average and current value
    Copied from: https://github.com/pytorch/examples/blob/master/imagenet/main.py
    """

    def __init__(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def accuracy(output, target, topk=(1,)):
    """Computes the precision@k for the specified values of k"""
    maxk = max(topk)
    batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(target.reshape(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].reshape(-1).float().sum(0, keepdim=True)
        res.append(correct_k.mul_(100.0 / batch_size))
    return res
