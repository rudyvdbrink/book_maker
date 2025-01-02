# %%

import os
from pydub import AudioSegment
from TTS.api import TTS

from audiobook_generator.config.general_config import GeneralConfig
from audiobook_generator.book_parsers.epub_book_parser import EpubBookParser

from mutagen.easyid3 import EasyID3

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

# %% text to speech

def split_text(text, max_length=250):
    def split_chunk(chunk):
        if len(chunk) <= max_length:
            return [chunk]
        mid = len(chunk) // 2
        split_point = chunk.rfind(' ', 0, mid)
        if split_point == -1:
            split_point = chunk.find(' ', mid)
        if split_point == -1:
            return [chunk]
        return split_chunk(chunk[:split_point].strip()) + split_chunk(chunk[split_point:].strip())

    chunks = []
    for sentence in text.split('. '):
        if len(sentence) > max_length:
            for sub_chunk in sentence.split(', '):
                chunks.extend(split_chunk(sub_chunk.strip()))
        else:
            chunks.append(sentence)
    return chunks

def generate_chapter_file(text, chapter_number, output_dir="temp"):
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    chunks = split_text(text)
    audio_files = []
    
    for i, chunk in enumerate(chunks):
        file_path = os.path.join(output_dir, f"chapter_{chapter_number}_part_{i}.wav")
        #skip if text is empty
        if not chunk.strip():
            continue
        tts.tts_to_file(text=chunk, file_path=file_path, speaker_wav="female_reference.wav", language="en")
        

        audio_files.append(file_path)
    
    combined = AudioSegment.empty()
    for file in audio_files:
        combined += AudioSegment.from_wav(file)
    
    combined.export(os.path.join(output_dir, f"chapter_{chapter_number}_combined.wav"), format="wav")

    # Delete all chapter parts
    for file in audio_files:
        os.remove(file)

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
