from src.report_generators.base_report_generator import BaseReportGenerator
from src.helpers.preprocess_text import extract_subtext
from src.utils.constants import ATTACHMENTS
from src.utils.html_validator import HtmlValidator

from src.utils.content_item_details import content_item_details, html_from_content_details

class AttachmentDescriptionReportGenerator(BaseReportGenerator):
    @property
    def headers(self):
        return ["base_path",
                "primary_publishing_organisation",
                "is_valid",
                "inaccurately_describes_pdf_as_download",
                "no_mention_of_format",
                "no_mention_of_size"]

    @property
    def filename(self):
        return "attachment_description_report.csv"

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
        attachment_link_accessibility_info = HtmlValidator.validate_attachment_link_accessibility(html_from_content_details(details_dict))

        # return only pages with relevant attachment links and problems
        if not attachment_link_accessibility_info.has_attachment_links():
            return []
        elif attachment_link_accessibility_info.is_valid():
            return []
        else:
            return [content_item['base_path'],
                    content_item['primary_publishing_organisation'][0],
                    str(attachment_link_accessibility_info.is_valid()),
                    str(attachment_link_accessibility_info.has_inaccurate_pdf_download_text()),
                    str(attachment_link_accessibility_info.has_no_format_description()),
                    str(attachment_link_accessibility_info.has_no_size_description())]
