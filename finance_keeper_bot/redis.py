import asyncio_redis
from finance_keeper_bot.logger import main_log as log
from finance_keeper_bot import config
from finance_keeper_bot import event_loop

redis_client = None

async def get_redis_client():
    global redis_client
    if redis_client is not None:
        log.debug("use existing redis client")
        return redis_client

    log.debug("Start connect to redis : %s:%s" % (config.REDIS['host'], config.REDIS['port']))
    redis_client = await asyncio_redis.Connection.create(
        host=config.REDIS['host'],
        port=config.REDIS['port']
    )
    log.debug("connection to redis ready.")
    return redis_client