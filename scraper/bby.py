'''
        This module might be a second standart template in Hacettepe.
        If you encounter this one, please open an issue first.
        We may need to standardise.
'''



import requests
from bs4 import BeautifulSoup


class InformationManagement:

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def complete_url(self, text):
        if text[:4] == 'http' or text[:3] == 'www':
            return text

        return self.address + text

    def get_announcements(self):
        new_announcements = []

        response = requests.get(self.address + 'duyurular.php', timeout=5)
        response.encoding = 'utf-8'
        html_text = response.text

        soup = BeautifulSoup(html_text, 'lxml')
        data = soup.find(id='yayinlar').find('tbody').find_all('tr')[-5:]

        for tr in data:
            a = tr.find('a')
            title = a.text

            try:
                url = self.complete_url(a.get('href'))
            except AttributeError:
                url = None

            announcement = {"title": title, "content": None, "url": url}
            new_announcements.append(announcement)

        return new_announcements
        
