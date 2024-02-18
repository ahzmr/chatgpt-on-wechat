#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'ahzmr'
"""

import datetime
from xmlrpc.server import SimpleXMLRPCServer

from common.log import logger
from config import conf

import threading


# 监听rpc消息, 并将消息转发到微信
# Path: mq/rpc_worker.py
class RpcWorker:

    def __init__(self, wechatNotice=None):
        self.serverIp = conf().get("szy_rpc_server_ip", 'localhost')
        self.serverPort = conf().get("szy_rpc_server_port", '8191')
        self.startTime = datetime.datetime.now()
        self.wechatNotice = wechatNotice
        self.consumer = None
        pass


    # 消息处理
    def send_wechat_msg(self, msgObj):
        print('Received message. name: ', msgObj['name'], ' msg: ', msgObj['msg'])

        if msgObj is not None and self.wechatNotice is not None:

            try:
                self.wechatNotice.send_msg(msgObj['msg'], msgObj)
            except:
                logger.error('[Szy]send wechat msg error: {}'.format(msgObj))


    def __start_server(self):
        with SimpleXMLRPCServer((self.serverIp, int(self.serverPort)), allow_none=True) as server:
            server.register_function(self.send_wechat_msg, "send_wechat_msg")

            logger.info(' [Szy] RPC server is started => {}:{}'
                        .format(self.serverIp, self.serverPort))
            self.startTime = datetime.datetime.now()

            server.serve_forever()


    def startup(self):
        server_thread = threading.Thread(target=self.__start_server)
        server_thread.start()