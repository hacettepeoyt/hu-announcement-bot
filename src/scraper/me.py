import requests
from bs4 import BeautifulSoup

class MechanicalEngineering:

    def __init__(self):
        self.announcement = {}
        self.name = 'Mechanical Engineering'

    def __complete_url(self, text):
        if text[:4] == 'http' or text[:3] == 'www':
            url = text
        else:
            url = 'http://www.me.hacettepe.edu.tr' + text
        return url

    def get_announcement(self):

        r = requests.get('http://www.me.hacettepe.edu.tr/tr/duyurular')
        r.encoding = 'utf-8'
        html_text = r.text

        soup = BeautifulSoup(html_text, 'html.parser')

        announcement = soup.select_one('.liste a')

        title = announcement.get_text(strip=True)
        content = None
        url = self.__complete_url(soup.select_one('.liste a').get('href'))

        self.announcement = {
            "title": title,
            "content": content,
            "url": url
        }
        return self.announcement
