#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'wenin819'
"""
import datetime
import json

from rocketmq.client import PushConsumer, ConsumeStatus

from clients.mq_sender.rpc_call import RpcCall
from common.log import logger
from config import conf


# 监听rocket mq消息, 并将消息转发到微信
# Path: mq/mq_worker.py
class MqWorker:

    def __init__(self):
        self.groupName = conf().get("szy_mq_group_name", "ticket-group")
        self.nameserver = conf().get("szy_mq_nameserver", '192.168.60.27:9876')
        self.accessKey = conf().get("szy_mq_access_key", '')
        self.secretKey = conf().get("szy_mq_secret_key", '')
        self.topicName = conf().get("szy_mq_topic_name", 'wechat_notify')
        self.TAGS = conf().get("szy_mq_tags", '*')
        self.startTime = datetime.datetime.now()
        self.client = RpcCall()
        self.consumer = None
        pass

    # 消息处理回调
    def callback(self, msg, *args, **kwargs):
        print('Received message. messageId: ', msg.id, ' body: ', msg.body)

        if msg.body is not None and self.client is not None:
            msgObj = None

            try:
                msgObj = json.loads(msg.body)
            except:
                logger.error('[Szy]json.loads error. body: {}'.format(msg.body))
                return ConsumeStatus.CONSUME_SUCCESS

            try:
                self.client.call(msgObj)
            except Exception as e:
                logger.error('[Szy]msg send error. body: {}'.format(msgObj))
                logger.exception(e)


        # 消费成功回复CONSUME_SUCCESS
        return ConsumeStatus.CONSUME_SUCCESS
        # 消费成功回复消息状态
        # return ConsumeStatus.RECONSUME_LATER

    def startup(self):
        # 初始化消费者，并设置消费者组信息
        self.consumer = PushConsumer(self.groupName)
        # 设置服务地址
        self.consumer.set_name_server_address(self.nameserver)
        # 设置权限（角色名和密钥）
        if self.accessKey:
            self.consumer.set_session_credentials(
                self.accessKey,  # 角色密钥
                self.secretKey,  # 角色名称
                ''
            )

        # 订阅topic
        self.consumer.subscribe(self.topicName, self.callback, self.TAGS)
        logger.info(' [Szy][Consumer] Waiting for messages from {} -- {} -- {}.'
                    .format(self.nameserver, self.groupName, self.topicName))
        self.startTime = datetime.datetime.now()
        # 启动消费者
        self.consumer.start()
