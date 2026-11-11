import spotipy
from spotipy.oauth2 import SpotifyOAuth
import subprocess
import os
import pygetwindow as gw
try:
    from Personal.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, DEVICE_NAME
except ImportError:
    SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", "")
    SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", "")
    SPOTIFY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:9090")
    DEVICE_NAME = os.environ.get("DEVICE_NAME", "")
default_spotify = os.path.join(os.environ.get("APPDATA", ""), "Spotify", "Spotify.exe")
spotify_path = default_spotify if os.path.exists(default_spotify) else "C:/Users/Siddharth/AppData/Roaming/Spotify/Spotify.exe"
# import psutil ## Time taking is longer using psutil
import time
from speak import speak
## Lazy Spotify initialization (prevents blocking on import if keys are not set)
class LazySpotify:
    _instance = None

    def __getattr__(self, name):
        if self._instance is None:
            if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
                raise ValueError("Spotify credentials not configured in Personal/config.py")
            self._instance = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET,
                redirect_uri=SPOTIFY_REDIRECT_URI,
                scope="user-read-playback-state,user-modify-playback-state,user-library-read,user-read-currently-playing",
                open_browser=False
            ))
        return getattr(self._instance, name)

sp = LazySpotify()

def get_device_info():
        devices_info = sp.devices()
        # speak(devices_info)
        # Iterate through devices
        for device in devices_info['devices']:
            if device['name'] == DEVICE_NAME :  # Match by device name
                device_id = device['id']
                break
        else:
            speak("❌ No matching device found.")
            return
        return device_id

def check_open():
    ##Time taken by this method = 2.01634
    # is_open=False
    # for proc in psutil.process_iter(['name']):
    #         speak(proc.info['name'])
    #         if proc.info['name'] == "Spotify.exe":
    #             is_open= True
        #             break
        result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq Spotify.exe"],capture_output=True, text=True)
        if ("Spotify.exe" not in result.stdout): ##Time taken= 1.376642 s
            subprocess.Popen(spotify_path)
        for window in gw.getWindowsWithTitle('Spotify'):
            window.minimize()
        time.sleep(1.5)
        return get_device_info()

# Search for the song
def search_song(query):
    device_id=check_open()
    results = sp.search(query, type="track", limit=1)
    tracks = results.get("tracks", {}).get("items", [])
    if not tracks:
        speak("Sorry, I couldn't find that song on Spotify.")
        return
    track = tracks[0]
    uri = track["uri"]
    artist_name = track["artists"][0]["name"] if track.get("artists") else "Unknown Artist"
    speak(f"Found: {track['name']} by {artist_name}")
    # Start playing (make sure Spotify app is running & a device is active)
    sp.start_playback(device_id=device_id,uris=[uri])

# Get the first 50 liked songs
def play_liked_songs():
    device_id=check_open()
    sp.shuffle(state=True, device_id=device_id)
    # Get the first 50 liked songs
    results = sp.current_user_saved_tracks(limit=50)
    uris = [item['track']['uri'] for item in results['items']]

    if uris:
        speak(f"Playing your liked songs (showing top {len(uris)})...")
        sp.start_playback(device_id=device_id,uris=uris)
    else:
        speak("No liked songs found.")

def play():
    device_id=get_device_info()
    sp.start_playback(device_id=device_id)

def pause():
    device_id=get_device_info()
    sp.pause_playback(device_id=device_id)

def next_track():
    device_id=get_device_info()
    sp.next_track(device_id=device_id)

def previous_track():
    device_id=get_device_info()
    sp.previous_track(device_id=device_id)

def get_current_track():
    playback = sp.current_playback()
    if playback and playback['is_playing']:
        track = playback['item']
        speak(f"Now playing: {track['name']} - {track['artists'][0]['name']}")
    else:
        speak("Nothing is playing right now.")

def search_album(album_name):
    device_id=check_open()
    results = sp.search(q=album_name, type='album', limit=1)
    items = results.get('albums', {}).get('items', [])
    if items:
        album_uri = items[0]['uri']
        sp.start_playback(device_id=device_id, context_uri=album_uri)
        speak(f"Playing album: {items[0]['name']}")
    else:
        speak("Album not found.")

def search_artist(artist_name):
    device_id=check_open()
    results = sp.search(q=artist_name, type='artist', limit=1)
    items = results.get('artists', {}).get('items', [])
    if items:
        artist_uri = items[0]['uri']
        sp.start_playback(device_id=device_id, context_uri=artist_uri)
        speak(f"Playing songs by: {items[0]['name']}")
    else:
        speak("Artist not found.")


