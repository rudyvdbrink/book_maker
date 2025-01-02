# %% libraries
from book_maker import book_maker
from supporting_functions import generate_sample_audio
import streamlit as st
import os

# %% Streamlit page title
st.set_page_config(layout="wide")
st.title("BookMaker")

# Create two columns
#col1, col2 = st.columns(2)
spacer1, col1, spacer2, col2, spacer3 = st.columns([1, 3, 1, 3, 1])

# Left column: Drop-down menu
with col1:
    st.header("Voice selection")
    # Get list of .wav files in the ./references/ folder
    voice_names = [f.split('.wav')[0] for f in os.listdir('./references/') if f.endswith('.wav')]

    #re-arrange list so it's sorted end to start
    voice_names = voice_names[::-1]

    # Drop-down menu
    selected_voice = st.selectbox("Select a voice", voice_names)

    #make box with input text
    input_text = st.text_input('Input text', 'The quick brown fox jumps over the lazy dog')

    if st.button('Generate sample'):
        st.audio(generate_sample_audio(input_text, selected_voice), format='audio/wav')


# Right column: BookMaker part
with col2:
    st.header("Upload and Process EPUB Files")
    # Allow user to upload one or more epub files
    uploaded_files = st.file_uploader("Upload epub files", type="epub", accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            if st.button('Run!'):
                st.write('selected voice: ' + selected_voice)
                book_name = uploaded_file.name.split('.epub')[0]
                st.write('working on: ' + book_name)

                with open('./temp/temp.epub', "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # convert book                
                book_maker('./temp/temp.epub',selected_voice)

                os.remove('./temp/temp.epub')
                st.write('done')