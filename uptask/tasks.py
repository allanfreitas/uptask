# -*- coding: utf-8 -*-

from .helpers import is_accessible, print_error, print_info, print_comment
from .CompileTasks import CompileTasks
from .remotessh import RemoteSsh
from colorama import Fore


class Tasks:

    def __init__(self, config):
        self.compiler = None
        self.config = config
        self.remote = None

    def initialize(self, arguments):
        filename = arguments.file

        if not is_accessible(filename, 'r'):
            print_error(
                'File "{}" doesnt exists in the current folder, or is not readable by the script'.format(filename))
            exit(1)

        with open(filename, 'r') as my_file:
            dados = my_file.read()

        compiler = CompileTasks()
        compiler.run(dados)

        self.compiler = compiler

    def run_task(self, arguments, name):
        self.initialize(arguments)

        if name in self.compiler.stories.keys():
            print_info('Running Story: {}'.format(name))
            print(self.compiler.stories[name])
            self._run_remote_story(name)
        else:
            if name in self.compiler.stories.keys():
                print_info('Running Task: {}'.format(name))
                print(self.compiler.tasks[name])
                self._run_remote_task(name)
            else:
                print_error('Error! Story or Task not found on the file')

    def list_tasks(self, arguments):
        self.initialize(arguments)

        print_comment('Available stories:')
        for story in self.compiler.stories.keys():
            print_info("    {}".format(story))

        print_comment('Available tasks:')
        for task in self.compiler.tasks.keys():
            print_info("    {}".format(task))

    def _run_story_mode(self, name):
        '''
            WIP - Not implemented yet
        '''
        pass

    def _run_remote_task(self, name):
        '''
            WIP - Not finished
        '''

        # refactor this next 5 lines to improve the "dry"
        # since it will be used in multiple places
        self.remote = RemoteSsh()
        host = self.config.get_attribute('host')
        user = self.config.get_attribute('user')
        password = self.config.get_attribute('pass')
        self.remote.connect(host, user, password)

        # find the task name passed on parameter and if exists run
        # print_comment('Running: ' + Fore.BLUE + '{}'.format(line[0:29].strip()), ' ')
        # ssh.exec_cmd(line)
