import json
import requests
from bs4 import BeautifulSoup



class Tomer:


    def __init__(self):

        self.announcement = {}
        self.name = 'TOMER'


    @staticmethod
    def __complete_url(text):

        if text[:4] == 'http' or text[:3] == 'www':
            url = text
        else:
            url = 'http://www.tomer.hacettepe.edu.tr/' + text

        return url


    def get_announcement(self):

        r = requests.get('http://www.tomer.hacettepe.edu.tr/')
        r.encoding = 'utf-8'
        html_text = r.text

        soup = BeautifulSoup(html_text, 'lxml')
        announcement = soup.select_one('.duyuru_baslik')

        title = announcement.text
        content = None
        url = self.__complete_url(announcement.select_one('a').get('href'))

        self.announcement = {
            "title": title,
            "content": content,
            "url": url
        }

        return self.announcement