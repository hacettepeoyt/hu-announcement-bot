import os
import json


def create_translation_unit() -> dict:
    """
    Read locale files and store them in memory to quickly access while doing translation.
    :return: Dictionary that stores translations
    """

    language_file_list = os.listdir('locale/')
    translation_unit = {}

    for language_file in language_file_list:
        language_code = language_file[:-5]

        with open(f'locale/{language_file}') as f:
            translation_unit[language_code] = json.load(f)

    return translation_unit


def create_locale_department_unit() -> dict:
    """
    Creates a map such:
    Language -> (Locale Department Name -> Department Key)
    :return: Dictionary in given format
    """

    tu = create_translation_unit()
    locale_department_map = {}

    for lang in tu:
        reversed_department_map = {}
        for key in tu[lang]:
            if key[:3] == 'hu-':
                reversed_department_map[tu[lang][key]] = key
        locale_department_map[lang] = reversed_department_map

    return locale_department_map


def find_next_language(language: str) -> str:
    """
    :param language: User's current language
    :return: Next language that can be chosen
    """

    language += '.json'
    language_list = sorted(os.listdir('locale/'))
    current_index = language_list.index(language)

    if current_index == len(language_list) - 1:
        return language_list[0][:-5]  # Removes ".json" part from the string

    return language_list[current_index + 1][:-5]  # Removes ".json" part from the string.
