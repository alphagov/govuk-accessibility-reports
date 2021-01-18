from src.report_generators.base_report_generator import BaseReportGenerator
from src.helpers.preprocess_text import extract_subtext, extract_from_path
from src.utils.constants import ATTACHMENTS

from bs4 import BeautifulSoup
from collections import Counter


class AttachmentTypeReportGenerator(BaseReportGenerator):
    @property
    def headers(self):
        return ["base_path",
                "primary_publishing_organisation",
                "publishing_app",
                "document_type",
                "first_published_at",
                "attachment_and_count"]

    @property
    def filename(self):
        return "attachment_type_report.csv"

    def process_page(self, content_item, html):
        # ignore empty details
        if not content_item['details']:
            return []

        # extract primary publishing organisations
        content_item['primary_publishing_organisation'] = extract_subtext(text=content_item['organisations'],
                                                                          key='primary_publishing_organisation',
                                                                          index=1)
        # extract attachment url
        content_item['attachment_and_count'] = self.count_attachment_from_html(text=content_item['details'])

        # return only pages with valid attachment extensions
        if not content_item['attachment_and_count']:
            return []
        else:
            return [content_item['base_path'],
                    content_item['primary_publishing_organisation'],
                    content_item['publishing_app'],
                    content_item['document_type'],
                    content_item['first_published_at'],
                    content_item['attachment_and_count']]

    @staticmethod
    def count_attachment_from_html(text: str) -> dict:
        """
        Extracts attachments as identified by links from a GOV.UK webpage via looking at href tags.
        Very similar to extract_links_from_html() but returns more results.
        Example: government/publications/measles-mumps-and-rubella-lab-confirmed-cases-in-england-2019
        Reference:
            - `src/helpers/prepreprocess_text/py`

        :param text: String of the HTML code to extract attachments from.
        :return: Dictionary of count of attachment extensions.
        """
        try:
            soup = BeautifulSoup(text, 'html5lib')
            links = [link.get('href') for link in soup.find_all(name='a', href=True)]
            # extract extension
            attachments = extract_from_path(data=links, part='ext')
            # take valid attachments only
            attachments = [x for x in attachments if x in ATTACHMENTS]
            # take unique html attachments
            attachments_html = [html for html in links if html.startswith('/')]
            attachments_html = list(set(attachments_html))
            # count repeated attachment elements in list
            attachment_counts = dict(Counter(attachments))
            # add html counts
            attachment_counts.update({'.html': len(attachments_html)})

            return attachment_counts

        except Exception as e:
            print("error @count_attachment_from_html", e)
