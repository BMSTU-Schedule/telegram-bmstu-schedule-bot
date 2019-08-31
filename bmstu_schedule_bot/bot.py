import telebot


import handlers


class Bot:
    def __init__(self, config):
        self.config = config
    

    def _init_handlers(self):
        handlers.register_handlers(self.bot, self.config)


    def _init_custom_handlers(self):
        handlers.register_custom_handlers(self.bot, self.config)


    def init(self):
        self.bot = telebot.TeleBot(self.config['ACCESS_TOKEN'])
        self._init_handlers()
        self._init_custom_handlers()


    def run(self):
        self.bot.polling(none_stop=True, timeout=30)
