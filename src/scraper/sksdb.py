import json
import requests
from bs4 import BeautifulSoup



class Sksdb:


    def __init__(self):

        self.announcement = {}
        self.name = 'SKSDB'


    def get_announcement(self):

        r = requests.get('http://www.sksdb.hacettepe.edu.tr/bidbnew/index.php', timeout=5)
        r.encoding = 'utf-8'
        html_text = r.text

        soup = BeautifulSoup(html_text, 'lxml')
        announcement = soup.find_all('p')[8].find('a')

        title = announcement.text
        content = None

        # Sometimes announcements don't contain a URL. This try-except block will bypass that problem.
        try:
            url = announcement.get('href')
        except AttributeError:
            print("ERROR: Attribute error for scraping URL")
            url = None

        self.announcement = {
            "title": title,
            "content": content,
            "url": url
        }

        return self.announcement
