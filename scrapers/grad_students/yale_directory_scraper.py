import urllib.request
from bs4 import BeautifulSoup


opener = build_opener(HTTPCookieProcessor())

with urllib.request.urlopen('https://directory.yale.edu/?queryType=field&firstname=abc&school=GS') as response:
   html = response.read()
   print(html)