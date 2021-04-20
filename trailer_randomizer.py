#!/usr/bin/python

# This script will randomize a directory of intros and pre-rolls for Plex Media Server
# use it in combination with youtube-dl to currate your own pre-rolls (and in HD too)
# the point of this is so that you may have a constantly changing pre-roll to give more of a theater experience.
# This script should be setup as a crontab or scheduled task, I run mine every hour during the hours I am awake.
# Example crontab setup
#    0 10-23/2 * * * /usr/bin/python3 /home/pi/trailer_randomizer.py >/dev/null 2>&1


from plexapi.server import PlexServer
import requests

from urllib.parse import quote_plus, urlencode

from plexapi import media, utils, settings, library
from plexapi.base import Playable, PlexPartialObject
from plexapi.exceptions import BadRequest, NotFound

import random

playlist_length = 9   # Change this number to however many videos are in your pre-roll folder
# Change these to where your pre-rolls are located, do not put them in the same directory
intro_loc = "C:\pre_rolls\intros"
trailers_loc = "C:\pre_rolls\trailers"

trailers = list(range(1,playlist_length))
intros = ["regal.intro.mp4","projector.intro.mp4","regal.intro.mp4"]    # Change these to whatever you have in your intro dir, as you can see regal intro is there twice to increase the chances of selecting it.
url = "http://192.168.1.X:32400"     # Change X (or entire IP) to what the plex server runs on
token = "TOKEN GOES HERE"    # Enter plex server token here

# Randomize the pre-rolls files and create the entry for Plex to use
random.shuffle(trailers)
random.shuffle(intros)
a = trailers[0]
b = trailers[1]
c = intros[0]

if len(trailers) > 10:
    if a < 10:
        a = str(a).zfill(2)
    if b < 10:
        b = str(b).zfill(2)

syntax = "{}\{}.mp4,{}\{}.mp4,{}\{}".format(trailers_loc, a, trailers_loc, b, intro_loc, c)


# Setup the plex api requests
session = requests.Session()
session.verify = False
requests.packages.urllib3.disable_warnings()

# Update plex to use the new pre-rolls
plex = PlexServer(url, token, session, timeout=None)
plex.settings.get("cinemaTrailersPrerollID").set(syntax)
plex.settings.save()

print("Pre-roll updated")
print(syntax)