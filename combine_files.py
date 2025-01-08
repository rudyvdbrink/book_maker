# %% 

#function to combine audio files into one 
input_directory = './readmesamples/'
input_type = 'wav'

def combine_files(input_directory, input_type):
    import os
    from pydub import AudioSegment

    #get all files in directory
    files = os.listdir(input_directory)
    #filter for only input_type files
    files = [file for file in files if file.endswith(input_type)]

    #combine all files into one
    combined = AudioSegment.from_file(input_directory + files[0])
    for file in files[1:]:
        combined += AudioSegment.from_file(input_directory + file)

        #add half a second silence in between each file
        silence = AudioSegment.silent(duration=500)
        combined = combined + silence

    #export combined file
    combined.export(input_directory + 'combined.wav', format='wav')

# %% example usage

combine_files(input_directory, input_type)