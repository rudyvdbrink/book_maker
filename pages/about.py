
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
st.sidebar.page_link(page="https://github.com/rudyvdbrink/book_maker", label="Code")
st.sidebar.page_link(page="https://ruudvandenbrink.net/", label="About author")

# %% layout

spacer1, col1, spacer2, = st.columns([2, 3, 2])

# %% content

with col1:
    st.markdown("""

    ### About BookMaker

    **BookMaker** is an application that lets you turn e-Books into audio books. It's primarily intended to make literature more accessible to people with reading disabilities. But you're of course also welcome to use it if you simply prefer listening over reading.

    You can choose between a number of standard voices, or use a custom voice. Support for 17 different languages is included, though it tends to work best for English text. There are also various options to modify speech, such as the speaker speed. 

    The app uses [XTTS V2](https://huggingface.co/coqui/XTTS-v2) text to speech, as the underlying model. Text is split up into parts before generating audio to keep the memory load low. You may thus notice the tone vary between sentences from time to time. Very long sentences are broken down further, so the app will work better for literature with relatively shorter sentences.

    Ideally, you would run this code on a machine with a CUDA-enabled GPU. The code is written device agnostically, so should run even when there is no GPU available. In that case, run time may be on the slow side. 
                
                """)

    #show audio player to play ./pages/about.wav
    st.audio('./pages/about.wav', format='audio/wav')