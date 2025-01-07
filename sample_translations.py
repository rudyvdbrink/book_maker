# %% functions to translate the default sample text

def translate_voice_name(selected_voice='Bert',language='en'):

    if selected_voice == 'Bert':
        if language == 'en':
            pass
        elif language == 'es':
            selected_voice = 'Alberto'
        elif language == 'fr':
            selected_voice = 'Albert'
        elif language == 'de':
            selected_voice = 'Albert'
        elif language == 'it':
            selected_voice = 'Alberto'
        elif language == 'pt':
            selected_voice = 'Alberto'
        elif language == 'pl':
            selected_voice = 'Albert'
        elif language == 'tr':
            selected_voice = 'Bertan'
        elif language == 'ru':
            selected_voice = 'Альберт'  # Albert in Cyrillic
        elif language == 'nl':
            selected_voice = 'Bert'
        elif language == 'cs':
            selected_voice = 'Albert'
        elif language == 'ar':
            selected_voice = 'ألبيرت'  # Albert in Arabic
        elif language == 'zh-cn':
            selected_voice = '阿尔伯特'  # Albert in Chinese
        elif language == 'hu':
            selected_voice = 'Albert'
        elif language == 'ko':
            selected_voice = '알버트'  # Albert in Korean
        elif language == 'ja':
            selected_voice = 'アルバート'  # Albert in Japanese
        elif language == 'hi':
            selected_voice = 'एल्बर्ट'  # Albert in Hindi
    elif selected_voice == 'Gemma':
        if language == 'en':
            pass
        elif language == 'es':
            selected_voice = 'Gemma'
        elif language == 'fr':
            selected_voice = 'Gemma'
        elif language == 'de':
            selected_voice = 'Gemma'
        elif language == 'it':
            selected_voice = 'Gemma'
        elif language == 'pt':
            selected_voice = 'Gemma'
        elif language == 'pl':
            selected_voice = 'Gemma'
        elif language == 'tr':
            selected_voice = 'Gemma'
        elif language == 'ru':
            selected_voice = 'Джема'  # Gemma in Cyrillic
        elif language == 'nl':
            selected_voice = 'Gemma'
        elif language == 'cs':
            selected_voice = 'Gemma'
        elif language == 'ar':
            selected_voice = 'جما'  # Gemma in Arabic
        elif language == 'zh-cn':
            selected_voice = '杰玛'  # Gemma in Chinese
        elif language == 'hu':
            selected_voice = 'Gemma'
        elif language == 'ko':
            selected_voice = '젬마'  # Gemma in Korean
        elif language == 'ja':
            selected_voice = 'ジェンマ'  # Gemma in Japanese
        elif language == 'hi':
            selected_voice = 'जेम्मा'  # Gemma in Hindi
    elif selected_voice == 'Greg':
        if language == 'en':
            pass
        elif language == 'es':
            selected_voice = 'Gregorio'  # Greg in Spanish
        elif language == 'fr':
            selected_voice = 'Grégoire'  # Greg in French
        elif language == 'de':
            selected_voice = 'Gregor'  # Greg in German
        elif language == 'it':
            selected_voice = 'Gregorio'  # Greg in Italian
        elif language == 'pt':
            selected_voice = 'Gregório'  # Greg in Portuguese
        elif language == 'pl':
            selected_voice = 'Grzegorz'  # Greg in Polish
        elif language == 'tr':
            selected_voice = 'Greg'  # Greg is used in Turkish as well
        elif language == 'ru':
            selected_voice = 'Грег'  # Greg in Cyrillic
        elif language == 'nl':
            selected_voice = 'Greg'  # Greg is used in Dutch
        elif language == 'cs':
            selected_voice = 'Greg'  # Greg is used in Czech
        elif language == 'ar':
            selected_voice = 'غريغ'  # Greg in Arabic
        elif language == 'zh-cn':
            selected_voice = '格雷格'  # Greg in Chinese
        elif language == 'hu':
            selected_voice = 'Greg'  # Greg is used in Hungarian
        elif language == 'ko':
            selected_voice = '그렉'  # Greg in Korean
        elif language == 'ja':
            selected_voice = 'グレッグ'  # Greg in Japanese
        elif language == 'hi':
            selected_voice = 'ग्रेग'  # Greg in Hindi
    elif selected_voice == 'Richard':
        if language == 'en':
            pass
        elif language == 'es':
            selected_voice = 'Ricardo'  # Richard in Spanish
        elif language == 'fr':
            selected_voice = 'Richard'  # Richard is used in French
        elif language == 'de':
            selected_voice = 'Richard'  # Richard is used in German
        elif language == 'it':
            selected_voice = 'Riccardo'  # Richard in Italian
        elif language == 'pt':
            selected_voice = 'Ricardo'  # Richard in Portuguese
        elif language == 'pl':
            selected_voice = 'Ryszard'  # Richard in Polish
        elif language == 'tr':
            selected_voice = 'Richard'  # Richard is used in Turkish
        elif language == 'ru':
            selected_voice = 'Ричард'  # Richard in Cyrillic
        elif language == 'nl':
            selected_voice = 'Richard'  # Richard is used in Dutch
        elif language == 'cs':
            selected_voice = 'Richard'  # Richard is used in Czech
        elif language == 'ar':
            selected_voice = 'ريتشارد'  # Richard in Arabic
        elif language == 'zh-cn':
            selected_voice = '理查德'  # Richard in Chinese
        elif language == 'hu':
            selected_voice = 'Richárd'  # Richard in Hungarian
        elif language == 'ko':
            selected_voice = '리차드'  # Richard in Korean
        elif language == 'ja':
            selected_voice = 'リチャード'  # Richard in Japanese
        elif language == 'hi':
            selected_voice = 'रिचर्ड'  # Richard in Hindi
    elif selected_voice == 'Sandy':
        if language == 'en':
            pass
        elif language == 'es':
            selected_voice = 'Sandra'  # Sandy in Spanish
        elif language == 'fr':
            selected_voice = 'Sandy'  # Sandy is used in French
        elif language == 'de':
            selected_voice = 'Sandy'  # Sandy is used in German
        elif language == 'it':
            selected_voice = 'Sandra'  # Sandy in Italian
        elif language == 'pt':
            selected_voice = 'Sandy'  # Sandy is used in Portuguese
        elif language == 'pl':
            selected_voice = 'Sandra'  # Sandy in Polish
        elif language == 'tr':
            selected_voice = 'Sandy'  # Sandy is used in Turkish
        elif language == 'ru':
            selected_voice = 'Сэнди'  # Sandy in Cyrillic
        elif language == 'nl':
            selected_voice = 'Sandy'  # Sandy is used in Dutch
        elif language == 'cs':
            selected_voice = 'Sandy'  # Sandy is used in Czech
        elif language == 'ar':
            selected_voice = 'ساندي'  # Sandy in Arabic
        elif language == 'zh-cn':
            selected_voice = '桑迪'  # Sandy in Chinese
        elif language == 'hu':
            selected_voice = 'Sandy'  # Sandy is used in Hungarian
        elif language == 'ko':
            selected_voice = '샌디'  # Sandy in Korean
        elif language == 'ja':
            selected_voice = 'サンディ'  # Sandy in Japanese
        elif language == 'hi':
            selected_voice = 'सैंडी'  # Sandy in Hindi
    elif selected_voice == 'Sky':
        if language == 'en':
            pass
        elif language == 'es':
            selected_voice = 'Cielo'  # Sky in Spanish
        elif language == 'fr':
            selected_voice = 'Ciel'  # Sky in French
        elif language == 'de':
            selected_voice = 'Skai'  # Sky is used in German
        elif language == 'it':
            selected_voice = 'Sky'  # Sky is used in Italian
        elif language == 'pt':
            selected_voice = 'Céu'  # Sky in Portuguese
        elif language == 'pl':
            selected_voice = 'Sky'  # Sky is used in Polish
        elif language == 'tr':
            selected_voice = 'Sky'  # Sky is used in Turkish
        elif language == 'ru':
            selected_voice = 'Скай'  # Sky in Cyrillic
        elif language == 'nl':
            selected_voice = 'Skai'  # Sky is used in Dutch
        elif language == 'cs':
            selected_voice = 'Sky'  # Sky is used in Czech
        elif language == 'ar':
            selected_voice = 'سماء'  # Sky in Arabic
        elif language == 'zh-cn':
            selected_voice = '天空'  # Sky in Chinese
        elif language == 'hu':
            selected_voice = 'Sky'  # Sky is used in Hungarian
        elif language == 'ko':
            selected_voice = '스카이'  # Sky in Korean
        elif language == 'ja':
            selected_voice = 'スカイ'  # Sky in Japanese
        elif language == 'hi':
            selected_voice = 'आसमान'  # Sky in Hindi

    return selected_voice

