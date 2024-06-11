import torch
from TTS.api import TTS

# Define Global Variables
device = "cuda" if torch.cuda.is_available() else "cpu"
output_path = "output.wav"


def print_TTS_models():
    print(TTS().list_models())


def multi_speaker_model():
    # Init TTS
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

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


def single_speaker_model():
    # Init TTS with the target model name and run
    tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC").to(device)
    tts.tts_to_file(text="Hello!", file_path=output_path)

    # Example voice cloning with YourTTS in English
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts").to(device)
    tts.tts_to_file(
        "This is voice cloning.",
        speaker_wav="my/cloning/audio.wav",
        language="en",
        file_path=output_path,
    )


print_TTS_models()
