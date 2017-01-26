#!/usr/bin/env python
# encoding: utf-8
import time


class DateUtil:

    def is_firstday(self):
        return time.localtime().tmday == 1
