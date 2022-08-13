import requests
from bs4 import BeautifulSoup
import re


class StandartDepartment:

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def fix_invalid_url(self, text):
        valid_path_pattern = r'(-\d+)$'
        invalid_path_pattern = r'\/([^\/]+-\d+)$'
        if re.search(invalid_path_pattern, text) == None:
            return text
        found_suffix = re.search(valid_path_pattern, text).group(1)

        text = re.sub(invalid_path_pattern, '/' + found_suffix, text)
        return text

    def complete_url(self, text):
        text = self.fix_invalid_url(text)
        if text[:4] == 'http' or text[:3] == 'www':
            return text

        if (text[0] == '/'):
            text = text[1:]

        return self.address + text

    def get_announcements(self):
        new_announcements = []

        response = requests.get(self.address, timeout=5)
        response.encoding = 'utf-8'
        html_text = response.text

        soup = BeautifulSoup(html_text, 'lxml')
        data = soup.find_all(class_='duyuru_baslik')[:5]

        for p in data:
            title = p.text.strip()

            try:
                url = self.complete_url(p.find('a').get('href'))
            except AttributeError:
                url = None

            announcement = {"title": title, "content": None, "url": url}
            print(announcement)
            new_announcements.append(announcement)

        return new_announcements


standard = StandartDepartment('Test', 'http://www.ydyo.hacettepe.edu.tr/')
standard.get_announcements()
