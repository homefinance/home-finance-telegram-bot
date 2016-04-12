import json

from finance_keeper_bot.commands.bot_command import BotCommand
from finance_keeper_bot.logger import main_log as log
from finance_keeper_bot import command_router


@command_router.command('balance')
class CheckBalanceCommand(BotCommand):
    """
    Command send user him current balance on account's
    """

    async def run(self, account=None):
        self.account = account

        log.debug("send user balance")
        if self.account is None:
            await self.send_request_account()
            return

        await self.send_balance()
        await self.end_command()

    async def send_request_account(self):
        test_accounts_list = (('cache', 'salary_card'),)

        await self.telegram_api.bot_request('sendMessage', dict(
            chat_id=self.chat_id,
            text='Select account',
            reply_markup=json.dumps(dict(
                keyboard=test_accounts_list,
                one_time_keyboard=True
            ))
        ))
        await self.set_state('provide_account')

    async def send_balance(self):
        await self.telegram_api.bot_request('sendMessage', dict(chat_id=self.chat_id,
                                                          text='You balance on account : 100.5 rub.'))
