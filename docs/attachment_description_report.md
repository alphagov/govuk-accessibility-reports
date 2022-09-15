# AttachmentDescriptionReport

This report looks through content items to determine if the attachments have descriptions that include size and format.

## Input

This report uses the preprocessed content store for a list of pages to check and the content to check. (It reads but does not use the production mirror).

## Special Output Columns

- is_valid: Always False - only non-valid content items will appear in the report (see Validity)
- no_mention_of_format: relevant text doesn't mention file format
- no_mention_of_size: relevant text doesn't have "kb", "mb", or "gb" anywhere

## Validity

A content item is valid for this purpose (and will not appear in the report) if:
- it contains no attachments, or
- it contains attachments, but the related text (see below) contains mention of file format and size

## Notes

There is code (unused) that determines if a content item has a PDF attachment and the link refers to it as a "download" (potentially confusing because PDFs commonly open in a new or the same browser tab now). This was deemed more complicated than useful in the 2022 audit and disabled.
