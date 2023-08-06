#!/usr/bin/env python
# -*- coding:utf-8 -*-
from logging import Filter, LogRecord
from threading import current_thread

from ..cache import CacheManager
from ..config import LogLevel

_trace_id_map_key = "trace_id_map_key"

FMTDCIT = {
    40: "\033[31m{}\033[0m",
    20: "\033[92m{}\033[0m",
    10: "\033[1m{}\033[0m",
    30: "\033[33m{}\033[0m",
    50: "\033[35m{}\033[0m",
    0: "{}"
}


class _SimpleLogFilter(Filter):
    def __init__(self, level: LogLevel):
        super().__init__()
        self.__level = level
        self.__name = ""

    def filter(self, record: LogRecord) -> bool:
        trace_id = CacheManager.get_data(_trace_id_map_key).get(current_thread().ident)
        record.traceid = trace_id or "%TRACEID%"
        record.levelname = FMTDCIT.get(record.levelno).format(record.levelname)
        record.msg = FMTDCIT.get(record.levelno).format(record.msg)
        record.name = self.__name
        return record.levelno <= self.__level.value

    def set_name(self, name):
        self.__name = name
