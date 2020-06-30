import os
import sys
import json
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
import Client

# Get the username from terminal
username = sys.argv[1]
scope = 'user-read-private user-read-playback-state user-modify-playback-state user-library-read'

# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope) # add scope
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope) # add scope

# Create our spotify object with permissions
clientSpotify = Client.Client(spotipy.Spotify(auth=token))
spotifyObject = clientSpotify.getSpotify()
# Get current device
devices = spotifyObject.devices()
selDevice = 0
deviceID = None

if devices['devices'] != []:
    if len(devices['devices']) > 1:
        print("Choose a device: ")
        for i in range(len(devices['devices'])):
            print(i, ". " + devices['devices'][i]['name'] + " - " + devices['devices'][i]['type'])
        while True:
            try:
                selDevice = (int)(input("Number of device: "))
                break
            except ValueError:
                print("Invalid selection...")
    else:
        deviceID = devices['devices'][selDevice]['id']

    clientSpotify.setDevice(deviceID)
    print("\nConnected to: ", devices['devices'][selDevice]['name'])
    # Current track information
    track = spotifyObject.current_user_playing_track()
    if track != None:
        artist = track['item']['artists'][0]['name']
        track = track['item']['name']

        if artist != "":
            print("\nCurrently playing:\n\t" + track + " - " + artist + "\n")
    # User information
    user = spotifyObject.current_user()
    displayName = user['display_name']

    clientSpotify.savedTracks()
    clientSpotify.setPlayList()
    clientSpotify.selectPlayList()
    clientSpotify.plMixed()
