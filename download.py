import os
import urllib.request

from bs4 import BeautifulSoup

ROOT_URL = "https://vaporwave.ivan.moe/list/"
DESTINATION = "E:\Vaporwave Library"

header= {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0"}

req = urllib.request.Request(url=ROOT_URL, headers=header)
page = urllib.request.urlopen(req).read()