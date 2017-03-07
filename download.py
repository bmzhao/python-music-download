import os
import sys

import requests
from bs4 import BeautifulSoup
from urllib import parse

def get_urls_on_page(url, func):
    result = requests.get(url)
    soup = BeautifulSoup(result.content)
    tags = soup.find_all(lambda tag: 'href' in tag.attrs)
    urls = list(map(lambda x: x['href'], tags))
    to_return = list(filter(func, urls))
    return to_return


def is_mp3(url):
    return url.endswith('.mp3')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write("Need to pass the url of site")
        sys.exit(1)

    os.makedirs('output', exist_ok=True)

    seen = set()
    urls_to_go = get_urls_on_page(sys.argv[1], is_mp3)
    for url in urls_to_go:
        if url in seen:
            continue
        for mp3_url in get_urls_on_page(url, is_mp3):
            if mp3_url in seen:
                continue

            seen.add(mp3_url)
            parsed_mp3_url = parse.unquote(mp3_url)
            mp3_name = parsed_mp3_url[parsed_mp3_url.rfind('/'):]
            mp3 = requests.get(mp3_url).content
            with open('output/' + mp3_name, 'wb') as f:
                f.write(mp3)
            print('downloaded',mp3_name)

        seen.add(url)
