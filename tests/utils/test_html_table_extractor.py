import pytest

from src.utils.html_table_extractor import HtmlTableExtractor
from tests.fixtures.tables import good_table, bad_table, bad_table_missing_row_scope, html


def test_extract_tables(html):
    tables = HtmlTableExtractor.extract_tables("<table><tr><td>This is fine</td></tr></table>")
    assert len(tables) == 1

    tables = HtmlTableExtractor.extract_tables(html)
    assert "<table" in str(tables)

def test_no_tables():
    tables = HtmlTableExtractor.extract_tables("<p>No tables</p>")
    assert tables is None

def test_extract_tables_with_no_headers(html, bad_table):
    tables = HtmlTableExtractor.extract_tables_with_no_headers(html)
    assert len(tables) == 2

    tables = HtmlTableExtractor.extract_tables_with_no_headers(bad_table)
    assert len(tables) == 2

def test_extract_nothing_with_no_headers(good_table):
    tables = HtmlTableExtractor.extract_tables_with_no_headers(good_table)
    assert len(tables) == 0

def test_extract_tables_missing_row_headers(html, bad_table_missing_row_scope):
    tables = HtmlTableExtractor.extract_tables_missing_row_headers(html)
    assert len(tables) == 2

    tables = HtmlTableExtractor.extract_tables_missing_row_headers(bad_table_missing_row_scope)
    assert len(tables) == 1

def test_extract_nothing_missing_row_headers(good_table):
    tables = HtmlTableExtractor.extract_tables_missing_row_headers(good_table)

def test_extract_two_column_tables(html, bad_table):
    tables = HtmlTableExtractor.extract_two_column_tables(html)
    assert len(tables) == 6

    tables = HtmlTableExtractor.extract_two_column_tables(bad_table)
    assert len(tables) == 6

def test_extract_nothing_two_column_tables(good_table):
    tables = HtmlTableExtractor.extract_two_column_tables(good_table)
    assert len(tables) == 0
