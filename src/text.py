'''
        Text module takes care of localization. Other modules generally use
        encode() function.
'''



import json


def encode(text_id, language):
    with open(f'locale/{language}.json') as file:
        text_json = json.load(file)

    return text_json[text_id]


def get_settings(dnd, holiday, language):
    '''
        Settings page shows the current status of DND, Holiday Mode and Language.
        Also, give them information about DND and Holiday Mode.
    '''


    text = ""

    if dnd:
        text += f"\U0001F508 <b>{encode('dnd-text', language)}:</b> {encode('enabled', language)}\n\n"
    else:
        text += f"\U0001F508 <b>{encode('dnd-text', language)}:</b> {encode('disabled', language)}\n\n"

    if holiday:
        text += f"\U0001F3D6 <b>{encode('holiday-text', language)}:</b> {encode('enabled', language)}\n\n"
    else:
        text += f"\U0001F3D6 <b>{encode('holiday-text', language)}:</b> {encode('disabled', language)}\n\n"

    text += f"\U0001F30D <b>{encode('language-text', language)}:</b> {encode('language', language)}\n\n\n"

    text += f"<b>{encode('dnd-text', language)}:</b> <i>{encode('dnd-desc', language)}</i>\n\n" \
            f"<b>{encode('holiday-text', language)}:</b> <i>{encode('holiday-desc', language)}</i>\n"

    return text


def create_announcement_text(department_id, announcement, language):
    '''
        Creates well formatted announcement message to notify users.
        All the announcements have title, some of them have no content and no url.
    '''


    title = announcement['title']
    content = announcement['content']
    url = announcement['url']
    text = f"<b>{encode(department_id, language)} {encode('header', language)}</b>\n\n\n"

    for key in announcement.keys():
        if key == 'title' and title is not None:
            text += f"\U0001F514 <b>{title}</b>\n\n"

        if key == 'content' and content is not None:
            text += f"\U0001F4AC {content}\n\n"

        if key == 'url' and url is not None:
            text += f"\U0001F310 <a href='{url}'>{encode('anchor-text', language)}</a>"

    return text


def get_departments(language):
    '''
        Department names are stored in database with IDs.
        User needs to see somehow not IDs but names with a specific language.
        This function finds the current id - name pair from locale and reverts it.
    '''


    with open(f'locale/{language}.json') as file:
        text_json = json.load(file)

    inverted = {}
    for key in text_json.keys():
        if 'hu-' in key:
            inverted[text_json[key]] = key

    return inverted
    