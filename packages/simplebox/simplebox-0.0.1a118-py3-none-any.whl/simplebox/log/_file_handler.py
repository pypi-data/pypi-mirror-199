#!/usr/bin/env python
# -*- coding:utf-8 -*-
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from time import time, localtime


class _TimedRotatingFileHandlerWrapper(TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False,
                 atTime=None):
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc)
        self.__filename = filename
        self.__atTime = atTime

    def doRollover(self):
        """
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        currentTime = int(time())
        dstNow = localtime(currentTime)[-1]
        dfn = f"{self.__filename}.{datetime.now().strftime('%Y-%m-%d')}.log"
        self.baseFilename = dfn
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:
                    addend = -3600
                else:
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt
