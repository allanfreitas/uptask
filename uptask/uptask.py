# -*- coding: utf-8 -*-

import os

from .helpers import display_title_header

from .commands import Commands

__version__ = "0.2.0"


def main():
    display_title_header(__version__)

    cmd = Commands(os.getcwd())
    cmd.run()
