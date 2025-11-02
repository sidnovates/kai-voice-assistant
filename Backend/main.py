from wake_word import detect_wake_word
from speak import speak
from listen import listen
# from llm_commands import handle_command
from brain import handle_command
import random
import pyautogui

while True:
    if detect_wake_word():
        print("Wake word detected")
        responses=  [
            "Yo. I'm here. What's the vibe today?",
            "Kai's up. Let's roll, Commander.",
            "I'm here. What's the vibe today?",
            "Greetings. Your semi-intelligent assistant has arrived.",
            "Okay okay, I'm awake. What now?"
        ]

        speak(random.choice(responses))
        while True:
            from bg_sound import check_bg_music
            count=check_bg_music()
            command=listen()
            if "goodbye" in command.lower() or "bye" in command.lower():
                speak("Goodbye to you too. See you later!")
                if count:##If earlier any song was playing then play it
                    pyautogui.press('playpause')
                break
            elif "exit" in command.lower():
                speak("You're welcome!")
                if count:##If earlier any song was playing then play it
                    pyautogui.press('playpause')
                exit()
            else:
                reply = handle_command(command.lower())


