from langdetect import detect_langs
from langdetect.lang_detect_exception import LangDetectException
from src.report_generators.base_report_generator import BaseReportGenerator

import pandas as pd


class NonEnglishDocsReportGenerator(BaseReportGenerator):
    @property
    def headers(self):
        return ["base_path", "text", "text_languages", "detected_as_english"]

    @property
    def filename(self):
        return "non_english_docs_report.csv"

    def process_page(self, content_item, html):
        if pd.isna(content_item['text']):
            return [content_item['base_path'], content_item['text'], [], content_item.get('detected_as_english',
                                                                                          default=False)]

        content_item['text'] = str(content_item['text'])

        content_item['text_lang'] = self.detect_languages(content_item['text'])
        languages_dict = dict([(language.lang, language.prob) for language in content_item['text_lang']])

        if 'en' in languages_dict and languages_dict['en'] > 0.5:
            content_item['detected_as_english'] = True

        return [content_item['base_path'], content_item['text'], content_item['text_lang'],
                content_item.get('detected_as_english', default=False)]

    def detect_languages(self, text):
        """Detects language of a text, moving onto next text if an error is thrown

        :param text: A string to detect the language of
        :return: A list returning the language detected and confidence score associated to it

        """
        try:
            return detect_langs(text)
        except LangDetectException:
            return []
