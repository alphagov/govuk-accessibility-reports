from src.report_generators.base_report_generator import BaseReportGenerator
from src.utils.html_validator import HtmlValidator

from src.utils.content_item_details import content_item_details, html_from_content_details

class AltTagReportGenerator(BaseReportGenerator):
    @property
    def headers(self):
        return self.base_headers() + [
                    "is_valid",
                    "has_images",
                    "missing_alt_tags",
                    "alt_tags_empty",
                    "alt_tags_double_quotes",
                    "alt_tags_filename"
                ]

    @property
    def filename(self):
        return "alt_tags_report.csv"

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
        alt_tags_info = HtmlValidator.validate_alt_tags(html_parts)

        # return only pages with relevant attachment links and problems
        if alt_tags_info.includes_images == False:
            return []
        elif alt_tags_info.is_valid():
            return []
        else:
            return  self.base_columns(content_item, html) + [
                        str(alt_tags_info.is_valid()),
                        str(alt_tags_info.includes_images()),
                        str(alt_tags_info.missing_tags()),
                        str(alt_tags_info.tags_empty()),
                        str(alt_tags_info.tags_double_quotes()),
                        str(alt_tags_info.tags_filename())
                    ]
