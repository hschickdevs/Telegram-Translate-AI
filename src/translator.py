from .utils import get_prompt

from json import loads
import openai


class Translator:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
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

        return loads(response["choices"][0]["message"]["content"])

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
        # Construct the detailed prompt for the translation task
        prompt = get_prompt(text, source_lang, target_lang)

        return self._call_api(prompt)