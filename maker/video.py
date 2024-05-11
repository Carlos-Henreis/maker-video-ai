from moviepy.editor import (
    ImageClip,
    CompositeVideoClip,
    CompositeAudioClip,
    AudioFileClip,
    concatenate_videoclips,
    TextClip,
    concatenate_audioclips,
)

import random
from concurrent.futures import ThreadPoolExecutor
from .audio import Audio
from model.scene import Scene, SceneType

class Video:
    _list_scene = []
    _video_clips = []
    _final_clip = None

    def __init__(self, roteiro, voice_id, LOGGER):
        self._LOGGER = LOGGER
        self._roteiro = roteiro
        self._audio_client = Audio(LOGGER)
        self._audio_client.setProperty('voice', voice_id)


    def _create_all_audio(self):

        #intros
        for index, intro in enumerate(self._roteiro["intro"]):
            self._audio_client.save_audio(intro, f'intro-{index}')
            intro = self._format_text(intro)
            scene = Scene(intro, f'./content/audios/intro-{index}.mp3', 0, SceneType.INTRO)
            self._list_scene.append(scene)
        #perguntas
        for index, p in enumerate(self._roteiro["perguntas"]):
            pergunta_audio = f'{p["pergunta"]}\n'

            p["pergunta"] = self._format_text(p["pergunta"])
            pergunta = f'{p["pergunta"]}\n'

            for i, q in enumerate(p["alternativas"]):
                pergunta += f'{q}.\n'
                pergunta_audio += f'{q}.\n'
            scene = Scene(pergunta, f'./content/audios/pergunta-{index}.mp3', 0, SceneType.PERGUNTA)
            self._list_scene.append(scene)

            self._audio_client.save_audio(pergunta_audio, f'pergunta-{index}')
            self._audio_client.save_audio(p["resposta"], f'resposta-{index}')

            p["resposta"] = self._format_text(p["resposta"])
            scene = Scene(p["resposta"], f'./content/audios/resposta-{index}.mp3', 0, SceneType.RESPOSTA)

            self._list_scene.append(scene)



        #encerramento
        for index, encerramento in enumerate(self._roteiro["encerramento"]):
            self._audio_client.save_audio(encerramento, f'encerramento-{index}')

            encerramento = self._format_text(encerramento)
            scene = Scene(encerramento, f'./content/audios/encerramento-{index}.mp3', 0, SceneType.ENCERRAMENTO)
            self._list_scene.append(scene)

    def _generate_video(self):
        # Write video to file
        output_file = './content/final.mp4'
        self._final_clip.write_videofile(output_file, fps=24, codec='libx264', audio_codec='aac')

    def file(self):
        self._create_all_audio()
        self._create_video()
        self._generate_video()

    def _create_video(self):

        # Create video clips for each sentence
        #loop com a lista de sentenças com index em cada interacao
        bg_clip = ImageClip(f'./content/images/img{random.randint(0, 4)}.png')

        for scene in self._list_scene:
            self._create_scene(scene, bg_clip)


        # Combine video clips and audio clip
        final_clip = concatenate_videoclips(self._video_clips)
        audio_clip = AudioFileClip(f'./content/audios/intro/intro{random.randint(0, 3)}.mp3')

        repeticoes_necessarias = int(final_clip.duration // audio_clip.duration) + 1
        for i in range(repeticoes_necessarias):
            audio_clip = concatenate_audioclips([audio_clip, audio_clip])

        audio_clip = audio_clip.set_duration(final_clip.duration)
        audio_repetido = audio_clip.volumex(0.1)



        audio_combinado = CompositeAudioClip([final_clip.audio, audio_repetido])

        self._final_clip = final_clip.set_audio(audio_combinado)



    def _create_scene(self, scene, bg_clip):
        self._calculate_scene_time(scene)

        # Load background image and create video clip
        bg_clip = (bg_clip
         .set_duration(scene._total_time)
         .resize(.5)
        )
        w_bg, h_bg = bg_clip.size

        # Load text image and create video clip

        text_clip = (TextClip(scene._text , fontsize=120, color='white')
                         .set_duration(scene._total_time))

        # Ajusta a largura do clipe de texto para que o texto caiba dentro dela
        w, h = text_clip.size
        proporcional = self._calculate_proporcional(w, w_bg)
        text_clip = text_clip.resize(proporcional).set_position(('center', 'center'))
        # Define a cor de fundo como vermelho e torna o fundo transparente
        text_clip = text_clip.on_color(
            size=(w_bg, h_bg),
            color=(0, 0, 0),
            col_opacity=0.4
        )


        compose = CompositeVideoClip([bg_clip, text_clip], use_bgclip=True)

        # Load audio file and create audio clip
        audio_clip = None
        if scene._scene_type == SceneType.PERGUNTA:
            audio_questions_clip = AudioFileClip(scene._audio_path)
            audio_clock_file = f'./content/audios/clock.mp3'
            audio_clock_clip = AudioFileClip(audio_clock_file)
            audio_clip = concatenate_audioclips([audio_questions_clip, audio_clock_clip])

        else:
            audio_questions_clip = AudioFileClip(scene._audio_path)
            audio_clip = audio_questions_clip


        # Set audio for scene clip
        compose = compose.set_audio(audio_clip)

        # Load correct answer image and create video clip
        self._video_clips.append(compose)

    def  _calculate_scene_time(self, scene):
        question_time = 0
        if scene._scene_type == SceneType.PERGUNTA:
            question_time = self._audio_client.get_audio_duration(scene._audio_path)
            question_time += self._audio_client.get_audio_duration(f'./content/audios/clock.mp3')
        else:
            question_time = self._audio_client.get_audio_duration(scene._audio_path)


        scene._total_time = question_time

    def _calculate_proporcional(self, weight_txt, weight_bg):
        return weight_bg / (weight_txt * 1.1)

    def _format_text(self, text):
        #qubrar com \n a cada 6 palavras
        words = text.split()
        new_text = ''
        count = 0
        for word in words:
            new_text += word + ' '
            count += 1
            if count == 5:
                new_text += '\n'
                count = 0

        return new_text

