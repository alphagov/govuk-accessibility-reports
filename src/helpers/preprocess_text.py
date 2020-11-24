import os
import re
import ast

from bs4 import BeautifulSoup
from lxml import etree


def is_html_like(text):
    """
    Checks whether text is html or not
    :param text: string
    :return: bool
    """
    if isinstance(text, str):
        text = text.strip()
        if text.startswith("<"):
            return True
        return False
    return False


def extract_text_from_content_details(data, keep_html=False):
    """
    Recurses through lists and dicts to find html and then extract text or html if specified
    :param data: This function can accept a nested list or dict, or string
    :return:
    """
    if isinstance(data, list):
        # whitespace aggregated as we skip through unsuitable text fragments (slugs, titles, govspeak)
        return re.sub(" +", " ",
                      " ".join([extract_text_from_content_details(item, keep_html) for item in data])).strip()
    elif isinstance(data, dict):
        if "content_type" in data.keys() and data["content_type"] != "text/html":
            return " "
        return extract_text_from_content_details(list(data.values()), keep_html)
    elif is_html_like(data):
        # could be optional
        # data = remove_tables_from_html(data)
        if keep_html:
            return data
        return extract_text(data)
    return " "


def extract_links_from_content_details(data):
    """
    Recurses through lists and dicts to find html and then extract links BE
    VERY CAREFUL AND PASS IN LINKS, otherwise old links may persist in the list
    :param data: This function can accept a nested list or dict, or string
    :return:
    """
    if isinstance(data, list):
        # could optionally return unique set of links: list(set(links))...
        return [link for item in data for link in extract_links_from_content_details(item)]
    elif isinstance(data, dict):
        if "content_type" in data.keys() and data["content_type"] != "text/html":
            return []
        return extract_links_from_content_details(list(data.values()))
    elif is_html_like(data):
        return extract_links_from_html(data)
    return []


def remove_tables_from_html(html):
    soup = BeautifulSoup(html, "lxml")
    for table in soup.find_all("table"):
        table.decompose()
    return str(soup)


def extract_text(body):
    """
    Extract text from html body
    :param body: <str> containing html.
    """
    # TODO: Tidy this up!
    r = None
    # body != "\n" and
    if body and body != "\n" and not body.isspace():
        try:
            # print("this is", body)
            tree = etree.HTML(body)
            r = tree.xpath('//text()')
            r = ' '.join(r)
            r = r.strip().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
            r = r.replace('\n', ' ').replace('\\"', '"')
            # r = r.lower()
            r = ' '.join(r.split())
        except ValueError as e:
            print("exception @ extract:", type(body), body, e)
    if not r:
        r = ' '
    return r


def extract_subtext(text, key, index=0):
    """
    Extracts the value of a key within a dictionary masquerading as a string

    :param text: A string that's in the format of a dictionary
    :param key: The name of the key you want to extract the associated value from
    :param index: The index of specific value if you extracted more than one value from the key
    :return: the extracted value of the key
    """
    try:

        # convert to dictionary
        dictionary = ast.literal_eval(text)

        # extract value of key entered from dictionary
        list_keys = list(map(lambda x: x[index], dictionary.get(key, {})))

        return list_keys
    except (ValueError, SyntaxError):
        return []


def extract_text_from_html(text: str, name: str) -> list:
    """
    Extracts text contained within HTML tags.

    :param text: String to extract HTML tags from.
    :param name: String of the HTML tag to extract from.
    :return: List of strings contained within HTML tags.
    """
    try:
        soup = BeautifulSoup(text, features='html5lib')
        soup = soup.body
        soup = soup.findAll(name)
        return [str(x) for x in soup]
    except (ValueError, TypeError, AttributeError):
        return []


def extract_links_from_html(text):
    """
    Grab any GOV.UK domain-specific links from page text (looks for a href tags)
    :param text: html
    :return: list of page_paths (empty list if there are no links)
    """
    links = []
    try:
        soup = BeautifulSoup(text, 'html5lib')
        links = [link.get('href') for link in soup.findAll('a', href=True)]
    # might be fine to except all exceptions here, as it's a low-level function
    except Exception as e:
        print("error @extract_links_from_html", e)

    return [link.replace('https://www.gov.uk/', '/') for link in links
            if (link.startswith('/') or
                link.startswith(
                    'https://www.gov.uk/')) and "/government/uploads/system/uploads/attachment_data/file/" not in link]


VALID_PART = {'path', 'name', 'ext', 'name and ext'}


def extract_from_path(data, part):
    """
    Extracts the path, name and/or extension of a file or web path
    :param data: A list of strings to extract file path, name and/or extension from
    :param part: The part you want to extract from in data. Must take one of the elements in set, VALID_PART
    :return: List of file name and/or extensions of the same length as list_text
    """

    if part not in VALID_PART:
        raise ValueError('results: part must be one of %r.' % VALID_PART)

    try:

        if isinstance(data, str):
            data = [data]
            return extract_from_path(data, part)

        elif isinstance(data, list):
            if part == 'path':
                return [os.path.split(text)[0] for text in data]
            elif part == 'name':
                return [os.path.splitext(text)[0] for text in data]
            elif part == 'ext':
                return [os.path.splitext(text)[1] for text in data]
            elif part == 'name and ext':
                return [os.path.split(text)[1] for text in data]

    except TypeError:
        return []
