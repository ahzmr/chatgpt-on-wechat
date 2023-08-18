#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'wenin819'
"""
import time

from config import conf
from szy.mq_worker import MqWorker
from szy.wechat_notice import WechatNotice


class SzyServices:
    def __init__(self):
        msgKeywordWhiteList = conf().get("szy_msg_keyword_white_list", ['【三只羊供应链】'])
        nameWhiteList = conf().get("szy_msg_name_white_list", ['~三只羊通知'])

        self.notice = WechatNotice(msgKeywordWhiteList, nameWhiteList)
        self.mq_worker = MqWorker(wechatNotice=self.notice)

    def startup(self):
        self.mq_worker.startup()


if __name__ == '__main__':
    mq_worker = MqWorker(wechatNotice=None)
    mq_worker.startup()

    while True:
        time.sleep(3600)
