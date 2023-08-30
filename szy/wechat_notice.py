#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信通知工具类
__author__ = 'wenin819'
"""
import time
from datetime import datetime

from common.log import logger
from lib import itchat


class WechatNotice:

    def __init__(self, msgKeywordWhiteList=None, nameWhiteList=None, sendInterval=200, _itchat=None):
        self.lastSendTime = datetime.now()
        self.sendInterval = sendInterval
        self.itchat = _itchat if _itchat else itchat
        self.nameWhiteList = nameWhiteList
        self.msgKeywordWhiteList = msgKeywordWhiteList

    # 等待可以发送消息
    def wait_send(self):
        # 如果没有登录，等待登录
        while self.itchat.instance.storageClass.userName is None:
            logger.info('[Szy]Waiting for login...')
            time.sleep(5)

        # 控制发送频率，每秒最多发送5条
        while True:
            now = datetime.now()
            if (now - self.lastSendTime).microseconds >= self.sendInterval:
                self.lastSendTime = now
                break
            else:
                time.sleep(0.1)

    # 获取具体发送对象
    # @lru_cache(maxsize=128)
    def get_user(self, name, chatType='chatroom', update=False):
        # 检查参数name必须有值
        if not name or len(name) == 0:
            logger.warn('[Szy] get_user: name is empty.')
            return None

        logger.info('[Szy] get_user: {} - {}. update: {}'.format(name, chatType, update))


        # 如果是好友
        if 'friend' == chatType:
            if update:
                self.itchat.get_friends(update=update)
            friends = self.itchat.search_friends(name=name)
            if len(friends) > 0:
                return friends[0]
            else:
                return None
        # 如果是群聊
        # elif 'chatroom' == chatType:
        else:
            if update:
                self.itchat.get_chatrooms(update=update)
            chatrooms = self.itchat.search_chatrooms(name=name)
            if len(chatrooms) > 0:
                return chatrooms[0]
            else:
                return None

    # 发送消息
    def send_msg(self, msg, target=dict()):
        # 检查参数msg必须有值
        if not msg or len(msg) == 0:
            logger.warn('[Szy] send_msg: msg is empty.')
            return None

        self.wait_send()

        # 检查名称是否在白名单中
        if self.msgKeywordWhiteList and all([k not in msg for k in self.msgKeywordWhiteList]):
            logger.warn('[Szy] send_msg: msg[{}] is not in white list.'.format(msg))
            return None

        name = target.get('name')
        # 检查名称是否在白名单中
        if self.nameWhiteList and all([n not in name for n in self.nameWhiteList]):
            logger.warn('[Szy] get_user: name[{}] is not in white list.'.format(name))
            return None

        user = None
        for update in [False, True]:
            user = self.get_user(name, target.get('type'), update)
            if user:
                break

        if user:
            logger.debug('[Szy]send message to {}: {}'.format(target, msg))
            user.send_msg(msg)
        else:
            logger.warn('[Szy]send message failed. user not found. {}: {}'.format(target, msg))