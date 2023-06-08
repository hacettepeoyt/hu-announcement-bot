import urllib.parse

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
        if url[0] != '/':
            url = '/' + url

        return self.address + url

    @staticmethod
    def _fix_invalid_url(url: str) -> str:
        return urllib.parse.quote(url, "\./_-:")

    async def get_announcements(self) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.address) as resp:
                html_text: str = await resp.text(encoding='utf-8', errors="replace")
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

    @staticmethod
    def cleanup(str_: str) -> str:
        """
        Reduces the number of consecutive `\n` by two. If there is an alone '\n', replaces it with space.
        :param str_: The string that is going to be formatted
        :return: String with new format
        """

        if len(str_) == 0 or str_ == "\n":
            return ""

        chars = list(str_)
        i = 0
        while i < len(chars):
            if chars[i] == "\n":
                j = i
                while j < len(chars) and chars[j] == "\n":
                    j += 1
                if j - i > 1:
                    chars[i] = ""
                    chars[i + 1] = ""
                else:
                    chars[i] = " "
                i = j
            i += 1
        return "".join(chars)

    async def get_announcements(self) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.address + '/json/announcements.json') as resp:
                data: list[dict] = await resp.json()
                data = data[:5]
                new_announcements: list[dict] = []

                for document in data:
                    body: BeautifulSoup = BeautifulSoup(document['body'], 'lxml')
                    title: str = document['title']
                    content = body.get_text("\n").replace("\r\n", "\n")  # CRLF to LF
                    content = self.cleanup(content)

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
                html_text: str = await resp.text(encoding='utf-8', errors="replace")
                soup: BeautifulSoup = BeautifulSoup(html_text, 'lxml')
                data = soup.find_all('p')[8:13]
                new_announcements: list[dict] = []

                for p in data:
                    a = p.find('a')
                    title: str = a.text.strip()

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
                html_text: str = await resp.text(encoding='utf-8', errors="replace")
                soup: BeautifulSoup = BeautifulSoup(html_text, 'lxml')
                data = soup.select_one('.homepageAnnouncements > section > div').find_all(['p', 'details'])[0:5]
                new_announcements: list[dict] = []
                title, content, url = None, None, None

                for document in data:
                    date = document.find('span', class_='tarih')

                    if date:
                        document.span.decompose()

                    if document.name == 'p':
                        title = document.text.strip(' \n')
                        content = None
                    elif document.name == 'details':
                        title = document.summary.extract().text.strip(' \n,')
                        content = document.text.strip(' \n')

                        if content == '':
                            content = None

                    try:
                        url = self._complete_url(document.find('a').get('href'))
                    except AttributeError:
                        url = None

                    # There are some blank p tags inside HTML. In that case, generated announcement becomes like below.
                    # That's why this control flow needed.
                    if title == '' and content is None and url is None:
                        continue

                    new_announcements.append({'title': title, 'content': content, 'url': url})

                return new_announcements


class Mat(BaseDepartment):
    def __init__(self, id: str, address: str):
        super().__init__(id, address)

    async def get_announcements(self) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.address + '/duyurular.html') as resp:
                html_text: str = await resp.text(encoding='utf-8', errors="replace")
                soup: BeautifulSoup = BeautifulSoup(html_text, 'lxml')
                data = soup.select('.duyurular_liste p')[:5]
                new_announcements: list[dict] = []

                for p in data:
                    title = p.text.strip()

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
            async with session.get(self.address + '/duyurular.php') as resp:
                html_text = await resp.text(encoding='utf-8', errors="replace")

                soup: BeautifulSoup = BeautifulSoup(html_text, 'lxml')
                data = soup.find(id='yayinlar').find('tbody').find_all('tr')[-5:]
                new_announcements: list[dict] = []

                for tr in data:
                    a = tr.find('a')
                    title = a.text.strip()

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
                html_text: str = await resp.text(encoding='iso-8859-9', errors="replace")

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


class EE(BaseDepartment):
    def __init__(self, id: str, address: str):
        super().__init__(id, address)

    async def get_announcements(self) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.address + '?link=archivedAnno&lang=e') as resp:
                html_text: str = await resp.text(errors="replace")
                soup: BeautifulSoup = BeautifulSoup(html_text, 'lxml')
                data = soup.find_all(
                    class_='w3-card w3-light-grey my-flexItem my-xl3m my-l3m my-m4m my-s6m w3-margin-bottom w3-medium')
                new_announcements: list[dict] = []

                for d in data[:5]:
                    title = d.findNext(class_='w3-medium').text.strip()
                    url = self._complete_url(d.findNext('a').get('href'))
                    announcement = {"title": title, "content": None, "url": url}
                    new_announcements.append(announcement)

                return new_announcements


