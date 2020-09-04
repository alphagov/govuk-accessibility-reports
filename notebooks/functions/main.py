import os
import ast
import json

import numpy as np

from bs4 import BeautifulSoup


# function to extract links from HTML
def get_links(text):
    """ Extract links found in <a> tags

    :param text: HTML code we want to extract links from
    :return: list of links extracted from HTML code
    """
    list_links = []
    soup = BeautifulSoup(text, "html.parser")
    for a in soup.find_all('a', href=True):
        link = a['href']
        list_links.append(link)
    return list_links


# function to extract filename from HTML
def extract_filename(list_text):
    """Extracts the last part of a URL path string, including the file name and extension

    :param list: A list of strings to extract last part from, e.g. everything after '/'
    :return: A list of the same length as list_text, but with the last parts kept e.g. everything after '/'

    """
    file_name = [os.path.split(text)[1] for text in list_text]
    return file_name


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
