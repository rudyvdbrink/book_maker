# %%

#https://github.com/p0n1/epub_to_audiobook

# https://github.com/rhasspy/piper

# %%
import subprocess

# %%
#text to convert to speech
my_text = 'The quick brown fox jumped over the lazy dog.'

# The command to execute in Git Bash
command = 'edge-tts --rate=-10% --volume=-20% --text "'  + my_text + '" --write-media hello.mp3'

# Run the command using subprocess
result = subprocess.run(command, 
                        shell=True, 
                        check=True, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE, 
                        text=True)


# command = "python.exe main.py ./epub/test.epub ./test --tts edge --no_prompt"

# settings = "--rate=-10% --volume=-20%" 
