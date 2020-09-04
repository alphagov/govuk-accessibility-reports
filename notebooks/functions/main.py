import os
import ast
import json

from multiprocessing import Pool
from functools import partial

import numpy as np
import pandas as pd

from bs4 import BeautifulSoup


# function to apply parallelised function
def parallelise_dataframe(df, func, n_cores=1, n_splits=1, **kwargs):
    """ Apply a function on a dataframe in parallel

    :param df: Dataframe to apply function on
    :param func: Function to apply to dataframe
    :param n_cores: Number of cores on machine you want to use to do parallel processing
    :param n_splits: Number of splits ypu want to make on your dataframe
    :param kwargs: Keyword arguments for the func function
    :return: Dataframe after function has been applied to it
    """

    df_split = np.array_split(ary=df, indices_or_sections=n_splits)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(partial(func, **kwargs), df_split))
    pool.close()
    pool.join()
    return df


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


# function to extract certain element from HTML
def extract_element(text, section, element):
    """Extracts all the attachment titles from GOV.UK pages

    :param text: String of the HTML code for the GOV.UK page being passed in
    :param element: The `element` within `section` part of HTML code to extract the contents of e.g. 'title', 'url'
    :return: list of all the attachment titles that were extracted from GOV.UK page
    """
    text = ast.literal_eval(text)
    text = text.get(section)

    titles = list(map(lambda x: x[element], text))

    return titles


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
