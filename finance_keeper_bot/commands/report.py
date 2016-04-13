from finance_keeper_bot import command_router
from finance_keeper_bot.commands.bot_command import BotCommand


@command_router.command('report')
class ReportCommand(BotCommand):
    async def run(self):
        report = """ You current spends, for current month (01.04.2016 - 13.04.2016 :

            car - 4 000 rub.
            food - 6 000 rub
            household - 2 000 rub

            You money supply:

            savings account - 350 000 rub
            cache - 10 000 rub
            """
        await self.telegram_api.bot_request('sendMessage', dict(
            text=report,
            chat_id = self.chat_id
        ))