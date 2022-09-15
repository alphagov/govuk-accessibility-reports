# TablesReport

This report looks through content items to determine if the tables included have accessible headings.

## Input

This report uses the preprocessed content store for a list of pages to check, then reads the HTML for those pages from the production mirror (ie it works on whole pages,
  not just content extracts).

## Special Output Columns

- is_valid: Always False - only non-valid content items will appear in the report (see Validity)
- num_of_tables: number of tables in the content item.
- tables_missing_headers: Are any tables missing column headings?
- tables_missing_row_headers: Are any tables missing row headings?
- two_column_tables: Are any tables simple two-column tables?

## Validity

A content item is valid for this purpose (and will not appear in the report) if:
- it contains no tables,
- it contains a single two-column table and that table has column headers (doesn't have to have row headers), or
- all tables on the page have both column and row headers.

## Notes
