from finance_keeper_bot.telegram_api import TelegramApi


class BotCommand:
    """
    Base class for all bot's commands.
    Command is a logic for response to certain user message.
    """
    def __init__(self, chat_id):
        self.telegram_api = TelegramApi()
        self.chat_id = chat_id

    async def run(self):
        """
        Command call. Must be redefined in child.
        """
        raise NotImplementedError
