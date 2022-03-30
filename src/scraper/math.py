import json
import requests
from bs4 import BeautifulSoup



class Math:


    def __init__(self):

        self.announcement = {}
        self.name = 'Math'

    @staticmethod
    def __complete_url(text):

        if text[:4] == 'http' or text[:3] == 'www':
            url = text
        else:
            url = 'http://www.mat.hacettepe.edu.tr/' + text

        return url


    def get_announcement(self):

        r = requests.get('http://www.mat.hacettepe.edu.tr/duyurular.html')
        r.encoding = 'utf-8'
        html_text = r.text

        soup = BeautifulSoup(html_text, 'lxml')
        p = soup.select_one('.duyurular_liste p')

        title = p.get_text()
        content = None

        # Sometimes announcements don't contain a URL. This try-except block will bypass that problem.
        try:
            url = self.__complete_url(p.select_one('a').get('href'))
        except AttributeError:
            print("ERROR: Attribute error for scraping URL")
            url = None


        self.announcement = {
            "title": title,
            "content": content,
            "url": url
        }

        return self.announcement