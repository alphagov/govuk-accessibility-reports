from src.utils.html_validator import HtmlValidator
from src.report_generators.base_report_generator import BaseReportGenerator
from src.helpers.preprocess_text import extract_subtext


class HeadingOrderingReportGenerator(BaseReportGenerator):
    @property
    def headers(self):
        return ["base_path", "primary_publishing_organisation", "has_valid_headings", "has_duplicate_h1s", "has_bad_ordering", "has_no_headings",
                "heading_order"]

    @property
    def filename(self):
        return "basic_heading_accessibility_report.csv"

    def process_page(self, content_item, html):
        heading_accessibility_info = HtmlValidator.validate_headings_accessibility(html)

        # extract primary publishing organisation
        primary_publishing_organisation = self.__primary_org(content_item['organisations'])

        row = [content_item['base_path'], primary_publishing_organisation, heading_accessibility_info.is_valid(),
               heading_accessibility_info.has_duplicate_h1s(), heading_accessibility_info.has_bad_ordering(),
               heading_accessibility_info.has_no_headings(), heading_accessibility_info.heading_order()]

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
