from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json


def check_announcement():
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get("http://cs.hacettepe.edu.tr/#announcements")

    # For the title
    # I found these ugly PATHs with Firefox xPath Finder add-on.
    titlePath = '/html/body/div[4]/div/div[2]/div/div/div/div[1]/div/div[2]/div/table/tbody/tr[1]/td[2]'
    title = browser.find_element(By.XPATH, titlePath).text

    # For the content
    button1 = '/html/body/div[4]/div/div[2]/div/div/div/div[1]/div/div[2]/div/table/tbody/tr[1]/td[1]'
    contentPath = '/html/body/div[4]/div/div[2]/div/div/div/div[1]/div/div[2]/div/table/tbody/tr[2]/td/div/p'
    linkPath = contentPath + '/a'

    browser.find_element(By.XPATH, button1).click()
    content = browser.find_element(By.XPATH, contentPath).text
    url = browser.find_element(By.XPATH, linkPath).get_attribute('href')

    lastAnnouncementFromWeb = {
        "title": title,
        "content": content,
        "url": url
    }

    with open('announcements.json') as file:
        oldAnnouncements = json.load(file)
        lastAnnouncementFromDB = oldAnnouncements['Computer Science'][0]

    if lastAnnouncementFromDB != lastAnnouncementFromWeb:

        with open('announcements.json', 'w') as f:
            oldAnnouncements['Computer Science'][0] = lastAnnouncementFromWeb
            json_object = json.dumps(oldAnnouncements, indent=4)

            f.write(json_object)

        return lastAnnouncementFromWeb

    else:
        return None
