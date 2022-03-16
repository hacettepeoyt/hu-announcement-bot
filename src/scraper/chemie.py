import requests
from bs4 import BeautifulSoup



class Chemie:


    def __init__(self):

        self.announcement = {}
        self.name = 'Chemie'


    @staticmethod
    def __complete_url(text):

        if text[:4] == 'http' or text[:3] == 'www':
            url = text
        else:
            url = 'http://www.chem.hacettepe.edu.tr/' + text

        return url


    def get_announcement(self):

        r = requests.get('http://www.chem.hacettepe.edu.tr/')
        r.encoding = 'utf-8'
        html_text = r.text

        soup = BeautifulSoup(html_text, 'lxml')
        announcement = soup.find(class_='duyuru_baslik')

        title = announcement.text.strip()
        content = None
        url = self.__complete_url(announcement.find('a').get('href'))

        self.announcement = {
            "title": title,
            "content": content,
            "url": url
        }

        return self.announcement