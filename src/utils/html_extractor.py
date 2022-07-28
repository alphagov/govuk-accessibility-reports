import re
from bs4 import BeautifulSoup


class HtmlExtractor:
    header_regex = re.compile("^h[1-6]{1}$")
    excluded_headings = [
        "Cookies on GOV.UK",
        "Navigation menu",
        "Find information and services",
        "Search for a department and find out what the government is doing",
        "Search",
        "Popular on GOV.UK"
    ]

    @classmethod
    def extract_headings(cls, html):
        soup = BeautifulSoup(html, 'html5lib')
        matches = soup.find_all(cls.header_regex)
        return [m.name for m in matches if m.text.strip() not in cls.excluded_headings]
