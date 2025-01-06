# %%

import os
from supporting_functions import book_parser, split_text


# %%
infile = './examples/Rage - Richard Bachman.epub'
book = book_parser(infile)

text = book.get_chapters(' ')[4][1]

# %%

chuncks = split_text(text)

# %% old split text function

def split_text(text, max_length=500):
    #max_length is hard-coded in:
    #.venv/Lib/TTS/tts/layers/xtts/tokenizer.py
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

# %% new split text function

import nltk
from nltk.tokenize import sent_tokenize

#download data if needed:
def prep_nltk(download_dir='./.venv/nltk_data'):
    if not os.path.exists(download_dir + '/tokenizers/punkt_tab'):
        nltk.download('punkt_tab',download_dir='./.venv/nltk_data')

#function for splitting chunks of text down further
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

def split_text_nltk(text, max_length=500):
   
    #prepare data download if it doesn't exist yet
    prep_nltk()
    
    #split text into sentences
    chunks = sent_tokenize(text)

    #split each sentence into chunks, if needed
    chunks = split_chunks(chunks,max_length) 

    #combine chunks that are below the max_length
    chunks = combine_chunks(chunks,max_length)
    
    return chuncks
# %%
