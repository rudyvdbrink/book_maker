
import streamlit as st

# %% logo

st.sidebar.image('./figures/logo.png', width=250)  # Set the desired width in pixels

# %% Side bar

#create a sidebar with options for navigation
st.sidebar.title('Navigation')
st.sidebar.page_link(page="app.py", label="Home")
st.sidebar.page_link(page="pages/about.py", label="About")

#links out
st.sidebar.title('Resources')
st.sidebar.page_link(page="https://github.com/rudyvdbrink/ISIC_skin_lesions_prediciton", label="Code")
st.sidebar.page_link(page="https://ruudvandenbrink.net/", label="About author")

# %% layout

spacer1, col1, spacer2, = st.columns([2, 3, 2])

# %% content

with col1:
    st.markdown("""

    ### About BookMaker

    This app is meant to make literature more accessible to people with reading disabilities. Reading can be taxing, and listening can alleviate some of this load. Of course, you can also use it if you simply prefer listening over reading.

    The app uses [XTTS V2](https://huggingface.co/coqui/XTTS-v2) text to speech with voice cloning as the underlying model. Text is split up into sentences before generating audio to keep the memory load low. You may thus notice the tone vary between sentences from time to time. Very long sentences are broken down further, so the app will work better for (usually more modern) literature with relatively shorter sentences.             
    """)

    #show audio player to play ./pages/about.wav
    st.audio('./pages/about.wav', format='audio/wav')