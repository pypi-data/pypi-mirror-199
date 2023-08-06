from .util import commands, CommandHelp
from termcolor import cprint
import sys


def main():
    try:
        args = sys.argv[1:]
        process_command(args[0], args[1:])
    except IndexError:
        cprint('No command given', 'red')
        print()
        CommandHelp.execute()


def process_command(command=None, arguments=None):
    if command in commands.available_commands.keys():
        cprint(f'running {command}')
        commands.available_commands.get(command).execute(arguments)
    else:
        CommandHelp.execute(arguments)
