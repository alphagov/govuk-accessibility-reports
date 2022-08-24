import pytest

from src.utils.html_validator import HtmlValidator
from src.utils.alt_tag_info import AltTagInfo
from src.utils.table_accessibility_info import TableAccessibilityInfo
from src.utils.heading_accessibility_info import HeadingAccessibilityInfo

from tests.fixtures.tables import two_tables
from tests.fixtures.html import good_html, wrong_start, good_alt_tags, missing_alt_tags, empty_alt_tags, double_quote_alt_tags, filename_alt_tags


def test_validate_table_accessibility(two_tables):
    table_info = TableAccessibilityInfo(has_tables=True, num_of_tables=2, no_headers=True, no_row_headers=True, two_columns=False)

    assert HtmlValidator.validate_table_accessibility(two_tables).__dict__ == table_info.__dict__

def test_validate_headings_accessibility_good_html(good_html):
    html_info = HeadingAccessibilityInfo(headings="h1, h2", duplicate_h1s=False, bad_ordering=False, wrong_start=False)

    assert HtmlValidator.validate_headings_accessibility(good_html).__dict__ == html_info.__dict__

def test_validate_headings_accessibility_wrong_start(wrong_start):
    html_info = HeadingAccessibilityInfo(headings="h2", wrong_start=True)

    assert HtmlValidator.validate_headings_accessibility(wrong_start).__dict__ == html_info.__dict__

def test_validate_alt_tags_good_tags(good_alt_tags):
    alt_tag_info = AltTagInfo(True, False, False, False, False)

    assert HtmlValidator.validate_alt_tags(good_alt_tags).__dict__ == alt_tag_info.__dict__

def test_validate_alt_tags_missing_tags(missing_alt_tags):
    alt_tag_info = AltTagInfo(True, True, False, False, False)

    assert HtmlValidator.validate_alt_tags(missing_alt_tags).__dict__ == alt_tag_info.__dict__

def test_validate_alt_tags_empty_tags(empty_alt_tags):
    alt_tag_info = AltTagInfo(True, False, True, False, False)

    assert HtmlValidator.validate_alt_tags(empty_alt_tags).__dict__ == alt_tag_info.__dict__

def test_validate_alt_tags_double_quote_tags(double_quote_alt_tags):
    alt_tag_info = AltTagInfo(True, False, False, True, False)

    assert HtmlValidator.validate_alt_tags(double_quote_alt_tags).__dict__ == alt_tag_info.__dict__

def test_validate_alt_tags_filename_tags(filename_alt_tags):
    alt_tag_info = AltTagInfo(True, False, False, False, True)

    assert HtmlValidator.validate_alt_tags(filename_alt_tags).__dict__ == alt_tag_info.__dict__
