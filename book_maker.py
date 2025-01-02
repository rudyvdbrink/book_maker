
# %% libraries
import os

from supporting_functions import book_parser, generate_chapter_file, convert_wav_to_mp3, clean_chapters

# %% get book text

infile = './examples/The call of Cthulhu - HP Lovecraft.epub'
#infile = './examples/The colour out of space - HP Lovecraft.epub'
book = book_parser(infile)

#filter out empty chapters and license
chapters = clean_chapters(book.get_chapters(' '))

#generate chapter files
for chapter_number, chapter in enumerate(chapters):
    #skip this chapter if it exists already
    if os.path.exists(f'temp/chapter_{chapter_number}_combined.wav'):
        continue
    text = chapter[1]  # Assuming chapter[1] contains the text of the chapter
    generate_chapter_file(text, chapter_number)


# Get book metadata
book_author = book.get_book_author()
book_title  = book.get_book_title()

#convert each chapter to mp3 with metadata
for chapter_number, chapter in enumerate(chapters):
    chapter_title = chapter[0]
    for file in os.listdir('temp'):
        if file.startswith(f'chapter_{chapter_number}_') and file.endswith('.wav'):
            mp3_file = file.replace('.wav', '.mp3').replace('_combined', '')
            convert_wav_to_mp3(os.path.join('temp', file), os.path.join('temp', mp3_file), chapter_title, chapter_number, book_author, book_title)
            
# %% file cleanup and organization

# create a folder with the book title in the 'books' folder
output_folder = os.path.join('books', book.get_book_title())
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