# FakeHeaderReport

This report looks through content items to determine if the text has been marked up with the strong tag and might look like a header without actually being a header.

## Input

This report uses the preprocessed content store for a list of pages to check and the content to check. (It reads but does not use the production mirror).

## Validity

A content item is valid for this purpose (and will not appear in the report) if:
- it contains no text marked up with strong tags.

## Notes
