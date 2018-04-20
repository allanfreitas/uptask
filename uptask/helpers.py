# -*- coding: utf-8 -*-

import platform
from colorama import Fore, Back, Style, init


# Start Colorama Lib
init(autoreset=True)


def clear_string(text):
    text = text.replace('\n','')
    text = text.replace('\t','')
    text = text.replace('\r','')
    return text


def print_lines(lines):
    for line in lines:
        print(clear_string(line))


def print_platform():
    print(Fore.RED + 'Platform: {}'.format(platform.system()))


def print_comment(text):
    print(Fore.YELLOW + text)


def print_info(text):
    print(Fore.GREEN + text)


def print_error(text):
    print(Fore.RED + text)


def print_question(text):
    print(Fore.CYAN + text)


def display_title_header(version):
    print("UpTask", end=' ')
    print_info(version)
    print(' ')