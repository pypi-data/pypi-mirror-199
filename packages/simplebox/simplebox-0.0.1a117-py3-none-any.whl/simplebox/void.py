#!/usr/bin/env python
# -*- coding:utf-8 -*-
from typing import Iterator


class Void(Iterator):
    """
    Represents an empty or useless object
    """
    def __str__(self):
        return Void.__name__

    def __repr__(self):
        return Void.__name__

    def __next__(self):
        raise StopIteration

    def __bool__(self):
        return False

    def __len__(self):
        return 0
