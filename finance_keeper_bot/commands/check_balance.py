from finance_keeper_bot.commands.bot_command import BotCommand
from finance_keeper_bot.logger import main_log as log
from finance_keeper_bot import command_router


@command_router.command('balance')
class CheckBalanceCommand(BotCommand):
    """
    Send user him current balance on account's
    """
    async def run(self, account=None, total=None):
        log.debug("send user balance")
        await self.telegram_api.bot_request('sendMessage', dict(chat_id=self.chat_id,
                                                          text='You balance on account : 100.5 rub.'))
