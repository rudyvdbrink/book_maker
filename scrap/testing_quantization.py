# %%
import torch
from TTS.api import TTS
import os

# Load the model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

# Quantize the model
quantized_model = torch.quantization.quantize_dynamic(
    tts, {torch.nn.Linear, torch.nn.Conv1d, torch.nn.Conv2d}, dtype=torch.qint8
)

if not os.path.exists("models"):
    os.makedirs("models")


# %% 

torch.save(quantized_model, './temp/quantized_model.pth')
# %% load model

the_model = torch.load('./temp/quantized_model.pth', weights_only=False)

# %%

# Saving
torch.save(quantized_model.state_dict(), "./temp/quantized_model_state_dict.pth")

# Loading
model = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
model.load_state_dict(torch.load("./temp/quantized_model_state_dict.pth"))

# %%


# Example of loading a model from a checkpoint file
tts_model = TTS(
    model_path='./temp/', 
    config_path="./models/config.json", 
    progress_bar=False, 
    gpu=True  # Set this to False if you don't have GPU support
)