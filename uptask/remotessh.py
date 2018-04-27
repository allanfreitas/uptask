# -*- coding: utf-8 -*-

from paramiko import SSHClient
import paramiko

from .helpers import print_lines, print_error, print_info


class RemoteSsh:
    def __init__(self):
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.user_host = ''

    def connect(self, hostname, username, password):
        self.user_host = '{}@{}'.format(username,hostname)

        print_info('Connecting on [{}]'.format(self.user_host))
        try:
            self.ssh.connect(hostname=hostname, username=username, password=password)
            print_info('Connected on [{}]'.format(self.user_host))
        except paramiko.BadHostKeyException:
            print_error('Cannot connect to the SSH server: Invalid Credentials')
            exit(1)
        except paramiko.AuthenticationException as e:
            error_message = str(e)
            error_message += '\n Check your credentials for the informed hostname: {}'.format(hostname)
            print_error(error_message)
            exit(1)

    def close_connection(self):
        self.ssh.close()

    def exec_cmd(self,cmd):
        stdin,stdout,stderr = self.ssh.exec_command(cmd)

        if stderr.channel.recv_exit_status() != 0:
            return_lines = stderr.readlines()
        else:
            return_lines = stdout.readlines()

        if len(return_lines) > 0:
            if return_lines[0].strip() == "":
                return_lines.pop(0)

        print_lines(return_lines)
