# -*- coding: utf-8 -*-
import sys
import argparse
from .helpers import print_comment, print_info, print_error, print_question, clear_string, is_accessible
from .remotessh import RemoteSsh
from .config import Config

from .tasks import Tasks

from colorama import Fore, Back, Style


class Commands:
    def __init__(self, current_path):
        self.arguments = {}
        self.arguments_custom_parse = []
        self.argParser = None
        self.positional_args = 0

        self.command_list = {
            'init': {
                'description': 'Create .env file if doesnt exists',
                'function_name': '_run_init'
            },
            'runfile': {
                'description': 'Read a Simple Text File With Linux Commands to execute',
                'function_name': '_run_file'
            },
            'tasks': {
                'description': 'Read tasks file and list the available tasks to execute',
                'function_name': '_run_tasks_list'
            },
            'run': {
                'description': 'Read tasks file and execute the requested task',
                'function_name': '_run_tasks_run'
            },
        }
        self.current_path = current_path
        self.config = Config(current_path)
        self.config.initialize()

    def _if_command_is_available(self, command):
        if command in self.command_list:
            return True
        else:
            return False

    def _list_available_commands(self):
        print_comment('Available Commands:')

        title_size = 0
        for cmd, info in self.command_list.items():
            cmd_size = len(cmd)
            if cmd_size > title_size:
                title_size = cmd_size

        for cmd, info in self.command_list.items():
            print_info("    {cmd} : {desc}".format(cmd=cmd.ljust(title_size), desc=info['description']))

        print_comment('\nHow run a command?')
        print_info("    updtask runfile mytxtfile\n")
        print_comment('# INFO: Each command has it\'s own params ##\n')

    def _run_tasks_list(self, param):
        tasks = Tasks(self.config)
        tasks.list_tasks(self.arguments)

    def _run_tasks_run(self, param):
        tasks = Tasks(self.config)
        tasks.run_task(self.arguments, param)

    def _run_file(self, param):
        if param == '':
            print_error('You must pass a file name to read and run')
        else:
            if is_accessible(param):
                with open(param, 'r') as f:
                    self.via_ssh(f)
            else:
                print_error('File doesnt exists in the current folder, or is not readable by the script')

    def _run_init(self, param):

        env_new_contents = """# UpTask Env
# Any Other Vars in the future will be using the "UPTASK_" Prefix
UPTASK_HOST=127.0.0.1
UPTASK_USER=your_user
UPTASK_PASS=your_pass
"""

        if not is_accessible(self.config.conf_file):
            with open(self.config.conf_file, 'w') as f:
                f.write(env_new_contents)

            print_info('The .env file was created!')
        else:
            print_info('The .env file already exists!')
            print_info('Nothing to do :)')

    def _run_cmd(self, command_name):
        func_to_call = self.command_list[command_name]['function_name']
        runner = getattr(self, func_to_call)

        param = ''
        if len(self.arguments_custom_parse) > 1:
            param = self.arguments_custom_parse[1]
            self.argParser.add_argument('cmd_param', help="Command Param to Run", default='list')

        self.argParser.add_argument("-f", "--file", help="File in Tasks Pattern", required=False,
                                    default="tasks.uptask")

        self.argParser.add_argument("--host", help="Host to Connect", required=False,
                                    default=None)

        self.arguments = self.argParser.parse_args()

        # runner it's the function_name on the command_list for the argv[1]
        runner(param)

    def via_ssh(self, f):
        ssh = RemoteSsh()
        host = self.config.get_attribute('host')
        user = self.config.get_attribute('user')
        password = self.config.get_attribute('pass')

        ssh.connect(host, user, password)

        for line in f:
            if not line.startswith('#'):
                print_comment('Running: '+Fore.BLUE + '{}'.format(line[0:29].strip()), ' ')
                ssh.exec_cmd(line)
                print('')

        f.close()

    def run(self):
        self.argParser = argparse.ArgumentParser()

        for arg in sys.argv[1:]:
            if not arg.startswith('-'):
                self.positional_args = self.positional_args + 1
                self.arguments_custom_parse.append(arg)

        if len(self.arguments_custom_parse) == 0:
            self._list_available_commands()
        else:
            # print(self.arguments_custom_parse)
            # If has more than 1 argument check for the command
            if self._if_command_is_available(self.arguments_custom_parse[0]):
                self.argParser.add_argument('command', help="Which Command to Run", default='list')
                self._run_cmd(self.arguments_custom_parse[0])
            else:
                print_error('#### ------------------------ ! ERROR ! ------------------------- ####')
                print_error('#### -------- Command not Found! Check the list below :) -------- ####')
                print(' ')
                self._list_available_commands()
                exit(1)
