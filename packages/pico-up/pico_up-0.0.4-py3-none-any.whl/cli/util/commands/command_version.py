import os
from termcolor import cprint
from .base import CommandBase


class CommandVersion(CommandBase):
    description = 'show the version of pico-up'

    @staticmethod
    def execute(configuration, arguments=None):
        output = os.popen('pip list').read()
        for item in output.split('\n'):
            if item.startswith('pico-up'):
                cprint(item, 'blue')
