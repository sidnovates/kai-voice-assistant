from wake_word import detect_wake_word
from speak import speak
from listen import listen
from brain import handle_command
from bg_sound import check_bg_music
import random
import pyautogui
import re

while True:
    if detect_wake_word():
        print("Wake word detected")
        responses = [
            "Yo. I'm here. What's the vibe today?",
            "Kai's up. Let's roll, Commander.",
            "I'm here. What's the vibe today?",
            "Greetings. Your semi-intelligent assistant has arrived.",
            "Okay okay, I'm awake. What now?"
        ]

        # Check and pause background music once when activated
        music_was_playing = check_bg_music()
        speak(random.choice(responses))

        while True:
            command = listen()
            clean_cmd = command.strip().lower()

            if not clean_cmd:
                continue

            # Check for standalone exit / goodbye intents (avoid matching phrases like 'exit full screen')
            is_goodbye = bool(re.search(r'^(goodbye|bye|bye\s+bye|see\s+you(\s+later)?)(\s+kai)?$', clean_cmd))
            is_exit = bool(re.search(r'^(exit|quit|terminate|close\s+kai|stop\s+kai)$', clean_cmd))

            if is_goodbye:
                speak("Goodbye to you too. See you later!")
                if music_was_playing:
                    pyautogui.press('playpause')
                break
            elif is_exit:
                speak("You're welcome!")
                if music_was_playing:
                    pyautogui.press('playpause')
                exit()
            else:
                try:
                    handle_command(clean_cmd)
                except Exception as e:
                    print(f"Error handling command: {e}")
                    speak("Sorry, I encountered an error while processing that command.")


