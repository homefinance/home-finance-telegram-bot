import aiohttp
from finance_keeper_bot import config
from finance_keeper_bot.singleton import Singleton
from finance_keeper_bot import event_loop


class TelegramApi:
    """
    Class provide async call's to telegram api methods.
    """
    __metaclass__ = Singleton

    API_BASE_URL = 'https://api.telegram.org'

    def __init__(self):
        self.session = aiohttp.ClientSession(loop=event_loop)

    def __del__(self):
        self.session.close()

    def make_bot_url(self, method):
        """
        Create full bot api url, by provided method name (ex. getUpdates or sendMessage)

        :param method: One of methods Telegram bot API (https://core.telegram.org/bots/api)
        :return finally URL
        """
        return '%s/bot%s/%s' % (self.API_BASE_URL, config.TELEGRAM_API_KEY, method)

    async def bot_request(self, method, params):
        """
        Send request to method of telegram bot API.

        :param method: One of methods Telegram bot API (https://core.telegram.org/bots/api)
        :param params: Dictionary of request parameters.

        :return (dict, int) - JSON response and HTTP status code
        """
        async with self.session.get(self.make_bot_url(method), params=params) as response:
            return await response.json(), response.status
