# %%

def options_text():
    return """ 
    **Help on voice options:**   

    ***Voice Speed:*** This controls the speed of the speaker, where 1 is default speed, 0.5 is half, and 2 is double.
                
    ***Temperature:*** Controls the randomness of the output. Lower values make the model more deterministic, while higher values make it more creative.

    ***Length penalty:*** This parameter controls the length of the output. Lower values make the output shorter, while higher values make it longer.

    ***Max chunk length:*** This controls the maximum length of the audio chunks. This is useful to prevent memory errors.

    ***Repetition penalty:*** This parameter controls the amount of repetition in the output. Lower values make the output less repetitive.

    ***Top k:*** This parameter controls the number of words to consider for each step of the generation process. Lower values make the output more deterministic.

    ***Top p:*** This parameter controls the probability mass to consider for each step of the generation process. Lower values make the output more deterministic.

    ***Number of beams:*** This parameter controls the number of beams to use for beam search. Higher values make the output more diverse.

    ***Split sentences:*** This parameter controls whether to split the input text into sentences before generating audio. This is useful for long texts with complex sentence structures. It functions in addition to the maximum chunk length.
    """
    