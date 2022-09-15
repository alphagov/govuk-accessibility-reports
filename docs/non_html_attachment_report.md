# NonHtmlAttachmentReport

This report looks through content items for specific publishing apps for links to attachments.

## Input

This report uses the preprocessed content store for a list of pages to check and for the HTML to check (it does not use the production mirror, although that still has to be present?).

## Special Output Columns

- attachment_path: A list of the paths for any attachments found

## Notes

Only scans content items created by the following apps:
- publisher
- service-manual-publisher
- specialist-publisher
- travel-advice-publisher
