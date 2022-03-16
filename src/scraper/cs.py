import json

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from database import UserDatabase



class ComputerScience:


    def __init__(self):

        self.announcement = {}
        self.name = 'CS'


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

        return self.announcement