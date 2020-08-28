import pytest

from src.utils.html_validator import HtmlValidator
from src.utils.table_accessibility_info import TableAccessibilityInfo

from tests.fixtures.tables import two_tables


def test_validate_table_accessibility(two_tables):
    table_info = TableAccessibilityInfo(has_tables=True, num_of_tables=2, no_headers=True, no_row_headers=True, two_columns=False)

    assert HtmlValidator.validate_table_accessibility(two_tables).__dict__ == table_info.__dict__

