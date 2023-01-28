import openai
from config import openai_token
from googletrans import Translator


class OpenAI:
    def __init__(self):
        # session token
        openai.api_key = openai_token
        # chat 3 engine (max)
        self.model_engine = "text-davinci-003"
        # translate
        self.translator = Translator()

    def chatgpt(self, text, temperature):
        # request on ChatGPT
        completion = openai.Completion.create(
            engine=self.model_engine,
            prompt=text,
            max_tokens=3900 - len(text),
            temperature=temperature,
            frequency_penalty=0,
            presence_penalty=0
        )
        return completion.choices[0].text

    def translate_chatgpt(self, text, temperature):
        # request on ChatGPT with translation
        text = self.translator.translate(text, dest='en').text
        completion = openai.Completion.create(
            engine=self.model_engine,
            prompt=text,
            max_tokens=3900 - len(text),
            temperature=temperature,
            frequency_penalty=0,
            presence_penalty=0
        )
        completion_text = self.translator.translate(completion.choices[0].text, dest='ru').text
        return completion_text