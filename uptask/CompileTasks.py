# -*- coding: utf-8 -*-

import re


class CompileTasks:

    def __init__(self):
        self.unparsed_file_content = ''
        self.tasks = {}
        self.stories = {}
        self.baseRegex = r'(?<={}).*?(?={})'

    def _parse_tasks(self):
        str_start = '@task'
        str_end = '@endtask'
        results = self._run_compiler(str_start, str_end)
        self.tasks = self._parse_regex_result(results)

    def _parse_stories(self):
        str_start = '@story'
        str_end = '@endstory'
        self.stories = self._parse_regex_result(self._run_compiler(str_start, str_end))
        self._check_stories()

    def _check_stories(self):
        for story_key, story in self.stories.items():
            for command in story['commands']:
                if not self.task_exists(command):
                    raise Exception("Story:{} - Task: {} not found".format(story_key, command))

    def _parse_regex_result(self, regex_result):
        parsed_list = {}
        for match in regex_result:
            task_code = match.group()
            task_code_lines = task_code.split('\n')
            task_name = task_code_lines[0].strip().strip("()")
            task_name_and_options = self._parse_task_options(task_name)
            task_options = task_name_and_options['options']
            task_name = task_name_and_options['name']

            del task_code_lines[0]

            parsed_lines = []
            for task in task_code_lines:
                task_clean = task.strip()

                if task_clean:
                    parsed_lines.append(task_clean)

            parsed_list[task_name] = {}
            parsed_list[task_name]['commands'] = parsed_lines
            parsed_list[task_name]['script'] = self._parse_commands_to_script(parsed_lines)
            parsed_list[task_name]['options'] = task_options

        return parsed_list


    def _parse_commands_to_script(self, commands):
        linesGlue = ' && '
        parsed_script = ''
        last_line = commands[-1]

        for command in commands[:-1]:
            command = command.strip(';')
            parsed_script += command
            if not command.endswith('&'):
                parsed_script += linesGlue
            else:
                parsed_script += ' '

        parsed_script += last_line.strip(';&')
        parsed_script += ';'

        return parsed_script

    # Work In Progress (WIP)
    def _parse_task_options(self, task_name):
        if task_name.find(',') == -1:
            return {'name': task_name, 'options': {}}
        else:
            task = task_name.split(',')
            return {'name': task[0], 'options': {}}

    def _run_compiler(self,str_start, str_end):
        pattern = self.baseRegex.format(str_start, str_end)
        return re.finditer(pattern, self.unparsed_file_content, re.MULTILINE | re.DOTALL)

    def task_exists(self, task_name):
        if task_name in self.tasks:
            return True
        else:
            return False

    def run(self, file_content):
        self.unparsed_file_content = file_content
        self._parse_tasks()
        self._parse_stories()
