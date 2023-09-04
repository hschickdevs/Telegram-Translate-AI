from os.path import join, dirname, isdir
from os import getenv, getcwd, mkdir
from dotenv import load_dotenv, find_dotenv


def get_prompt(text: str, from_lang: str, to_lang: str) -> str:
    """
    TODO: SHOULD FORMAT THE PROMPT WITH THE USER'S INPUT
    """
    with open(join(dirname(__file__), 'resources', 'prompt.txt'), 'r') as f:
        return f.read().format(from_lang=from_lang, to_lang=to_lang, text=text)


def get_command_template(context: str) -> str:
    """
    Open the /resources directory relative to __file__ and read the help.txt file.

    Args:
        context (str): The template's filename without the extension

    Returns:
        str: The corresponding prompt template in Markdown to be formatted by the Telegram bot
    """
    with open(join(dirname(__file__), 'resources', 'templates', f'{context}.md'), 'r', encoding='utf8') as f:
        return f.read()


def handle_env():
    """Checks if the .env file exists in the current working dir, and imports the variables if so"""
    try:
        envpath = find_dotenv(raise_error_if_not_found=True, usecwd=True)
        load_dotenv(dotenv_path=envpath)
    except:
        pass
    finally:
        mandatory_vars = ['BOT_TOKEN', 'OPENAI_TOKEN']
        for var in mandatory_vars:
            val = getenv(var)
            if val is None:
                raise ValueError(f"Missing environment variable: {var}")
            
def get_logfile() -> str:
    log_dir = join(getcwd(), 'logs')
    if not isdir(log_dir):
        mkdir(log_dir)
    return join(log_dir, 'log.txt')