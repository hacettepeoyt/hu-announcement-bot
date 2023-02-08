import re

import aiohttp
from bs4 import BeautifulSoup


class BaseDepartment:
    address: str
    id: str

    def __init__(self, id: str, address: str) -> None:
        self.id = id
        self.address = address

    def _complete_url(self, url: str) -> str:
        url = self._fix_invalid_url(url)

        if url[:4] == 'http' or url[:3] == 'www':
            return url
        if url[0] == '/':
            url = url[1:]

        return self.address + url

    @staticmethod
    def _fix_invalid_url(url: str) -> str:
        valid_path_pattern = r'(-\d+)$'
        invalid_path_pattern = r'\/([^\/]+-\d+)$'

        if re.search(invalid_path_pattern, url) is None:
            return url

        found_suffix = re.search(valid_path_pattern, url).group(1)
        return re.sub(invalid_path_pattern, '/' + found_suffix, url)

    async def get_announcements(self) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.address) as resp:
                html_text: str = await resp.text(encoding='utf-8')
                soup: BeautifulSoup = BeautifulSoup(html_text, 'lxml')
                data = soup.find_all(class_='duyuru_baslik')[:5]
                new_announcements: list[dict] = []

                for p in data:
                    title: str = p.text.strip()

                    try:
                        url = self._complete_url(p.find('a').get('href'))
                    except AttributeError:
                        url = None

                    announcement = {"title": title, "content": None, "url": url}
                    new_announcements.append(announcement)

                return new_announcements


class CS(BaseDepartment):
    def __init__(self, id: str, address: str):
        super().__init__(id, address)

    async def get_announcements(self) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.address + '/json/announcements.json') as resp:
                data: list[dict] = await resp.json()
                data = data[:5]
                new_announcements: list[dict] = []

                for document in data:
                    body: BeautifulSoup = BeautifulSoup(document['body'], 'lxml')
                    title: str = document['title']
                    paragraphs = body.find_all('p')
                    content: str = ''

                    for p in paragraphs:
                        content += p.text.replace('\n', ' ')  # Texts are in static layout, we need to clean up.
                        content += '\n\n'

                    content = content[:-2]  # Removes last two new line chars.

                    try:
                        url = self._complete_url(body.find('a').get('href'))
                    except AttributeError:
                        url = None

                    announcement = {'title': title, 'content': content, 'url': url}
                    new_announcements.append(announcement)

                return new_announcements


class SKSDB(BaseDepartment):
    def __init__(self, id: str, address: str):
        super().__init__(id, address)

    async def get_announcements(self) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.address) as resp:
                html_text: str = await resp.text(encoding='utf-8')
                soup: BeautifulSoup = BeautifulSoup(html_text, 'lxml')
                data = soup.find_all('p')[8:13]
                new_announcements: list[dict] = []

                for p in data:
                    a = p.find('a')
                    title: str = a.text

                    try:
                        url = a.get('href')
                    except AttributeError:
                        url = None

                    announcement = {"title": title, "content": None, "url": url}
                    new_announcements.append(announcement)

                return new_announcements


class IE(BaseDepartment):
    def __init__(self, id: str, address: str):
        super().__init__(id, address)

    async def get_announcements(self) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.address) as resp:
                html_text: str = await resp.text(encoding='utf-8')
                soup: BeautifulSoup = BeautifulSoup(html_text, 'lxml')
                data = soup.select_one('.homepageAnnouncements > section > div').find_all(['p', 'details'])[0:5]
                new_announcements: list[dict] = []
                title, content, url = None, None, None

                for document in data:
                    if document.name == 'p':
                        document.span.decompose()
                        title = document.text.strip(' \n')
                        content = None
                    elif document.name == 'details':
                        document.summary.span.decompose()
                        title = document.summary.extract().text.strip(' \n,')
                        content = document.text.strip(' \n')
                        if content == '':
                            content = None

                    try:
                        url = self._complete_url(document.find('a').get('href'))
                    except AttributeError:
                        url = None

                    new_announcements.append({'title': title, 'content': content, 'url': url})

                return new_announcements


class Mat(BaseDepartment):
    def __init__(self, id: str, address: str):
        super().__init__(id, address)

    async def get_announcements(self) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.address + 'duyurular.html') as resp:
                html_text: str = await resp.text(encoding='utf-8')
                soup: BeautifulSoup = BeautifulSoup(html_text, 'lxml')
                data = soup.select('.duyurular_liste p')[:5]
                new_announcements: list[dict] = []

                for p in data:
                    title = p.text

                    try:
                        url = self._complete_url(p.select_one('a').get('href'))
                    except AttributeError:
                        url = None

                    announcement = {"title": title, "content": None, "url": url}
                    new_announcements.append(announcement)

                return new_announcements


class BBY(BaseDepartment):
    def __init__(self, id: str, address: str):
        super().__init__(id, address)

    async def get_announcements(self) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.address + 'duyurular.php') as resp:
                html_text = await resp.text(encoding='utf-8')

                soup: BeautifulSoup = BeautifulSoup(html_text, 'lxml')
                data = soup.find(id='yayinlar').find('tbody').find_all('tr')[-5:]
                new_announcements: list[dict] = []

                for tr in data:
                    a = tr.find('a')
                    title = a.text

                    try:
                        url = self._complete_url(a.get('href'))
                    except AttributeError:
                        url = None

                    announcement = {"title": title, "content": None, "url": url}
                    new_announcements.append(announcement)

                return new_announcements


class Edebiyat(BaseDepartment):
    def __init__(self, id: str, address: str):
        super().__init__(id, address)

    async def get_announcements(self) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.address) as resp:
                html_text: str = await resp.text(encoding='iso-8859-9')

                soup: BeautifulSoup = BeautifulSoup(html_text, 'lxml')
                section = soup.find(id='duyurular')
                data = section.find_all('p')[:5]
                new_announcements: list[dict] = []

                for p in data:
                    content = p.text.strip()
                    content = content.replace(u'\xa0', u' ')

                    try:
                        url = self._complete_url(p.find('a').get('href'))
                    except AttributeError:
                        url = None

                    announcement = {"title": None, "content": content, "url": url}
                    new_announcements.append(announcement)

                return new_announcements