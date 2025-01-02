from gtts import gTTS
import os

def speak_text_gTTS(text, lang='en', tld='com'):
    tts = gTTS(text=text, lang=lang, tld=tld)
    filename = "output.mp3"
    
    # Save the converted speech to an MP3 file
    tts.save(filename)
    
    # Play the MP3 file (this works on most systems, use other methods on Windows/macOS if needed)
    os.system(f"mpg123 {filename}")

if __name__ == "__main__":
    # Define available languages and accents
    voices = {
        '1': {'lang': 'en', 'tld': 'com', 'name': 'English (US)'},
        '2': {'lang': 'en', 'tld': 'co.uk', 'name': 'English (UK)'},
        '3': {'lang': 'en', 'tld': 'com.au', 'name': 'English (Australia)'},
        '4': {'lang': 'en', 'tld': 'ca', 'name': 'English (Canada)'},
        '5': {'lang': 'en', 'tld': 'ie', 'name': 'English (Ireland)'},
        '6': {'lang': 'en', 'tld': 'co.in', 'name': 'English (India)'},
        '7': {'lang': 'fr', 'tld': 'fr', 'name': 'French'},
        '8': {'lang': 'es', 'tld': 'es', 'name': 'Spanish'},
        '9': {'lang': 'de', 'tld': 'de', 'name': 'German'},
    }

    # Display available voices
    print("Available voices:")
    for key, value in voices.items():
        print(f"{key}: {value['name']}")

    # Get user choice
    voice_choice = input("Enter the number of the voice you want to use: ")
    voice = voices.get(voice_choice, voices['1'])  # Default to English (US)
    
    # Get user text
    text = input("Enter the text to convert to speech: ")
    
    # Speak using gTTS with selected voice (language/locale)
    speak_text_gTTS(text, lang=voice['lang'], tld=voice['tld'])