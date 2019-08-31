import logging
import os


from bot import Bot


logging.basicConfig(
    format='%(asctime)s %(name)-5s %(levelname)-8s %(message)s', 
    level = logging.INFO
)

log = logging.getLogger("tgbot")


def get_config():
    cfg = {
        'ACCESS_TOKEN': os.environ.get('ACCESS_TOKEN'),
        'VAULT_PATH': os.environ.get('VAULT_PATH'),
        'DIALOGUE_CFG_PATH': os.environ.get('DIALOGUE_CFG_PATH'),
        'BMSTU_SCHEDULE_API': os.environ.get('BMSTU_SCHEDULE_API'),
    }

    return cfg


def create_app():
    config = get_config()

    bot = Bot(config)
    bot.init()

    return bot
