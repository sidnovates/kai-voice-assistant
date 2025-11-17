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

🚀 Backend & Frontend Setup Guide
2. Configure the Backend (Python)

Note: All Python backend files should be inside the Backend/ directory.

1. Create a Virtual Environment
cd Backend
python -m venv venv
venv\Scripts\activate

2. Install Dependencies
pip install -r requirements.txt

3. Add Your Personal Configuration Files

These files are intentionally NOT included in the GitHub repo (for security).
You must create them manually on your system.

🔐 Backend/Personal/config.py (API Keys)

Create this file:

# Backend/Personal/config.py
GOOGLE_API_KEY = "Your_Google_AI_Studio_API_Key"
ACCESS_KEY = "Your_PicoVoice_Access_Key"

🎤 Wake Word Configuration (Wake Word/)

Go to the PicoVoice Console → https://console.picovoice.ai

Create a free account

Open Porcupine → create your custom wake word (e.g., “Arise Kai”)

Train and download the model

Choose Windows platform

Download the .zip → unzip it

Locate the .ppn file (e.g., Arise-Kai_en_windows_v3_0_0.ppn)

Place this single .ppn file inside:

Wake Word/


The backend automatically detects it.

📇 WhatsApp Contacts (Backend/Personal/contacts.txt)

Create this file:

Format:

ContactName:path/to/image.png


Example:

Rahul:assets/whatsapp/rahul.png
Mom:assets_old/whatsapp/mom.png


Make sure the images exist in your assets folder.

🖼️ WhatsApp UI Assets

Inside:

Backend/assets/whatsapp/


Add your own screenshots of:

Search bar

Call button

All contacts (matching contacts.txt)

⚠️ These must match your WhatsApp theme (dark/light), otherwise automation breaks.

🎵 Spotify Setup (Backend/spotify.py)

Inside this file:

Update your Spotify device name inside get_device_info()

Update the Spotify app path if needed

On first run, spotipy will open the browser for authentication

3. Configure the Frontend (Electron)
1. Install Node.js dependencies
cd frontend/floating_mic
npm install

▶️ How to Run the Assistant
1. Activate Python Environment
cd Backend
.\venv\Scripts\activate


You only need to activate it. The frontend will start main.py automatically.

2. Start the Electron App

Open a separate terminal:

cd frontend/floating_mic
npm start


A crystal orb will appear at the bottom-right corner of your screen.

💬 Using the Assistant
Start the Assistant

Click the orb once

A “light burst” animation appears

The backend (main.py) starts

The assistant becomes active & listens for the wake word

🛑 How to Stop the Assistant
Option 1: Voice Command (Assistant Stays Open)

Activate using wake word

Say:
“exit”

Backend stops

Music (if paused) resumes

Orb stays open (idle)

Option 2: Mouse Click (Everything Closes)

Click the orb a second time

This will:

Stop the backend

Close the Electron app completely