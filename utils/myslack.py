#!/usr/bin/env python
# encoding: utf-8


import requests
import json
import logging


class SlackUtil(object):

    def __init__(self):
        self.slack_hook_url = ''

    def send_notify(self, msg):
        payload={'text': msg, 'mrkdwn': 'true'}
        resp = requests.post(self.slack_hook_url, data=json.dumps(payload))
        logging.info(resp)
