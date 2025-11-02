## This file is used to listen to commands

import speech_recognition as sr
from speak import speak

#initialize recognizer
r = sr.Recognizer()
r.pause_threshold = 1
r.energy_threshold = 100 ##IF the energy is less than 300, it will not listen
r.dynamic_energy_threshold = True ## Adjusts the energy threshold dynamically


def listen():

    # Get mic input
    with sr.Microphone() as source:
        print(" Say something...")
        speak("Speak..")
        #  Start timing for listening
        # listen_start = time.time()
        audio = r.listen(source,timeout=None, phrase_time_limit=None)
        
        # listen_end = time.time()
        # print(f" Listening time: {listen_end - listen_start:.2f} seconds")

    try:
        #  Start timing for transcription
        # transcribe_start = time.time()

        ##Made changes in faster_whisper.py file to fit compute_type
        # Use Faster Whisper with batching
        text = r.recognize_faster_whisper(audio,language="en")
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