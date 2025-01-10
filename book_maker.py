
# %% libraries
import os
import sys
from tqdm import tqdm
import streamlit as st

# make python able to find the functions it needs
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from supporting_functions import (book_parser, 
                                  generate_chapter_file, 
                                  convert_wav_to_mp3, 
                                  clean_chapters,
                                  suppress_output,
                                  )


def book_maker(infile, tts, gpt_cond_latent, speaker_embedding, parameters=None):

    if parameters is None:
        parameters = {'selected_voice':'Bert','speed':1.0,'split_sentences':False,'language':'en'}            

    # %% get book text

    #infile = './examples/The colour out of space - HP Lovecraft.epub'
    with suppress_output():
        book = book_parser(infile)

    #filter out empty chapters and license
    chapters = clean_chapters(book.get_chapters(' '))

    #get book metadata
    book_author = book.get_book_author()
    book_title  = book.get_book_title()

    print(str(len(chapters)) + ' chapters found' )
    st.write('number of chapters found: ' + str(len(chapters)))

    # %% produce raw audio files

    #generate chapter files
    for chapter_number, chapter in enumerate(chapters):
        #skip this chapter if it exists already
        if os.path.exists(f'temp/chapter_{chapter_number}_combined.wav'):
            continue
        text = chapter[1]  # Assuming chapter[1] contains the text of the chapter
        #with suppress_output():
        #generate_chapter_file(text, chapter_number,output_dir="temp",selected_voice=selected_voice,max_length=max_length,speed=speed,emotion=emotion,split_sentences=split_sentences)
        generate_chapter_file(text, tts, gpt_cond_latent, speaker_embedding, chapter_number, output_dir="temp", parameters=parameters)

            
    # %% file cleanup and organization

    #convert each chapter to mp3 with metadata
    for chapter_number, chapter in enumerate(chapters):
        chapter_title = chapter[0]
        for file in os.listdir('temp'):
            if file.startswith(f'chapter_{chapter_number}_') and file.endswith('.wav'):
                mp3_file = file.replace('_combined', '').replace('_',' ').title().replace('.Wav', '.mp3')
                convert_wav_to_mp3(os.path.join('temp', file), os.path.join('temp', mp3_file), chapter_title, chapter_number, book_author, book_title)

    # create a folder with the book title in the 'books' folder
    output_folder = os.path.join('books', book.get_book_author())
    output_folder = os.path.join(output_folder, book.get_book_title())
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    #copy over all the chapter mp3 files
    for file in os.listdir('temp'):
        if file.startswith('Chapter') & file.endswith('.mp3'):
            #if the output file exists already, delete it
            if os.path.exists(os.path.join(output_folder, file)):
                os.remove(os.path.join(output_folder, file))
            os.rename(os.path.join('temp', file), os.path.join(output_folder, file))

    #remove chapter files from the temp folder
    for file in os.listdir('temp'):
        if file.startswith('chapter'):
            os.remove(os.path.join('temp', file))