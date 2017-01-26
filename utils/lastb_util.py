#!/usr/bin/env python
# encoding: utf-8

import cPickle as pk


class LastbUtil(object):

    save_path = './lastb.txt'
    hosts_deny_path = '/etc/hosts.deny'
    max_allowed_num = 3

    def __init__(self):
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
