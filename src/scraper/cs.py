import requests
from bs4 import BeautifulSoup



class ComputerScience:


    def __init__(self):

        self.announcement = {}
        self.name = 'CS'


    def get_announcement(self):

        r = requests.get('http://cs.hacettepe.edu.tr/json/announcements.json')
        announcements = r.json()
        last_announcement = announcements[0]

        title = last_announcement['title']
        body = BeautifulSoup(last_announcement['body'], 'lxml')
        content = str(body.find('p')).replace('<p>', '').replace('</p>', '')
        url = None

        self.announcement = {'title': title, 'content': content, 'url': url}

        return self.announcement