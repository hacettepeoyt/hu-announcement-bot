# Hacettepe Duyurucusu

## How To Scrape?

We used [requests](https://realpython.com/python-requests/) and [beautifulsoup4](https://beautiful-soup-4.readthedocs.io/en/latest/) libraries. They are really easy to use. If you are going to contribute to the project, I highly recommend you to use these stuff. Modules like [Selenium](https://www.selenium.dev/) isn't appreciated. Also, all departments' websites can be parsed with [beautifulsoup4](https://beautiful-soup-4.readthedocs.io/en/latest/).

However, if you think there is an exception with your department, you should [open an issue](https://github.com/furkansimsekli/hu-announcement-bot/issues) first.

## Technical Details

1. Before scraping check out [standart.py](https://github.com/furkansimsekli/hu-announcement-bot/blob/master/scraper/standart.py), some websites use the very same template If it is your case, you should use it and go to 4th step.
2. If your website is unique then you should create a file which indicates the department name with letters.
   > For example; **Computer Science** becomes `cs.py`, **Industrial Engineering** becomes `ie.py`.
3. These files must contain a `class` just like others. Also, there need to be a method called `get_announcements`. How to implement that method is up to you, but it needs to **return** *a list that contains last five announcements.*
   ```python
      new_announcements = []
      
      announcement = {
        'title': title,
        'content': content,
        'url': url
      }
      ```
4. After scraping, you need to edit [index.py](https://github.com/furkansimsekli/hu-announcement-bot/blob/master/scraper/index.py). If the latest is **hu-19**, you need to give **hu-20** to your department.https://github.com/furkansimsekli/hu-announcement-bot/blob/master/locale/README.md
5. Last step is important for end-users. Did you notice that you never write department's name while coding? It's because Hacettepe Duyurucusu support more than one language, so you need go to [locale](https://github.com/furkansimsekli/hu-announcement-bot/blob/master/locale) and put the names for every language with the id you choose earlier. You can find more explanation [here](https://github.com/furkansimsekli/hu-announcement-bot/blob/master/locale/README.md).

That's it, now [Hacettepe Duyurucusu](t.me/HacettepeDuyurucuBot) is checking  a brand new department!

Also, don't forget to add yourself down below :)

## Contributors

- [M.Eren SOYKOK](https://github.com/rentale)
- [Melike Vurucu](https://github.com/melikechan)