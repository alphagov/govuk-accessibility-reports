import ast

from src.utils.html_validator import HtmlValidator
from src.report_generators.base_report_generator import BaseReportGenerator
from src.helpers.preprocess_text import extract_primary_org_from_organisations


class TablesReportGenerator(BaseReportGenerator):

    @property
    def filename(self):
        return "table_report.csv"

    @property
    def headers(self):
        return self.base_headers() + ["is_valid", "num_of_tables", "tables_missing_headers", "tables_missing_row_headers", "two_column_tables"]

    def process_page(self, content_item, html):
        accessibility = HtmlValidator.validate_table_accessibility(html)

        if accessibility.has_tables is not True or accessibility.is_valid():
            return []

        row = [accessibility.is_valid(),
               accessibility.num_of_tables,
               accessibility.no_headers,
               accessibility.no_row_headers,
               accessibility.two_columns]

        return self.base_columns(content_item, html) + row
