from dotenv import load_dotenv
import os
import google.generativeai as genai
import logging

from excptions import ScriptGeneratorException


class ScriptGenerator:

    _model = None
    _chat = None
    _LOGGER = None

    def __init__(self, LOGGER):
        try:
            self._LOGGER = LOGGER
            self._LOGGER.debug('Iniciando modelo GenAI')
            load_dotenv()
            genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
            self._model = genai.GenerativeModel('gemini-1.0-pro-latest')
            self._chat = self._model.start_chat(history=[])
            self._load_initial_prompt()
            self._LOGGER.debug('Modelo GenAI iniciado com sucesso')
        except Exception as e:
            raise ScriptGeneratorException(f'Erro ao iniciar o modelo: {e}')

    def generator(self, prompt):
        try:
            response = self._chat.send_message(prompt)
            return response.text
        except Exception as e:
            raise ScriptGeneratorException("Desculpe, não gerar roteiro sobre o assunto.")

    def _load_initial_prompt(self):
        try:
            file = open("./content/initial_prompt.txt", "r", encoding="utf8")
            self._chat.send_message(file.read())
        except Exception as e:
            raise ScriptGeneratorException(f'Erro ao carregar prompt inicial: {e}')



