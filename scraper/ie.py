import json
import requests
from bs4 import BeautifulSoup



class IndustrialEngineering:

    def __init__(self):
        self.announcement = {}
        self.name = 'IE'

        with open('userConfigs.json') as file:
            self.subscribers = json.load(file)[self.name]

    @staticmethod
    def __complete_url(text):

        if text[:4] == 'http' or text[:3] == 'www':
            url = text
        else:
            url = 'http://www.ie.hacettepe.edu.tr/' + text

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

        r = requests.get('http://www.ie.hacettepe.edu.tr/index.php?lang=tr')
        r.encoding = 'utf-8'
        html_text = r.text

        try:
            soup = BeautifulSoup(html_text, 'lxml')
            announcement = soup.select_one('.homepageAnnouncements p')

            title = announcement.get_text().split('\n')[0]
            content = ' '.join(announcement.get_text().split()[1:-1])

            try:
                url = announcement.select_one('a').get('href')
            except:
                print("Inner exception has raised for ie")
                url = None

        except:
            print("Outer exception has raised for ie")
            title, content, url = None, None, None

        self.announcement = {
            "title": title,
            "content": content,
            "url": url
        }

        with open('announcements.json') as file:
            oldAnnouncements = json.load(file)
            lastAnnouncementFromDB = oldAnnouncements['IE'][0]

        if lastAnnouncementFromDB != self.announcement:
            with open('announcements.json', 'w', encoding='utf-8') as f:
                oldAnnouncements['IE'][0] = self.announcement
                json_object = json.dumps(oldAnnouncements, indent=4, ensure_ascii=False)

                f.write(json_object)
        else:
            self.announcement = None

        return self.announcement