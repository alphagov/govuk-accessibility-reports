from dataclasses import dataclass

@dataclass
class TableAccessibilityInfo:
    def __init__(self, has_tables=False, num_of_tables=0, no_headers=False, no_row_headers=False, two_columns=False, links_in_first_column=False, numbers_in_first_column=False):
        self.has_tables = has_tables
        self.num_of_tables = num_of_tables
        self.no_headers = no_headers
        self.no_row_headers = no_row_headers
        self.two_columns = two_columns
        self.first_column_links = links_in_first_column
        self.first_column_numbers = numbers_in_first_column

    def has_tables(self):
        return self.has_tables

    def num_of_tables(self):
        return self.num_of_tables

    def no_headers(self):
        return self.no_headers

    def no_row_headers(self):
        return self.no_row_headers

    def two_columns(self):
        return self.two_columns

    def links_in_first_column(self):
        return self.first_column_links

    def numbers_in_first_column(self):
        return self.numbers_in_first_column

    def is_valid(self):
        if self.num_of_tables == 0:
            return True
        if self.num_of_tables == 1 and self.two_columns is True:
            if self.no_headers:
                return False
            else:
                return True

        if self.no_headers or self.no_row_headers:
            return False

        return True
