##Using pvporcupine for wake word detection

import pvporcupine
import pyaudio
import struct
import os
import glob # <-- Import glob to find files
import sys  # <-- Import sys to exit on error
from Personal.config import ACCESS_KEY

# Path to the directory containing the .ppn file
WAKE_WORD_DIR = "Wake Word/"

def get_keyword_path():
    """Finds and validates the .ppn file in the Wake Word directory."""
    
    # Look for any file ending in .ppn in the directory
    pattern = os.path.join(WAKE_WORD_DIR, "*.ppn")
    keyword_files = glob.glob(pattern)

    # --- Error Handling ---
    if len(keyword_files) == 0:
        print(f"❌ FATAL ERROR: No .ppn wake word file found in '{WAKE_WORD_DIR}'.")
        print("---")
        print("To fix this:")
        print("1. Go to https://console.picovoice.ai/")
        print("2. Create a custom wake word (e.g., 'Arise Kai').")
        print(f"3. Download the '.ppn' file for 'Windows'.")
        print(f"4. Place that single file inside the '{WAKE_WORD_DIR}' folder.")
        print("---")
        sys.exit(1) # Force exit the program
    
    if len(keyword_files) > 1:
        print(f"⚠️ WARNING: Multiple .ppn files found in '{WAKE_WORD_DIR}'.")
        print(f"Using the first one: {os.path.basename(keyword_files[0])}")
    
    # Return the path as a list, which Porcupine expects
    return [keyword_files[0]]


def detect_wake_word():
    
    keyword_paths = get_keyword_path() # This will exit if it fails
    
    # Dynamically get the name for the console message
    wake_word_name = os.path.basename(keyword_paths[0]).split('_')[0] 
    print(f"🔇 Waiting for '{wake_word_name}'...")

    porcupine = None
    pa = None
    audio_stream = None

    try:
        porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            keyword_paths=keyword_paths # <-- Use the dynamic path
        )

        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)

            result = porcupine.process(pcm_unpacked)

            if result >= 0:
                print("🎤 Wake word detected!")
                return True

    except KeyboardInterrupt:
        print("🛑 Stopped listening.")
        return False # Return False to stop the main loop if needed
    except Exception as e:
        print(f"An error occurred with Porcupine: {e}")
        return False
    finally:
        if audio_stream:
            audio_stream.stop_stream()
            audio_stream.close()
        if pa:
            pa.terminate()
        if porcupine:
            porcupine.delete()
    
    return False
