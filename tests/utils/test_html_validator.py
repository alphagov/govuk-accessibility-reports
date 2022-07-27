import pytest

from src.utils.html_validator import HtmlValidator
from src.utils.table_accessibility_info import TableAccessibilityInfo
from src.utils.heading_accessibility_info import HeadingAccessibilityInfo

from tests.fixtures.tables import two_tables
from tests.fixtures.html import good_html, wrong_start


def test_validate_table_accessibility(two_tables):
    table_info = TableAccessibilityInfo(has_tables=True, num_of_tables=2, no_headers=True, no_row_headers=True, two_columns=False)

    assert HtmlValidator.validate_table_accessibility(two_tables).__dict__ == table_info.__dict__

def test_validate_headings_accessibility_good_html(good_html):
    html_info = HeadingAccessibilityInfo(headings="h1, h2", duplicate_h1s=False, bad_ordering=False, wrong_start=False)

    assert HtmlValidator.validate_headings_accessibility(good_html).__dict__ == html_info.__dict__

def test_validate_headings_accessibility_wrong_start(wrong_start):
    html_info = HeadingAccessibilityInfo(headings="h2", wrong_start=True)

    assert HtmlValidator.validate_headings_accessibility(wrong_start).__dict__ == html_info.__dict__
