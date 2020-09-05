import youtube_dl
import os, sys, shutil, subprocess
import eyed3
import urllib.request
from urllib.parse import urlparse
import requests
import bs4

# ydl stuff
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

# Function to download each video as MP3
def downloadVideo():
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:

        # Download video as mp3
        global ytVid
        ydl.download([str(ytVid)])

if __name__ == "__main__":
    # Select directory
    dir = input('Please input the path of your music folder: ')
    os.chdir(dir)

    # Make directory for songs which do not have metadata
    try:
        os.mkdir(dir + '\\' + 'no metadata')
    except:
        pass
    noMet = dir + '\\' + 'no metadata'
    os.chdir(noMet)

    ytVid = input('URL of YT video or playlist: ')
    # downloadVideo()

    # Rename file to song name
    for song in os.listdir(noMet):
        print('File name: '+ song)
        songName = input('What is the name of the song? ')+'.mp3'
        os.rename(song, songName)
        print('Song renamed!')

        audiofile = eyed3.load(songName)

        # User input song metadata
        audiofile.tag.title = songName
        audiofile.tag.artist = input('Input artist name: ')
        audiofile.tag.album = input('Input album name: ')
        audiofile.tag.album_artist =  input('Input album artist name: ')
        audiofile.tag.track_num = input('Input the track number: ')
        
        # Get cover art
        imgURL = input('Input cover art URL: ')
        imgLink = requests.get(imgURL)

        # Downloads cover art
        f = open('cover.jpg','wb')
        f.write(imgLink.content)
        f.close()

        # Sets cover art
        audiofile.tag.images.set(3, open('cover.jpg','rb').read(), 'image/jpeg') #test if png or jpeg, also error checks
        
        # Deletes cover art
        os.remove('cover.jpg')
        print('Cover art added!') #playlist iteration

        # Saves song
        audiofile.tag.save(version=eyed3.id3.ID3_V2_3)
        print('Video successfully downloaded!')

        # Move song out into original directory
        shutil.move(noMet + '\\' + songName, dir)
        # os.chdir(dir)

# # If playlist: 
# if 'index' or 'playlist' in ytVid:
#     playlistVideos = []
#     video = requests.get(ytVid)
#     soup = bs4.BeautifulSoup(video.text,'lxml')
#     playlistVideos.append(soup.select('title')[0].getText())
# # If single video:

