import requests
from bs4 import BeautifulSoup



class StandartDepartment:


    def __init__(self, name, address):

        self.announcement = {}
        self.name = name
        self.address = address



    def __complete_url(self, text):

        if text[:4] == 'http' or text[:3] == 'www':
            url = text
        else:
            url = self.address + text

        return url


    def get_announcement(self):

        r = requests.get(self.address, timeout=5)
        r.encoding = 'utf-8'
        html_text = r.text

        soup = BeautifulSoup(html_text, 'lxml')
        announcement = soup.find(class_='duyuru_baslik')

        title = announcement.text.strip()
        content = None

        # Sometimes announcements don't contain a URL. This try-except block will bypass that problem.
        try:
            url = self.__complete_url(announcement.find('a').get('href'))
        except AttributeError:
            print("ERROR: Attribute error for scraping URL")
            url = None

        self.announcement = {
            "title": title,
            "content": content,
            "url": url
        }

        return self.announcement
