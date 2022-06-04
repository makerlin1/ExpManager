# _*_ coding: utf-8 _*_
"""
Time:     2022-05-22 14:07
Author:   Haolin Yan(XiDian University)
File:     trial.py
"""
from loguru import logger
import pandas as pd
import os
import uuid
from .utils import send_email, visualize


class Trial(object):
    def __init__(self, record_path, profile=None, **hyparam):
        # 生成 trial id
        self.hyparam = hyparam
        self.record_path = record_path
        fp = os.path.dirname(self.record_path)
        self.id = str(uuid.uuid1())
        self.output_path = os.path.join(fp, self.id)
        # 创建文件夹
        os.mkdir(self.output_path)
        logger.add(self.output_path + "/runtime.log")
        self.profile = profile

    def report_final_result(self, **result):
        # 合并
        for k, v in result.items():
            self.hyparam[k] = v
        # 写入
        if os.path.isfile(self.record_path):
            leaderboard_ = pd.read_csv(self.record_path)
            leaderboard = {}
            for k, v in leaderboard_.items():
                leaderboard[k] = v.values.tolist()
        else:
            leaderboard = {}

        for k, v in self.hyparam.items():
            column = leaderboard.get(k, [])
            if not isinstance(column, list):
                column = column.values.tolist()
            column.append(v)
            leaderboard[k] = column

        id_list = leaderboard.get("trial_id", [])
        id_list.append(self.id)
        leaderboard["trial_id"] = id_list
        if isinstance(leaderboard, dict):
            leaderboard = pd.DataFrame(leaderboard)
        leaderboard.to_csv(self.record_path, index=False)
        info = "Trial Finished (%s)" % self.id
        if self.profile is not None:
            html = visualize(leaderboard)
            send_email(html, **self.profile)
