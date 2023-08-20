#!/usr/bin/env python

import re
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import json

def extract_track_id(link):
    match = re.search(r'/([a-zA-Z0-9]+)\?', link)
    if match:
        return match.group(1)
    return None

reader = SimpleMFRC522()

try:
    print("Waiting for you to scan an RFID sticker/card")
    id = reader.read()[0]
    print("The ID for this card is:", id)
    
    spotify_link = input("Please enter the Spotify link for this card: ")
    track_id = extract_track_id(spotify_link)
    
    if track_id:
        track_type = None
        if "track" in spotify_link:
            track_type = "track"
        elif "album" in spotify_link:
            track_type = "album"
        elif "playlist" in spotify_link:
            track_type = "playlist"
        
        if track_type:
            data = {}
            try:
                with open("rfid_data.json", "r") as json_file:
                    data = json.load(json_file)
            except FileNotFoundError:
                pass

            data[str(id)] = {"track_id": track_id, "track_type": track_type}

            with open("rfid_data.json", "w") as json_file:
                json.dump(data, json_file)
                print("Data saved to rfid_data.json")
        else:
            print("Invalid Spotify link type")
    else:
        print("Invalid Spotify link format")
        
finally:
    GPIO.cleanup()
