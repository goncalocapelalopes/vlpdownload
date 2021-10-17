import argparse
import os
from urllib.parse import quote, unquote
import urllib.request

from bs4 import BeautifulSoup
import requests

ROOT_URL = "https://vaporwave.ivan.moe/list/"
DESTINATION = "E:\Vaporwave Library"

HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:10.0) \
            Gecko/20100101 Firefox/10.0"}


def get_artists(root_url=ROOT_URL, http_headers=HEADERS):
    """Obtain list of artist names in root directory."""
    req = urllib.request.Request(url=root_url, headers=http_headers)
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")

    # artist list is inside a <pre> tag
    # each artist name is in a hyperlink <a> to the respective artist folder
    artist_hrefs = soup.find("pre").find_all("a")

    # first element of the list is the parent directory "\.." link
    # child text alwas ends in "/" so .text[:-1] removes that char
    artist_list = [child.text[:-1] for child in artist_hrefs][1:]
    
    return artist_list

def get_album(artist_list, artist_name, album_name,
              root_url=ROOT_URL, http_headers=HEADERS,):
    if artist_name not in artist_list:
        raise Exception("Invalid artist name.")
    artist_name = quote(artist_name)
    artist_url = root_url + artist_name + "/"
    artist_url = artist_url.replace(" ", "%20")
    req = urllib.request.Request(url=artist_url, headers=http_headers)
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")
    
    # album list is inside a <pre> tag
    # each album name is in a hyperlink <a> to the respective album folder
    album_hrefs = soup.find("pre").find_all("a")

    # first element of the list is the parent directory "\.." link
    # child text alwas ends in "/" so .text[:-1] removes that char
    album_list = [child.text[:-1] for child in album_hrefs][1:]
    
    if album_name not in album_list:
        raise Exception("Invalid album name.")
    album_name = quote(album_name)
    album_url = artist_url + album_name + "/"
    album_url = album_url.replace(" ", "%20")
    req = urllib.request.Request(url=album_url, headers=http_headers)
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")
    
    song_hrefs = soup.find("pre").find_all("a")

    # first element of the list is the parent directory "\.." link
    # child text alwas ends in "/" so .text[:-1] removes that char
    song_list = [child["href"] for child in song_hrefs][1:]
    artist_name = unquote(artist_name)
    artist_folder = os.path.join(DESTINATION, artist_name)
    if not os.path.exists(artist_folder):
        os.mkdir(artist_folder)
    album_name = unquote(album_name)
    album_folder = os.path.join(artist_folder, album_name)
    if not os.path.exists(album_folder):
        os.mkdir(album_folder)
    print("DOWNLOADING "+ artist_name + " -> " + album_name)
    print("*"*20)
    for song_name in song_list:
        # remove invalid filename characters
        song_name = unquote(song_name)
        filename = os.path.join(album_folder, song_name)
        song_url = album_url + song_name
        song_url = song_url.replace(" ", "%20")
        print(song_name)
        
        r = requests.get(song_url)
        with open(filename, "wb+") as f:
            f.write(r.content)

if __name__ == "__main__":
    artists = get_artists()
    parser = argparse.ArgumentParser()
    parser.add_argument("--t", help="Artist name")
    parser.add_argument("--a", help="Album name")
    
    args = parser.parse_args()
    
    get_album(artists, args.t, args.a)
