import httpx
from bs4 import BeautifulSoup
import re
from datetime import datetime
import lib.lastfm as lastfm

def get_ratings_from_page(page=1, user="y2bd"):
    ratings = []
    last_rating = None

    page_text = get_recent_page(page, user)
    soup = BeautifulSoup(page_text, "html.parser")

    rows = soup.find_all("tr", id=re.compile("^page_catalog_item"))
    for row in rows:
        try:
            if row.find('th', class_='or_q_header'):
                # This is a header row, skip it
                continue
            elif row.find('td', class_='or_q_small_album'):
                # This is a rating row
                album = row.find('a', class_='album').text
                artist = row.find('a', class_='artist').text
                rating = int(float(row.find('td', class_='or_q_rating_date_s').find('img')['title'][:4]) * 2)
                timestamp = datetime.strptime(row.find('div', class_='date_element').text.replace('\n', ' ').strip(), '%b %d %Y').date()
                
                rating = {
                    'album': album,
                    'artist': artist,
                    'rating': rating,
                    'timestamp': timestamp,
                    'album_art_url': lastfm.get_album_art_url(artist, album),
                    'review': None,
                }

                ratings.append(rating)
                last_rating = rating
            elif row.find('div', class_='or_q_review'):
                # This is a review row
                review = row.find('div', class_='or_q_review').text

                if last_rating:
                    last_rating['review'] = review
                    last_rating = None
        except:
            pass

    return ratings

def get_recent_page(page=1, user="y2bd"):
    url = f"https://rateyourmusic.com/collection/{user}/recent/{page}"
    r = httpx.get(url)
    return r.text
