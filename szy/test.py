#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'wenin819'
"""

import time
from rocketmq.client import PushConsumer, ConsumeStatus

# 消息处理回调
def callback(msg):
   # 模拟业务
   print('Received message. messageId: ', msg.id, ' body: ', msg.body)
   # 消费成功回复CONSUME_SUCCESS
   return ConsumeStatus.CONSUME_SUCCESS
   # 消费成功回复消息状态
   # return ConsumeStatus.RECONSUME_LATER



if __name__ == '__main__':
   # 初始化消费者，并设置消费者组信息
   consumer = PushConsumer('ticket-group')
   # 设置服务地址
   consumer.set_name_server_address('192.168.60.27:9876')
   # 设置权限（角色名和密钥）
   # consumer.set_session_credentials(
   #     accessKey,	 # 角色密钥
   #     secretKey,   # 角色名称
   #     ''
   # )
   # 订阅topic
   consumer.subscribe('wechat_notify', callback)
   print(' [Consumer] Waiting for messages.')
   # 启动消费者
   consumer.start()

   while True:
       time.sleep(3600)
   # 资源释放
   consumer.shutdown()
