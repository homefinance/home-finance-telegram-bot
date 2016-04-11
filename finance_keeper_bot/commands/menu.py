from finance_keeper_bot.commands.bot_command import BotCommand
from finance_keeper_bot import command_router
import json


@command_router.command('menu')
class MenuCommand(BotCommand):
    MENU_LIST = [
        ['/credit', '/debit'],
        ['/balance', '/report']
    ]

    async def run(self):
        markup = dict(
            one_time_keyboard=True,
            keyboard=self.MENU_LIST
        )
        await self.telegram_api.bot_request('sendMessage', dict(text='please, select one of the commands',
                                                                           reply_markup=json.dumps(markup),
                                                                           chat_id=self.chat_id))
