# NonEnglishDocsReport

This report looks through content items to determine if the predominant language of the content item is English.

## Input

This report uses the preprocessed content store for a list of pages to check and for the HTML to check (it does not use the production mirror, although that still has to be present?).

## Special Output Columns

- text: The text found in the content item
- text_languages: languages detected, and probability of correct identification
- detected_as_english: True if english is in text_languages with probability (?) of > 0.5

## Notes

This uses the [langdetect module](https://pypi.org/project/langdetect/)
