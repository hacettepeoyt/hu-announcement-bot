import requests
from bs4 import BeautifulSoup



class ComputerScience:


    def __init__(self):

        self.announcement = {}
        self.name = 'Computer Science'


    @staticmethod
    def __complete_url(text):

        if text[:4] == 'http' or text[:3] == 'www':
            url = text
        else:
            url = 'http://www.cs.hacettepe.edu.tr/' + text

        return url


    def get_announcement(self):

        r = requests.get('http://cs.hacettepe.edu.tr/json/announcements.json')

        announcements = r.json()
        last_announcement = announcements[0]
        body = BeautifulSoup(last_announcement['body'], 'lxml')

        title = last_announcement['title']
        content = body.find('p').text
        url = self.__complete_url(body.find('a').get('href'))

        self.announcement = {'title': title, 'content': content, 'url': url}

        return self.announcement
