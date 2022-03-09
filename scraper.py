import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


class ComputerScience:

    def __init__(self):
        self.announcement = {}
        self.name = 'CS'

        with open('userConfigs.json') as file:
            self.subscribers = json.load(file)[self.name]

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
        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.get("http://cs.hacettepe.edu.tr/#announcements")

        # For the title
        # I found these ugly PATHs with Firefox xPath Finder add-on.
        titlePath = '/html/body/div[4]/div/div[2]/div/div/div/div[1]/div/div[2]/div/table/tbody/tr[1]/td[2]'
        title = browser.find_element(By.XPATH, titlePath).text

        # For the content and url
        button1 = '/html/body/div[4]/div/div[2]/div/div/div/div[1]/div/div[2]/div/table/tbody/tr[1]/td[1]'
        contentPath = '/html/body/div[4]/div/div[2]/div/div/div/div[1]/div/div[2]/div/table/tbody/tr[2]/td/div/p'
        urlPath = contentPath + '/a'

        browser.find_element(By.XPATH, button1).click()
        content = browser.find_element(By.XPATH, contentPath).text
        url = browser.find_element(By.XPATH, urlPath).get_attribute('href')

        self.announcement = {
            "title": title,
            "content": content,
            "url": url
        }

        with open('announcements.json') as file:
            oldAnnouncements = json.load(file)
            lastAnnouncementFromDB = oldAnnouncements['CS'][0]

        if lastAnnouncementFromDB != self.announcement:
            with open('announcements.json', 'w') as f:
                oldAnnouncements['CS'][0] = self.announcement
                json_object = json.dumps(oldAnnouncements, indent=4)

                f.write(json_object)

            return self.announcement

        else:
            return None


class Math:

    def __init__(self):
        self.announcement = {}
        self.name = 'Math'

        with open('userConfigs.json') as file:
            self.subscribers = json.load(file)[self.name]

    def __complete_url(self, text):
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
        print("**math checkpoint**")
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
            print('math is different')
            with open('announcements.json', 'w', encoding='utf-8') as f:
                oldAnnouncements['Math'][0] = self.announcement
                json_object = json.dumps(oldAnnouncements, indent=4, ensure_ascii=False)

                f.write(json_object)

            return self.announcement

        else:
            print('math is the same')
            return None


class Sksdb:

    def __init__(self):
        self.announcement = {}
        self.name = 'SKSDB'

        with open('userConfigs.json') as file:
            self.subscribers = json.load(file)[self.name]

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
        print("**sksdb checkpoint**")
        r = requests.get('http://www.sksdb.hacettepe.edu.tr/bidbnew/index.php')

        r.encoding = 'utf-8'
        html_text = r.text

        soup = BeautifulSoup(html_text, 'lxml')
        announcement = soup.find_all('p')[8].find('a')

        title = announcement.text
        content = None
        url = announcement.get('href')

        self.announcement = {
            "title": title,
            "content": content,
            "url": url
        }

        with open('announcements.json') as file:
            oldAnnouncements = json.load(file)
            lastAnnouncementFromDB = oldAnnouncements['SKSDB'][0]

        if lastAnnouncementFromDB != self.announcement:
            print('sksdb is different')
            with open('announcements.json', 'w', encoding='utf-8') as f:
                oldAnnouncements['SKSDB'][0] = self.announcement
                json_object = json.dumps(oldAnnouncements, indent=4, ensure_ascii=False)

                f.write(json_object)

            return self.announcement

        else:
            print('sksdb is the same')
            return None


class Chemie:

    def __init__(self):
        self.announcement = {}
        self.name = 'Chemie'

        with open('userConfigs.json') as file:
            self.subscribers = json.load(file)[self.name]

    def __complete_url(self, text):
        if text[:4] == 'http' or text[:3] == 'www':
            url = text
        else:
            url = 'http://www.chem.hacettepe.edu.tr/' + text

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
        print("**chemie checkpoint**")
        r = requests.get('http://www.chem.hacettepe.edu.tr/')

        r.encoding = 'utf-8'
        html_text = r.text

        soup = BeautifulSoup(html_text, 'lxml')
        announcement = soup.find(class_='duyuru_baslik')
        title = announcement.text.strip()
        content = None
        url = self.__complete_url(announcement.find('a').get('href'))

        self.announcement = {
            "title": title,
            "content": content,
            "url": url
        }

        with open('announcements.json') as file:
            oldAnnouncements = json.load(file)
            lastAnnouncementFromDB = oldAnnouncements['Chemie'][0]

        if lastAnnouncementFromDB != self.announcement:
            print('chemie is different')
            with open('announcements.json', 'w', encoding='utf-8') as f:
                oldAnnouncements['Chemie'][0] = self.announcement
                json_object = json.dumps(oldAnnouncements, indent=4, ensure_ascii=False)

                f.write(json_object)

            return self.announcement

        else:
            print('chemie is the same')
            return None
