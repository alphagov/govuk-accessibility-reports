import re
from bs4 import BeautifulSoup


class HtmlExtractor:
    header_regex = re.compile("^h[1-6]{1}$")
    excluded_headings = [
        "Cookies on GOV.UK"
    ]

    @classmethod
    def extract_headings(cls, html):
        soup = BeautifulSoup(html, 'html5lib')
        matches = soup.find_all(cls.header_regex)

        filtered_headings = filter(lambda match: match.text not in cls.excluded_headings, matches)

        return list(map(lambda match: match.name, filtered_headings))
