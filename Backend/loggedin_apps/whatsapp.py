import pyautogui
import time
import subprocess
def close_whatsapp():
    pyautogui.hotkey("alt", "f4")

def close_if_open():
    result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq WhatsApp.exe"], capture_output=True, text=True)
    if "WhatsApp.exe" in result.stdout:
           # Kill the process
        subprocess.run(["taskkill", "/F", "/IM", "WhatsApp.exe"])
        time.sleep(1)


def open_whatsapp(contact,path):
    close_if_open()
    pyautogui.press("win")
    pyautogui.write("whatsapp")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(2)
    location=pyautogui.locateCenterOnScreen('assets/whatsapp/search_bar.png', confidence=0.7)
    if location:
        pyautogui.click(location)
    pyautogui.write(contact)
    time.sleep(1)
    location= pyautogui.locateCenterOnScreen(path, confidence=0.7)
    if location:
        pyautogui.click(location)
    time.sleep(3)  


def message(contact,message,path):
    ####
    open_whatsapp(contact,path)
    ####
    
    # location = pyautogui.locateCenterOnScreen('assets/whatsapp/msg_bar.png', confidence=0.7)
    # if location:
    #     print("Search bar found at:", location)
    #     pyautogui.click(location)
    # else:
    #     print("Could not find search bar on the screen.")

    pyautogui.write(message)
    pyautogui.press("enter")
    time.sleep(1)
    close_whatsapp()

def voice_call(contact,path):
    ####
    open_whatsapp(contact,path)
    ####
    location = pyautogui.locateCenterOnScreen('assets/whatsapp/call.png', confidence=0.7)
    if location:
        print("Search bar found at:", location)
        pyautogui.click(location)
    else:
        print("Could not find search bar on the screen.")

def video_call(contact,path):
    ####
    open_whatsapp(contact,path)
    ####

    location = pyautogui.locateCenterOnScreen('assets/whatsapp/video.png', confidence=0.7)
    if location:
        print("Search bar found at:", location)
        pyautogui.click(location)
    else:
        print(" Could not find search bar on the screen.")