def default_sample_text(selected_voice='Bert',language='en'):

    if language == 'en':
         default_text = "Hello, I'm " + selected_voice + ", and I'd be happy to read your books aloud for you."
    elif language == 'es':
        default_text = "Hola, soy " + translate_voice_name(selected_voice,language=language) + ", y estaré encantado de leer tus libros en voz alta para ti."
    elif language == 'fr':
        default_text = "Bonjour, je suis " + translate_voice_name(selected_voice,language=language) + ", et je serais ravi de lire vos livres à haute voix pour vous."
    elif language == 'de':
        default_text = "Hallo, ich bin " + translate_voice_name(selected_voice,language=language) + ", und würde mich freuen, Ihnen Ihre Bücher vorzulesen."
    elif language == 'it':
        default_text = "Ciao, sono " + translate_voice_name(selected_voice,language=language) + ", e sarò felice di leggere i tuoi libri ad alta voce per te."
    elif language == 'pt':
        default_text = "Olá, sou " + translate_voice_name(selected_voice,language=language) + ", e eu ficaria feliz em ler seus livros em voz alta para você."
    elif language == 'pl':
        default_text = "Cześć, jestem " + translate_voice_name(selected_voice,language=language) + ", i z przyjemnością przeczytam dla Ciebie na głos Twoje książki."
    elif language == 'tr':
        default_text = "Merhaba, ben " + translate_voice_name(selected_voice,language=language) + ", ve kitaplarınızı sizin için yüksek sesle okumaktan mutluluk duyarım."
    elif language == 'ru':
        default_text = "Привет, я " + translate_voice_name(selected_voice,language=language) + ", и я был бы рад прочитать вам ваши книги вслух."
    elif language == 'nl':
        default_text = "Hallo, ik ben " + translate_voice_name(selected_voice,language=language) + ", en ik lees uw boeken graag voor u voor."
    elif language == 'cs':
        default_text = "Ahoj, jsem " + translate_voice_name(selected_voice,language=language) + ", a rád bych vám nahlas přečetl vaše knihy."
    elif language == 'ar':
        default_text = "مرحبًا، أنا " + translate_voice_name(selected_voice,language=language) + "، وسأكون سعيدًا بقراءة كتبك بصوت عالٍ لك."
    elif language == 'zh-cn':
        default_text = "你好，我是" + translate_voice_name(selected_voice,language=language) + "，我很高兴为您大声朗读您的书。"
    elif language == 'hu':
        default_text = "Helló, én vagyok " + translate_voice_name(selected_voice,language=language) + ", és szívesen felolvasom Önnek a könyveit."
    elif language == 'ko':
        default_text = "안녕하세요, 저는 " + translate_voice_name(selected_voice,language=language) + "입니다. 책을 읽어 드릴 수 있습니다."
    elif language == 'ja':
        default_text = "こんにちは、私は" + translate_voice_name(selected_voice,language=language) + "です。あなたの本を読み上げるのを楽しみにしています。"
    elif language == 'hi':
        default_text = "नमस्ते, मैं " + translate_voice_name(selected_voice,language=language) + " हूँ, और मैं आपकी किताबें आपके लिए उच्च ध्वनि में पढ़ने के लिए खुश होऊंगा।"
        
    return default_text