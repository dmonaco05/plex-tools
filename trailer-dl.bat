@echo off


del *.mp4

youtube-dl -f 137+140 -o "%%(playlist_index)s.%%(ext)s" https://www.youtube.com/playlist?list=ENTER YOUR PLAYLIST ID HERE