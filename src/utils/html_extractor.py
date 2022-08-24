from src.utils.constants import ATTACHMENTS
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

    @classmethod
    def extract_links(cls, html):
        soup = BeautifulSoup(html, 'html5lib')
        links = soup.find_all(name="a", href=True)
        return links

    @classmethod
    def extract_attachment_links(cls, html):
        soup = BeautifulSoup(html, 'html5lib')
        links = soup.find_all(name="a", href=True)
        attachment_links = [l for l in links if HtmlExtractor.is_attachment_link(l)]
        return links

    @staticmethod
    def link_extension(link):
        parts = link.attrs['href'].split('.')
        return parts[-1].lower()

    @staticmethod
    def is_attachment_link(link):
        return ("." + HtmlExtractor.link_extension(link)) in ATTACHMENTS

    @classmethod
    def extract_images(cls, html):
        soup = BeautifulSoup(html, 'html5lib')
        links = soup.find_all(name="img")
        return links
