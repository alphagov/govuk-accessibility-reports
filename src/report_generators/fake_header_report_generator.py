from src.report_generators.base_report_generator import BaseReportGenerator
from src.helpers.preprocess_text import extract_subtext

import pandas as pd
from bs4 import BeautifulSoup


class FakeHeaderReportGenerator(BaseReportGenerator):
    @property
    def headers(self):
        return ['base_path',
                'primary_publishing_organisation',
                'publishing_app',
                'document_type']

    @property
    def filename(self):
        return "fake_header_page_report.csv"

    def process_page(self, content_item, html):

        # ignore empty fields
        if pd.isna(content_item['details']):
            return []

        # extract text in bold and strong
        soup = BeautifulSoup(content_item['details'], 'html5lib')
        content_item['text_in_bold'] = [txt.string for txt in soup.findAll('b')]
        content_item['text_in_strong'] = [txt.string for txt in soup.findAll('strong')]

        # ignore content with no text in bold nor strong
        if not (content_item['text_in_bold'] or content_item['text_in_strong']):
            return []

        # extract primary publishing organisation
        content_item['primary_publishing_organisation'] = extract_subtext(text=content_item['organisations'],
                                                                          key='primary_publishing_organisation',
                                                                          index=1)

        return [content_item['base_path'],
                content_item['primary_publishing_organisation'],
                content_item['publishing_app'],
                content_item['document_type']]
