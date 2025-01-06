import torch
from TTS.api import TTS
import os

# %% load saved model

model_path  = "./models/"
config_path = model_path + "config.json"

tts = TTS.load_tts_model_by_path(TTS,model_path=model_path,config_path=model_path+'config.json')

# %% save model

torch.save(tts, './temp/model.pth')
# %% load model

the_model = torch.load('./temp/model.pth', weights_only=False)