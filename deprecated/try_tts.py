# %%

import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"


# Initialize TTS with a female voice model
tts = TTS(model_name="tts_models/en/jenny/jenny")

# Text to convert to speech
text = "Hey I think this might work as a voice model."

# Generate speech
tts.tts_to_file(text=text, file_path="output.wav")