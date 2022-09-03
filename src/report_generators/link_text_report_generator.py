import ast
import json
import re

from bs4 import BeautifulSoup
from src.report_generators.base_report_generator import BaseReportGenerator

class LinkTextReportGenerator(BaseReportGenerator):

    @property
    def filename(self):
        return "link_text_report.csv"

    @property
    def headers(self):
        return self.base_headers() + ["title", "links_compliant", "non_compliant_links", "links_descriptive", "non_descriptive_links"]

    def process_page(self, content_item, html):
        non_compliant_links = self.non_compliant_links(html)
        non_descriptive_links = self.non_descriptive_links(html)

        links_are_compliant = not any(non_compliant_links)
        links_are_descriptive = not any(non_descriptive_links)

        if links_are_compliant and links_are_descriptive:
            return []

        return self.base_columns(content_item, html) + [
                    content_item.get('title', ''),
                    str(links_are_compliant),
                    "\n".join(non_compliant_links),
                    str(links_are_descriptive),
                    "\n".join(non_descriptive_links),
                ]

    def links_are_compliant(self, html):
        return not any(self.non_compliant_links(html))

    def non_compliant_links(self, html):
        """
        Returns non compliant links
        Will return links that have the same link text but different urls
        >>> item = ContentItem('/education')
        >>> item.html = "<a href='https://www.gov.uk/page_one'>one</a><a href='https://www.gov.uk/page_two'>one</a>"
        "<a href='https://www.gov.uk/page_three'>three</a>"
        >>> item.non_compliant_links()
        ['There are 2 links all with text `one` that point to different urls: https://www.gov.uk/page_one,
        https://www.gov.uk/page_two']
        """

        soup = BeautifulSoup(html, features="html.parser")
        links_by_text = {}

        excluded_link_texts = [
            'Request an accessible format.'
        ]

        excluded_link_urls = [
            '#content',
            'https://www.gov.uk/'
        ]

        excluded_link_url_prefixes = [
            '#',
            'mailto:'
        ]

        for link in soup.findAll('a'):
            if self._is_not_feedback(link) and self._is_not_global_bar(link) and self._is_not_cookie_banner(
                    link) and self._is_not_footer(link) and self._is_not_skip_link(link):
                text = " ".join(list(link.stripped_strings))

                if text in excluded_link_texts:
                    continue

                if len(text) > 0 and 'href' in link:
                    href = link['href']

                    # There will always be different links to the homepage on every page,
                    # which include "GOV.UK" and "Home". Including this would make the
                    # analysis a lot more noisy and less useful.
                    if href in excluded_link_urls or any(href.startswith(prefix)
                                                         for prefix in excluded_link_url_prefixes):
                        continue

                    if text not in links_by_text:
                        links_by_text[text] = []

                    # We know relative links point to GOV.UK, so specify this in the href to reduce false matches
                    if href.startswith('/'):
                        href = f"https://www.gov.uk{href}"

                    links_by_text[text].append(href)

        non_compliant_links = []

        # A link points to a unique destination, but uses the same text as other links;
        for link_text, hrefs in links_by_text.items():
            if len(list(set(hrefs))) > 1:
                problem_urls = '\n\t'.join(hrefs)
                problem_statement = f"There are {len(hrefs)} links all with text `{link_text}` that point to " \
                    f"different urls:\n\t{problem_urls}\n"
                non_compliant_links.append(problem_statement)

        return non_compliant_links

    def non_descriptive_links(self, html):
        """
        Returns non descriptive link texts
        Will return the text of links if the text is considered non-descriptive,
        for instance "view online", "view", "read", "click here", etc.
        """

        soup = BeautifulSoup(html, "html5lib")
        links_by_text = {}

        bad_link_texts = [
            "click here", "read more", "view online", "tell us here",
            "see guidance", "read guidance", "view guidance", "more guidance", "further guidance",
            "see information", "read information", "view information", "more information", "further information",
            "click", "here", "read", "more", "view", "see", "guidance",
            "information", "online"
        ]

        invalid_texts_regex_str = "|".join(map(lambda str: "^{}$".format(str), bad_link_texts))

        invalid_texts_regex = re.compile(invalid_texts_regex_str, re.IGNORECASE)

        non_descriptive_links = []

        for link in soup.findAll('a'):
            if self._is_not_feedback(link) and self._is_not_global_bar(link) and self._is_not_cookie_banner(
                    link) and self._is_not_footer(link) and self._is_not_skip_link(link):
                text = " ".join(list(link.stripped_strings))
                if len(re.findall(invalid_texts_regex, text)) > 0:
                    non_descriptive_links.append(text)

        return non_descriptive_links

    @staticmethod
    def _is_not_feedback(link):
        return not any(link.find_parents("div", {'class': 'gem-c-feedback'}))

    @staticmethod
    def _is_not_global_bar(link):
        return not any(link.find_parents("div", {'id': 'global-bar'}))

    @staticmethod
    def _is_not_cookie_banner(link):
        return not any(link.find_parents("div", {'id': 'global-cookie-message'}))

    @staticmethod
    def _is_not_footer(link):
        return not any(link.find_parents("footer", {'id': 'footer'}))

    @staticmethod
    def _is_not_skip_link(link):
        return not any(link.find_parents("div", {'id': 'skiplink-container'}))

    @staticmethod
    def _primary_publishing_organisation(content_item):
        organisations_json = json.loads(json.dumps((content_item.get("organisations", ""))))
        organisations = ast.literal_eval(organisations_json)

        return list(map(lambda org: org[1], organisations.get("primary_publishing_organisation", {})))
