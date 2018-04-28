# -*- coding: utf-8 -*-

from .helpers import is_accessible, print_error, print_info, print_comment, print_lines
from .CompileTasks import CompileTasks
from .remotessh import RemoteSsh
from colorama import Fore
import os
import sys
import subprocess
import shlex

class Tasks:

    def __init__(self, config):
        self.compiler = None
        self.config = config
        self.remote = None
        self.stopAfterMe = False
        self.stopAfterTask = None

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
            self._run_remote_story(name ,self.compiler.stories[name])
        else:
            if name in self.compiler.tasks.keys():
                if not self.config.is_local:
                    self._connect_ssh()

                self._run_remote_task(name, self.compiler.tasks[name]['script'])
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

    def _run_remote_story(self, name, story):
        print_comment('Running Story: {}'.format(name))

        if not self.config.is_local:
            self._connect_ssh()

        for task in story['commands']:
            self._run_remote_task(task, self.compiler.tasks[task]['script'])

    def _run_remote_task(self, name, script, error_triggered=False):
        if not error_triggered:
            print_comment('Running Task: ' + Fore.BLUE + '{}'.format(name))
        else:
            print_comment('Running Halt Trigger: ' + Fore.RED + '{}'.format(name))

        if not self.config.is_local:
            self.remote.exec_cmd(script)
            print('')
        else:
            self._run_local_command(script, name)

    def _run_local_command(self, command, name):

        process = subprocess.Popen(
            command, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf8'
        )

        while True:
            output = process.stdout.readline()

            if output == '' and process.poll() is not None:
                # print(process.returncode)
                if process.returncode > 0:
                    self.stopAfterMe = True
                    self.stopAfterTask = name
                    print_lines(process.stderr.readlines())
                    name_halted = name+'.halt'
                    if self.compiler.task_exists(name_halted):
                        
                        self._run_remote_task(name_halted, self.compiler.tasks[name_halted]['script'], True)

                break

            if output:
                print(output.strip())

        if self.stopAfterMe:
            print_error('\nError on Task: {}'.format(self.stopAfterTask))
            sys.exit(1)

        rc = process.poll()
        return rc

    def _connect_ssh(self):
        self.remote = RemoteSsh()
        host = self.config.get_attribute('host')
        user = self.config.get_attribute('user')
        password = self.config.get_attribute('pass')
        self.remote.connect(host, user, password)
