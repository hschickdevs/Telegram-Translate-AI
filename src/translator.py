from json import loads
import openai
from os.path import join, dirname, isdir
from os import getenv, getcwd, mkdir
from dotenv import load_dotenv, find_dotenv

from .logger import logger


class Translator:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Initializes the translator object.
        
        Args:
            api_key (str): Your OpenAI API key
            model (str, optional): The OpenAI model to use. Defaults to "gpt-3.5-turbo".
        """
        self.model = model
        openai.api_key = api_key
    
    def _call_api(self, prompt: str) -> dict:
        """
        Handles the call to the OpenAI API ChatCompletions endpoint, and the parsing of the response.
        
        Args:
            prompt (str): The formatted prompt string

        Returns:
            dict: The parsed response in the format of: {"success": bool, "message": str}
        """
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # TODO: Handle 502 errors
        print("Response:", response)
        print("Response Content:", response["choices"][0]["message"]["content"])
        
        try:
            return loads(response["choices"][0]["message"]["content"])
        except Exception as err:
            logger.error(f"Received an error while parsing the response from the API: {str(err)}\nWith response: {response}\nFor prompt: {prompt}")
            return {"success": False, "message": f"API response could not be loaded (see logs): {str(err)}"}

    def translate(self, text: str, source_lang: str, target_lang: str) -> dict:
        """
        Translate the text from source language to target language.

        Args:
            text (str): Text to be translated.
            source_lang (str): Source language.
            target_lang (str): Target language.

        Returns:
            dict: Returns the dict object from the self._call_api return
        """
        # Format the translate.txt prompt file to construct the detailed prompt for the translation task
        with open(join(dirname(__file__), 'resources', 'prompts', 'translate.txt'), 'r') as f:
            prompt = f.read().format(from_lang=source_lang, to_lang=target_lang, text=text)

        return self._call_api(prompt)
    
    def translate_session(self, text: str, language1: str, language2: str, started: bool = True) -> dict:
        """
        Translate the text from source language to target language using the session prompt

        Args:
            text (str): Text to be language autodetected and translated.
            language1 (str): First language of the session pair.
            language2 (str): Second language of the session pair.
        """
        # Format the session.txt prompt file to construct the detailed prompt for the session task
        with open(join(dirname(__file__), 'resources', 'prompts', 'session.txt'), 'r') as f:
            prompt = f.read().format(lang1=language1, lang2=language2, text=text, started=started)
        
        return self._call_api(prompt)