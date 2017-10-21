import argparse
import random
from collections import defaultdict

import requests
from bs4 import BeautifulSoup as bs


def get_lyric_pages(artist_name):
    history = []
    contents = []
    page_num = 1
    status = 200
    while status == 200 and len(history) == 0:
        url = 'http://www.metrolyrics.com/{keyword}-alpage-{page_num}.html'.format(  # NOQA
            keyword=artist_name,
            page_num=page_num
        )
        r = requests.get(url)
        status = r.status_code
        history = r.history
        contents.append(r.text)
        page_num += 1
    return contents[:-1]


def parse_song_list(contents, artist_name):
    artist_name = artist_name.replace('-', ' ')
    songs_dict = defaultdict(str)
    for content in contents:
        soup = bs(content, 'html.parser')
        a_tags = soup.find_all('a', class_='title hasvidtable')
        for a in a_tags:
            if artist_name in (a['title']).lower():
                title = a.get_text().replace('Lyrics', '')
                songs_dict[title] = a['href']
    return songs_dict


def parse_lyrics(content):
    soup = bs(content, 'html.parser')
    p = soup.find_all('p', class_='verse')
    for each in p:
        print(each.get_text())


def create_parser():
    parser = argparse.ArgumentParser(description='Fetch lyric randomly')
    parser.add_argument(
        'artist_name',
        metavar='ARTIST NAME',
        type=str,
        nargs='*',
        help='Name of the artist who wants to fetch lyrics.'
    )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    artist_name = '-'.join([word.lower() for word in args.artist_name])

    contents = get_lyric_pages(artist_name)
    songs_dict = parse_song_list(contents, artist_name)

    random_song = random.choice([song for song in songs_dict.keys()])
    random_song_url = songs_dict.get(random_song)

    print(random_song)
    song_page = requests.get(random_song_url)
    if song_page.status_code == 200:
        content = song_page.text
    else:
        print('HTTP Error {}'.format(song_page.status_code))
    parse_lyrics(content)


if __name__ == "__main__":
    main()
