import httpx
import os
import re
from html import escape

def get_album_art_url(artist, album):
    try:
        for (partist, palbum) in get_permutations_of_artist_album(artist, album):
            release_info = get_release_info(partist, palbum)
            try:
                album_art_url = release_info['album']['image'][-1]['#text']

                if album_art_url and album_art_url != '':
                    return album_art_url
            except KeyError:
                pass
        return None
    except:
        return None

def get_release_info(artist, album):
    lastfm_api_key = os.environ.get('LASTFM_API_KEY')
    if not lastfm_api_key:
        raise Exception('LASTFM_API_KEY not set')

    url = f"http://ws.audioscrobbler.com/2.0/"
    r = httpx.get(url, params={'method': 'album.getinfo', 'api_key': lastfm_api_key, 'artist': artist, 'album': album, 'autocorrect': 1, 'format': 'json'})
    return r.json()

def get_permutations_of_artist_album(artist, album):
    # First, try the artist and album as-is
    yield (artist, album)

    # Next, try the album name with no punctuation
    yield (artist, re.sub(r'[!\?\.\-,/]', '', album).strip())

    # Next, try removing anything after a colon in the album name for albums with subtitles
    yield (artist, re.sub(r':.*', '', album).strip())

    # Next, try removing anything after the final parenthesis in the album name for artist names with translations
    yield (artist, re.sub(r'\(.*\)$', '', album.strip()).strip())

    # Next, try removing anything after the final bracket in the artist name for artist names with translations
    yield (re.sub(r'\[.*\]$', '', artist.strip()).strip(), album)

    # Last, try both bracket and parenthesis removals
    yield (re.sub(r'\[].*\]$', '', artist.strip()).strip(), re.sub(r'\(.*\)$', '', album.strip()).strip())