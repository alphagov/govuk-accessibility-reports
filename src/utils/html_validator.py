from src.utils.html_extractor import HtmlExtractor
from src.utils.heading_accessibility_info import HeadingAccessibilityInfo


class HtmlValidator:

    @staticmethod
    def validate_headings_accessibility(html):
        headings = HtmlExtractor.extract_headings(html)
        number_of_headings = len(headings)

        if number_of_headings == 0:
            return HeadingAccessibilityInfo(headings='', no_headings=True)

        if headings[0] != 'h1':
            return HeadingAccessibilityInfo(headings=headings[0], bad_ordering=True)

        if number_of_headings == 1:
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
                                        bad_ordering=bad_ordering)
