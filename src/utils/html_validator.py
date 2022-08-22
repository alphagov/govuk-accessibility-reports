from src.utils.html_extractor import HtmlExtractor
from src.utils.html_table_extractor import HtmlTableExtractor
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
