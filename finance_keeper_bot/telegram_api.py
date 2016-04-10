import aiohttp
from finance_keeper_bot import config


class TelegramApi:
    API_BASE_URL = 'https://api.telegram.org'

    def __init__(self, loop):
        self.session = aiohttp.ClientSession(loop=loop)

    def __del__(self):
        self.session.close()

    def make_bot_url(self, method):
        return '%s/bot%s/%s' % (self.API_BASE_URL, config.TELEGRAM_API_KEY, method)

    async def bot_request(self, method, params):
        async with self.session.get(self.make_bot_url(method), params=params) as response:
            return await response.json(), response.status