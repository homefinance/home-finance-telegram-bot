import json
from inspect import getfullargspec

from finance_keeper_bot.redis import get_redis_client
from finance_keeper_bot.telegram_api import TelegramApi


class BotCommand:
    """
    Base class for all bot's commands.
    Command is a logic for response to certain user message.
    """

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.telegram_api = TelegramApi()

    async def a_init(self):
        """
        Async init. Income command arguments.
        Must be redefined in child.
        """
        self.redis_client = await get_redis_client()

    async def save_args_to_list(self):
        self.args_list = list()
        args_list_inspect = getfullargspec(self.run)

        for arg in args_list_inspect[0][1:]:
            if not hasattr(self, arg) or getattr(self, arg) is None:
                return
            self.args_list.append(getattr(self, arg))

        print(self.args_list)


    async def run(self):
        """
        Command call.
        """
        raise NotImplementedError

    async def set_state(self, stage):
        await self.save_args_to_list()

        state_dict = dict(
            command=self._command_name,
            stage=stage,
            args_list=self.args_list
        )
        await self.redis_client.set(str(self.chat_id), json.dumps(state_dict))

    async def end_command(self):
        await self.redis_client.delete([str(self.chat_id), ])