from .telegram import TranslateBot
from .translator import Translator
from .utils import handle_env

from os import getenv

if __name__ == "__main__":
    handle_env()

    bot = TranslateBot(getenv("BOT_TOKEN"), Translator("OPENAI_TOKEN"))
    bot.polling()
    # TODO: Implement error handling