class Phys(BaseDepartment):
    def __init__(self, id: str, address: str):
        super().__init__(id, address)

    async def get_announcements(self) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.address + '/index.php') as resp:
                html_text: str = await resp.text(errors="replace")
                soup: BeautifulSoup = BeautifulSoup(html_text, 'lxml')
                data = soup.find_all('p')
                new_announcements: list[dict] = []

                for p in data[2:7]:
                    title = p.text.strip().replace('\n', ' ').replace('\r', '')

                    try:
                        url = self._complete_url(p.findNext('a').get('href'))
                    except AttributeError:
                        url = None

                    announcement = {"title": title, "content": None, "url": url}
                    new_announcements.append(announcement)

                return new_announcements


class ABOfisi(BaseDepartment):
    def __init__(self, id: str, address: str):
        super().__init__(id, address)

    async def get_announcements(self) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.address) as resp:
                html_text: str = await resp.text(encoding='utf-8', errors="replace")
                soup: BeautifulSoup = BeautifulSoup(html_text, 'lxml')
                data = soup.select_one('#nav-1').find_all('p')[:5]
                new_announcements: list[dict] = []

                for p in data:
                    date = p.find('span', class_='tarih')

                    if date:
                        p.span.decompose()

                    title = p.text.strip()

                    try:
                        url = self._complete_url(p.find('a').get('href'))
                    except AttributeError:
                        url = None

                    announcement = {"title": title, "content": None, "url": url}
                    new_announcements.append(announcement)

                return new_announcements


class BIDB(BaseDepartment):
    def __init__(self, id: str, address: str):
        super().__init__(id, address)

    async def get_announcements(self) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.address) as resp:
                html_text: str = await resp.text(encoding='utf-8', errors="replace")
                soup: BeautifulSoup = BeautifulSoup(html_text, 'lxml')
                data = soup.find(class_='duyurular_liste').find_all('p')[:5]
                new_announcements: list[dict] = []

                for p in data:
                    date = p.find('span', class_='tarih')

                    if date:
                        p.span.decompose()

                    title: str = p.text.strip()

                    try:
                        url = self._complete_url(p.find('a').get('href'))
                    except AttributeError:
                        url = None

                    announcement = {"title": title, "content": None, "url": url}
                    new_announcements.append(announcement)

                return new_announcements


class JeoMuh(BaseDepartment):
    def __init__(self, id: str, address: str):
        super().__init__(id, address)

    async def get_announcements(self) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.address) as resp:
                html_text: str = await resp.text(encoding='utf-8', errors="replace")
                soup: BeautifulSoup = BeautifulSoup(html_text, 'lxml')
                data = soup.find(id='vision').find_all('p')[:5]
                new_announcements: list[dict] = []

                for p in data:
                    date = p.find('span', class_='tarih')

                    if date:
                        p.span.decompose()

                    title: str = p.text.strip()

                    try:
                        url = self._complete_url(p.find('a').get('href'))
                    except AttributeError:
                        url = None

                    announcement = {"title": title, "content": None, "url": url}
                    new_announcements.append(announcement)

                return new_announcements


class Hidro(BaseDepartment):
    def __init__(self, id: str, address: str):
        super().__init__(id, address)

    async def get_announcements(self) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.address) as resp:
                html_text: str = await resp.text(encoding='utf-8', errors="replace")
                soup: BeautifulSoup = BeautifulSoup(html_text, 'lxml')
                data = soup.find(class_='tabs').find_all('p')[:5]
                new_announcements: list[dict] = []

                for p in data:
                    date = p.find('span', class_='tarih')

                    if date:
                        p.span.decompose()

                    title: str = p.text.strip()

                    try:
                        url = self._complete_url(p.find('a').get('href'))
                    except AttributeError:
                        url = None

                    if title == '' and url is None:
                        continue

                    announcement = {"title": title, "content": None, "url": url}
                    new_announcements.append(announcement)

                return new_announcements
