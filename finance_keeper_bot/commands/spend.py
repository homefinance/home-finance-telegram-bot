from finance_keeper_bot.commands.bot_command import BotCommand
from finance_keeper_bot import command_router


@command_router.command('spend')
class SpendCommand(BotCommand):
    """
    Command add credit operation
    """
    async def run(self):
        pass