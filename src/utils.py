from os.path import join, dirname, isdir, abspath
from os import getenv, getcwd, mkdir
from dotenv import load_dotenv, find_dotenv
import yaml
import yaml.loader
import json
from os import path, makedirs


def get_command_template(context: str) -> str:
    """
    Open the /resources directory relative to __file__ and read the help.txt file.

    Args:
        context (str): The template's filename without the extension

    Returns:
        str: The corresponding prompt template in Markdown to be formatted by the Telegram bot
    """
    with open(
        join(dirname(__file__), "resources", "templates", f"{context}.md"),
        "r",
        encoding="utf8",
    ) as f:
        return f.read()


def handle_env():
    """Checks if the .env file exists in the current working dir, and imports the variables if so"""
    try:
        envpath = find_dotenv(raise_error_if_not_found=True, usecwd=True)
        load_dotenv(dotenv_path=envpath)
    except:
        pass
    finally:
        mandatory_vars = ["BOT_TOKEN", "OPENAI_TOKEN"]
        for var in mandatory_vars:
            val = getenv(var)
            if val is None:
                raise ValueError(f"Missing environment variable: {var}")


def get_logfile() -> str:
    log_dir = join(getcwd(), "logs")
    if not isdir(log_dir):
        mkdir(log_dir)
    return join(log_dir, "log.txt")


def get_commands() -> dict:
    """Fetches the commands from the templates for the help command"""
    commands = {}

    # Define the path to the commands.txt file
    file_path = join(dirname(abspath(__file__)), "..", "commands.txt")

    with open(file_path, "r") as f:
        for line in f.readlines():
            # Splitting at the first '-' to separate command and description
            command, description = line.strip().split(" - ", 1)
            commands[command.strip()] = description.strip()

    return commands


def load_ai_models() -> dict:
    """Loads the models from the models.yml file"""
    with open(join(dirname(abspath(__file__)), "resources", "models.yml"), "r") as f:
        return yaml.load(f, Loader=yaml.loader.FullLoader)["models"]


def get_chat_config_path(chat_id: int) -> str:
    """Returns the path to the chat's config file"""
    config_dir = path.join(getcwd(), "chat_configs")
    if not path.isdir(config_dir):
        makedirs(config_dir)
    return path.join(config_dir, f"{chat_id}.json")


def get_chat_config(chat_id: int) -> dict:
    """Gets the chat's config, creates default if doesn't exist"""
    config_path = get_chat_config_path(chat_id)

    if path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)

    # Default config
    default_config = {"model": getenv("DEFAULT_MODEL", "gpt-4o-mini")}

    save_chat_config(chat_id, default_config)
    return default_config


def save_chat_config(chat_id: int, config: dict):
    """Saves the chat's config to disk"""
    config_path = get_chat_config_path(chat_id)
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
