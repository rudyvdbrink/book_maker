# %%

import subprocess

# %%

command = "python.exe main.py ./epub/test.epub ./test --tts edge --no_prompt"

#edge-tts --list-voices

# Name: en-GB-LibbyNeural
# Gender: Female

# Name: en-GB-MaisieNeural
# Gender: Female

# Name: en-GB-SoniaNeural
# Gender: Female

settings = " --voice_rate=-15% --voice_volume=-20% --voice_name=en-GB-LibbyNeural" 

def convert_epub(infile,settings):

    command = "python.exe main.py " + infile + " ./test --tts edge --no_prompt"

    # Run the command using subprocess
    result = subprocess.run(command + settings, 
                            shell=True, 
                            check=True, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            text=True)
