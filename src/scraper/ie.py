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

        r = requests.get('http://www.ie.hacettepe.edu.tr/index.php?lang=tr')
        r.encoding = 'utf-8'
        html_text = r.text

        try:
            soup = BeautifulSoup(html_text, 'lxml')
            announcement = soup.select_one('.homepageAnnouncements p')

            title = announcement.get_text().split('\n')[0]
            content = ' '.join(announcement.get_text().split()[1:-1])

            try:
                url = announcement.select_one('a').get('href')
            except:
                print("Inner exception has raised for ie")
                url = None

        except:
            print("Outer exception has raised for ie")
            title, content, url = None, None, None

        self.announcement = {
            "title": title,
            "content": content,
            "url": url
        }

        return self.announcement
