import requests
from bs4 import BeautifulSoup


class IndustrialEngineering:
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
        data = soup.select_one(
            '.homepageAnnouncements > section > div').find_all(['p', 'details'])[0:5]

        for document in data:
            if document.name == 'p':
                document.span.decompose()
                title = document.text.strip(' \n')
                content = None
            elif document.name == 'details':
                document.summary.span.decompose()
                title = document.summary.extract().text.strip(' \n,')
                content = document.text.strip(' \n')
                if (content == ''):
                    content = None

            try:
                url = self.complete_url(document.find('a').get('href'))
            except AttributeError:
                url = None

            new_announcements.append(
                {'title': title, 'content': content, 'url': url})

        return new_announcements
        