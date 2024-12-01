from telebot import TeleBot, types
import json
from os import path
import os

from .utils import (
    get_command_template,
    load_ai_models,
    get_chat_config,
    save_chat_config,
)
from .translator import Translator


class TranslateBot(TeleBot):
    def __init__(self, bot_token: str, translator: Translator):
        super().__init__(token=bot_token)

        self.translator = translator
        self.available_models = load_ai_models()
        self.translation_limit = os.getenv('TRANSLATION_LIMIT')
        if self.translation_limit:
            self.translation_limit = int(self.translation_limit)
            
        self.translation_limit_exclusions = {}
        exclusions = os.getenv('TRANSLATION_LIMIT_EXCLUSIONS', '')
        if exclusions:
            for exclusion in exclusions.replace(' ', '').split(','):
                if ':' in exclusion:
                    chat_id, limit = exclusion.split(':')
                    self.translation_limit_exclusions[chat_id] = int(limit)

        @self.message_handler(commands=["start"])
        def on_start(message):
            self.send_message(
                message.chat.id,
                get_command_template("help").format(bot_name=self.get_me().first_name),
                parse_mode="Markdown",
            )

        @self.message_handler(commands=["help"])
        def on_help(message):
            self.reply_to(
                message,
                get_command_template("help").format(bot_name=self.get_me().first_name),
                parse_mode="Markdown",
            )

        @self.message_handler(commands=["contact"])
        def on_contact(message):
            self.reply_to(
                message,
                get_command_template("contact").format(
                    bot_name=self.get_me().first_name
                ),
                parse_mode="Markdown",
            )

        @self.message_handler(commands=["t", "translate"])
        def on_translate(message):
            # Check translation limit first
            if not self._check_translation_limit(message.chat.id):
                self.reply_to(
                    message,
                    "*❌ Translation limit reached. `/contact` to request more credits.*",
                    parse_mode="Markdown"
                )
                return

            # Send initial "Processing translation..." message and store its message ID
            processing_msg = self.reply_to(
                message, "*Translating, please wait... ⏳*", parse_mode="Markdown"
            )
            processing_msg_id = processing_msg.message_id

            try:
                # Parse command
                try:
                    (
                        from_lang,
                        to_lang,
                        text,
                    ) = self._parse_command(message.text)
                except Exception:
                    raise Exception(
                        "Could not parse command - please check your syntax with /help and try again."
                    )

                # Call Translator
                data = self.translator.translate(
                    text,
                    from_lang,
                    to_lang,
                    get_chat_config(message.from_user.id)["model"],
                )

                # Update message based on translation success status if response from API is successful
                if data["success"]:
                    self._increment_translation_count(message.chat.id)
                    template = get_command_template("translate-success")
                    self.edit_message_text(
                        chat_id=message.chat.id,
                        message_id=processing_msg_id,
                        text=template.format(
                            from_lang=from_lang,
                            to_lang=to_lang,
                            translated_text=data["message"],
                        ),
                        parse_mode="Markdown",
                    )
                else:
                    raise Exception(data["message"])

            except Exception as err:
                self.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=processing_msg_id,
                    text=get_command_template("translate-failure").format(error=err),
                    parse_mode="Markdown",
                )

        @self.message_handler(commands=["s", "session"])
        def start_session(message):
            try:
                lang1, lang2 = self._parse_command(message.text)[
                    :2
                ]  # Parse only the first two
            except:
                self.reply_to(
                    message,
                    "*❌ Invalid command syntax.\n\nPlease use the following format:*\n`/session <language 1> - <language 2>`\n\n *Example:*\n`/session English - Spanish (Mexico City Dialect)`",
                    parse_mode="Markdown",
                )
                return

            try:
                self._set_active_session(message.chat.id, lang1, lang2)
                self.reply_to(
                    message,
                    get_command_template("session").format(lang1=lang1, lang2=lang2),
                    parse_mode="Markdown",
                )
            except Exception as err:
                self.reply_to(
                    message,
                    f"*❌ Could not start session - {err}*",
                    parse_mode="Markdown",
                )

        @self.message_handler(commands=["m", "models"])
        def on_models(message):
            try:
                # Get current user config
                chat_config = get_chat_config(message.chat.id)
                current_model = chat_config.get("model", "gpt-4o")

                # Create inline keyboard
                markup = types.InlineKeyboardMarkup(row_width=1)
                for model, details in self.available_models.items():
                    # Add a checkmark to the current model
                    button_text = f"{'✓ ' if model == current_model else ''}{model} - {details['description']}"
                    markup.add(
                        types.InlineKeyboardButton(
                            text=button_text, callback_data=f"select_model:{model}"
                        )
                    )

                self.reply_to(
                    message,
                    f"*Current model:* `{current_model}`\n\nSelect a model to switch:",
                    parse_mode="Markdown",
                    reply_markup=markup,
                )

            except Exception as err:
                self.reply_to(
                    message, f"*❌ Error:* `{str(err)}`", parse_mode="Markdown"
                )
                
        @self.message_handler(commands=["q", "quit"])
        def quit_session(message):
            active_session = self._get_active_session(message.chat.id)
            
            if active_session:
                lang1 = active_session['lang1']
                lang2 = active_session['lang2']
                
                self._clear_active_session(message.chat.id)
                self.reply_to(
                    message,
                    f"*🛑 Translation Session Ended for {lang1} and {lang2}.*",
                    parse_mode="Markdown"
                )
            else:
                self.reply_to(
                    message,
                    "*ℹ️ You don't have any active translation sessions.*",
                    parse_mode="Markdown"
                )

        @self.message_handler(
            content_types=[
                "text",
                "photo",
                "document",
                "audio",
                "video",
                "voice",
                "location",
                "contact",
                "sticker",
            ]
        )
        def generic_handler(message):
            chat_id = message.chat.id
            active_session = self._get_active_session(chat_id)
            
            if active_session:
                # Check translation limit first
                if not self._check_translation_limit(chat_id):
                    self.reply_to(
                        message,
                        "*❌ Translation limit reached. Contact administrator for more information.*",
                        parse_mode="Markdown"
                    )
                    return

                text = extract_text(message)
                if text:
                    lang1 = active_session['lang1']
                    lang2 = active_session['lang2']

                    # Send initial "Processing translation..." message and store its message ID
                    processing_msg = self.reply_to(
                        message,
                        "*Translating, please wait... ⏳*",
                        parse_mode="Markdown",
                    )
                    processing_msg_id = processing_msg.message_id

                    # Add a "Quit Session" button to the response
                    # markup = types.InlineKeyboardMarkup()
                    # markup.add(types.InlineKeyboardButton("Quit Session", callback_data="quit_session"))

                    try:
                        # Call Translator
                        data = self.translator.translate_session(
                            text,
                            language1=lang1,
                            language2=lang2,
                            model=get_chat_config(message.from_user.id)["model"],
                            started=True,
                        )

                        # Update message based on translation success status if response from API is successful
                        if data["success"]:
                            # template = get_command_template('translate-success')
                            text = f"`{data['message']}`"
                            self.edit_message_text(
                                chat_id=message.chat.id,
                                message_id=processing_msg_id,
                                text=text,
                                parse_mode="Markdown",
                            )  # , reply_markup=markup
                            self._increment_translation_count(chat_id)
                        else:
                            raise Exception(data["message"])
                    except Exception as err:
                        self.edit_message_text(
                            chat_id=message.chat.id,
                            message_id=processing_msg_id,
                            text=get_command_template("translate-failure").format(
                                error=err
                            ),
                            parse_mode="Markdown",
                        )  # reply_markup=markup
            # else:
            #     self.send_message(chat_id, "You're not in an active translation session. Please start a session first.")

        def extract_text(message):
            """Helper function to extract text based on message content type."""
            if message.content_type == "text":
                return message.text
            else:
                # Handler for document and media captions
                return message.caption

        @self.callback_query_handler(func=lambda call: call.data == "quit_session")
        def end_session(call):
            chat_id = call.message.chat.id
            active_session = self._get_active_session(chat_id)
            
            if active_session:
                lang1 = active_session['lang1']
                lang2 = active_session['lang2']

                # Remove the "Quit Session" button
                self.edit_message_reply_markup(
                    call.message.chat.id, call.message.message_id, reply_markup=None
                )

                # Append "Session Ended" to the existing message
                text = f"*🛑 Translation Session Ended for {lang1} and {lang2}.*"
                self.send_message(
                    chat_id=call.message.chat.id, text=text, parse_mode="Markdown"
                )

                self._clear_active_session(chat_id)
                self.answer_callback_query(call.id, "Session ended.")

        @self.callback_query_handler(
            func=lambda call: call.data.startswith("select_model:")
        )
        def on_model_selected(call):
            try:
                # Extract the selected model from callback data
                selected_model = call.data.split(":")[1]

                # Update user config
                chat_config = get_chat_config(call.message.chat.id)
                chat_config["model"] = selected_model
                save_chat_config(call.message.chat.id, chat_config)

                # Create updated keyboard
                markup = types.InlineKeyboardMarkup(row_width=1)
                for model, details in self.available_models.items():
                    button_text = f"{'✓ ' if model == selected_model else ''}{model} - {details['description']}"
                    markup.add(
                        types.InlineKeyboardButton(
                            text=button_text, callback_data=f"select_model:{model}"
                        )
                    )

                # Update the message with new keyboard
                self.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=f"*Current model:* `{selected_model}`\n\nSelect a model to switch:",
                    parse_mode="Markdown",
                    reply_markup=markup,
                )

                # Answer the callback query
                self.answer_callback_query(
                    call.id, text=f"✅ Switched to {selected_model}"
                )

            except Exception as err:
                self.answer_callback_query(
                    call.id, text=f"❌ Error: {str(err)}", show_alert=True
                )

    @staticmethod
    def _parse_command(text: str) -> list:
        """
        Parses the /t command message sent from the telegram user.

        Args:
            text (str): The message.text, expected in the format of /t from_lang - to_lang - text

        Returns:
            list: The parsed message in the order of [lang1, lang2, text]
        """
        # Initial split to separate the command from the rest of the text
        cmd, rest_of_text = text.split(" ", 1)

        # Split by the first and second occurrences of the "-" delimiter
        return [token.strip() for token in rest_of_text.split("-", 2)]

    @staticmethod
    def _get_active_session(chat_id: int) -> dict:
        """Helper method to get active session from chat config"""
        config = get_chat_config(chat_id)
        return config.get('active_session', None)

    @staticmethod
    def _set_active_session(chat_id: int, lang1: str, lang2: str):
        """Helper method to set active session in chat config"""
        config = get_chat_config(chat_id)
        config['active_session'] = {'lang1': lang1, 'lang2': lang2}
        save_chat_config(chat_id, config)

    @staticmethod
    def _clear_active_session(chat_id: int):
        """Helper method to clear active session from chat config"""
        config = get_chat_config(chat_id)
        if 'active_session' in config:
            del config['active_session']
            save_chat_config(chat_id, config)

    def _check_translation_limit(self, chat_id: int) -> bool:
        """
        Check if the chat has reached its translation limit
        Returns True if translation is allowed, False otherwise
        """
        if not self.translation_limit:
            return True
            
        config = get_chat_config(chat_id)
        translations_count = config.get('translations_count', 0)
        
        # Check if chat has custom limit
        chat_id_str = str(chat_id)
        if chat_id_str in self.translation_limit_exclusions:
            return translations_count < self.translation_limit_exclusions[chat_id_str]
            
        # Use default limit
        return translations_count < self.translation_limit

    def _increment_translation_count(self, chat_id: int):
        """Increment the translation count for a chat"""
        config = get_chat_config(chat_id)
        config['translations_count'] = config.get('translations_count', 0) + 1
        save_chat_config(chat_id, config)
