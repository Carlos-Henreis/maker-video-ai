from maker.script_generator import ScriptGenerator
import  json
from logging_config import LoggingConfig
from maker.video import Video
from maker.audio import Audio

if __name__ == '__main__':
    try:
        LOGGER = LoggingConfig().get_logger()
        LOGGER.debug("Iniciando script")
        voice_id = Audio(LOGGER).get_voice_id()
        assunto = input('Qual tema do quiz de hoje? ')
        roteiro = ScriptGenerator(LOGGER).generator(f'Roteiro sobre {assunto}')

        json_roteiro = json.loads(roteiro)

        print(json_roteiro['titulo'])
        maker = Video(json_roteiro, voice_id, LOGGER)
        maker.file()
    except Exception as e:
        print('Erro ao gerar video: ', e)