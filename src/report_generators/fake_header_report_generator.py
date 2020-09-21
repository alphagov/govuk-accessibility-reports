from src.report_generators.base_report_generator import BaseReportGenerator


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
        pass
