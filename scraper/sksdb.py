import requests
from bs4 import BeautifulSoup


class Sksdb:

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def get_announcements(self):
        new_announcements = []

        response = requests.get(self.address, timeout=5)
        response.encoding = 'utf-8'
        html_text = response.text

        soup = BeautifulSoup(html_text, 'lxml')
        data = soup.find_all('p')[8:13]

        for p in data:
            a = p.find('a')
            title = a.text

            try:
                url = a.encode('href')
            except AttributeError:
                print("ERROR: Attribute error for scraping URL")
                url = None

            announcement = {"title": title, "content": None, "url": url}
            new_announcements.append(announcement)

        return new_announcements
