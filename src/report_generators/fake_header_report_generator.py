from src.report_generators.base_report_generator import BaseReportGenerator
from src.helpers.preprocess_text import extract_text_from_html


class FakeHeaderReportGenerator(BaseReportGenerator):
    @property
    def headers(self):
        return self.base_headers()

    @property
    def filename(self):
        return "fake_header_page_report.csv"

    def process_page(self, content_item, html):

        # ignore empty fields
        if content_item['details'] in (None, ''):
            return []

        # extract text in strong
        content_item['text_in_strong'] = extract_text_from_html(text=content_item['details'],
                                                                name='strong')

        # ignore content with no text in bold nor strong
        if not content_item['text_in_strong']:
            return []

        return self.base_columns(content_item, html)
