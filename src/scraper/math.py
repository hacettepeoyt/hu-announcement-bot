import requests
from bs4 import BeautifulSoup


class Math:

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def complete_url(self, text):
        if text[:4] == 'http' or text[:3] == 'www':
            return text

        return self.address + text

    def get_announcements(self):
        new_announcements = []

        response = requests.get(self.address + 'duyurular.html', timeout=5)
        response.encoding = 'utf-8'
        html_text = response.text

        soup = BeautifulSoup(html_text, 'lxml')
        data = soup.select('.duyurular_liste p')[:5]

        for p in data:
            title = p.text

            try:
                url = self.complete_url(p.select_one('a').get('href'))
            except AttributeError:
                url = None

            announcement = {"title": title, "content": None, "url": url}
            new_announcements.append(announcement)

        return new_announcements
        