## This file is used to speak the text

import pyttsx3

# Initialize recognizer and tts engine safely
engine = None
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)  # 0 = male, 1 = female (depends on OS)
    engine.setProperty('rate', 200)
except Exception as e:
    print(f"Warning: TTS Engine initialization skipped ({e}). Running in silent/console mode.")

def speak(text):
    if isinstance(text, (list, tuple)):
        clean_text = " ".join(str(item) for item in text)
    else:
        clean_text = str(text)
    print("Kai:", clean_text)
    if engine:
        try:
            engine.say(clean_text)
            engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")