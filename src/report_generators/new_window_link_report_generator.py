from src.report_generators.base_report_generator import BaseReportGenerator
from src.utils.html_extractor import HtmlExtractor
from src.utils.html_validator import HtmlValidator
from src.utils.content_item_details import content_item_details, html_from_content_details


class NewWindowLinkReportGenerator(BaseReportGenerator):

    @property
    def filename(self):
        return "new_window_links_report.csv"

    @property
    def headers(self):
        return self.base_headers() + ["links"]

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

        links_with_targets = HtmlExtractor.extract_links_with_target(html)

        if not links_with_targets:
            return []

        links_without_open_in_text = []

        for link in links_with_targets:
            if not HtmlValidator.link_has_open_text(link):
                links_without_open_in_text.append(" ".join(list(link.stripped_strings)))

        if not links_without_open_in_text:
            return []

        return self.base_columns(content_item, html) + ["\n".join(links_without_open_in_text)]
