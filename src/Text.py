import json


def encode(text_id, language):
    with open(f'locale/{language}.json') as file:
        text_json = json.load(file)

    return text_json[text_id]


def get_settings(dnd, holiday, language):
    text = ""

    if dnd:
        text += f"{encode('dnd-text', language)}: {encode('enabled', language)}\n"
    else:
        text += f"{encode('dnd-text', language)}: {encode('disabled', language)}\n"

    if holiday:
        text += f"{encode('holiday-text', language)}: {encode('enabled', language)}\n"
    else:
        text += f"{encode('holiday-text', language)}: {encode('disabled', language)}\n"

    text += f"{encode('language-text', language)}: {encode('language', language)}\n\n\n"

    text += f"{encode('dnd-desc', language)}\n\n{encode('holiday-desc', language)}\n"

    return text


def create_announcement_text(department_id, announcement, language):
    title = announcement['title']
    content = announcement['content']
    url = announcement['url']
    text = f"{encode(department_id, language)} {encode('header', language)}\n\n"

    for key in announcement.keys():
        if key == 'title' and title is not None:
            text += f"\U0001F514 <b>{title}</b>\n\n"

        if key == 'content' and content is not None:
            text += f"\U0001F4AC {content}\n\n"

        if key == 'url' and url is not None:
            text += f"\U0001F310 <a href='{url}'>{encode('anchor-text', language)}</a>"

    return text


def get_departments(language):
    with open(f'locale/{language}.json') as file:
        text_json = json.load(file)

    inverted = {}
    for key in text_json.keys():
        if 'hu-' in key:
            inverted[text_json[key]] = key

    return inverted
