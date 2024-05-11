from enum import Enum

class SceneType(Enum):
    INTRO = 1
    PERGUNTA = 2
    RESPOSTA = 3
    ENCERRAMENTO = 4

class Scene:
    def __init__(self, text, audio_path, total_time, scene_type: SceneType):
        self._text = text
        self._scene_type = scene_type
        self._audio_path = audio_path
        self._total_time = total_time