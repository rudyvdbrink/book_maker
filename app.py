# %% libraries
import tempfile
import streamlit as st
import os

# %%

import subprocess

settings = " --voice_rate=-15% --voice_volume=-20% --voice_name=en-GB-LibbyNeural" 

def convert_epub(infile,outfile,settings):

    
    command = 'python.exe main.py "' + infile + '" "' + outfile + '" --tts edge --no_prompt'

    command = 'python.exe main.py "./temp/temp.epub" "' + outfile + '" --tts edge --no_prompt'

    # Run the command using subprocess
    result = subprocess.run(command + settings, 
                            shell=True, 
                            check=True, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            text=True)
    

# %%
# Streamlit page title
st.title("epub file uploader")

# Allow user to upload one or more epub files
uploaded_files = st.file_uploader("Upload epub files", type="epub", accept_multiple_files=True)

# List to hold file paths and names (simulated since Streamlit doesn't provide actual file paths)
file_details = []

#st.write(uploaded_files[0].name)

if uploaded_files:
    for uploaded_file in uploaded_files:
        book_name = uploaded_file.name.split('.epub')[0]
        outfile = './books/' + book_name
        #outfile = './books/temp'

        st.write('working on: ' + book_name)

        with open('./temp/temp.epub', "wb") as f:
            f.write(uploaded_file.getbuffer())

        convert_epub('./.temp/temp.epub', outfile, settings)
        os.remove('./temp/temp.epub')
        st.write('done')




# if uploaded_files:
#     # Create a temporary directory
#     with tempfile.TemporaryDirectory() as temp_dir:
#         for uploaded_file in uploaded_files:
#             # Create a full temporary file path
#             temp_file_path = os.path.join(temp_dir, uploaded_file.name)

#             # Write the uploaded file to the temporary file
#             with open(temp_file_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())

#             # Add the file path and name to the list
#             file_details.append((temp_file_path, uploaded_file.name))

#         # Display the paths and names
#         st.write("Uploaded epub files (saved in temporary folder):")
#         for path, name in file_details:
#             st.write(f"File path: {path}, File name: {name}")

#             convert_epub(path,settings)
