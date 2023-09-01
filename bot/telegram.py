from telebot import TeleBot

from .utils import get_command_template
from .translator import Translator


class TranslateBot(TeleBot):
    def __init__(self, bot_token: str, translator: Translator):
        super().__init__(token=bot_token)

        self.translator = translator

        @self.message_handler(commands=['start'])
        def on_start(message):
            self.reply_to(message, get_command_template('start'), parse_mode='MarkdownV2')

        @self.message_handler(commands=['help'])
        def on_help(message):
            self.reply_to(message, get_command_template('help'), parse_mode='Markdown')

        @self.message_handler(commands=['t'])
        def on_translate(message):
            # Send initial "Processing translation..." message and store its message ID
            processing_msg = self.reply_to(message, "*Translating, please wait... ⏳*", parse_mode='Markdown')
            processing_msg_id = processing_msg.message_id

            # Parse Message
            from_lang, to_lang, text, = self._parse_command(message.text)

            # Call Translator
            try:
                data = self.translator.translate(text, from_lang, to_lang)
            except Exception as err:
                # If translation fails without a response, send the error.
                self.edit_message_text(chat_id=message.chat.id,
                                       message_id=processing_msg_id,
                                       text=get_command_template('translation-failure').format(error=err),
                                       parse_mode='Markdown')
                return

            # Update message based on translation success status if response from API is successful
            if data['success']:
                template = get_command_template('translate-success')
                self.edit_message_text(chat_id=message.chat.id,
                                       message_id=processing_msg_id,
                                       text=template.format(from_lang=from_lang,
                                                            to_lang=to_lang,
                                                            translated_text=data['message']),
                                       parse_mode='Markdown')
            else:
                self.edit_message_text(chat_id=message.chat.id,
                                       message_id=processing_msg_id,
                                       text=get_command_template('translate-failure').format(error=data['message']),
                                       parse_mode='Markdown')

    @staticmethod
    def _parse_command(text: str) -> list:
        """
        Parses the /t command message sent from the telegram user.

        Args:
            text (str): The message.text, expected in the format of /t from_lang - to_lang - text

        Returns:
            list: The parsed message in the order of [from_lang, to_lang, text]
        """
        # Initial split to separate the command from the rest of the text
        cmd, rest_of_text = text.split(' ', 1)

        # Split by the first and second occurrences of the "-" delimiter
        return [token.strip() for token in rest_of_text.split('-', 2)]
