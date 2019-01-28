import urllib3

import handlers
from bot import BOT

if __name__ == '__main__':
    try:
        BOT.polling(none_stop=True, timeout=30)
    except urllib3.exceptions.ReadTimeoutError:
        pass
