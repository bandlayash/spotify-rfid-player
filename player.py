#!/usr/bin/env python

from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import json

DEVICE_ID = "YOUR_DEVICE_ID"
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"

def load_data(filename):
    try:
        with open(filename, "r") as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        return {}

def main():
    try:
        reader = SimpleMFRC522()
        
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                       client_secret=CLIENT_SECRET,
                                                       redirect_uri="http://localhost:8080",
                                                       scope="user-read-playback-state,user-modify-playback-state"))
        
        data = load_data("rfid_data.json")

        while True:
            print("Waiting for record scan...")
            id = reader.read()[0]
            print("Card Value is:", id)
            sp.transfer_playback(device_id=DEVICE_ID, force_play=False)

            track_info = data.get(str(id))
            if track_info:
                track_id = track_info.get("track_id")
                track_type = track_info.get("track_type")
                
                if track_id and track_type:
                    if track_type == "track":
                        sp.start_playback(device_id=DEVICE_ID, uris=[f'spotify:track:{track_id}'])
                    elif track_type == "album":
                        sp.start_playback(device_id=DEVICE_ID, context_uri=f'spotify:album:{track_id}')
                    elif track_type == "playlist":
                        sp.start_playback(device_id=DEVICE_ID, context_uri=f'spotify:playlist:{track_id}')
                    sleep(2)
                else:
                    print("Invalid track information for this card.")
            else:
                print("No track found for this card.")

    except Exception as e:
        print(e)
        pass

    finally:
        print("Cleaning up...")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
