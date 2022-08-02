import requests
from bs4 import BeautifulSoup


class StandartDepartment:

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
        response.encoding = 'utf-8'
        html_text = response.text

        soup = BeautifulSoup(html_text, 'lxml')
        data = soup.find_all(class_='duyuru_baslik')[:5]

        for p in data:
            title = p.text.strip()

            try:
                url = self.complete_url(p.find('a').encode('href'))
            except AttributeError:
                print("ERROR: Attribute error for scraping URL")
                url = None

            announcement = {"title": title, "content": None, "url": url}
            new_announcements.append(announcement)

        return new_announcements
