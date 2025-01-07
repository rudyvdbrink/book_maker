# %% libraries
from book_maker import book_maker
from supporting_functions import generate_sample_audio, load_tts_model, get_tts_latents
import streamlit as st
import os

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
st.sidebar.page_link(page="https://github.com/rudyvdbrink/ISIC_skin_lesions_prediciton", label="Code")
st.sidebar.page_link(page="https://ruudvandenbrink.net/", label="About author")

# %% Main page
# Left column: Drop-down menu
with col1:
    st.header("Voice options")
    # Get list of .wav files in the ./references/ folder
    voice_names = [f.split('.wav')[0] for f in os.listdir('./references/') if f.endswith('.wav')]

    #re-arrange list so it's sorted end to start
    #voice_names = voice_names[::-1]

    #drop-down menu with voice name
    selected_voice = st.selectbox("Select a voice:", voice_names)

    l, r = col1.columns(2)
    with l:
        #slider with voice speed
        speed = st.slider('Voice speed:', min_value=0.5, max_value=2.0, value=1.0, step=0.1)

        #tick box for split setences
        split_sentences = st.checkbox('Split sentences', value=False)

    with r:
        #slider with max length
        max_length = st.slider('Max chunk length:', min_value=50, max_value=500, value=250, step=25)
        #drop-down for voice emotion
        #emotion = st.selectbox("Select an emotion:", ['Neutral', 'Happy', 'Sad', 'Angry', 'Fearful', 'Disgusted', 'Surprised'])
        emotion = 'Neutral'

    #make box with input text
    input_text = st.text_input('Read the following:', "Hello, I'm " + selected_voice + ", and I'd be happy to read your books aloud for you.")

    parameters = {'selected_voice': selected_voice,
                  'max_length': max_length,
                  'speed': speed,
                  'split_sentences': split_sentences,
                  'language': 'en'}
    

    temperature=0.75, #range 0.1 to 10
    length_penalty=1.0, #0.5 to 10
    repetition_penalty=10.0, #1 to 10
    top_k=50, #10 to 100
    top_p=0.85, #0.1 to 1
    num_beams=1, #1 to 10?


    if st.button('Generate sample'):
        #st.write('Split sentences: ' + str(split_sentences))
        #display loading wheel while generating audio
        with st.spinner('Preparing the model...'):
            tts = load_tts_model()
            gpt_cond_latent, speaker_embedding = get_tts_latents(tts, selected_voice=selected_voice)

        with st.spinner('Generating audio...'):
            st.audio( generate_sample_audio(input_text, 
                                            tts, 
                                            gpt_cond_latent, 
                                            speaker_embedding, 
                                            parameters) , format='audio/wav')

            # st.audio(generate_sample_audio(input_text, 
            #                                selected_voice,
            #                                max_length=max_length, 
            #                                speed=speed, 
            #                                emotion=emotion,
            #                                split_sentences=split_sentences), format='audio/wav')


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

                with st.spinner('Preparing the model...'):
                    tts = load_tts_model()
                    gpt_cond_latent, speaker_embedding = get_tts_latents(tts, selected_voice=selected_voice)

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