import requests
from bs4 import BeautifulSoup


class ComputerScience:

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def complete_url(self, text):
        if text[:4] == 'http' or text[:3] == 'www':
            return text

        return self.address + text

    def get_announcements(self):
        new_announcements = []

        response = requests.get(self.address + '/json/announcements.json', timeout=5)
        data = response.json()[:5]

        for document in data:
            body = BeautifulSoup(document['body'], 'lxml')
            title = document['title']
            content = body.text

            try:
                url = self.complete_url(body.find('a').get('href'))
            except AttributeError:
                print("ERROR: Attribute error for scraping URL")
                url = None

            announcement = {'title': title, 'content': content, 'url': url}
            new_announcements.append(announcement)

        return new_announcements
