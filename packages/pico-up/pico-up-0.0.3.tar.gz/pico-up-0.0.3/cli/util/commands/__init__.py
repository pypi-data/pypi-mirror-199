from .command_build import CommandBuild
from .command_init import CommandInit
from .command_push import CommandPush
from .command_wipe import CommandWipe

available_commands = {
    'build': CommandBuild,
    'init': CommandInit,
    'push': CommandPush,
    'wipe': CommandWipe,
}
