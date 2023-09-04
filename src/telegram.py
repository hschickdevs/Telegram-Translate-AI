from telebot import TeleBot, types

from .utils import get_command_template
from .translator import Translator


class TranslateBot(TeleBot):
    def __init__(self, bot_token: str, translator: Translator):
        super().__init__(token=bot_token)

        self.translator = translator
        self.active_sessions = {}  # {user_id: {'from_lang': 'xx', 'to_lang': 'yy'}}

        @self.message_handler(commands=['start'])
        def on_start(message):
            self.send_message(message.chat.id, get_command_template('help').format(bot_name=self.get_me().first_name), parse_mode='Markdown')

        @self.message_handler(commands=['help'])
        def on_help(message):
            self.reply_to(message, get_command_template('help').format(bot_name=self.get_me().first_name), parse_mode='Markdown')

        @self.message_handler(commands=['t'])
        def on_translate(message):
            # Send initial "Processing translation..." message and store its message ID
            processing_msg = self.reply_to(message, "*Translating, please wait... ⏳*", parse_mode='Markdown')
            processing_msg_id = processing_msg.message_id
            
            try:
                # Parse command 
                try:
                    from_lang, to_lang, text, = self._parse_command(message.text)
                except Exception:
                    raise Exception("Could not parse command - please check your syntax with /help and try again.")
                
                # Call Translator
                data = self.translator.translate(text, from_lang, to_lang)

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
                    raise Exception(data['message'])
                                
            except Exception as err:    
                self.edit_message_text(chat_id=message.chat.id,
                                        message_id=processing_msg_id,
                                        text=get_command_template('translate-failure').format(error=err),
                                        parse_mode='Markdown')
                            
        @self.message_handler(commands=['session'])
        def start_session(message):
            try:
                from_lang, to_lang = self._parse_command(message.text)[:2]  # Parse only the first two
            except:
                self.reply_to(message, "*❌ Invalid command syntax - Please use /session <source lang> - <target lang>*", parse_mode='Markdown')
                return
            
            try:
                self.active_sessions[message.from_user.id] = {'from_lang': from_lang, 'to_lang': to_lang}
                # markup = types.InlineKeyboardMarkup()
                # markup.add(types.InlineKeyboardButton("Quit Session", callback_data="quit_session"))
                self.reply_to(message, 
                              get_command_template('session').format(from_lang=from_lang, to_lang=to_lang), 
                              parse_mode='Markdown')  # , reply_markup=markup
            except Exception:
                self.reply_to(message, "*❌ Could not start session - please check your syntax and try again*", parse_mode='Markdown')

        @self.message_handler(func=lambda message: True)  # This should be your last handler
        def generic_handler(message):
            # Generic handler to check and handle active sessions
            user_id = message.from_user.id
            if user_id in self.active_sessions:
                from_lang = self.active_sessions[user_id]['from_lang']
                to_lang = self.active_sessions[user_id]['to_lang']
                text = message.text
                
                # Send initial "Processing translation..." message and store its message ID
                processing_msg = self.reply_to(message, "*Translating, please wait... ⏳*", parse_mode='Markdown')
                processing_msg_id = processing_msg.message_id

                # Add a "Quit Session" button to the response
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("Quit Session", callback_data="quit_session"))
                
                try:
                    # Call Translator
                    data = self.translator.translate(text, from_lang, to_lang)

                    # Update message based on translation success status if response from API is successful
                    if data['success']:
                        template = get_command_template('translate-success')
                        self.edit_message_text(chat_id=message.chat.id,
                                            message_id=processing_msg_id,
                                            text=template.format(from_lang=from_lang,
                                                                    to_lang=to_lang,
                                                                    translated_text=data['message']),
                                            parse_mode='Markdown', reply_markup=markup)
                    else:
                        raise Exception(data['message'])                            
                except Exception as err:    
                    self.edit_message_text(chat_id=message.chat.id,
                                            message_id=processing_msg_id,
                                            text=get_command_template('translate-failure').format(error=err),
                                            parse_mode='Markdown', reply_markup=markup)

        @self.callback_query_handler(func=lambda call: call.data == 'quit_session')
        def end_session(call):
            user_id = call.from_user.id
            if user_id in self.active_sessions:
                from_lang = self.active_sessions[user_id]['from_lang']
                to_lang = self.active_sessions[user_id]['to_lang']
                
                # Remove the "Quit Session" button
                self.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
                
                # Append "Session Ended" to the existing message and remove the "Quit Session" button
                text = f"*🛑 {from_lang} to {to_lang} Translation Session Ended.*"
                self.send_message(chat_id=call.message.chat.id,
                                    text=text,
                                    parse_mode='Markdown')
                
                del self.active_sessions[user_id]
                self.answer_callback_query(call.id, "Session ended.")

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