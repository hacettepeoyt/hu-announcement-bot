# Hacettepe Duyurucusu

## How To Scrape?

In general, [aiohttp]() and [beautifulsoup4]() are recommended while scraping. Keep in mind that using [Selenium]()
isn't an option.

However, if you think there is an exception with your department, you
should [open an issue](https://github.com/hacettepeoyt/hu-announcement-bot/issues) first.

## Technical Details

1. Before scraping check out `BaseDepartment`, be aware that some websites use the very same template. If it is your
   case, you should
   use it and go to 4th step.
2. If your website is unique then you should create a new `class` that inherits `BaseDepartment` and implement the
   `get_announcements` method in it. You can take `CS` and `IE` as references.
3. The format for announcements should be in:
    ```json
      {
        "title": "Great News!",
        "content": "Details on great news.",
        "url": "https://example.com"
      }
      ```
    - **title:** Every department share the announcements with a title. (Of course there might be exceptions!)
    - **content:** An announcement also may have a content without clicking to given url. However, most of them doesn't
      have content. You should assign `None` in such cases.
    - **url:** Most of the announcements lead somewhere on the web when you click on it.
4. After writing the scraper itself, you must add the new department into `AVAILABLE_DEPARTMENTS`.
5. Last step is important for end-users. Did you notice that you never write department's name while coding? It's
   because Hacettepe Duyurucusu supports more than one language, so you need go
   to [locale](https://github.com/furkansimsekli/hu-announcement-bot/blob/master/locale) and put the names for every
   language. You can find more
   explanation [here](https://github.com/hacettepeoyt/hu-announcement-bot/blob/master/docs/translation-guide.md).

That's it, now [Hacettepe Duyurucusu](https://t.me/HacettepeDuyurucuBot) is controlling a brand-new department's
announcements!

Also, don't forget to add yourself down below!

## Contributors

- [M.Eren SOYKOK](https://github.com/rentale)
- [Melike Vurucu](https://github.com/melikechan)