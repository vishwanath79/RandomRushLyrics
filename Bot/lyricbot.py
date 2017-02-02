import pprint
import random
import reprlib

import colorlog
import requests
import tweepy
from bs4 import BeautifulSoup

import creds
from creds import ACCESS_SECRET, ACCESS_TOKEN, CONSUMER_KEY, CONSUMER_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

logger = colorlog.getLogger()
r = reprlib.Repr()
# r.maxlist = 10000   # max elements displayed for lists
r.maxstring = 100  # max characters displayed for strings


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


def randomizer(tracks):
    logger.info("Into randomizer")

    # print((title.upper()),"------" ,artist.upper(), "\n")
    for track in tracks:
        # get json response from MusiXmatch search for track
        response = track_search(track.title, track.artist)
        urls = []
        # get URLs
        for i in response['message']['body']['track_list']:
            urls.append((i['track']['track_share_url']))
        logger.info("Getting URL")

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
    logger.info("Returning lyrics")
    botlyrics = lyrics_all_versions[0]
    # print(lyrics_all_versions[0])
    return (botlyrics)


def call_lyrics():
    # get data
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
            str_error = None
            tracks = [Song(title, artist)]
            logger.info("calling Randomizer")
            return randomizer(tracks)
            str_error = None
            # return title, artist


        except Exception as str_error:
            logger.debug("Into exception" + str(Exception))
            pass


if __name__ == "__main__":
    logger.setLevel(colorlog.colorlog.logging.INFO)
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter())
    logger.addHandler(handler)
    # get data
    # what the bot will tweet

    # tweetlist = ['Test tweet two!']
    tweetlist = str(call_lyrics())
    info = (tweetlist[:130] + '... #rush') if len(tweetlist) > 140 else tweetlist
    pprint.pprint(info)
    if len(info) > 10:
        api.update_status(info)
        logger.info("Done tweeting")
    else:
        logger.info("None returned")
        pass




