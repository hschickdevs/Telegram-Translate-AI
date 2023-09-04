from .telegram import TranslateBot
from .translator import Translator
from .utils import handle_env
from .logger import logger

import threading
from os import getenv
from time import sleep

RESTART_DELAY = 5  # The number of seconds to wait before restarting the bot after an error is thrown

def start_bot(bot_instance: TranslateBot):
    try:
        bot_instance.polling()
    except Exception as err:
        logger.error(f"An error occurred while polling: {err}", exc_info=err)

if __name__ == "__main__":
    handle_env()
    
    bot = TranslateBot(getenv("BOT_TOKEN"), Translator(getenv("OPENAI_TOKEN")))

    while True:
        logger.info(f"Bot started with token {getenv('BOT_TOKEN')} ...")

        # Start bot polling as a daemon thread (so that it can be stopped by KeyboardInterrupt in the main thread)
        polling_thread = threading.Thread(target=start_bot, args=(bot,), daemon=True)
        polling_thread.start()

        try:
            # Keep the main thread running to allow daemon threads to run
            while polling_thread.is_alive():
                sleep(1)
        except KeyboardInterrupt:
            logger.info("Bot stopped by the console.")
            break
        except Exception as err:
            logger.error(f"An unexpected error occurred: {err}")

        logger.info(f"Restarting bot in {RESTART_DELAY} seconds...")
        sleep(RESTART_DELAY)
