
# %%

from audiobook_generator.config.general_config import GeneralConfig
from audiobook_generator.book_parsers.epub_book_parser import EpubBookParser

# %% define arguments class

class Args:
    def __init__(self):
        self.input_file = 'path_to_your_epub_file.epub'
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

# %% parse the book

args = Args()
args.input_file = './examples/The_Life_and_Adventures_of_Robinson_Crusoe.epub'
#args.input_file = './temp/The Colour Out of Space - HP Lovecraft.epub'
config = GeneralConfig(args)

# %%

book = EpubBookParser(config)

# %%

# def generate_chapter_file(text):
#     from TTS.api import TTS
#     tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)

#     # generate speech by cloning a voice using default settings
#     tts.tts_to_file(text=text,
#                     file_path="temp/chapter.wav",
#                     speaker_wav="female_reference.wav",
#                     language="en")
    
# # %%

# generate_chapter_file(text)

# %%

import os
from pydub import AudioSegment
from TTS.api import TTS

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

#function to convert wav to mp3
def convert_wav_to_mp3(wav_file, mp3_file):
    AudioSegment.from_wav(wav_file).export(mp3_file, format="mp3")

# %%

#generate chapter files
chapters = book.get_chapters(' ')
for chapter_number, chapter in enumerate(chapters):
    #skip this chapter if it exists already
    if os.path.exists(f'temp/chapter_{chapter_number}_combined.wav'):
        continue
    text = chapter[1]  # Assuming chapter[1] contains the text of the chapter
    generate_chapter_file(text, chapter_number)

#convert each chapter to mp3
for file in os.listdir('temp'):
    if file.startswith('chapter_') and file.endswith('.wav'):
        convert_wav_to_mp3(os.path.join('temp', file), os.path.join('temp', file.replace('.wav', '.mp3')))

# %%

# create a folder with the book title in the 'books' folder
output_folder = os.path.join('books', book.title)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

#copy over all the chapter mp3 files
for file in os.listdir('temp'):
    if file.startswith('chapter_') & file.endswith('.mp3'):
        os.rename(os.path.join('temp', file), os.path.join(output_folder, file))

#remove chapter files from the temp folder
for file in os.listdir('temp'):
    if file.startswith('chapter_'):
        os.remove(os.path.join('temp', file))