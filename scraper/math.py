import json
import requests
from bs4 import BeautifulSoup



class Math:


    def __init__(self):

        self.announcement = {}
        self.name = 'Math'

        with open('userConfigs.json') as file:
            self.subscribers = json.load(file)[self.name]


    @staticmethod
    def __complete_url(text):

        if text[:4] == 'http' or text[:3] == 'www':
            url = text
        else:
            url = 'http://www.mat.hacettepe.edu.tr/' + text

        return url


    def __update_subscribers(self):

        with open('userConfigs.json') as file:
            user_configs = json.load(file)
            user_configs[self.name] = self.subscribers
            json_object = json.dumps(user_configs)

        with open('userConfigs.json', 'w') as file:
            file.write(json_object)


    def add_subscriber(self, user_id):

        if user_id not in self.subscribers:
            self.subscribers.append(user_id)
            self.__update_subscribers()


    def remove_subscriber(self, user_id):

        if user_id in self.subscribers:
            self.subscribers.remove(user_id)
            self.__update_subscribers()


    def get_announcement(self):

        r = requests.get('http://www.mat.hacettepe.edu.tr/duyurular.html')
        r.encoding = 'utf-8'
        html_text = r.text

        soup = BeautifulSoup(html_text, 'lxml')
        p = soup.select_one('.duyurular_liste p')

        title = p.get_text()
        content = None
        url = self.__complete_url(p.select_one('a').get('href'))

        self.announcement = {
            "title": title,
            "content": content,
            "url": url
        }

        with open('announcements.json') as file:
            oldAnnouncements = json.load(file)
            lastAnnouncementFromDB = oldAnnouncements['Math'][0]

        if lastAnnouncementFromDB != self.announcement:
            with open('announcements.json', 'w', encoding='utf-8') as f:
                oldAnnouncements['Math'][0] = self.announcement
                json_object = json.dumps(oldAnnouncements, indent=4, ensure_ascii=False)

                f.write(json_object)
        else:
            self.announcement = None

        return self.announcement