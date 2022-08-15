import requests
from bs4 import BeautifulSoup


class Literature:

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def complete_url(self, text):
        if text[:4] == 'http' or text[:3] == 'www':
            return text

        return self.address + text

    def get_announcements(self):
        new_announcements = []

        response = requests.get(self.address, timeout=5)
        response.encoding = 'iso-8859-9'
        html_text = response.text

        soup = BeautifulSoup(html_text, 'lxml')
        section = soup.find(id='duyurular')
        data = section.find_all('p')[:5]

        for p in data:
            content = p.text.strip()
            content = content.replace(u'\xa0', u' ')

            try:
                url = self.complete_url(p.find('a').get('href'))
            except AttributeError:
                url = None

            announcement = {"title": None, "content": content, "url": url}
            new_announcements.append(announcement)

        return new_announcements
        