from __future__ import unicode_literals
import sys
import spotipy
import spotipy.util as util
import youtube_dl
from youtube_search import YoutubeSearch
import json
import shutil
import os
import threading
from os.path import exists

output_dir = ''
token = ''

class YtLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def get_username():
    return os.getenv('USERNAME')

def get_token():
    global token
    if not token:
        scope = 'playlist-read-private'

        token = util.prompt_for_user_token(
            get_username(), 
            scope, 
            client_id=os.getenv('CLIENT_ID').strip(),
            client_secret=os.getenv('CLIENT_SECRET').strip(),
            redirect_uri='http://localhost:8080'
        )

    if token:
        return token
    else: 
        raise Exception('Could not get user-token. Make you set them in the .env file')

def download_yt_video(url, config):
    with youtube_dl.YoutubeDL(config) as ydl:
        try:
            ydl.download([url])
        except:
            print('something went wrong when downloading')

def download_from_yt(tracks):
    """
    Tracks are coming from spotify with the spotipy api
    """
    for i, item in enumerate(tracks['items']):
        track = item['track']
        track_name = track['name']
        album_name = track['album']['name']
        artist_name = track['artists'][0]['name']
        
        track_name = f'{track_name} - {artist_name}'

        filename = f'{output_dir}/{artist_name}/{album_name}/{track_name}'
        # filename = filename.replace(' ', '_')
        filename = filename + '.%(ext)s'

        # if exists(filename) == False:
        results = json.loads(YoutubeSearch(f'{track_name} {artist_name}', max_results=1).to_json())
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                # 'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': YtLogger(),
            'quiet': True,
            'restrictfilenames': True,
            'outtmpl': filename,
            'prefer_ffmpeg': True,
        }
        if len(results['videos']) > 0:
            vid_id = results['videos'][0]['id'] 
            if vid_id:
                # docs https://github.com/ytdl-org/youtube-dl/blob/master/README.md#embedding-youtube-dl
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    print(track_name)
                    try:
                        ydl.download([f'https://youtu.be/{vid_id}'])
                    except youtube_dl.utils.DownloadError:
                        print("error occurd while downloading video")
        else:
            print(f'track "{track_name}" not found')


def download_playlist(selected_playlist_id):
    global video_title_mapper
    sp = spotipy.Spotify(auth=get_token())

    results = sp.playlist(selected_playlist_id, fields="tracks,next")
    tracks = results['tracks']
    download_from_yt(tracks)

    while True:
        tracks = sp.next(tracks)
        download_from_yt(tracks)


def select_playlist(playlist_ids):
    while True:
        selected_id = input("select one of the playlists by entering its id: ")
        for playlist_id in playlist_ids:
            if playlist_id == selected_id:
                return playlist_id
        print("invalid id try again. \n")

def print_and_get_playlists():
    sp = spotipy.Spotify(auth=get_token())
    playlists = sp.user_playlists(get_username())

    ids = []
    for playlist in playlists['items']:
        ids.append(playlist['id'])
        print(f"id: {playlist['id']} name: {playlist['name']} amount: {playlist['tracks']['total']}")
    return ids

def main():
        # while True:
        global output_dir

        output_dir = input("output-dir:")
        ids = print_and_get_playlists()
        selected_playlist = select_playlist(ids)
        download_playlist(selected_playlist)

if __name__ == '__main__':
    main()
