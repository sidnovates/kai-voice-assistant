
##TO stop the background music so that pc can listen to the user

from pycaw.pycaw import AudioUtilities, IAudioMeterInformation
from ctypes import POINTER, cast
import time
import pyautogui

def is_audio_playing(threshold=0.01):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.State == 1:  # 1 = active
            volume = session._ctl.QueryInterface(IAudioMeterInformation)
            peak = volume.GetPeakValue()
            if peak > threshold:
                return True
    return False

def check_bg_music():
    if is_audio_playing():
        print("Background audio is playing.")
        pyautogui.press('playpause')
        return True
    else:
        print("No background audio detected.")
        return False