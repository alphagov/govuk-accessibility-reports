# TableRelationshipReport

This report looks through content items to determine if a table has been mentioned in the content but there is no table in the content itself (ie "see table for details" in the text, but the table is actually an attached XLSX file).

## Input

This report uses the preprocessed content store for a list of pages to check and the content to check. (It reads but does not use the production mirror).

## Special Output Columns

- is_valid: Always False - only non-valid content items will appear in the report (see Validity)
- mentions_table: does the text contain the phrases "in table", "see table", or "the table"?
- table_in_document: is there a table in the content item? (nor in an attachment)
- possible_table_attachment: true if there are attachments (any one of which might be the mentioned table)

## Validity

A content item is valid for this purpose (and will not appear in the report) if:
- it does not mention tables in the text, or
- it does mention tables, but there is a table in the content item (not in an attachment)

## Notes
