import os
import time
from termcolor import cprint
from .base import CommandBase
from .command_build import CommandBuild
from .command_wipe import CommandWipe


class CommandPush(CommandBase):
    description = 'push local application code to a connected pico'
    options = ['push build: run the build command and push built code to the pico']

    @staticmethod
    def execute(arguments=None):
        try:
            if arguments[0] == 'build':
                CommandBuild.execute()
                os.chdir('build')
        except IndexError:
            pass

        CommandWipe.execute()
        cprint('waiting for device', 'blue')
        time.sleep(2.0)
        cprint('pushing local code to device', 'blue')

        os.system(f'mpremote mkdir app')
        for root, dirs, files in os.walk("app", topdown=True):
            for name in files:
                remote_name = os.path.join(root, name).replace('\\', '/')
                os.system(f'mpremote cp {remote_name} :{remote_name}')
            for name in dirs:
                remote_name = os.path.join(root, name).replace('\\', '/')
                os.system(f'mpremote mkdir {remote_name}')

        os.system('mpremote cp main.py :main.py')
        os.system('mpremote cp settings.py :settings.py')
        os.system('mpremote reset')
