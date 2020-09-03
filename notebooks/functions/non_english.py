import numpy as np

import json
import ast

from langdetect import detect_langs
from langdetect.lang_detect_exception import LangDetectException


def extract_publishing_organisation(content_item, key, index=0):
    """ Extracts the value of a key within a dictionary masquerading as a string

    :param content_item: A string that's in the format of a dictionary
    :param key: The name of the key you want to extract the associated value from
    :param index: The index of specific value if you extracted more than one value from the key
    :return: the extracted value of the key
    """
    try:
        # convert object to string
        content_item = json.dumps(content_item)
        # convert string to object
        content_item = json.loads(content_item)

        # convert to dictionary
        organisations = ast.literal_eval(content_item)

        # extract value of key entered from dictionary
        organisations = list(map(lambda org: org[index], organisations.get(key, {})))

        return organisations
    except (ValueError, SyntaxError):
        return [np.NaN]


def extract_title(text):
    """Extracts all the attachment titles from GOV.UK pages

    :param html: String of the HTML code for the GOV.UK page being passed in
    :return: list of all the attachment titles that were extracted from GOV.UK page

    """
    text = ast.literal_eval(text)
    text = text.get('attachments')

    titles = list(map(lambda x: x['title'], text))

    return titles


def detect_language(text):
    """Detects language of a text, moving onto next text if an error is thrown

    :param text: A string to detect the language of
    :return: A list returning the language detected and confidence score associated to it

    """

    try:
        return detect_langs(text)
    except LangDetectException:
        return np.NaN
