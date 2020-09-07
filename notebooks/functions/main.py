import os
import ast
import json

import numpy as np


# function to extract filename from HTML
def extract_filename(list_text):
    """Extracts the last part of a URL path string, including the file name and extension

    :param list_text: A list of strings to extract last part from, e.g. everything after '/'
    :return: A list of the same length as list_text, but with the last parts kept e.g. everything after '/'

    """
    try:
        file_name = [os.path.split(text)[1] for text in list_text]
        return file_name
    except (TypeError):
        # deals with attachment paths that don't end in .pdf, .txt, etc.
        # e.g. /government/publications/happy-days-farming-company-limited-application-made-to-abstract-water/happy-days-farming-company-limited-application-made-to-abstract-water # noqa
        return [np.NaN]


def extract_fileextension(list_text):
    """Extracts the extension of a file or webpath

    :param list_text: A list of strings to extract file extension from
    :return: List of file extensions of the same length as list_text
    """
    try:
        file_extension = [os.path.splitext(text)[1] for text in list_text]
        return file_extension
    except (TypeError):
        return [np.NaN]


# function to extract certain element from HTML
def extract_element(text, section, element):
    """Extracts all the 'elements' from a specified 'section' from GOV.UK pages

    :param text: String of the HTML code for the GOV.UK page being passed in
    :param element: The `element` within `section` part of HTML code to extract the contents of e.g. 'title', 'url'
    :return: list of all the attachment titles that were extracted from GOV.UK page
    """

    try:
        text = ast.literal_eval(text)
        text = text.get(section)

        titles = list(map(lambda x: x[element], text))
        return titles

    except (ValueError):
        return [np.NaN]


# function to extract from list nested in HTML
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
