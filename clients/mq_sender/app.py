#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'ahzmr'
"""

import time

from clients.mq_sender.mq_worker import MqWorker
from common.log import logger
from config import load_config


def run():
    try:
        # load config
        load_config()

        worker = MqWorker()
        worker.startup()

        while True:
            time.sleep(1)
    except Exception as e:
        logger.error("App startup failed!")
        logger.exception(e)


if __name__ == '__main__':
    run()
