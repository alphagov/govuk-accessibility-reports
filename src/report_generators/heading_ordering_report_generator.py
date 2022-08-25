from src.utils.html_validator import HtmlValidator
from src.report_generators.base_report_generator import BaseReportGenerator

class HeadingOrderingReportGenerator(BaseReportGenerator):
    @property
    def headers(self):
        return self.base_headers() + [
                "has_valid_headings",
                "has_duplicate_h1s",
                "has_wrong_start",
                "has_bad_ordering",
                "has_no_headings",
                "heading_order"
            ]

    @property
    def filename(self):
        return "basic_heading_accessibility_report.csv"

    def process_page(self, content_item, html):
        heading_accessibility_info = HtmlValidator.validate_headings_accessibility(html)

        if heading_accessibility_info.is_valid() == True:
            return []
        else:
            return  self.base_columns(content_item, html) + [
                        str(heading_accessibility_info.is_valid()),
                        str(heading_accessibility_info.has_duplicate_h1s()),
                        str(heading_accessibility_info.has_wrong_start()),
                        str(heading_accessibility_info.has_bad_ordering()),
                        str(heading_accessibility_info.has_no_headings()),
                        str(heading_accessibility_info.heading_order())
                    ]
