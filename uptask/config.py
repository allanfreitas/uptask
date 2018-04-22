# -*- coding: utf-8 -*-

import os
from .helpers import is_accessible

from dotenv import load_dotenv


class Config:

    def __init__(self, current_path):
        self.attributes = {
            'host': '',
            'user': '',
            'pass': '',
            'user_host': ''
        }
        self.conf_file = current_path + '/.env'
        self.is_valid = False

    def initialize(self):
        if is_accessible(self.conf_file, 'r'):
            load_dotenv(dotenv_path=self.conf_file)

            self.set_attribute('host', os.getenv("UPTASK_HOST", ''))
            self.set_attribute('user', os.getenv("UPTASK_USER", ''))
            self.set_attribute('pass', os.getenv("UPTASK_PASS", ''))
            self.set_attribute('user_host', '{}@{}'.format(self.attributes['user'],self.attributes['host']))
            self.is_valid = True

    def set_attribute(self, atrr, value):
        self.attributes[atrr] = value

    def get_attribute(self, attr):
        if attr in self.attributes:
            return self.attributes[attr]
        else:
            return ''
