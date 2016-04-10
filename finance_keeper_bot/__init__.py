import asyncio
import json

from finance_keeper_bot.telegram_api import TelegramApi
from finance_keeper_bot.logger import main_log as log


class FinanceKeeperBot:
    def __init__(self):
        self.listen_updates = True
        self.loop = asyncio.get_event_loop()
        self.telegram_api = TelegramApi(loop=self.loop)
        self.last_update_id = None

    def run(self):
        try:
            self.loop.run_until_complete(self.updates_loop())
        except KeyboardInterrupt:
            self.listen_updates = False
            log.info("Shutdown...")

    async def updates_loop(self):
        while self.listen_updates:
            await self.get_updates()

    async def get_updates(self):
        params = dict(timeout=5)
        if self.last_update_id is not None:
            params['offset'] = self.last_update_id + 1
        response, status_code = await self.telegram_api.bot_request('getUpdates', params=params)
        if not response['ok']:
            log.error('error read updates from telegram.')
            print(response)
            return

        update_items = response['result']
        for item in update_items:
            await self.processes_update_item(item=item)

    async def processes_update_item(self, item):
        self.last_update_id = item['update_id']
        message_chat = item['message']['chat']
        if message_chat['type'] != 'private':
            log.error('chat %s is not private, chat type: %s' % (message_chat['id'], message_chat['type'] ))
            return

        reply_markup = dict(keyboard=[['add debit operation', 'add credit operation'], ['check balance', 'send report to email']])
        await self.telegram_api.bot_request('sendMessage',
                                        params=dict(
                                            chat_id=message_chat['id'],
                                            text='Please, select command',
                                            reply_to_message_id=item['message']['message_id'],
                                            reply_markup=json.dumps(reply_markup)),
                                      )
