# %%
from TTS.api import TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)

# generate speech by cloning a voice using default settings
tts.tts_to_file(text="The quick brown fox jumped over the lazy dog.",
                file_path="output.wav",
                speaker_wav="female_reference.wav",
                language="en")