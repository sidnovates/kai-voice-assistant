## This file is used to listen to commands

import speech_recognition as sr
from speak import speak

#initialize recognizer
r = sr.Recognizer()
r.pause_threshold = 1
r.energy_threshold = 100 ##IF the energy is less than 300, it will not listen
r.dynamic_energy_threshold = True ## Adjusts the energy threshold dynamically


def listen():
    print("🎤 Listening... Speak now.")
    # Get mic input
    with sr.Microphone() as source:
        audio = r.listen(source, timeout=None, phrase_time_limit=None)

    try:
        # Check if customized faster-whisper method exists, fallback gracefully
        if hasattr(r, "recognize_faster_whisper"):
            text = r.recognize_faster_whisper(audio, language="en")
        elif hasattr(r, "recognize_whisper"):
            text = r.recognize_whisper(audio, language="en")
        else:
            text = r.recognize_google(audio)
        print("You said:", text)
        return text.lower()
        # transcribe_end = time.time()
        # print(f" Transcription time: {transcribe_end - transcribe_start:.2f} seconds")
        print("You said:", text)
        return text.lower()
    
    except sr.UnknownValueError:
        print("Speech was unintelligible")
        return ""
    
    except sr.RequestError as e:
        print("Recognition error:", e)
        return ""