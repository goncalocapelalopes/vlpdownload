import os
import urllib.request

from bs4 import BeautifulSoup

ROOT_URL = "https://vaporwave.ivan.moe/list/"
DESTINATION = "E:\Vaporwave Library"

HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:10.0) \
            Gecko/20100101 Firefox/10.0"}


def get_artists(root_url=ROOT_URL, http_headers=HEADERS):
    """Obtain list of artist names in root directory."""
    req = urllib.request.Request(url=ROOT_URL, headers=http_headers)
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")

    # artist list is inside a <pre> tag
    # each artist name is in a hyperlink <a> to the respective artist folder
    artist_hrefs = soup.find("pre").find_all("a")

    # first element of the list is the parent directory "\.." link
    # child text alwas ends in "/" so .text[:-1] removes that char
    artist_list = [child.text[:-1] for child in artist_hrefs][1:]
    
    return artist_list


if __name__ == "__main__":
    artists = get_artists()
