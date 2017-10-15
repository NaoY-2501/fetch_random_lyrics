import random
from collections import defaultdict

import requests
from bs4 import BeautifulSoup as bs


def get_html(url):
    req = requests.get(url)
    if req.status_code == 200:
        return req.text
    else:
        print('error')


def parse_song_list(content):
    soup = bs(content, 'html.parser')
    a = soup.find_all('a', class_='title hasvidtable')
    songs_dict = defaultdict(str)
    for each in a:
        if 'oasis' in (each['title']).lower():
            songs_dict[each.get_text()] = each['href']
    return songs_dict


def parse_lyric(content):
    soup = bs(content, 'html.parser')
    p = soup.find_all('p', class_='verse')
    for each in p:
        print(each.get_text())


def main():
    keyword = 'oasis'
    url = 'http://www.metrolyrics.com/{keyword}-lyrics.html'.format(
        keyword=keyword
    )
    content = get_html(url)
    songs_dict = parse_song_list(content)

    random_song = random.choice([song for song in songs_dict.keys()])
    random_song_url = songs_dict.get(random_song)

    print(random_song)
    content = get_html(random_song_url)
    parse_lyric(content)


if __name__ == "__main__":
    main()
