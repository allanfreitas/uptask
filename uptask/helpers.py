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


def print_lines(lines, end=''):
    for line in lines:
        print(clear_string(line), end)


def print_platform():
    print(Fore.RED + 'Platform: {}'.format(platform.system()))


def print_comment(text, end=''):
    print(Fore.YELLOW + text, end)


def print_info(text, end=''):
    print(Fore.GREEN + text, end)


def print_error(text, end=''):
    print(Fore.RED + text, end)


def print_question(text, end=''):
    print(Fore.CYAN + text, end)


def display_title_header(version):
    print("UpTask", end=' ')
    print_info(version)
    print(' ')


def is_accessible(path, mode='r'):
    """
    Check if the file or directory at `path` can
    be accessed by the program using `mode` open flags.
    """
    try:
        f = open(path, mode)
        f.close()
    except IOError:
        return False
    return True
