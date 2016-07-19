from urllib.parse import urljoin
import pdb
import requests
import random
import creds
import wikipedia
from bs4 import BeautifulSoup
import requests

class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

source_code = requests.get('https://en.wikipedia.org/wiki/List_of_songs_recorded_by_Rush')
soup = BeautifulSoup(source_code.content)

table = soup.find('span', id='Singles').parent.find_next_sibling('table')
for single in table.find_all('th', scope='row'):
    print(single.text)

artistsdb = ['rush']
titlesdb = ["closer to the heart", "towm sawyer", "presto"]

title = random.choice(titlesdb)
artist = "rush"

def track_search(title, artist):
    url = creds.generate_url('track_search')
    payload = {'apikey': creds.api_key(), 'q_track': title, 'q_artist': artist, 'has_lyrics': 1}
    return requests.get(url, params=payload).json()




def track_lyrics_get(track_id):
    url = creds.generate_url('track_lyrics_get')
    payload = {'apikey': creds.api_key(), 'track_id': str(track_id)}
    return requests.get(url, params=payload).json()


if __name__ == "__main__":
    tracks = [
                Song(title,artist)
    ]
    for track in tracks:
        # get json response from MusiXmatch search for track
        response = track_search(track.title, track.artist)
        for i in response['message']['body']['track_list']:
            print(i['track']['track_share_url'])

        # pull out track_ids
        track_ids = []
        for each in response['message']['body']['track_list']:
            if each['track']['has_lyrics'] == 1:
                track_ids.append(each['track']['track_id'])


        # get lyrics
        # if len(track_ids) > 0:
        lyrics_all_versions = []
        for trk in track_ids:
            response = track_lyrics_get(track_ids[0])  # just use the first
            lyrics_all_versions.append(response['message']['body']['lyrics']['lyrics_body'])


        #print(lyrics_all_versions[0])
        #for each in lyrics_all_versions:
            #print (each)