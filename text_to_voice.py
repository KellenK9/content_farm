import torch
from TTS.api import TTS
import time
import librosa

# Tortoise Imports
# from TTS.tts.configs.tortoise_config import TortoiseConfig
# from TTS.tts.models.tortoise import Tortoise


class TTSGenerator:
    # Define Global Variables
    device = "cuda" if torch.cuda.is_available() else "cpu"
    output_path = "output.wav"

    def print_TTS_models():
        print(TTS().list_models())
        # "<model_type>/<language>/<dataset>/<model_name>"

    def multi_speaker_model():
        # Init TTS
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True).to(
            TTSGenerator.device
        )

        # Run TTS
        # Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
        # Text to speech list of amplitude values as output
        wav = tts.tts(
            text="Hello world!", speaker_wav="my/cloning/audio.wav", language="en"
        )
        # Text to speech to a file
        tts.tts_to_file(
            text="Hello world!",
            speaker_wav="my/cloning/audio.wav",
            language="en",
            file_path=TTSGenerator.output_path,
        )

    def single_speaker_model(model_name, file_path, text):
        # Init TTS with the target model name and run
        tts = TTS(model_name=model_name)  # , gpu=True)
        print(f"text for use is: {text}")
        tts.tts_to_file(
            text=text,
            file_path=f"{file_path}.wav",
        )
        duration = librosa.get_duration(path=f"temp_audio/{file_path}.wav")
        return duration

    def tortoise_model(text):
        config = TTSGenerator.TortoiseConfig()
        model = TTSGenerator.Tortoise.init_from_config(config)
        model.load_checkpoint(config, checkpoint_dir="paths/to/models_dir/", eval=True)

        # with random speaker
        output_dict = model.synthesize(
            text, config, speaker_id="random", extra_voice_dirs=None
        )

    # Let's compare a bunch of the base models that have direct Python integration. We can compare the output and compute time.
    def test_models():
        # "<model_type>/<language>/<dataset>/<model_name>"
        model_names = [
            ("tts_models/en/multi-dataset/tortoise-v2", "tortoise"),  # 5835 seconds
            (
                "tts_models/en/ljspeech/tacotron2-DDC_ph",
                "tacotron2_DDC_ph",
            ),  # 26 seconds
            ("tts_models/en/ljspeech/glow-tts", "glow"),  # 115 seconds
            (
                "tts_models/en/blizzard2013/capacitron-t2-c150_v2",
                "capacitron2",
            ),  # 166 seconds
            ("tts_models/en/ljspeech/overflow", "overflow"),  # 96 seconds
            ("tts_models/en/ljspeech/vits", "vits"),  # 26 seconds
            ("tts_models/en/ljspeech/speedy-speech", "speedy_speech"),  # 26 seconds
            ("tts_models/en/ljspeech/neural_hmm", "neural"),  # 47 seconds
            ("tts_models/en/jenny/jenny", "jenny"),  # 421 seconds
            ("tts_models/en/sam/tacotron-DDC", "tacotron_sam"),  # 252 seconds
            ("tts_models/en/ljspeech/vits--neon", "vits_neon"),  # 68 seconds
            ("tts_models/en/ljspeech/tacotron2-DDC", "tacotron2_DDC"),  # 58 seconds
            ("tts_models/en/ljspeech/tacotron2-DCA", "tacotron2_DCA"),  # 66 seconds
            ("tts_models/en/ek1/tacotron2", "tacotron_ek1"),  # 1897 seconds
            ("tts_models/en/vctk/vits", "vits_by_vctk"),  # multi-speaker
            ("tts_models/en/vctk/fast_pitch", "fast_pitch"),  # multi-speaker
        ]
        durations = []

        for model in model_names:
            curr_time = time.time()
            TTSGenerator.single_speaker_model(model[0], model[1])
            duration = time.time() - curr_time
            print(f"{model[1]} took this many seconds: {duration}")
            durations.append(duration)

        for i in range(len(durations)):
            print(f"{model_names[i][1]} took this many seconds: {durations[i]}")


# My favorites:
# Overflow
# vits_neon
# Tacotron2 DDC_ph
