![Hacettepe Duyurucusu Banner](assets/hu-announcement-bot-banner-light.png#gh-light-mode-only)
![Hacettepe Duyurucusu Banner](assets/hu-announcement-bot-banner-dark.png#gh-dark-mode-only)

# 🎉 What is this?

<p align="center">
  <img src="https://github.com/hacettepeoyt/hu-announcement-bot/assets/51515287/a6a92fec-f9cf-4767-b516-e297af32600c" width="300">
</p>

Who really enjoys visiting department websites regularly? Probably nobody. Now it's time to automate it with a Telegram
Bot. [Hacettepe Duyurucusu](https://t.me/HacettepeDuyurucuBot) offers this simple service to you with no cost.

<a href="https://t.me/HacettepeDuyurucuBot">
  <img src="https://github.com/user-attachments/assets/58c18620-ebda-45e9-affe-9c0c31aaae1e" width="200px">
</a>

# 🦾 How To Contribute?

There are 4 ways of contributing for this project.

## 🐛 Reporting Problems

This is the place if you are facing an issue while using the bot. To report it, you can use `/feedback` command and say
hi to admins! Even better, you
can [open an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue) on GitHub.

## 🙏 Feature Requests

If you have anything in your mind about improvements, go ahead and use `/feedback`. You can also
use [issue page](https://github.com/hacettepeoyt/hu-announcement-bot/issues) for it.

## 🗣 Adding New Languages

Any language even [High Valyrian](https://awoiaf.westeros.org/index.php/High_Valyrian). For a detailed instructions, go
ahead and see [this](https://github.com/hacettepeoyt/hu-announcement-bot/blob/master/docs/translation-guide.md).

### 🈶 Supported Languages

| **Language**       | **Status**                                                                                |
|--------------------|-------------------------------------------------------------------------------------------|
| **🇬🇧 English**     | [🟢](https://github.com/hacettepeoyt/hu-announcement-bot/blob/master/locale/en.json) 100% |
| **🇫🇷 French**      | [🟢](https://github.com/hacettepeoyt/hu-announcement-bot/blob/master/locale/fr.json) 100% |
| **🇹🇷 Turkish**     | [🟢](https://github.com/hacettepeoyt/hu-announcement-bot/blob/master/locale/tr.json) 100% |

## 💻 Development

If you know a bit Python, I'm sure you can do something.

- There are lots of departments in Hacettepe University. Hacettepe Duyurucusu doesn't include them all, yet. You can
  grap a soup from [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/), and scrape the department
  website you want. Don't forget to
  visit [detailed instructions](https://github.com/furkansimsekli/hu-announcement-bot/tree/master/docs/scraper-guide.md).
- There might be open issues right now, maybe you know the solution, and you have the free time. Any help is
  appreciated.
- You have an idea for a new feature, and you want to add it; I'm waiting for your pull request mate!

### 🧑‍💻 Development Environment

After cloning the repository, you should create a virtual environment. Python3.11 is recommended but any version higher
than or equal to 3.9 should work just fine. Then, install the requirements.

```bash
# Clone the repository
git clone git@github.com:hacettepeoyt/hu-announcement-bot.git
cd hu-announcement-bot

# Create a virtual environment with venv and activate it 
python3 -m venv .venv
source .venv/bin/activate

# Install the requirements
pip install -r requirements.txt
```

Fill the missing configurations in `config.toml`. Then, run the following command:

```bash
python -m src -c <path/to/config.toml> -d <path/to/database.json>
```

# 🆕 Changelog
<a href="https://t.me/hacettepeduyuru">
  <img src="https://github.com/user-attachments/assets/f1175906-80d5-48b6-b642-2e4128458268" width="200px">   
</a>

# 📃 License

[GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)
