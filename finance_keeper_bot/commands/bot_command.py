import json

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

    async def run(self):
        """
        Command call. Must be redefined in child.
        """
        raise NotImplementedError

    async def set_state(self, stage, args_list=None):
        if args_list is None:
            args_list = list()

        state_dict = dict(
            command=self._command_name,
            stage=stage,
            args_list=args_list
        )
        await self.redis_client.set(str(self.chat_id), json.dumps(state_dict))

    async def end_command(self):
        await self.redis_client.delete([str(self.chat_id), ])