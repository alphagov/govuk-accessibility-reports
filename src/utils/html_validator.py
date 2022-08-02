import re

from src.utils.constants import ATTACHMENTS
from src.utils.html_extractor import HtmlExtractor
from src.utils.html_table_extractor import HtmlTableExtractor

from src.utils.alt_tag_info import AltTagInfo
from src.utils.attachment_link_accessibility_info import AttachmentLinkAccessibilityInfo
from src.utils.heading_accessibility_info import HeadingAccessibilityInfo
from src.utils.table_accessibility_info import TableAccessibilityInfo
from src.utils.table_relationship_info import TableRelationshipInfo

class HtmlValidator:

    @staticmethod
    def validate_headings_accessibility(html):
        headings = HtmlExtractor.extract_headings(html)
        number_of_headings = len(headings)
        wrong_start = False

        if number_of_headings == 0:
            return HeadingAccessibilityInfo(headings='', no_headings=True)

        if headings[0] != 'h1':
          wrong_start=True

        if number_of_headings == 1 and not wrong_start:
            return HeadingAccessibilityInfo(headings='h1')

        heading_levels = [int(heading.replace('h', '')) for heading in headings]
        duplicate_h1s = False
        bad_ordering = False


        for i in range(1, number_of_headings):
            previous_level = heading_levels[i - 1]
            current_level = heading_levels[i]

            if current_level == 1:
                duplicate_h1s = True

            if current_level > (previous_level + 1):
                bad_ordering = True

        return HeadingAccessibilityInfo(headings=", ".join(headings), duplicate_h1s=duplicate_h1s,
                                        bad_ordering=bad_ordering, wrong_start=wrong_start)

    def validate_table_accessibility(html):
        tables = HtmlTableExtractor.extract_tables(html)

        if tables is None:
            return TableAccessibilityInfo()

        has_tables = False
        no_headers = False
        num_of_tables = 0
        no_row_headers = False
        two_columns = False

        if tables is not str and len(tables) > 0:
            has_tables = True
            num_of_tables = len(tables)

        if len(HtmlTableExtractor.extract_tables_with_no_headers(tables)) > 0:
            no_headers = True

        if len(HtmlTableExtractor.extract_tables_missing_row_headers(tables)) > 0:
            no_row_headers = True

        if len(HtmlTableExtractor.extract_two_column_tables(tables)) > 0:
            two_columns = True

        return TableAccessibilityInfo(has_tables=has_tables, num_of_tables=num_of_tables, no_headers=no_headers, no_row_headers=no_row_headers, two_columns=two_columns)

    def validate_table_relationships(html):
        table_mentions = HtmlTableExtractor.extract_table_mentions(html)

        if len(table_mentions) == 0:
            return TableRelationshipInfo([], [])

        tables = HtmlTableExtractor.extract_tables(html)

        if tables is not None :
            return TableRelationshipInfo(table_mentions, [], table_in_document=True)

        attachment_links = HtmlExtractor.extract_attachment_links(html)

        return TableRelationshipInfo(table_mentions, attachment_links, table_in_document=False)

    @staticmethod
    def validate_attachment_link_accessibility(html):
        attachment_links = HtmlExtractor.extract_attachment_links(html)

        if len(attachment_links) == 0:
            return AttachmentLinkAccessibilityInfo([])

        inaccurate_pdf_download_text = False
        no_format_description = False
        no_size_description = False

        for link in attachment_links:
            relevant_text = HtmlValidator.relevant_text(link)

            if HtmlValidator.is_pdf(link) and HtmlValidator.describes_link_as_download(relevant_text):
                inaccurate_pdf_download_text = True

            if not HtmlValidator.has_format_description(relevant_text, format = HtmlValidator.link_extension(link)):
                no_format_description = True

            if not HtmlValidator.has_size_description(relevant_text):
                no_size_description = True

        return AttachmentLinkAccessibilityInfo(attachment_links, inaccurate_pdf_download_text = inaccurate_pdf_download_text, no_format_description = no_format_description, no_size_description = no_size_description)

    @staticmethod
    def is_attachment_link(link):
        return ("." + HtmlExtractor.link_extension(link)) in ATTACHMENTS

    @staticmethod
    def is_pdf(link):
        return HtmlExtractor.link_extension(link) == 'pdf'

    # The text of the link, of the parent, and of the parent's previous sibling
    # (This is likely to be a header)
    @staticmethod
    def relevant_text(link):
        texts = [link.text]
        parent = link.find_parent('p')
        if parent is not None:
            texts.append(parent.text)
            parent_sib = parent.find_previous_sibling()
            if parent_sib is not None:
                texts.append(parent_sib.text)
        return " ".join(texts)

    @staticmethod
    def describes_link_as_download(text):
        return "Download".casefold() in text.casefold()

    @staticmethod
    def has_format_description(text, format = 'pdf'):
        return format.casefold() in text.casefold()

    @staticmethod
    def has_size_description(text):
        for unit in [' kb', ' mb', ' gb']:
            if unit.casefold() in text.casefold():
                return True
        return False

    def validate_alt_tags(html):
        images = HtmlExtractor.extract_images(html)

        if images == None or len(images) == 0:
            return AltTagInfo()

        missing_alt_tags = False
        alt_tags_empty = False
        alt_tags_double_quotes = False
        alt_tags_filename = False
        image_regex = re.compile("png|jpg|webp|_", re.IGNORECASE)

        for image in images:
            if not 'alt' in image.attrs.keys():
                missing_alt_tags = True
            else:
                if image['alt'] == "":
                    alt_tags_empty = True
                if image['alt'] == '""':
                    alt_tags_double_quotes = True
                if image_regex.search(image['alt']) != None:
                    alt_tags_filename = True

        return AltTagInfo(True, missing_alt_tags, alt_tags_empty, alt_tags_double_quotes, alt_tags_filename)
