import telebot


import handlers


class Bot:
    def __init__(self, config):
        self.config = config
    

    def _init_handlers(self):
        handlers.register_handlers(self.bot, self.config)
        handlers.register_custom_handlers(self.bot, self.config)
        handlers.register_group_parser_handler(self.bot, self.config)


    def init(self):
        self.bot = telebot.TeleBot(self.config['ACCESS_TOKEN'])
        self._init_handlers()


    def run(self):
        self.bot.polling(none_stop=True, timeout=30)
