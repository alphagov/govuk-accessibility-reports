import re
from bs4 import BeautifulSoup


class HtmlTableExtractor:

    no_th_css = "table > :not(thead):first-child > tr:first-child > :not(th)"
    no_row_header_css = "table tbody tr:nth-child(2) th:not([scope=row]), table tbody tr:first-child *:not(th):first-child"
    two_column_table_css = "td:first-child:nth-last-child(2), td:first-child:nth-last-child(2) ~ td"

    @classmethod
    def extract_tables(cls, html):
        soup = BeautifulSoup(html, "html5lib")
        matches = soup.select("table")

        if matches is None or len(matches) == 0:
            return None

        return matches

    @classmethod
    def extract_tables_with_no_headers(cls, tables):
        soup = BeautifulSoup(str(tables), "html5lib")
        matches = soup.select(cls.no_th_css)

        return list(matches)

    @classmethod
    def extract_tables_missing_row_headers(cls, tables):
        soup = BeautifulSoup(str(tables), "html5lib")
        matches = soup.select(cls.no_row_header_css)

        return list(matches)

    @classmethod
    def extract_two_column_tables(cls, tables):
        soup = BeautifulSoup(str(tables), "html5lib")
        matches = soup.select(cls.two_column_table_css)

        return list(matches)
