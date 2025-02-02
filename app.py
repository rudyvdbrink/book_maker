# make python able to find the functions it needs
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# %% libraries
from book_maker import book_maker
from supporting_functions import generate_sample_audio, load_tts_model, get_tts_latents, get_model_file
from sample_translations import default_sample_text
from options_text import options_text
import streamlit as st

# %% page layout

st.set_page_config(layout="wide")

#create two columns
spacer1, col1, spacer2, col2, spacer3 = st.columns([1, 3, 1, 3, 1])

# %% Streamlit page title

# %% Side bar

#logo
st.sidebar.image('./figures/logo.png', width=250)  # Set the desired width in pixels

#create a sidebar with options for navigation
st.sidebar.title('Navigation')
st.sidebar.page_link(page="app.py", label="Home")
st.sidebar.page_link(page="pages/about.py", label="About")

#links out
st.sidebar.title('Resources')
st.sidebar.page_link(page="https://github.com/rudyvdbrink/book_maker", label="Code")
st.sidebar.page_link(page="https://ruudvandenbrink.net/", label="About author")

# %% Main page
# Left column: Drop-down menu
with col1:
    st.header("Voice options")
    # Get list of .wav files in the ./references/ folder
    voice_names = [f.split('.wav')[0] for f in os.listdir('./references/') if f.endswith('.wav')]
    try:
        voice_names.remove('custom_voice')
    except:
        pass

    #add custom voice to the list
    voice_names.append('[Custom voice]')
    #re-arrange list so it's sorted end to start
    #voice_names = voice_names[::-1]

    #drop-down menu with voice name
    selected_voice = st.selectbox("Select a voice:", voice_names)

    #if custom voice is selected, show file upload
    if selected_voice == '[Custom voice]':
        custom_voice = st.file_uploader("Upload a .wav file with the voice you want to use (roughly 6 to 20 seconds long)", type="wav")
        selected_voice = 'custom_voice'
        if custom_voice:
            with open('./references/custom_voice.wav', "wb") as f:
                f.write(custom_voice.getbuffer())
                st.write('Custom voice uploaded successfully!')
                 

    l, r = col1.columns(2)
    with l:
        #slider with voice speed
        speed = st.slider('Voice speed:', min_value=0.5, max_value=2.0, value=1.0, step=0.1)
        
        #slider for length penalty
        length_penalty = st.slider('Length penalty:', min_value=0.5, max_value=10.0, value=1.0, step=0.1)

        #slider for number of beams
        num_beams = st.slider('Number of beams:', min_value=1, max_value=10, value=1, step=1)
        
        #slider for top k
        top_k = st.slider('Top k:', min_value=10, max_value=100, value=50, step=10)
        
        #tick box for split setences
        split_sentences = st.checkbox('Split sentences', value=False)

    with r:
        #slider with temperature
        temperature = st.slider('Temperature:', min_value=0.1, max_value=10.0, value=0.75, step=0.05)

        #slider with max length
        max_length = st.slider('Max chunk length:', min_value=50, max_value=500, value=250, step=25)
        
        #slider with repetition penalty
        repetition_penalty = st.slider('Repetition penalty:', min_value=1.0, max_value=10.0, value=5.0, step=0.5)

        #slider with top p
        top_p = st.slider('Top p:', min_value=0.1, max_value=1.0, value=0.85, step=0.05)

        #drop-down menu with language
        language = st.selectbox("Select a language:", ['en', 'es', 'fr', 'de', 'it', 'pt', 'pl', 'tr', 'ru', 'nl', 'cs', 'ar', 'zh-cn', 'hu', 'ko', 'ja', 'hi'])
    
    #pop-over with explanation of options
    with st.popover('Help'):
        st.markdown(options_text())

    #make box with input text
    default_text = default_sample_text(selected_voice,language)
    input_text = st.text_input('Read the following:', default_text)

    parameters = {  'selected_voice': selected_voice,
                    'max_length': max_length,
                    'speed': speed,
                    'split_sentences': split_sentences,
                    'temperature': temperature,
                    'length_penalty': length_penalty,
                    'repetition_penalty': repetition_penalty,
                    'top_k': top_k,
                    'top_p': top_p,
                    'num_beams': num_beams,
                    'language': language}
    
    if st.button('Generate sample',key='sample_button'):

        #if custom voice is selected but no file is uploaded, show error message
        if selected_voice == 'custom_voice' and not custom_voice:
            st.error('Please upload a custom voice file first')                        

        #st.write('Split sentences: ' + str(split_sentences))
        #display loading wheel while generating audio
        with st.spinner('Downloading model...'):
            get_model_file()

        with st.spinner('Preparing the model...'):
            tts = load_tts_model()
            gpt_cond_latent, speaker_embedding = get_tts_latents(tts, selected_voice=selected_voice)

        with st.spinner('Generating audio...'):
            st.audio( generate_sample_audio(input_text, 
                                            tts, 
                                            gpt_cond_latent, 
                                            speaker_embedding, 
                                            parameters) , format='audio/wav')

# Right column: BookMaker part
with col2:
    st.header("Upload and Process EPUB Files")
    # Allow user to upload one or more epub files
    uploaded_files = st.file_uploader("Upload epub files", type="epub", accept_multiple_files=True)

    if uploaded_files:
        
        if st.button('Run!',key='book_run_button'):

            #if custom voice is selected but no file is uploaded, show error message
            if selected_voice == 'custom_voice' and not custom_voice:
                st.error('Please upload a custom voice file first')  

            st.write('selected voice: ' + selected_voice)       
            with st.spinner('Downloading model...'):
                    get_model_file()

            with st.spinner('Preparing the model...'):
                tts = load_tts_model()
                gpt_cond_latent, speaker_embedding = get_tts_latents(tts, selected_voice=selected_voice) 

            for uploaded_file in uploaded_files:
                
                book_name = uploaded_file.name.split('.epub')[0]
                st.write('working on: ' + book_name)
                
                with open('./temp/temp.epub', "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # convert book                
                book_maker('./temp/temp.epub',
                           tts, 
                           gpt_cond_latent, 
                           speaker_embedding,
                           parameters)

                os.remove('./temp/temp.epub')
                st.write('done')