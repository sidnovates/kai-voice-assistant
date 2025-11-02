import pyautogui
from speak import speak
import os

def basic_commands(action_no):
    if action_no == 1:
        pyautogui.scroll(500)
        speak("Scrolling down")
    elif action_no == 2:
        pyautogui.scroll(-500)
        speak("Scrolling up")
    elif action_no == 3:
        pyautogui.press("space")
        speak("Pausing")
    elif action_no == 4:
        pyautogui.press("playpause")
        speak("Starting")
    elif action_no == 5:
        pyautogui.press("backspace")
        speak("Going back")
    elif action_no == 6:
        pyautogui.press("pageup")
        speak("Moving page up")
    elif action_no == 7:
        pyautogui.press("pagedown")
        speak("Moving page down")
    elif action_no == 8:
        pyautogui.press("esc")
        speak("Pressing escape")
    elif action_no == 9:
        pyautogui.press("enter")
    elif action_no == 10:     # Close Tab (Ctrl + W)
        pyautogui.hotkey('ctrl', 'w')

    elif action_no == 11:     # New Tab (Ctrl + T)
        pyautogui.hotkey('ctrl', 't')

    elif action_no == 12:     # Close Window (Alt + F4)
        pyautogui.hotkey('alt', 'f4')

    elif action_no == 13:     # Minimize Window (Win + Down)
        pyautogui.hotkey('win', 'down')

    elif action_no == 14:     # Maximize Window (Win + Up)
        pyautogui.hotkey('win', 'up')

    elif action_no == 15:     # Switch Tab (Ctrl + Tab)
        pyautogui.hotkey('ctrl', 'tab')

    elif action_no == 16:     # Switch Window (Alt + Tab)
        pyautogui.hotkey('alt', 'tab')

    elif action_no == 17:     # Volume Up
        pyautogui.press('volumeup')

    elif action_no == 18:     # Volume Down
        pyautogui.press('volumedown')

    elif action_no == 19:     # Mute
        pyautogui.press('volumemute')

    elif action_no == 20:     # Unmute (press volumeup as workaround)
        pyautogui.press('volumeup')

    elif action_no == 21:     # Shutdown
        os.system("shutdown /s /t 1")  # Windows only

    elif action_no == 22:     # Restart
        os.system("shutdown /r /t 1")  # Windows only

    elif action_no == 23:     # Lock Screen
        os.system("rundll32.exe user32.dll,LockWorkStation")  # Windows only

    elif action_no == 24:     # Sleep (requires privileges)
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    elif action_no == 25:     # Open Task Manager
        pyautogui.hotkey('ctrl', 'shift', 'esc')

    elif action_no == 26:     # Take Screenshot
        pyautogui.screenshot("screenshot.png")
        print("Screenshot saved as screenshot.png")

    elif action_no == 27:     # Open File Explorer
        pyautogui.hotkey('win', 'e')

    else:
        print("Unknown action number.")
