import os
import random
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

import creds

app = Flask(__name__)


class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist


def track_search(title, artist):
    url = creds.generate_url('track_search')
    payload = {'apikey': creds.api_key(), 'q_track': title, 'q_artist': artist, 'has_lyrics': 1}
    return requests.get(url, params=payload).json()


def track_lyrics_get(track_id):
    url = creds.generate_url('track_lyrics_get')
    payload = {'apikey': creds.api_key(), 'track_id': str(track_id)}
    return requests.get(url, params=payload).json()


def randomizer(tracks, title, artist):
    print(title.upper(), "------", artist.upper())
    for track in tracks:
        # get json response from MusiXmatch search for track
        response = track_search(track.title, track.artist)
        urls = []
        # get urls
        for i in response['message']['body']['track_list']:
            urls.append((i['track']['track_share_url']))
        # print(urls[0],"\n")



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
    lyr = lyrics_all_versions[0]
    loneurl = urls[0]
    # return (lyrics_all_versions[0])
    return lyr, loneurl


# GET ALL
@app.route('/rushrandom')
def run_app():
    source_code = requests.get('https://en.wikipedia.org/wiki/List_of_songs_recorded_by_Rush')
    soup = BeautifulSoup(source_code.content, "lxml")
    songsdb = []
    table = soup.find("table", {"class": "wikitable sortable"})
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) == 5:
            songs = cells[0].find(text=True)
            songsdb.append(songs)
            # print(songsdb)

    for x in range(0, 1):
        # try 4 times
        try:
            title = random.choice(songsdb)
            artist = "rush"
            tracks = [Song(title, artist)]
            # randomizer(tracks)
            lyrics, loneurl = randomizer(tracks, title, artist)
            # return randomizer(tracks, title,artist)
            return render_template("index.html", lyrics=lyrics, loneurl=loneurl)
        except Exception as e:
            render_template("Error.html", error=str(e))


if __name__ == "__main__":
    server = '127.0.0.1'
    port = int(os.environ.get('PORT', 8001))
    app.run(host=server, port=port, debug=True)