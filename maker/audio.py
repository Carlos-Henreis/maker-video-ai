import pyttsx3
import os
from pydub import AudioSegment
from pymenu import select_menu

class Audio:

    def __init__(self, LOGGER):
        self._LOGGER = LOGGER
        self._motor = self._set_motor()

    def save_audio(self, text, file_name):

        if not os.path.exists('./content/audios'):
            os.makedirs('./content/audios')
        output_file = f'./content/audios/{file_name}.mp3'

        self._motor.save_to_file(text, output_file)
        self._motor.runAndWait()

        self._LOGGER.debug(f'> [audio] audio created: {output_file}')

    def get_audio_duration(self, file_path):
        audio = AudioSegment.from_file(file_path)
        duration = audio.duration_seconds
        return duration

    def _set_motor(self):
        motor = pyttsx3.init()

        voices = motor.getProperty('voices')
        # tenta alterar voice para Daniel
        for voice in voices:
            if 'Daniel' in voice.id:
                motor.setProperty('voice', voice.id)
                break
        motor.setProperty('rate', 250)
        return motor

    def get_voice_id(self):
        motor = pyttsx3.init()
        voices: object = motor.getProperty('voices')

        voices_name = [voice.name for voice in voices]

        selected_option = select_menu.create_select_menu(voices_name, 'Selecione uma voz')

        #get_voice retorna id da voz selecionada
        for voice in voices:
            if selected_option == voice.name:
                return voice.id

        return voices[0].id

    def setProperty(self, property, value):
        self._motor.setProperty(property, value)