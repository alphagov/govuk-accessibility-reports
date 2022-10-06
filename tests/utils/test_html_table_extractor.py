import pytest

from src.utils.html_table_extractor import HtmlTableExtractor
from tests.fixtures.tables import good_table, bad_table, bad_table_missing_row_scope, bad_table_missing_row_th, html, good_table_mention, bad_table_mention, missing_table_mention

# extract_tables
def test_extract_tables_extracts_single_table(html):
    tables = HtmlTableExtractor.extract_tables("<table><tr><td>This is fine</td></tr></table>")
    assert len(tables) == 1

def test_extract_tables_extracts_single_table_string(html):
    tables = HtmlTableExtractor.extract_tables(html)
    assert "<table" in str(tables)

def test_extract_tables_extracts_no_tables():
    tables = HtmlTableExtractor.extract_tables("<p>No tables</p>")
    assert tables is None

# extract_tables_with_no_headers
def test_extract_table_with_no_headers_good_table(good_table):
    tables = HtmlTableExtractor.extract_tables_with_no_headers(good_table)
    assert len(tables) == 0

def test_extract_tables_with_no_headers_bad_table(bad_table):
    tables = HtmlTableExtractor.extract_tables_with_no_headers(bad_table)
    assert len(tables) == 2

def test_extract_tables_with_no_headers_multiple_tables(html):
    tables = HtmlTableExtractor.extract_tables_with_no_headers(html)
    assert len(tables) == 2

# extract_tables_missing_row_headers
def test_extract_tables_missing_row_headers_good_table(good_table):
    tables = HtmlTableExtractor.extract_tables_missing_row_headers(good_table)
    assert len(tables) == 0

def test_extract_tables_missing_row_headers_multiple_tables(html):
    tables = HtmlTableExtractor.extract_tables_missing_row_headers(html)
    assert len(tables) == 2

def test_extract_tables_missing_row_headers_missing_row_scope(bad_table_missing_row_scope):
    tables = HtmlTableExtractor.extract_tables_missing_row_headers(bad_table_missing_row_scope)
    assert len(tables) == 1

def test_extract_tables_missing_row_headers_missing_th(bad_table_missing_row_th):
    tables = HtmlTableExtractor.extract_tables_missing_row_headers(bad_table_missing_row_th)
    assert len(tables) == 1

# extract_two_column_tables
def test_extract_two_column_tables_good_table(good_table):
    tables = HtmlTableExtractor.extract_two_column_tables(good_table)
    assert len(tables) == 0

def test_extract_two_column_tables_bad_table(bad_table):
    tables = HtmlTableExtractor.extract_two_column_tables(bad_table)
    assert len(tables) == 4

def test_extract_two_column_tables_multiple_tables(html):
    tables = HtmlTableExtractor.extract_two_column_tables(html)
    assert len(tables) == 4


# extrac_table_mentions
def test_extract_table_mentions_no_mention(missing_table_mention):
    table_mentions = HtmlTableExtractor.extract_table_mentions(missing_table_mention)
    assert len(table_mentions) == 0

def test_extract_table_mentions_one_mention_good_table(good_table_mention):
    table_mentions = HtmlTableExtractor.extract_table_mentions(good_table_mention)
    assert len(table_mentions) == 1

def test_extract_table_mentions_one_mention_bad_table(bad_table_mention):
    table_mentions = HtmlTableExtractor.extract_table_mentions(bad_table_mention)
    assert len(table_mentions) == 1
