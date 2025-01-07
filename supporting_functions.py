# %%

import os
import sys
from pydub import AudioSegment
import torch

from TTS.api import TTS

from TTS.tts.models.xtts import Xtts
from TTS.tts.configs.xtts_config import XttsConfig

import torch
import os

from tqdm import tqdm

import nltk
from nltk.tokenize import sent_tokenize

import streamlit as st

from audiobook_generator.config.general_config import GeneralConfig
from audiobook_generator.book_parsers.epub_book_parser import EpubBookParser

from mutagen.easyid3 import EasyID3

import soundfile as sf

from contextlib import contextmanager

# %% context management

@contextmanager
def suppress_output():
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

# %% book parsing

class Args:
    def __init__(self, input_file):
        self.input_file = input_file
        self.output_folder = 'output_directory'
        self.preview = False
        self.output_text = True
        self.log = None
        self.no_prompt = True
        self.title_mode = 'auto'  # Options: 'auto', 'tag_text', 'first_few'
        self.newline_mode = 'single'  # Options: 'single', 'double', 'none'
        self.chapter_start = None
        self.chapter_end = None
        self.remove_endnotes = True
        self.search_and_replace_file = None
        self.tts = None
        self.language = None
        self.voice_name = None
        self.output_format = None
        self.model_name = None
        self.break_duration = None
        self.voice_rate = None
        self.voice_volume = None
        self.voice_pitch = None
        self.proxy = None
        self.piper_path = None
        self.piper_speaker = None
        self.piper_sentence_silence = None
        self.piper_length_scale = None

def book_parser(infile):
    # infile = './examples/The_Life_and_Adventures_of_Robinson_Crusoe.epub'
    # book = book_parser(infile)
    args = Args(infile)
    config = GeneralConfig(args)
    book = EpubBookParser(config)
    return book

def clean_chapters(chapters):
    #remove empty chapters
    chapters = [chapter for chapter in chapters if chapter != ('', '')]

    #remove chapters with the project gutenburg license
    chapters = [chapter for chapter in chapters if 'project gutenberg license' not in chapter[0].lower().replace('_',' ')]
    return chapters

# %% preparing text for speech conversion

#download data if needed:
def prep_nltk(download_dir='./.venv/nltk_data'):
    if not os.path.exists(download_dir + '/tokenizers/punkt_tab'):
        nltk.download('punkt_tab',download_dir='./.venv/nltk_data')

#function for splitting sentence parts (chunks) down further
def split_chunk(chunk,max_length=500):
        if len(chunk) <= max_length:
            return [chunk]
        mid = len(chunk) // 2
        split_point = chunk.rfind(' ', 0, mid)
        if split_point == -1:
            split_point = chunk.find(' ', mid)
        if split_point == -1:
            return [chunk]
        return split_chunk(chunk[:split_point].strip()) + split_chunk(chunk[split_point:].strip())

#function for splitting sentences into chunks
def split_chunks(chunks,max_length=500):
    all_chunks = []
    for chunk in chunks: #loop over sentences
        if len(chunk) > max_length:
            for sub_chunk in chunk.split(', '):
                all_chunks.extend(split_chunk(sub_chunk.strip()))
        else:
            all_chunks.append(chunk)    
    
    return all_chunks

#funcion for combining chucks that are below the max_length
def combine_chunks(chunks,max_length=500):
    combined_chunks = []
    combined_text = ''
    for chunk in chunks:
        if len(combined_text) + len(chunk) < max_length-20:
            if chunk[-1] != '.':
                chunk += ', '
            else:
                chunk += ' '
            combined_text += chunk
        else:
            combined_chunks.append(combined_text)
            combined_text = chunk

    combined_chunks.append(combined_text)
    
    return combined_chunks

def split_text(text, max_length=500):
   
    #prepare data download if it doesn't exist yet
    prep_nltk()
    
    #split text into sentences
    chunks = sent_tokenize(text)

    #split each sentence into chunks, if needed
    chunks = split_chunks(chunks,max_length) 

    #combine chunks that are below the max_length
    chunks = combine_chunks(chunks,max_length)

    return chunks

