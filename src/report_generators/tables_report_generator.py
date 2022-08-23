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
        return self.base_headers() + ["num_of_tables", "tables_missing_headers", "tables_missing_row_headers", "two_column_tables"]

    def process_page(self, content_item, html):
        accessibility = HtmlValidator.validate_table_accessibility(html)

        # a11y Team don't want to look at pages that only have one table that have just 2 columns
        if accessibility.has_tables is not True or (accessibility.num_of_tables == 1 and accessibility.two_columns is True):
            return []

        row = [accessibility.num_of_tables,
               accessibility.no_headers,
               accessibility.no_row_headers,
               accessibility.two_columns]

        return self.base_columns(content_item, html) + row
