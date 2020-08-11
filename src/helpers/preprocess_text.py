import re

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
