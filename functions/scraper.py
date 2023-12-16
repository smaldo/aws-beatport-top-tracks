from bs4 import BeautifulSoup
from datetime import datetime
import json
import requests


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
}


def getBeatportTop100(genre):
    url = f"https://www.beatport.com/genre/{genre['slug']}/{genre['id']}/top-100"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_tag = soup.find('script', id="__NEXT_DATA__")
    json_data = json.loads(script_tag.string)
    tracks = json_data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['results']
    topTracks = []
    for index, track in enumerate(tracks):
        artists = []
        for artist in track['artists']:
            artists.append(artist['name'])

        bpm = track['bpm']

        genre = track['genre']['name']

        isrc = track['isrc']

        key = track['key']['name']

        label = track['release']['label']['name']

        length = track['length']

        length_ms = track['length_ms']

        mix_name = track['mix_name']

        name = track['name']

        price = track['price']['value']

        publish_date = track['publish_date']

        ranking = str(index+1)

        ranking_date = datetime.today().strftime('%Y-%m-%d')

        remixers = []
        for remixer in track['remixers']:
            remixers.append(remixer['name'])

        slug = track['slug']

        track_id = track['id']

        date_genre = f"{ranking_date}#{genre}"

        url = f"https://www.beatport.com/track/{slug}/{track_id}"

        topTracks.append({
            "artists": artists,
            "bpm": bpm,
            "date_genre": date_genre,
            "genre": genre,
            "isrc": isrc,
            "key": key,
            "label": label,
            "length": length,
            "length_ms": length_ms,
            "mix_name": mix_name,
            "name": name,
            "price": price,
            "publish_date": publish_date,
            "ranking": ranking,
            "ranking_date": ranking_date,
            "remixers": remixers,
            "slug": slug,
            "track_id": track_id,
            "url": url
        })
    return topTracks


def beatportScraperHandler(event, context):
    result = dict()
    result['name'] = event['name']
    result['data'] = getBeatportTop100(event)
    return json.loads(json.dumps(result, default=str))
