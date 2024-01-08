import httpx
import os
from html import escape

def get_album_art_url(artist, album):
    try:
        release_info = get_release_info(artist, album)
        album_art_url = release_info['album']['image'][-1]['#text']
        return album_art_url
    except Exception as e:
        return None

def get_release_info(artist, album):
    lastfm_api_key = os.environ.get('LASTFM_API_KEY')
    if not lastfm_api_key:
        raise Exception('LASTFM_API_KEY not set')

    url = f"http://ws.audioscrobbler.com/2.0/"
    r = httpx.get(url, params={'method': 'album.getinfo', 'api_key': lastfm_api_key, 'artist': artist, 'album': album, 'autocorrect': 1, 'format': 'json'})
    return r.json()