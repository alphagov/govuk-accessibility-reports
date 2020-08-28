import ast

from src.utils.html_validator import HtmlValidator
from src.report_generators.base_report_generator import BaseReportGenerator


class TablesReportGenerator(BaseReportGenerator):

    @property
    def filename(self):
        return "table_report.csv"

    @property
    def headers(self):
        return ["base_path", "organisations", "num_of_tables", "tables_missing_headers", "tables_missing_row_headers", "two_column_tables"]

    def process_page(self, content_item, html):
        accessibility = HtmlValidator.validate_table_accessibility(html)

        # a11y Team don't want to look at pages that only have one table that have just 2 columns
        if accessibility.has_tables is not True or (accessibility.num_of_tables == 1 and accessibility.two_columns is True):
            return []

        primary = self.__primary_org(content_item['organisations'])

        row = ["https://gov.uk" + content_item['base_path'],
               primary,
               accessibility.num_of_tables,
               accessibility.no_headers,
               accessibility.no_row_headers,
               accessibility.two_columns]

        return row

    @staticmethod
    def __primary_org(content_item_orgs) -> str:
        # Parses Content Item list of Organisations, extracts the Primary Publishing Organisation
        #  and returns its title.
        #  Falls back to first Organisation if there is no Primary Publishing Organisation.
        #
        # Structure of `orgs` would look like:
        # {
        #     'organisations': [
        #         ('b548a09f-8b35-4104-89f4-f1a40bf3136d', 'Department for Work and Pensions', 'D10')
        #     ],
        #     'primary_publishing_organisation': [
        #         ('b548a09f-8b35-4104-89f4-f1a40bf3136d', 'Department for Work and Pensions', 'D10')
        #     ]
        # }

        primary = None
        orgs = ast.literal_eval(content_item_orgs)

        try:
            if orgs is not None:
                primary = (orgs.get('primary_publishing_organisation'))[0][1]
            if primary is None:
                primary = (orgs.get('organisations'))[0][1]
        except TypeError:
            primary = "NO ORG"

        return primary