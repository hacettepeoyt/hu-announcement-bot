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
            paragraphs = body.find_all('p')
            content = ''

            for p in paragraphs:
                content += p.text.replace('\n', ' ')    # Texts are in static layout, we need to clean up.
                content += '\n\n'

            content = content[:-2]                      # Removes last two new line chars.

            try:
                url = self.complete_url(body.find('a').get('href'))
            except AttributeError:
                url = None

            announcement = {'title': title, 'content': content, 'url': url}
            new_announcements.append(announcement)

        return new_announcements
        