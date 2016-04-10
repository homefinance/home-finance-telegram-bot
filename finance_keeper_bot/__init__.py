import asyncio

from finance_keeper_bot.commands import CommandRouter

event_loop = asyncio.get_event_loop()
command_router = CommandRouter()

from finance_keeper_bot.commands.check_balance import CheckBalanceCommand