# %% modifying audio

# import librosa
# import soundfile as sf

# def slow_audio_speed(input_file, speed=1.0):
#     # Load the audio file
#     y, sr = librosa.load(input_file, sr=None)
    
#     # Change the tempo of the audio
#     y = librosa.effects.time_stretch(y, rate=float(speed))
    
#     # Save the slowed down audio
#     sf.write(input_file, y, sr)


# def change_audio_speed(input_file, speed):
#     if speed > 1.0:
#         audio = AudioSegment.from_wav(input_file)
#         audio = audio.speedup(playback_speed=speed)
#         audio.export(input_file, format="wav")
#     elif speed < 1.0:
#         slow_audio_speed(input_file, speed)


# %% text to speech

# #load standard text to speech module (probably wanna modify to run with st.cache)
# def load_tts_model():
#     with suppress_output():
#         device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#         tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
#         tts = tts.to(device)
#         return tts  

# #function for generating an audio file for a chunk of text
# def produce_audio(tts,chunk,chunk_file_path,selected_voice='Sky',speed=1.0,emotion='Neutral',split_sentences=False):
#     with suppress_output():
#         tts.tts_to_file(text=chunk, 
#                         file_path=chunk_file_path, 
#                         speaker_wav='./references/' + selected_voice + '.wav', 
#                         language="en", 
#                         speed=speed, 
#                         emotion=emotion,
#                         split_sentences=split_sentences)
        
#         if speed != 1.0:
#             change_audio_speed(chunk_file_path, speed)
   
