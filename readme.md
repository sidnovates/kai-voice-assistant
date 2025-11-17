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
```

### 2. Configure the Backend (Python)

*Note: This guide assumes all your Python code is inside the `Backend/` folder.*

1.  **Create Virtual Environment:**
    ```bash
    cd Backend
    python -m venv venv
    venv\Scripts\activate
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Keys & Personal Files:**
    You must create and configure several files that are *not* on GitHub for security and personalization.

    * **`.gitignore`:** First, ensure the `.gitignore` file (from this repo) exists so you don't accidentally upload your keys.

    * **`Backend/Personal/config.py` (API Keys):**
        Create this file and add your keys:
        ```python
        # Backend/Personal/config.py
        GOOGLE_API_KEY = "Your_Google_AI_Studio_API_Key"
        ACCESS_KEY = "Your_PicoVoice_Access_Key"
        ```

    * **`Wake Word/` (Wake Word File):**
        1.  Go to the [PicoVoice Console](https://console.picovoice.ai/).
        2.  Sign up for a free account (this is required to get your `ACCESS_KEY` and train a wake word).
        3.  Go to the **"Porcupine"** page and create a new custom wake word (e.g., "Arise Kai", "Hey Computer").
        4.  Train and download the model. Select **"Windows"** as the platform.
        5.  This will download a `.zip` file. Unzip it.
        6.  Find the **`.ppn`** file inside (e.g., `Arise-Kai_en_windows_v3_0_0.ppn`).
        7.  Place this single **`.ppn` file** inside the `Wake Word/` folder. The script will now automatically find and use it.

    * **`Backend/Personal/contacts.txt` (WhatsApp Contacts):**
        Create this file and map contact names to their screenshot paths.
        **Format:** `ContactName:path/to/image.png`
        ```
        Rahul:assets/whatsapp/rahul.png
        Mom:assets_old/whatsapp/mom.png
        ```

    * **`Backend/assets/whatsapp/` (WhatsApp GUI Assets):**
        You must take your *own* screenshots of the WhatsApp UI elements (e.g., `search_bar.png`, `call.png`) and all contact images listed in `contacts.txt`.
        *Note: This is very fragile and will break on UI updates or a theme change (Light/Dark mode).*

    * **`Backend/spotify.py` (Spotify Config):**
        * **Device Name:** You must hardcode your Spotify device name in the `get_device_info()` function (e.g., `DESKTOP-FESEIHA`).
        * **App Path:** You may need to update the `spotify_path` variable.
        * **Authentication:** The first time you run it, `spotipy` will open a browser window for you to authenticate.

### 3. Configure the Frontend (Electron)

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend/floating_mic
    ```
2.  **Install Node.js packages:**
    ```bash
    npm install
    ```

## How to Run

1.  **Activate the Python Environment:**
    * Make sure your `venv` is active in one terminal:
        ```bash
        cd Backend
        .\venv\Scripts\activate 
        ```
    *(You only need to activate it. The frontend will start the Python script for you.)*

2.  **Start the Electron App:**
    * In a **separate terminal**, navigate to the frontend directory:
        ```bash
        cd frontend/floating_mic
        ```
    * Run the Electron app:
        ```bash
        npm start
        ```
    * The crystal orb assistant will appear in the bottom-right corner of your screen.

## Using the Assistant

The application is now running, but the voice assistant (backend) is not yet active.

### To Start the Assistant:
1.  **Click the orb once.**
2.  You will see a "light burst" animation.
3.  This action starts the `main.py` backend script. The assistant is now active and listening for its wake word.

### To Stop the Assistant (Two Ways):

* **Option 1: Voice Command (Keops Orb Open)**
    1.  After activating the assistant with the wake word, say **"exit"**.
    2.  The backend script (`main.py`) will stop running (and resume any music that was playing).
    3.  The crystal orb will remain open and return to its idle state.
    4.  You can click it again later to reactivate the backend.

* **Option 2: Mouse Click (Closes Everything)**
    1.  **Click the orb a second time.**
    2.  This action will:
        * Safely stop the backend Python script.
        * Completely close the Electron application (the orb will disappear).