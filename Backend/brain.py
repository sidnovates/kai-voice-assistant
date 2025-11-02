import os
from Personal.config import GOOGLE_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from speak import speak
import pyautogui ##Use for taking control of mouse and keyboard
from loggedin_apps.whatsapp import message, voice_call, video_call
import time
from typing import Annotated
from typing_extensions import TypedDict

from loggedin_apps.site import open_site
import difflib
import loggedin_apps.spotify as spfun
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)


#################
##This is used to classify the original prompt given by user to identify whether the user wants to make a call, or play a song in spotify or open a site or do some keyboard related stuff or just chit-chat with ai
prompt_refine = ChatPromptTemplate.from_messages([
    ("system", "You are an intelligent assistant who analysis the prompt and classifies it based on the action and assigns a number.Now if the user wants to just chit-chat with the assistant then check the prompt if there are any meaningless words.If the user wants perform a specific action like 'open a site' or 'play a music', then give the number according to below:\n1.If the user wants to send a message or video or voice call a person then output is '1',if asked to open a site then '2', if user asks to play a music or any music related stuff like 'stop the music' or 'play next track' and no specific site or anything is mentioned then '3', if asked for some specific commands to be performed screen-related or keyboard related like increase the volume or move the page down or any such stuff then '4' and if the user just wants to chit-chat then return '5'"),
    ("human", "{input}")
])


# prompt_refine = ChatPromptTemplate.from_messages([
#     ("system", "You are an intelligent assistant who analysis the prompt and classifies it based on the action and assigns a number.Now if the user wants to just chit-chat with the assistant then check the prompt if there are any meaningless words.If the user wants perform a specific action like 'open a site' or 'play a music', then give the number according to below:\n1.If the user wants to send a message or video or voice call a person then output is '1',if asked to open a site then '2', if user asks to play a music or any music related stuff like 'stop the music' or 'play next track' and no specific site or anything is mentioned then '3',if just chit-chat random talk then  refines the prompt without changing any sentence formation nor its meaning ."),
#     ("human", "{input}")
# ])

def prompt_refiner(command):
    chain = prompt_refine |llm
    response = chain.invoke({"input":command})
    return response.content

#################

# ##This is used for simple chatting purpose

prompt_chat = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant with real emotions who understands others feelings and loves to chit-chat.Also don't make it too long that it becomes boring to listen to."),
    ("human", "{input}")
])

def chat(command):
    chain = prompt_chat |llm
    response = chain.invoke({"input" :command})
    return response.content


###################

class CommandList(TypedDict):

    '''You are a smart command interpreter. Your job is to analyze natural language input from the user and convert it into specific system-level actions.

    The user may say commands like "scroll down", "press escape", "go back", "move the page up", "pause", etc. You must identify each intended action and return a list of corresponding action numbers.

    Use the following mappings:
    - 1 → "scroll down"
    - 2 → "scroll up"
    - 3 → "pause" or "press space"
    - 4 → "start", "resume", or "play"  
    - 5 → "go back" or "backspace"
    - 6 → "move page up" or "page up"
    - 7 → "move page down" or "page down"
    - 8 → "press escape" or "escape"
    - 9 → "press enter" or "enter"
    - 10 → "close tab"
    - 11 → "new tab"
    - 12 → "close window"
    - 13 → "minimize window"
    - 14 → "maximize window"
    - 15 → "switch tab"
    - 16 → "switch window"
    - 17 → "volume up"
    - 18 → "volume down"
    - 19 → "mute"
    - 20 → "unmute"
    - 21 → "shutdown"
    - 22 → "restart"
    - 23 → "lock screen"
    - 24 → "sleep"
    - 25 → "open task manager"
    - 26 → "take screenshot"
    - 27 → "open file explorer"

    If none of the user's input matches the above commands, return an empty list.

    Example:
    - Input: "scroll down and then pause" → commands = [1, 3]
    - Input: "move page down and scroll up" → commands = [7, 2]
    - Input: "say hi" → commands = []

    Only return action numbers in the order they appear in the user's input.
    Do not explain or add anything extra.
    '''
    commands: Annotated[list[int], "List of action numbers in order of user's request"]


def command_refiner(command):
    try:
        structured_llm = llm.with_structured_output(CommandList)
        response = structured_llm.invoke(command)
        return response['commands']
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't understand the command properly.")
        return []

##################
class SiteLink(TypedDict):
    """ You are an intelligent and helpful assistant. You will be given a statement and in that statement you have to identify the specific site asked for and give its full url like for youtube give "https://youtube.com" .Also what to search for in that site is also asked for so think clearly and add the part to be searched in 'search'.In the 'search' part if something is wrong according to you, then use your own thinking and give meaningful 'search'.Also give some fun,witty or themed reaction to the site.\n Output should be in the following format:"""

    url: Annotated[str,"Give me URL of the site asked for"]
    search:Annotated[str,"Give me the search query like if asked 'play Hindi songs' in youtube then give 'Hindi songs' only"]
    reaction: Annotated[str,"Some reaction related to the site so that I can show it to the user"]

def siteUrl(command):
    try:
        structured_llm=llm.with_structured_output(SiteLink)
        response = structured_llm.invoke(command)
        return response
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't find the site link for the given command.")

#############

