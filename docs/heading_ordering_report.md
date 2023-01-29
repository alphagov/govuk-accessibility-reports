# HeadingOrderingReport

This report looks through pages for correct heading ordering and related problems:

## Input

This report uses the preprocessed content store for a list of pages to check, then reads the HTML for those pages from the production mirror (ie it works on whole pages,
  not just content extracts). Because the govuk header contains header tags, it ignores a certain number of headers by their content text.

## Special Output Columns

- has_duplicate_h1s: Is there more than one H1 on this page?
- has_wrong_start: Is the first heading not an H1?
- bad_ordering: Are there any skipped numbers? (eg H1 followed by H3 with no H2)
- no_headings: Are there no header tags in this page at all?
- heading_order: A list of header tags in order in the document, to check.

## Notes
