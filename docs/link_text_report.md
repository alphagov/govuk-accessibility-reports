# LinkTextReport

This report looks through content items to determine if link texts on the page are compliant (no two links have the same text but go to different URLs) and descriptive (have reasonable link texts)

## Input

This report uses the preprocessed content store for a list of pages to check, then reads the HTML for those pages from the production mirror (ie it works on whole pages,
  not just content extracts).

## Special Output Columns

- title: content_item title
- links_compliant: True if all links are compliant
- non_compliant_links: list of all non-compliant link texts found
- links_descriptive: True if all links are descriptive
- non_descriptive_links: list of all non-descriptive link texts found

## Validity

A content item is valid for this purpose (and will not appear in the report) if:
- all link texts are compliant
- all links texts are descriptive

## Notes