class Whatsapp(TypedDict):
    """You are an intelligent assistant that interprets the user's prompt carefully and extracts three things:

        1. The **contact name** the user wants to interact with.  
        - Example: if the user says 'call Ima' or 'send a message to Rahul', extract 'Ima' or 'Rahul' as the contact.

        2. The **intended action**, based on the user's input:
        - If the user is trying to **send a message**, set:  
            action: 1  
        - If the user wants to make a **voice call**, set:  
            action: 2  
        - If the user wants to make a **video call**, set:  
            action: 3  
        - If the prompt is unclear or vague, assume a **normal voice call** (action: 2).

        3. The **message content**, only if the action is 1 (i.e., sending a message). Otherwise, keep it as an empty string.

        Return the result in the following format:"""
    contact: Annotated[str, "Contact name extracted from the user's prompt"]
    action: Annotated[int, "1 for sending message, 2 for voice call, 3 for video call"]
    message: Annotated[str, "Message content if action is 1, otherwise empty string"]



def whatsapp(command):
    try:
        structured_llm=llm.with_structured_output(Whatsapp)
        response = structured_llm.invoke(command)
        return response
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't find the contact for the given command.")

###################
class Spotify(TypedDict):

    """You are a smart assistant that analyzes the user's input and returns the appropriate information needed to play music on Spotify.Also if you think something is wrong with input then do some thinking and give meaningful output.For your record I mainly listen to Hindi songs only. 

    Your main goal is to extract relevant song, artist, or album information from the input and determine the correct action to take.

    For example:
    - If the input is "play arijit qaafirana", the output should be:  
    song: "qaafirana kedarnath", action: 1
    - If the input is "play album moosetape", then:  
    album: "moosetape", action: 2
    - If the input is "play songs by arijit singh", then:  
    artist: "arijit singh", action: 3
    - If the input is "play my liked songs", then:  
    action: 4

    You mainly listen to Hindi songs, so prioritize results accordingly. If something is unclear or incorrect in the input, make a smart guess and give meaningful output.

    Rules:
    - If it's a **single song** → action = 1 → fill 'song', leave others empty.
    - If it's an **album** → action = 2 → fill 'album', leave others empty.
    - If it's an **artist** → action = 3 → fill 'artist', leave others empty.
    - If it's **liked songs** → action = 4 → leave all fields empty.
    - If it's **general "play music"** → action = 5 → leave all fields empty.
    - If it's **pause music** → action = 6 → leave all fields empty.
    - If it's **next track** → action = 7 → leave all fields empty.
    - If it's **previous track** → action = 8 → leave all fields empty.

    Expected Output Format (always follow this structure):\n"""
    song: Annotated[str, "Give me the song name to be searched in Spotify"]
    artist: Annotated[str, "Give me the artist name of the song to be searched in Spotify"]
    album: Annotated[str, "Give me the album name of the song to be searched in Spotify"]
    action: Annotated[int, "1: play song, 2: play album, 3: play artist, 4: play liked songs, 5: play music, 6: pause music, 7: next track, 8: previous track"]

    

def spotify(command):
    try:
        structured_llm=llm.with_structured_output(Spotify)
        response = structured_llm.invoke(command)
        return response
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't find the song for the given command.")

def handle_command(command):
    if(command==""):
        speak("No command Provided.")
    else:
        refine=prompt_refiner(command)
        print("Refined Version: ",refine)
        # if "whatsapp" in command:
        if refine=='1':
            reply = whatsapp(command)
            print(reply)
            try:


                if reply is not None:
                    # Load contacts with their image paths
                    contact_images = {}
                    with open("Personal/contacts.txt", "r") as f:
                        for line in f:
                            if ":" in line:
                                name, path = line.strip().split(":")
                                contact_images[name.lower()] = path

                    # Get list of contact names
                    contacts = list(contact_images.keys())
                    print(contacts)
                    # Find the closest match
                    close_match = difflib.get_close_matches(reply['contact'].lower(), contacts, n=1, cutoff=0.6)
                    
                    if close_match:
                        reply['contact'] = close_match[0]
                        reply['image_path'] = contact_images[close_match[0]]
                        print(reply)
                    else:
                        print("No close match found for contact.")

            except Exception as e:
                print(e)
            if reply is not None and reply['action']==1:
                message(reply['contact'],reply['message'],reply['image_path'])
            elif  reply is not None and reply['action']==2:
                video_call(reply['contact'],reply['image_path'])
            elif reply is not None and reply['action']==3:
                voice_call(reply['contact'],reply['image_path'])
        
        # elif "spotify" in command:
        elif refine=='3':
            reply = spotify(command)
            print(reply)
            if reply is not None:
                try:

                    if(reply['action']==1):
                        spfun.search_song(reply['song'])
                    elif (reply['action']==2):
                        spfun.search_album(reply['album'])
                    elif (reply['action']==3):
                        spfun.search_artist(reply['artist'])
                    elif (reply['action']==4):
                        spfun.play_liked_songs()
                    elif (reply['action']==5):
                        spfun.play()
                    elif (reply['action']==6):
                        spfun.pause()
                    elif (reply['action']==7):
                        spfun.next_track()
                    elif (reply['action']==8):
                        spfun.previous_track()
                    else:
                        speak("Sorry, I couldn't understand song for the given command.")
                except Exception as e:
                    print(e)
                    speak("Sorry, I couldn't play the song for the given command.")
                
        # elif "open".lower() in command:
        elif refine=='2':
            reply = siteUrl(command)
            if reply is not None:
                print(reply)
                reaction = reply.get('reaction')
                if reaction:
                    speak(reply['reaction'])
                try:
                    open_site(reply['url'],reply['search'])
                except Exception as e:
                    print(e)
                    speak("Sorry, I couldn't open the site for the given command.")

        elif refine=='4':
            reply = command_refiner(command)
            print(reply)
            for i in reply:
                print(i)
                from basic_commands import basic_commands
                basic_commands(i)

        else:
            reply=chat(command)
            # reply = "Can you repeat please!"
            speak(reply)
        