def load_tts_model(base_path="./models/"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model_path    = os.path.join(base_path, 'model.pth')
    config_path   = os.path.join(base_path, 'config.json')
    vocab_path    = os.path.join(base_path, 'vocab.json')
    speaker_path  = os.path.join(base_path, 'speakers_xtts.pth')

    config = XttsConfig()

    #load configuration
    config.load_json(config_path)

    #adjust parameters if needed

    #load the model
    tts = Xtts.init_from_config(config)
    with suppress_output():
        tts.load_checkpoint(config, 
                            checkpoint_path=model_path, 
                            vocab_path=vocab_path, 
                            speaker_file_path=speaker_path,
                            eval=True)
    
    #move model to GPU if we have one
    tts = tts.to(device)

    return tts

def get_tts_latents(tts, audio_path='./references/', selected_voice='Bert'):
     
    audio_path = os.path.join(audio_path, selected_voice + '.wav')
    
    gpt_cond_latent, speaker_embedding = tts.get_conditioning_latents(audio_path=audio_path)
    
    return gpt_cond_latent, speaker_embedding

def run_inference(tts,text,gpt_cond_latent,speaker_embedding,parameters=None):

    if parameters is None:
        parameters = {'selected_voice':'Bert','speed':1.0,'split_sentences':False,'language':'en'}

    speed           = parameters['speed']
    split_sentences = parameters['split_sentences']
    language        = parameters['language']

    output = tts.inference( text, 
                            gpt_cond_latent=gpt_cond_latent,
                            speaker_embedding=speaker_embedding,
                            enable_text_splitting=split_sentences,
                            speed=speed,
                            language=language )
    
    #save only the audio
    output = output['wav']

    return output

def write_audio_to_file(output, file_path='./temp/',file_name='output.wav'):

    #write sound information to file
    sf.write(os.path.join(file_path, file_name), output, 24000)

#function for generating an audio file for a chunk of text
def produce_audio(tts, gpt_cond_latent, speaker_embedding, text, file_path='./temp',file_name='output.wav',parameters=None):
    
    #generate audio file
    output = run_inference(tts,text,gpt_cond_latent,speaker_embedding,parameters=parameters)
    
    #write sound information to file
    write_audio_to_file(output, file_path=file_path, file_name=file_name)


#function to generate a .wav file for an entire chapter
def generate_chapter_file(text, tts, gpt_cond_latent, speaker_embedding, chapter_number, output_dir="temp", parameters=None):

    if parameters is None:
        parameters = {'selected_voice':'Bert','speed':1.0,'split_sentences':False,'language':'en','max_length':250}

    max_length      = parameters['max_length']

    progress_text = "Chapter " + str(chapter_number+1) 
    progress_bar  = st.progress(0, text=progress_text)
        
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    chunks = split_text(text,max_length=max_length)
    audio_files = []
    
    for i, chunk in enumerate( tqdm(chunks, desc='Chapter ' + str(chapter_number+1)) ):

        #print(f"Generating chapter {chapter_number} part {i+1}/{len(chunks)}")

        #draw streamlit progress bar
        progress_bar.progress((i+1)/len(chunks), text=progress_text) 

        file_name = f"chapter_{chapter_number}_part_{i}.wav"
        #skip if text is empty
        if not chunk.strip():
            continue

        #skip if text is a period or elipses
        if chunk.strip() in ['.', '..', '...']:
            continue
        
        #generate audio file for chunk
        #produce_audio(tts, chunk, file_path, selected_voice, speed, emotion, split_sentences=split_sentences )
        
        produce_audio(tts, gpt_cond_latent, speaker_embedding, chunk, output_dir, file_name=file_name, parameters=parameters)

        audio_files.append( os.path.join(output_dir, file_name) )
    
    combined = AudioSegment.empty()
    for file in audio_files:
        combined += AudioSegment.from_wav(file)
    
    combined.export(os.path.join(output_dir, f"chapter_{chapter_number}_combined.wav"), format="wav")

    # Delete all chapter parts
    for file in audio_files:
        os.remove(file)

#function to generate sample audio
def generate_sample_audio(text, tts, gpt_cond_latent, speaker_embedding, parameters=None):

    if parameters is None:
        parameters = {'selected_voice':'Bert','speed':1.0,'split_sentences':False,'language':'en','max_length':250}

    max_length      = parameters['max_length']

    
    #create temp folder if needed
    if not os.path.exists('temp'):
        os.makedirs('temp')
        
    chunks = split_text(text, max_length)
    audio_files = []
    
    for i, chunk in enumerate(chunks):
        chunk_file_path = os.path.join('temp', f'sample_part_{i}.wav')
        #produce_audio(tts, chunk, chunk_file_path, selected_voice, speed, emotion, split_sentences=split_sentences)
        produce_audio(tts, gpt_cond_latent, speaker_embedding, chunk, './temp', file_name=f'sample_part_{i}.wav', parameters=parameters)

        audio_files.append(chunk_file_path)
    
    combined = AudioSegment.empty()
    for file in audio_files:
        combined += AudioSegment.from_wav(file)
    
    combined_file_path = os.path.join('temp', 'sample.wav')
    combined.export(combined_file_path, format="wav")

    # Clean up temporary chunk files
    for file in audio_files:
        os.remove(file)
    
    return combined_file_path

# #delete all files with the word 'part' in the name
# for file in os.listdir('temp'):
#     if 'part' in file:
#         os.remove(os.path.join('temp', file))

# %% file conversion

def convert_wav_to_mp3(wav_file, mp3_file, chapter_title, chapter_number, artist, album):
    chapter_title = chapter_title.lower().replace('_',' ').title()
    audio = AudioSegment.from_wav(wav_file)
    audio.export(mp3_file, format="mp3", tags={
        "title": chapter_title,
        "tracknumber": str(chapter_number),
        "artist": artist,
        "album": album
    })
    # Add additional metadata using mutagen
    audiofile = EasyID3(mp3_file)
    audiofile["title"] = chapter_title
    audiofile["tracknumber"] = str(chapter_number)
    audiofile["artist"] = artist
    audiofile["album"] = album
    audiofile.save()

