# AltTagReport

This report looks through content items to determine if image have appropriate alt text attributes.

## Input

This report uses the preprocessed content store for a list of pages to check and the content to check. (It reads but does not use the production mirror).

## Special Output Columns

- is_valid: Always False - only non-valid content items will appear in the report (see Validity)
- has_images: True if the content has images, False if not (in practise always true)
- missing_alt_tags: True is any images have no alt attributes
- alt_tags_empty: True if any images have empty alt attributes
- alt_tags_double_quotes: True if any images have alt attributes that are a set of smart quotes (ie a copy and paste problem has created an alt attribute that isn't technically empty, but which appears that way.)
- alt_tags_filename: True if any images have alt attributes that appear to be a filename rather than a description (triggered if they include "png", "jpg", "webp" or an underscore).

## Validity

A content item is valid for this purpose (and will not appear in the report) if:
- it contains no attachments, or
- it contains attachments, but the related text (see below) contains mention of file format and size

## Notes
