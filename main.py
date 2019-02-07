import urllib3
import os

from bmstu_schedule_bot import logger, BOT

if __name__ == '__main__':
    try:
        logger.log('Bot is starting up')
        BOT.polling(none_stop=True, timeout=30)
    except urllib3.exceptions.ReadTimeoutError as e:
        logger.log(e)
    except Exception as e:
        logger.log(e)
    finally:
        logger.log('Bot is shutting down')
