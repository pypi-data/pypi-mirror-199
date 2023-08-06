class CommandBase:
    description = ''
    options = []

    @staticmethod
    def execute():
        raise NotImplemented
