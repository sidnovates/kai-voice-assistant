## This file is used to speak the text

import pyttsx3

# Initialize recognizer and tts engine
engine=pyttsx3.init()

# Optional: Set voice (male/female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 = male, 1 = female (depends on OS)
engine.setProperty('rate', 200)

def speak(text):
    print("Kai:", text)
    engine.say(text)
    engine.runAndWait()