#!/usr/bin/env python
# encoding: utf-8

import cPickle as pk
import ConfigParser


class LastbUtil(object):

    def __init__(self):
        self._init_from_config()

    def _init_from_config(self):
        config = ConfigParser.ConfigParser()
        config.read('resources/lastb.conf')
        self.save_path = config.get('modes', 'save_path')
        self.hosts_deny_path = config.get('modes', 'hosts_deny_path')
        self.max_allowed_num = config.getint('modes', 'max_allowed_num')
        self.log_dict = {}

    def save(self):
        f = open(self.save_path, 'wb')
        pk.dump(self.log_dict, f)
        f.close()

    def load(self):
        f = open(self.save_path, 'rb')
        self.log_dict = pk.load(f)
        f.close()

    def add_to_blacklist(self, ip):
        f = open(self.hosts_deny_path, 'a')
        f.write('\nALL:%s:deny' % ip)
        f.close()

    def add_to_blacklist_patch(self, black_dict):
        black_dict = {}
        f = open(self.hosts_deny_path, 'a')
        for ip, n in black_dict.iteritems:
            if n > 3:
                f.write('\nALL:%s:deny' % ip)
                del black_dict[ip]
        f.close()

    def add_to_blacklist_for_set(self, black_set):
        f = open(self.hosts_deny_path, 'a')
        for ip in black_set:
            f.write('\nALL:%s:deny' % ip)
        f.close()
