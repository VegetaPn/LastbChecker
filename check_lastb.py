#!/usr/bin/env python
# encoding: utf-8


import os
import time
import ConfigParser

from models.lastb import Lastb
from utils.common_utils import DateUtil
from utils.lastb_util import LastbUtil


class LastbChecker(object):

    config_path = 'resources/lastb.conf'

    def __init__(self):
        self._init_from_config(self.config_path)
        # self.lastb_cmd = 'lastb'
        # self.lastb_num = 10
        # self.lastb_opt = ' -' + str(10)
        # self.check_interval = 30
        # self.lastb_log = os.popen(self.lastb_cmd).readlines()
        # self.lastb_len = len(self.lastb_log)
        # self.history_len = self.lastb_len
        # self.lastb_util = LastbUtil()

    def _init_from_config(self, path):
        config = ConfigParser.ConfigParser()
        config.read(path)

        self.lastb_cmd = config.get('lastb', 'lastb_cmd')
        self.lastb_num = config.getint('lastb', 'lastb_num')
        self.lastb_opt = ' -' + str(10)
        self.check_interval = config.getint('lastb', 'check_interval')
        self.lastb_log = os.popen(self.lastb_cmd).readlines()
        self.lastb_len = len(self.lastb_log)
        self.history_len = self.lastb_len
        self.lastb_util = LastbUtil()

    '''
    ALL:123.123.123:deny
    '''
    def _load_blacklist(self, result):
        config = ConfigParser.ConfigParser()
        config.read(self.config_path)
        load_path = config.get('modes', 'hosts_deny_path')
        f = open(load_path, 'r')
        for line in f.readlines():
            if line.strip().startswith('#') or line.strip() == '':
                continue

            ip = ''
            try:
                ip = line.strip().split(':')[1]
            except Exception as e:
                print(e)

            if ip:
                result.add(ip)

    def do_easy_check(self):
        history_black_set = set()
        black_set = set()
        counter = 0
        self._load_blacklist(history_black_set)

        while True:
            time.sleep(self.check_interval)
            counter += 1
            print('new round start: ' + str(counter))

            self.lastb_log = os.popen(self.lastb_cmd + self.lastb_opt).readlines()
            self.lastb_len = len(self.lastb_log)

            for i in range(self.lastb_num):
                if self.lastb_log[i] == '' or self.lastb_log[i].startswith('btmp begins'):
                    continue
                lastb = Lastb()
                lastb.parse_from_str(self.lastb_log[i])
                if lastb.ip not in history_black_set:
                    black_set.add(lastb.ip)
                    history_black_set.add(lastb.ip)
                    print("new black ip founded and added to blacklist: " + lastb.ip)
                else:
                    pass
            self.lastb_util.add_to_blacklist_for_set(black_set)
            black_set.clear()

    def do_check(self):
        date_util = DateUtil()
        black_count_dict = {}
        while True:
            time.sleep(60)
            self.lastb_log = os.popen(self.lastb_cmd).readlines()
            self.lastb_len = len(self.lastb_log)
            if self.lastb_len < self.history_len:
                if date_util.is_firstday():
                    self.history_len = 0
                else:
                    from utils import myslack
                    myslack.send_notify('lastb accoured an error: lastb_len < history_len')
                    break

            if self.lastb_len != self.history_len:
                len_diff = self.lastb_len - self.history_len
                for i in range(len_diff):
                    if self.lastb_log[i] == '' or self.lastb_log[i].startswith('btmp begins'):
                        self.history_len == self.lastb_len
                        break
                    lastb = Lastb()
                    lastb.parse_from_str(self.lastb_log[i])
                    black_count_dict[lastb.ip] = black_count_dict[lastb.ip] + 1 if lastb.ip in black_count_dict else 1
                self.lastb_util.add_to_blacklist_patch(black_count_dict)


if __name__ == '__main__':
    checker = LastbChecker()
    # checker.do_check()
    checker.do_easy_check()
