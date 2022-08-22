from src.report_generators.base_report_generator import BaseReportGenerator
from src.helpers.preprocess_text import extract_subtext
from src.utils.constants import ATTACHMENTS
from src.utils.html_validator import HtmlValidator

from src.utils.content_item_details import content_item_details, html_from_content_details

class TableRelationshipReportGenerator(BaseReportGenerator):
    @property
    def headers(self):
        return ["base_path",
                "primary_publishing_organisation",
                "is_valid",
                "mentions_table",
                "table_in_document",
                "possible_table_attachment"]

    @property
    def filename(self):
        return "table_relationship_report.csv"

    def process_page(self, content_item, html):
        # ignore empty details
        if not content_item['details']:
            return []

        # extract primary publishing organisations
        content_item['primary_publishing_organisation'] = extract_subtext(text=content_item['organisations'],
                                                                          key='primary_publishing_organisation',
                                                                          index=1)
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
            return [content_item['base_path'],
                    content_item['primary_publishing_organisation'][0],
                    str(table_relationship_info.is_valid()),
                    str(table_relationship_info.has_mention_of_table()),
                    str(table_relationship_info.has_table_in_document()),
                    str(table_relationship_info.has_possible_table_attachment())]
