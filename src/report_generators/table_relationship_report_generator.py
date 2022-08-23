from src.report_generators.base_report_generator import BaseReportGenerator
from src.utils.constants import ATTACHMENTS
from src.utils.html_validator import HtmlValidator

from src.utils.content_item_details import content_item_details, html_from_content_details

class TableRelationshipReportGenerator(BaseReportGenerator):
    @property
    def headers(self):
        return self.base_headers() + [
                    "is_valid",
                    "mentions_table",
                    "table_in_document",
                    "possible_table_attachment"
                ]

    @property
    def filename(self):
        return "table_relationship_report.csv"

    def process_page(self, content_item, html):
        # ignore empty details
        if not content_item['details']:
            return []

        details_dict = content_item_details(content_item)

        # extract attachment url
        if "body" not in details_dict:
            return []

        html_parts = html_from_content_details(details_dict)
        if html_parts == None:
            return []
        table_relationship_info = HtmlValidator.validate_table_relationships(html_parts)

        # return only pages with relevant attachment links and problems
        if not table_relationship_info.has_mention_of_table():
            return []
        elif table_relationship_info.is_valid():
            return []
        else:
            return  self.base_columns(content_item, html) + [
                        str(table_relationship_info.is_valid()),
                        str(table_relationship_info.has_mention_of_table()),
                        str(table_relationship_info.has_table_in_document()),
                        str(table_relationship_info.has_possible_table_attachment())
                    ]
