import json

from finance_keeper_bot.commands.bot_command import BotCommand
from finance_keeper_bot import command_router
from finance_keeper_bot.logger import main_log as log


@command_router.command('spend')
class SpendCommand(BotCommand):
    """
    Command add credit operation
    """
    async def run(self, sum=None, account=None, category=None):
        self.sum = sum
        self.account = account
        self.category = category
        self.args_list = list()

        log.debug("spend command, chat : %s" % (self.chat_id, ))

        if self.sum is None:
            return await self.send_request_sum()

        if self.account is None:
            return await self.send_request_account()

        if self.category is None:
            return await self.send_request_category()

        await self.end_command()

    async def send_request_sum(self):
        await self.telegram_api.bot_request('sendMessage', dict(
            chat_id=self.chat_id,
            text='Please enter sum: ',
        ))
        await self.set_state('provide_sum')

    async def send_request_account(self):
        test_accounts_list = (('cache', 'salary_card'),)

        await self.telegram_api.bot_request('sendMessage', dict(
            chat_id=self.chat_id,
            text='Please select account: ',
            reply_markup=json.dumps(dict(
                keyboard=test_accounts_list,
                one_time_keyboard=True
            ))
        ))
        await self.set_state('provide_account')

    async def send_request_category(self):
        test_category_list = (('food', 'clothes', 'car', 'alcohol', 'household'),)
        await self.telegram_api.bot_request('sendMessage', dict(
            chat_id=self.chat_id,
            text='Please select category of spend: ',
            reply_markup=json.dumps(dict(
                keyboard=test_category_list,
                one_time_keyboard=True
            ))
        ))
        await self.set_state('provide_category')