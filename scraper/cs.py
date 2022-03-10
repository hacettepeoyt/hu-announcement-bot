import json
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
        else:
            self.announcement = None

        return self.announcement