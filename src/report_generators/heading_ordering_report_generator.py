from src.utils.html_validator import HtmlValidator
from src.report_generators.base_report_generator import BaseReportGenerator


class HeadingOrderingReportGenerator(BaseReportGenerator):
    @property
    def headers(self):
        return ["base_path", "has_valid_headings", "has_duplicate_h1s", "has_bad_ordering", "has_no_headings",
                "heading_order"]

    @property
    def filename(self):
        return "basic_heading_accessibility_report.csv"

    def process_page(self, content_item, html):
        heading_accessibility_info = HtmlValidator.validate_headings_accessibility(html)

        row = [content_item['base_path'], heading_accessibility_info.is_valid(),
               heading_accessibility_info.has_duplicate_h1s(), heading_accessibility_info.has_bad_ordering(),
               heading_accessibility_info.has_no_headings(), heading_accessibility_info.heading_order()]

        return row
