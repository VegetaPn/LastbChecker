#!/usr/bin/env python
# encoding: utf-8


class Lastb(object):

    def __init__(self):
        self.user = None
        self.tty = None
        self.ip = None
        self.day_of_week = None
        self.date = None
        self.time_from = None
        self.time_to = None

    def parse_from_str(self, str):
        '''
        111111   ssh:notty    159.122.133.233  Fri Dec  2 17:16 - 17:16  (00:00)
        '''
        data_arr = str.split()
        if len(data_arr) != 10:
            pass
        self.user = data_arr[0]
        self.tty = data_arr[1]
        self.ip = data_arr[2]
        self.day_of_week = data_arr[3]
        self.date = (data_arr[4] + ' ' + data_arr[5])
        self.time_from = data_arr[6]
        self.time_to = data_arr[8]
