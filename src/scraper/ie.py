import json
import requests
from bs4 import BeautifulSoup



class IndustrialEngineering:

    def __init__(self):
        self.announcement = {}
        self.name = 'Industrial Engineering'


    @staticmethod
    def __complete_url(text):

        if text[:4] == 'http' or text[:3] == 'www':
            url = text
        else:
            url = 'http://www.ie.hacettepe.edu.tr/' + text

        return url


    def get_announcement(self):

        r = requests.get('http://www.ie.hacettepe.edu.tr/index.php?lang=tr', timeout=(5,10))
        r.encoding = 'utf-8'
        html_text = r.text

        soup = BeautifulSoup(html_text, 'lxml')
        announcement = soup.select_one('.homepageAnnouncements p')

        title = announcement.get_text().split('\n')[0]
        content = None

        # Sometimes announcements don't contain a URL. This try-except block will bypass that problem.
        try:
            url = self.__complete_url(announcement.select_one('a').get('href'))
        except AttributeError:
            print("ERROR: Attribute error for scraping URL")
            url = None

        self.announcement = {
            "title": title,
            "content": content,
            "url": url
        }

        return self.announcement
