import torch
from TTS.api import TTS
import time

# Tortoise Imports
# from TTS.tts.configs.tortoise_config import TortoiseConfig
# from TTS.tts.models.tortoise import Tortoise

# Define Global Variables
device = "cuda" if torch.cuda.is_available() else "cpu"
output_path = "output.wav"


def print_TTS_models():
    print(TTS().list_models())
    # "<model_type>/<language>/<dataset>/<model_name>"


def multi_speaker_model():
    # Init TTS
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True).to(device)

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
        file_path=output_path,
    )


def single_speaker_model(model_name, file_path):
    # Init TTS with the target model name and run
    tts = TTS(model_name=model_name, gpu=True)
    tts.tts_to_file(
        text="Here is an intriguing sentence that should be long and versatile in order to serve as a nice example of different models. This second sentence will be a similar length to the first one and continue serving our testing purpose. The last sentence is short.",
        file_path=f"{file_path}.wav",
    )
    # First attempt seemed to use 3 different voices, 1 per sentence. The second voice sounded nice but the other 2 were rough.
    # Compute time for this little blurb ended up being around an hour with my old CPU


def tortoise_model(text):
    config = TortoiseConfig()
    model = Tortoise.init_from_config(config)
    model.load_checkpoint(config, checkpoint_dir="paths/to/models_dir/", eval=True)

    # with random speaker
    output_dict = model.synthesize(
        text, config, speaker_id="random", extra_voice_dirs=None
    )


# Let's compare a bunch of the base models that have direct Python integration. We can compare the output and compute time.
def test_models():
    # "<model_type>/<language>/<dataset>/<model_name>"
    model_names = [
        # ("tts_models/en/multi-dataset/tortoise-v2", "tortoise"),  # 5835 seconds
        ("tts_models/en/ljspeech/tacotron2-DDC_ph", "tacotron2_DDC_ph"),
        ("tts_models/en/ljspeech/glow-tts", "glow"),
        ("tts_models/uk/mai/glow-tts", "glow_uk"),
        ("tts_models/uk/mai/vits", "vits_uk"),
        # ("tts_models/en/blizzard2013/capacitron-t2-c150_v2", "capacitron2"),
        ("tts_models/en/ljspeech/overflow", "overflow"),
        ("tts_models/en/ljspeech/vits", "vits"),
        # ("tts_models/en/vctk/vits", "vits_by_vctk"),
        # ("tts_models/en/vctk/fast_pitch", "fast_pitch"),
        # ("tts_models/en/ljspeech/speedy-speech", "speedy_speech"),
        # ("tts_models/en/jenny/jenny", "jenny"),
        # ("tts_models/en/ljspeech/neural_hmm", "neural"),
    ]
    durations = []

    for model in model_names:
        curr_time = time.time()
        single_speaker_model(model[0], model[1])
        duration = time.time() - curr_time
        print(f"{model[1]} took this many seconds: {duration}")
        durations.append(duration)

    for i in range(len(durations)):
        print(f"{model[i]} took this many seconds: {durations[i]}")


# test_models()

print(torch.cuda.is_available())
