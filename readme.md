# Kai Voice Assistant

Kai is a personalized, offline-first voice assistant for Windows. It uses a local wake word ("Arise Kai") and high-quality local speech-to-text to understand commands, which are then processed by a generative AI (Gemini) to perform a wide range of tasks.

This project is built with a modern, modular architecture that separates listening, understanding (intent classification), and acting, and features a Three.js-powered animated frontend.

## Features

* **Animated Frontend:** A floating, clickable orb powered by Electron and Three.js.
* **Local Wake Word:** Powered by `pvporcupine` for a fast, efficient "Arise Kai" detection.
* **High-Quality STT:** Uses `faster-whisper` for accurate, local speech-to-text.
* **LLM-Powered Brain:** Uses Google's Gemini model (via `langchain`) to:
    1.  **Classify Intent:** Determine if you want to chat, open a site, play music, or control the system.
    2.  **Extract Entities:** Pull out the specific details, like "Spotify," "Rahul," or "scroll down."
* **Background Music-Aware:** Automatically detects and pauses background music (e.g., on Spotify) when activated, and resumes it on "goodbye."
* **Rich Integrations:**
    * **Spotify:** Full control via the Spotipy API to play songs, artists, albums, and liked songs.
    * **Web:** Opens and searches websites (YouTube, Google, Amazon, Wikipedia, etc.).
    * **System:** Controls basic OS functions like volume, scrolling, window management, and even shutdown/restart.
    * **WhatsApp:** (Experimental) Can send messages and initiate calls via GUI automation.

## Project Structure

* **Kai-Voice-Assistant/** (Root Directory)
    * **frontend/**
        * **floating_mic/**: Electron/Three.js frontend
            * `index.html`
            * `main.js`: Electron main process
            * `preload.js`
            * `package.json`
    * **Backend/**
        * `main.py`: Main loop: detects wake word, orchestrates tasks
        * `brain.py`: Core logic: classifies intent and extracts entities using LLM
        * `wake_word.py`: Handles "Arise Kai" detection
        * `listen.py`: Records audio and transcribes
        * `speak.py`: Handles text-to-speech (TTS)
        * `bg_sound.py`: Detects and pauses/plays background music
        * `basic_commands.py`: Executes system-level commands
        * `requirements.txt`: All Python dependencies
        * **loggedin_apps/**
            * `site.py`: Handles opening/searching websites
            * `spotify.py`: Handles all Spotify API interactions
            * `whatsapp.py`: Handles WhatsApp GUI automation
        * **Personal/** (Ignored by Git)
            * `config.py`: Stores all API keys
            * `contacts.txt`: Stores contact information
        * **assets/** (Ignored by Git)
            * **whatsapp/**: PNG assets for GUI automation
    * **Wake Word/** (Ignored by Git - *Assuming this is in root*)
        * `Arise-Kai...ppn`: Porcupine wake word file
    * `.gitignore`: Tells Git which files to ignore

## Setup & Installation

This project is built for a **Windows** environment and requires setup for *both* the backend and frontend.

### 1. Clone the Repository
```bash
git clone [https://github.com/YourUsername/Kai-Voice-Assistant.git](https://github.com/YourUsername/Kai-Voice-Assistant.git)
cd Kai-Voice-Assistant