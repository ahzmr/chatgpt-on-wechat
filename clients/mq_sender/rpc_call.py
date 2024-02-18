#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'ahzmr'
"""

import xmlrpc.client
from common.log import logger
from config import conf


class RpcCall:

    def __init__(self):
        self.serverUrl = conf().get("szy_rpc_server_url", 'http://localhost:8191')
        self.client = None

    def call(self, msgObj):
        self.startup()
        if self.client is None:
            logger.error('[Szy]call RPC error: client is not inited.')
            return

        self.client.send_wechat_msg(msgObj)  # 调用服务器端的方法

    def startup(self):
        if self.client is None:
            self.client = xmlrpc.client.ServerProxy(self.serverUrl, allow_none=True)

if __name__ == '__main__':
    call = RpcCall()
    call.call({'name': '彤妍家', 'msg': '【三只羊供应链】这是测试消息'})
