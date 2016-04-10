from inspect import getfullargspec

from finance_keeper_bot.logger import main_log as log


class InvalidCommandException(Exception):
    pass


class InvalidCommandArgumentsException(Exception):
    pass


class CommandRouter:
    def __init__(self):
        self.commands_map = dict()

    def command(self, name):
        def decorator(cls):
            self.commands_map[name] = cls
            return cls
        return decorator

    async def resolve(self, command, chat_id):
        if type(command) == str:
            command = (command, list())

        if command[0] not in self.commands_map:
            log.error('command %s not found' % (command[0],))
            raise InvalidCommandException(command[0])

        call_class = self.commands_map[command[0]]
        command_instance = call_class(chat_id=chat_id)

        args_list = getfullargspec(command_instance.run)
        if len(command[1]) > len(args_list.args) -1:
            raise InvalidCommandArgumentsException('max args count : %s' % (len(args_list.args)-1))

        await command_instance.run(*command[1])