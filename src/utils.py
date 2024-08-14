import os
import json


def create_translation_unit() -> dict:
    """
    Reads locale files from the 'locale' directory and creates a dictionary
    mapping language codes to their respective translations.

    Returns:
        A dictionary where keys are language codes and values are dictionaries
        of translations for those languages.
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
    Creates a mapping of languages to locale department names and their keys.

    The resulting dictionary maps each language to another dictionary where
    keys are department names and values are department keys, specifically
    for departments with keys starting with 'hu-'.

    Returns:
        A dictionary where keys are language codes and values are dictionaries
        mapping department names to department keys.
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
    Finds the next language in the sorted list of available languages.

    The language parameter should be provided without the '.json' extension.
    This function returns the next language code in the sorted order or wraps
    around to the first language if the current one is the last in the list.

    Args:
        language: The current language code (without the '.json' extension).

    Returns:
        The language code of the next language in the sorted list.
    """

    language += '.json'
    language_list = sorted(os.listdir('locale/'))
    current_index = language_list.index(language)

    if current_index == len(language_list) - 1:
        return language_list[0][:-5]  # Removes ".json" part from the string

    return language_list[current_index + 1][:-5]  # Removes ".json" part from the string.
