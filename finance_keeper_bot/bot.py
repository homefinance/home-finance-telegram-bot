import json

from finance_keeper_bot.commands import InvalidCommandArgumentsException, InvalidCommandException
from finance_keeper_bot.logger import main_log as log
from finance_keeper_bot import event_loop
from finance_keeper_bot.redis import get_redis_client
from finance_keeper_bot.telegram_api import TelegramApi
from finance_keeper_bot import config
from finance_keeper_bot import command_router


class FinanceKeeperBot:
    def __init__(self):
        self.telegram_api = TelegramApi()
        self.listen_updates = True
        self.last_update_id = None

    async def a_init(self):
        self.redis_client = await get_redis_client()

    def run(self):
        try:
            event_loop.run_until_complete(self.async_start())
        except KeyboardInterrupt:
            self.listen_updates = False
            log.info("Shutdown...")
            event_loop.close()

    async def async_start(self):
        await self.a_init()
        await self.updates_loop()

    async def updates_loop(self):
        while self.listen_updates:
            await self.get_updates()

    async def get_updates(self):
        params = dict(timeout=config.TELEGRAM_LONG_POOLING_TIMEOUT)
        if self.last_update_id is not None:
            params['offset'] = self.last_update_id + 1
        response, status_code = await self.telegram_api.bot_request('getUpdates', params=params)
        if not response['ok']:
            log.error('error read updates from telegram(code %s), reason: %s' % (
                response['error_code'],
                response['description']
                )
            )
            return

        update_items = response['result']
        for item in update_items:
            await self.processes_update_item(item=item)

    async def processes_update_item(self, item):
        self.last_update_id = item['update_id']
        message_chat = item['message']['chat']
        log.info("incoming message, from chat %s, text: %s" % (message_chat['id'],  item['message']['text']))
        if message_chat['type'] != 'private':
            log.error('chat %s is not private, chat type: %s' % (message_chat['id'], message_chat['type'] ))
            return

        await self.route_command(item['message'])

    async def route_command(self, msg):
        command = self.extract_command(msg['text'])
        if command is None:
            command = await self.get_chat_state(msg['chat'])

        if command is None:
            command = 'menu'
        try:
            await command_router.resolve(command, msg['chat']['id'])
        except InvalidCommandException as e:
            await self.telegram_api.bot_request('sendMessage', dict(chat_id=msg['chat']['id'],
                                                                    text='invalid command : %s.' % (e,)))
        except InvalidCommandArgumentsException as e:
            await self.telegram_api.bot_request('sendMessage', dict(chat_id=msg['chat']['id'],
                                                              text='invalid command parameters: %s.' % (e, )))

    def extract_command(self, inp):
        if inp[0] != '/':
            return None

        command_inp = inp[1:].split()

        if len(command_inp) < 1:
            return None

        command_name = command_inp[0]
        command_args = command_inp[1:]
        log.debug("command income: %s, args: %s" % (command_name, command_args))
        return command_name, command_args

    async def get_chat_state(self, chat):
        current_state = await self.redis_client.get(str(chat['id']))
        if current_state is None:
            log.info("no state presented for chat %s" % (chat['id'], ))
            await self.redis_client.set(str(chat['id']), 'yep')
        else:
            log.info("state presented for chat %s : %s" % (chat['id'], current_state))
